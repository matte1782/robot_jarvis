# RL Failure Modes Cheat Sheet — Biped Locomotion

Quick-reference diagnostic guide. For each failure mode: what you see, probable causes, what to inspect, and what to do next.

---

## 1. Freeze and Fall

**What it looks like:** Robot stands motionless, then topples over. Episodes are very short (20-50 steps). Reward is near zero or slightly positive.

**Probable causes:**
- Reward clipping prevents negative feedback (this project's Fix #1)
- Alive reward dominates all other components (this project's Fix #2)
- Entropy collapsed — policy is deterministic, stuck on "do nothing" (Fix #3)

**What to inspect:**
- `reward_lower_bound` in reward clipping — must allow negatives
- Reward component fractions — alive should be <60% of total
- Entropy in TensorBoard — must be >0.5

**Next action:** Fix reward clipping, rebalance scales, increase entropy_cost. Restart from scratch (don't continue from collapsed checkpoint).

---

## 2. Shaking in Place

**What it looks like:** Robot vibrates or oscillates rapidly without making forward progress. May stay upright for a long time. Reward is positive but low.

**Probable causes:**
- `action_rate` penalty too high — penalizes large movements
- Tracking reward too weak — moving forward doesn't pay enough
- Stand-still penalty too weak — not penalized for staying put

**What to inspect:**
- `action_rate` scale — should be small (e.g., -0.1)
- `stand_still` scale — should be meaningful (e.g., -2.0)
- Action magnitudes in rollout data — are they tiny?

**Next action:** Reduce action_rate penalty, increase stand_still penalty. Verify tracking reward is achievable (check tracking_sigma).

---

## 3. Spinning / Thrashing

**What it looks like:** Robot spins in circles, flails limbs chaotically, or rapidly alternates between extreme joint positions.

**Probable causes:**
- Angular velocity tracking reward is mis-signed or un-bounded
- Joint limits not enforced in env → impossible poses that exploit physics
- Reward for movement without directional constraint

**What to inspect:**
- `tracking_ang_vel` reward implementation — is it correctly computing error?
- Joint limit enforcement in the MuJoCo XML / env
- Action clipping — are actions bounded to physical range?

**Next action:** Render a rollout video. Check if the spinning actually maximizes some reward component. Fix the specific component being exploited.

---

## 4. Reward Rising But Gait Useless

**What it looks like:** TensorBoard shows reward increasing over millions of steps. But video reveals the "walking" is degenerate — shuffling, hopping on one foot, dragging legs, etc.

**Probable causes:**
- `tracking_sigma` too large — policy gets high tracking reward for approximate matching
- Imitation reward too weak — no incentive for proper gait
- Reward components don't capture gait quality (only velocity matching)

**What to inspect:**
- Render checkpoint video at 5M, 10M, 20M — does the gait actually improve?
- Imitation reward fraction — should be 20-40% of total
- Tracking_sigma value — should be tight enough to require good velocity matching

**Next action:** Increase imitation weight. Tighten tracking_sigma. Add gait-specific penalties (e.g., foot clearance, symmetry).

---

## 5. Episodes Too Short

**What it looks like:** Episode length is 20-100 steps consistently, not improving over training. Robot keeps falling early.

**Probable causes:**
- Termination conditions too strict (height threshold too high)
- Policy hasn't learned basic balance yet (too early in training)
- Observation normalization wrong — policy gets garbage inputs
- If LATE in training: see "Freeze and Fall" above

**What to inspect:**
- Termination height threshold — is it reasonable for this robot?
- Observation magnitudes — are they in [-5, 5] range?
- Is episode length trending up at all? If flat, the policy isn't learning balance.

**Next action:** If early training (<1M steps): may be normal, wait. If persistent: check observations, check termination thresholds, check reward allows the policy to learn balance.

---

## 6. Imitation Reward Ineffective

**What it looks like:** Policy ignores reference motions entirely. Imitation reward fraction is <5% of total. Robot finds its own (ugly) way to walk.

**Probable causes:**
- Imitation scale too low relative to other rewards (this project: was 1.2%)
- Reference motions don't cover the commanded velocity range
- Imitation uses different math than tracking (e.g., -MSE vs exp(-MSE)) — incompatible

**What to inspect:**
- Imitation reward fraction in logged metrics
- Reference motion coverage (243 trajectories — do they cover all commanded velocities?)
- Mathematical form: is imitation reward on same scale as tracking reward?

**Next action:** Increase imitation scale (to 5.0 as in Fix #2). Verify reference motion coverage. Check that imitation and tracking rewards use compatible math.

---

## 7. Unstable Training After Initial Progress

**What it looks like:** Reward increases for 5-10M steps, then oscillates wildly or crashes. Entropy may spike or collapse. Loss becomes noisy.

**Probable causes:**
- Learning rate too high for later training stages
- No learning rate schedule (constant LR causes oscillations)
- Clipping epsilon too large — updates are too aggressive
- Gradient norm exploding (check if hitting clip ceiling)

**What to inspect:**
- Learning rate schedule — is there decay?
- Gradient norm in TensorBoard — is it constantly at the clip ceiling?
- Policy loss — is it oscillating?
- Entropy — sudden drop = policy collapsed again

**Next action:** Add cosine LR decay (Fix #5). Tighten clipping epsilon. Reduce max_grad_norm. Consider saving checkpoints more frequently so you can roll back.

---

## 8. NaN / Inf in Training

**What it looks like:** Training crashes with NaN loss. Or reward becomes inf. Or observations contain NaN.

**Probable causes:**
- Physics simulation exploded (joint penetration, extreme forces)
- Division by zero in reward computation (e.g., dividing by sigma=0)
- Gradient explosion (max_grad_norm too high or not applied)
- Bad observation normalization (running stats diverge)

**What to inspect:**
- Which tensor first became NaN? (Loss? Observation? Action?)
- Are actions exceeding joint limits? (Causes MuJoCo instability)
- Is any reward component division-by-zero possible?

**Next action:** Add NaN checks to training loop. Clip actions before env.step(). Verify observation normalization. Reduce learning rate.

---

## Quick Diagnosis Flowchart

```
Training running?
├── No: fix imports / dependencies / env setup first
└── Yes: check episode_length
    ├── Very short (<50): likely reward bug or observation bug
    │   └── Check: alive%, clip bounds, entropy
    ├── Medium (50-200): learning but not yet converged
    │   └── Check: is it trending up? If flat for >5M steps → problem
    └── Long (200-500): policy is surviving
        └── Check: is the GAIT good? Render video.
            ├── Gait good: continue training, monitor stability
            └── Gait bad: reward hacking → fix reward components
```
