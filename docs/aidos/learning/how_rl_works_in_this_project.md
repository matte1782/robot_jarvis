# How RL Works in This Project

**Date:** 2026-03-15 (updated — training code now located and verified)
**Scope:** Open Duck Mini V2/V3 biped locomotion via PPO in MuJoCo
**Source evidence:** Direct code inspection of `C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground\`, plus `RL_TRAINING_FIXES_V2.md`, `MUJOCO_SIMULATION_DECISION_MATRIX.md`
**Note:** Many sections upgraded from "inferred" to "verified from code" after locating the training repository. See `docs/aidos/audits/rl_codebase_map.md` for the full code map.

---

## 1. What Is the Environment?

**[inferred from code references + Open Duck architecture]**

The environment is a MuJoCo physics simulation of the Open Duck Mini V2 biped robot. It runs inside the `mujoco_playground` framework (Google DeepMind's playground or a fork), using JAX for hardware-accelerated simulation.

The specific environment file is `playground/open_duck_mini_v2/joystick.py`. "Joystick" means the robot receives velocity commands (like a joystick input) and must walk to follow them.

**Key properties:**
- Physics engine: MuJoCo (via `mujoco-mjx` for JAX-accelerated batched sim)
- Robot: 14-DOF biped (10 leg joints + 4 head joints)
- Task: Follow commanded linear and angular velocities
- Timestep: `self.dt` (simulation timestep, likely 0.002-0.01s)
- Episode: runs until termination or max steps

---

## 2. The Observation Vector

**[inferred from Open Duck architecture + reward components]**

The observation vector is what the policy "sees" each timestep. For a locomotion task like this, it typically contains:

| Component | Meaning | Why It Matters |
|-----------|---------|----------------|
| Joint positions (14) | Current angle of each joint | Policy must know current pose |
| Joint velocities (14) | Angular velocity of each joint | Needed for smooth control |
| Base orientation (3-4) | Robot torso rotation (quaternion or euler) | Detect falling, tilting |
| Base angular velocity (3) | How fast torso is rotating | Stability signal |
| Base linear velocity (3) | How fast robot is moving | Compare to command |
| Commanded velocity (3) | Target linear_x, linear_y, angular_z | The "goal" |
| Previous actions (14) | What the policy did last step | Smooth action transitions |
| Gravity vector (3) | Projected gravity in body frame | Which way is "up" |

**[general RL background]** The observation is a flat vector fed to the neural network. Every element must be normalized to roughly [-1, 1] range for stable training. Missing or badly scaled observations cause learning failures.

---

## 3. The Action Vector

**[inferred from code references]**

The action vector has 14 dimensions — one per actuated joint:
- Indices 0-4: left leg (hip_yaw, hip_roll, hip_pitch, knee, ankle)
- Indices 5-9: right leg (same order)
- Indices 10-13: head (neck_pitch, head_pitch, head_yaw, head_roll)

**[verified from `MUJOCO_SIMULATION_DECISION_MATRIX.md`]** For V3 deployment, indices 10 and 13 are discarded (V3 has only 2 head DOF). Leg actions map 1:1.

**[general RL background]** Actions are typically position targets (desired joint angles) output by the policy network. They are clipped to joint limits and converted to torques by a PD controller inside the simulation. The policy outputs continuous values, usually in [-1, 1], which are then scaled to the joint's range.

---

## 4. Reward Components

**[verified from `RL_TRAINING_FIXES_V2.md` lines 53-66]**

The reward function is a weighted sum of components. Here are the documented scales (BROKEN values, pre-fix):

| Component | Scale (broken) | Scale (fixed) | Purpose |
|-----------|---------------|---------------|---------|
| `tracking_lin_vel` | 2.5 | 2.5 | Reward for matching commanded linear velocity |
| `tracking_ang_vel` | 6.0 | 6.0 | Reward for matching commanded angular velocity |
| `torques` | -1e-3 | -1e-3 | Penalize high motor torques (energy efficiency) |
| `action_rate` | -0.5 | -0.1 | Penalize rapid action changes (smoothness) |
| `stand_still` | -0.2 | -2.0 | Penalize standing still when commanded to move |
| `alive` | 20.0 | 2.0 | Reward for not falling/terminating |
| `imitation` | 1.0 | 5.0 | Reward for matching reference motion trajectories |

**[verified from code]** `tracking_sigma=0.01` (broken) → `0.05` (fixed). This controls how sharply the tracking reward drops off. At 0.01, even small velocity errors give near-zero reward — too sparse for learning.

**[verified from code]** The total reward is: `reward = clip(sum(component * scale) * dt, lower, upper)`. The critical bug was `lower=0.0` which prevents any negative feedback.

### Why the Broken Rewards Cause Freeze-and-Fall

**[verified from fix doc analysis]**

1. `alive=20.0` dominates: 7407% of total reward. Policy learns "staying alive = maximum reward."
2. `clip(_, 0.0, _)` means mistakes cost nothing. Bad actions get reward=0, same as doing nothing.
3. `imitation=1.0` is only 1.2% of total. Following reference motion provides negligible incentive.
4. Rational policy: do absolutely nothing → stay alive as long as possible → collect alive reward → eventually fall over → reward=0 (not negative).
5. Result: "freeze and fall" — the policy literally learns that inaction is optimal.

---

## 5. Termination

**[inferred from standard MuJoCo locomotion envs]**

An episode terminates when:
- Robot torso falls below a height threshold (e.g., 0.15m)
- Robot torso tilts beyond a safe angle (e.g., >60° from vertical)
- Maximum episode steps reached (e.g., 1000 steps)

**[verified from fix doc]** Current episodes last only ~47 steps on average. Healthy training should produce 300-450 step episodes. The short episodes confirm the robot falls quickly — consistent with the "freeze then topple" behavior.

---

## 6. Domain Randomization

**[inferred from Open Duck architecture — NOT verified in code]**

Domain randomization varies simulation parameters during training so the policy generalizes to real hardware. Typical randomizations for biped locomotion:

| Parameter | Typical Range | Why |
|-----------|--------------|-----|
| Mass | ±15% | Real robot mass varies with assembly |
| Friction | ±30% | Floor surface varies |
| Motor strength | ±10% | Servo torque varies unit-to-unit |
| Observation noise | ±5% | Real sensors are noisy |
| Push perturbations | random force | Real-world bumps |
| Joint damping | ±20% | Mechanical wear |

**Status: UNKNOWN whether this environment uses domain randomization.** The fix doc does not mention it. The `joystick.py` environment may or may not implement it. This must be verified when the code is cloned.

**[general RL background]** Without domain randomization, sim-to-real transfer will likely fail. The policy overfits to exact simulation parameters and breaks on real hardware where friction, mass, and delays differ.

---

## 7. What PPO Does in This Pipeline

**[general RL background, anchored to this project's parameters]**

PPO (Proximal Policy Optimization) is the algorithm that updates the policy network.

### The Training Loop (simplified)

```
repeat for N_total_steps:
    1. ROLLOUT: Run policy in K parallel envs for T steps
       → collect observations, actions, rewards, dones
    2. COMPUTE ADVANTAGES: For each timestep, estimate
       "how much better was this action than average?"
       Uses discount=0.99 (fixed) to weight future rewards
    3. UPDATE POLICY: For M epochs over the rollout data:
       a. Compute new action probabilities under current policy
       b. Compute ratio = new_prob / old_prob
       c. Clip ratio to [1-ε, 1+ε] where ε=0.15 (fixed)
       d. Update policy to increase probability of good actions
       e. Also update value function (critic)
       f. Add entropy bonus (0.05) to prevent premature convergence
       g. Clip gradients to max_norm=0.5 (fixed)
    4. LOG METRICS: reward, entropy, KL divergence, episode length
```

### Why PPO Specifically?

- Stable: clipping prevents catastrophically large updates
- Sample efficient enough for sim (millions of steps are cheap in MuJoCo)
- Works well with continuous action spaces (joint angles)
- Standard choice for locomotion (used by most Open Duck, ANYmal, etc.)

### Key PPO Parameters in This Project

| Parameter | Broken | Fixed | Effect |
|-----------|--------|-------|--------|
| `clipping_epsilon` | 0.2 | 0.15 | How much the policy can change per update. Lower = more conservative updates. |
| `discounting` | 0.97 | 0.99 | How far ahead the agent "looks". 0.97 = ~33 step horizon. 0.99 = ~100 step horizon. |
| `max_grad_norm` | 1.0 | 0.5 | Gradient clipping. Lower = more stable but slower learning. |
| `entropy_cost` | 0.005 | 0.05 | Bonus for maintaining randomness. Higher = more exploration. |
| `learning_rate` | 3e-4 (constant) | warmup→3e-4→cosine decay | Schedule prevents early instability and late oscillations. |

---

## 8. Why Degenerate Behaviors Happen

**[general RL background, illustrated with this project's bugs]**

### Freeze / Collapse
- **Cause:** Alive reward dominates + no negative reward possible
- **Mechanism:** Doing nothing maximizes alive bonus. Falling gives reward=0, not negative. Policy converges to "stand still until you fall."
- **This project:** Exactly what happened. 47-step episodes, frozen policy.

### Shaking in Place
- **Cause:** High action_rate penalty + low tracking reward
- **Mechanism:** Policy learns small oscillations stay within action_rate budget while collecting some alive reward. Not walking, just vibrating.

### Spinning / Thrashing
- **Cause:** Reward bug where angular velocity tracking is mis-signed or the policy finds an unintended reward exploit
- **Mechanism:** Spinning maximizes angular velocity matching for certain commanded values.

### Reward Rising But Gait Useless
- **Cause:** Reward hacking. The metric goes up but the behavior is degenerate.
- **Example:** If `tracking_sigma` is too loose, the policy gets high tracking reward for moving in roughly the right direction, even with terrible gait quality.

### Entropy Collapse
- **Cause:** `entropy_cost` too low → policy becomes deterministic too early
- **Mechanism:** Without exploration bonus, the first "good enough" strategy gets reinforced. The policy loses the ability to try new behaviors.
- **This project:** Entropy collapsed to -0.043. The policy is deterministic — stuck in the "freeze" strategy.

---

## 9. Why Sim-to-Real Is Hard Here

**[general RL background + verified from project docs]**

| Gap | Simulation | Real Hardware | Impact |
|-----|-----------|---------------|--------|
| Actuator model | Ideal torque | STS3215 servos with backlash, delay | Gait timing breaks |
| Contact model | Soft contact with MuJoCo solver | Hard plastic on floor | Foot slip differs |
| Sensor noise | Clean observations | IMU drift, encoder quantization | Policy sees different inputs |
| Latency | ~0ms (sim step = observation + action) | 5-20ms (serial bus + processing) | Actions arrive late |
| Mass distribution | CAD model (approximate) | Real assembly (cables, batteries shift CoM) | Balance point shifts |
| Floor | Flat, uniform friction | Variable surface | Different traction |
| DOF mismatch | 14 DOF (V2 sim) | 12 DOF (V3 hardware) | 2 head DOF discarded |

**[verified from `MUJOCO_SIMULATION_DECISION_MATRIX.md`]** The V2→V3 leg mapping is 1:1 (100% compatible). Head DOF mismatch is irrelevant for locomotion. But all other sim-to-real gaps remain.

**[inferred]** Without domain randomization AND careful system identification (measuring real servo response curves, friction, etc.), the trained policy will likely fail on hardware even if it walks perfectly in simulation.

---

## 10. Value Function Clipping — Why It Matters Here

**[verified from Brax source: losses.py:187-193]**

### What is value clipping?

In PPO, the **critic** (value function) predicts the expected total future reward from each state. The **policy** uses these predictions to compute advantages: "was this action better or worse than expected?"

Without value clipping, the critic can make arbitrarily large updates each training step. If a single batch contains unusual states (from domain randomization or noisy rewards), the critic's prediction can jump wildly — and those wild predictions corrupt the advantage estimates for the next batch.

### How Brax implements it (clipping_epsilon_value)

```python
# losses.py:187-193
if clipping_epsilon_value is not None:
    old_values = data.extras['policy_extras']['value']
    v_clipped = old_values + jnp.clip(
        baseline - old_values, -clipping_epsilon_value, clipping_epsilon_value
    )
    v_loss_clipped = (vs - v_clipped) ** 2
    v_loss = jnp.maximum(v_loss, v_loss_clipped)
```

With `clipping_epsilon_value=0.2`, the critic's output can only change by ±0.2 from its previous prediction per update. This prevents runaway divergence.

### Why critic instability can freeze the policy

1. Critic predicts wildly wrong values → advantages become noise
2. Noisy advantages → policy gradient has random direction
3. PPO's clipping (clipping_epsilon=0.15) prevents large policy changes
4. Policy effectively ignores the noisy gradient → policy_loss ≈ 0, KL ≈ 0
5. Result: critic diverges exponentially while policy stands still

This is exactly what the 10M baseline showed: v_loss went from 10^7 to 10^18 while KL stayed at 0.00014.

### What value clipping should fix

- v_loss should stay bounded (not explode by 11 orders of magnitude)
- With stable critic → stable advantages → meaningful policy gradients
- Policy should show nonzero KL (actually updating) and nonzero policy_loss
- Reward trends should become more interpretable

### What value clipping does NOT fix

- If the reward function itself is poorly shaped → walking won't emerge regardless
- If the LR is too high → clipping helps but doesn't eliminate oscillation
- If the environment has fundamental issues → clipping is irrelevant

---

## 11. What the 10M Value Clipping Run Proved

**[verified by execution — full 22.9M env steps, 15 eval points, exit 0]**

### Critic stabilization works

Before value clipping: v_loss grew from 3.5×10^7 to 1.2×10^18 over 22.9M steps — an 11 order-of-magnitude divergence. After adding `clipping_epsilon_value=0.2`: v_loss started at 0.598 and ended at 0.147, bouncing within the range 0.060–0.598 throughout. The fix directly addresses the root cause by constraining the critic's per-update change to ±0.2.

### Policy unfreezes when the critic is stable

The most important downstream effect: when the critic stopped diverging, advantage estimates became meaningful again. KL divergence rose from 0.00014 (constant, frozen) to 0.007 (stable, 50× higher). Policy_loss moved from ≈0 to -0.020. The policy switched from "do nothing" to "actively update."

### Imitation learning accelerates dramatically

With a stable critic, the imitation cost (how far the robot's motion deviates from the reference trajectories) dropped from -322 to -157 over the full run — a 51% reduction. The baseline run showed essentially flat imitation cost (-322 → -314, 2.5% after the same number of steps). This is the clearest evidence that the policy is learning something useful.

### Episode length decrease is expected, not a failure

Episode length fell from 54 to 35 steps while reward improved from -9.04 to -4.69. This is the signature of active locomotion replacing freeze-and-stand: the robot now attempts to move, which causes falls during early learning, shortening episodes. The reward improvement is real (robot is doing useful things). Episode length should recover as the policy refines over 50M+ steps. **If episode length stays below 30 at 50M steps, investigate.**

### What remains unproven

- Whether the improvement trajectory continues beyond 22.9M steps (requires 50M run)
- Whether a LR schedule (Fix #5) would accelerate or improve final policy quality
- Whether the trained policy produces visually recognizable walking (requires checkpoint rendering)
- Whether the policy transfers to hardware (requires sim-to-real gap analysis)

---

## Summary of Evidence Quality (updated 2026-03-16)

| Section | Evidence Level |
|---------|---------------|
| Environment structure | **Verified from code** (joystick.py read directly) |
| Observation vector | **Verified by execution** (101-dim state, 212-dim privileged) |
| Action vector | **Verified by execution** (14-dim: 10 leg + 4 head) |
| Reward components | **Verified from code** (8 components, line numbers confirmed) |
| Reward clipping (Fix #1) | **Verified by execution** (negative reward -1.74 observed) |
| Termination | **Verified from code** (height < 0.08m, NaN check) |
| Domain randomization | **Verified from code** (randomize.py: 8 params randomized) |
| PPO parameters | **Verified from code** (runner.py lines 325-333) |
| Degenerate behaviors | General RL background + verified bug analysis |
| Sim-to-real gaps | General background + verified DOF mapping |

---

## What This Validation Actually Exercised (2026-03-16)

### What was truly validated
- **Environment construction:** MuJoCo model loads, XML parses, joints/actuators enumerated correctly
- **Reset path:** Initial state generation works — random position/orientation noise, command sampling, reference motion loading
- **Step path:** Physics simulation, reward computation, observation assembly, termination check — all execute without errors
- **Fix #1 (negative rewards):** Confirmed at runtime — reward of -1.74 observed under adversarial actions
- **Observation/action shapes:** Corrected from earlier documentation (101-dim obs, 14-dim action)

### What was NOT validated
- **PPO training loop:** The smoke test only exercises env.reset() and env.step(). It does NOT run any PPO updates. Entropy, KL divergence, policy loss — none of these have been tested.
- **Domain randomization during training:** The randomizer is imported but only runs during the full training loop (wrapped by Brax).
- **Checkpointing/ONNX export:** Not tested. ONNX export is currently stubbed.
- **Multi-environment batching:** Training uses 8192 parallel envs via JAX vmap. The smoke test runs a single env.
- **Reward shaping correctness:** We verified rewards are computed and can be negative. We have NOT verified that the reward components guide the policy toward walking (that requires the full training loop and TensorBoard inspection).

### Why passing imports is not the same as proving training health
Imports prove that:
- Python packages are installed and compatible
- Module-level code executes without errors
- The environment class can be instantiated

Imports do NOT prove that:
- The PPO training loop converges
- The reward function produces useful learning signals
- The observation normalization is stable over millions of steps
- Checkpointing works correctly
- The policy network architecture is appropriate for this task

**The next required validation step is a 100K-step training run** which exercises the full PPO loop for the first time.
