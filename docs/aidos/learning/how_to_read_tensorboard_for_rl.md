# How to Read TensorBoard for RL Training

Practical guide for monitoring Open Duck Mini locomotion training. What to look at first, what healthy curves look like, and what suspicious patterns mean.

---

## Priority Order: What to Check First

When you open TensorBoard during a training run, check these metrics in this order:

### 1. Entropy (FIRST — always check this first)

**Where:** `policy/entropy` or `training/entropy`

| Value | Meaning |
|-------|---------|
| 1.5-2.5 | Healthy start (lots of exploration) |
| 0.5-1.5 | Normal mid-training (gradually specializing) |
| < 0.3 | WARNING: policy is becoming deterministic too early |
| < 0.0 | CRITICAL: entropy collapsed — training is dead |

**Healthy pattern:** Starts high (~2.0), gradually decreases over millions of steps, stabilizes around 0.5-1.0.

**Suspicious pattern:** Drops rapidly in first 1-2M steps to near-zero → policy locked into one strategy (probably bad). This happened in the broken training (collapsed to -0.043).

**If entropy collapses:** Stop training. Increase `entropy_cost`. Restart from scratch.

### 2. Episode Length

**Where:** `eval/episode_length` or `environment/episode_length`

| Value | Meaning |
|-------|---------|
| < 50 | Robot falling immediately — not learning balance |
| 50-150 | Learning basic balance, not yet walking |
| 150-300 | Walking but unstable |
| 300-500 | Good — sustained walking |
| > 800 | Excellent — reaching episode limit |

**Healthy pattern:** Starts very low (20-50), steadily increases over 5-20M steps, eventually plateaus at 300-500+.

**Suspicious pattern:**
- Flat at ~47 steps for millions of steps → freeze-and-fall (reward bug)
- Sudden drop after being high → training destabilized (LR too high?)
- Oscillating wildly → reward signal is noisy or contradictory

### 3. Episode Reward

**Where:** `eval/episode_reward` or `eval/reward`

**Healthy pattern:** Starts negative or near-zero, gradually increases, eventually plateaus at a positive value.

**Suspicious patterns:**
- Constant at 0.0 → reward clipping bug (Fix #1)
- Very high immediately → alive reward dominance (Fix #2)
- Increasing but gait is bad → reward hacking (render video to verify)
- Oscillating → unstable training (check LR, grad norm)

### 4. Reward Component Fractions

**Where:** `reward/alive_fraction`, `reward/imitation_fraction`, etc.

| Component | Healthy Range | Problem If |
|-----------|--------------|------------|
| alive | 20-50% | >60% = dominates, policy ignores task |
| imitation | 20-40% | <5% = reference motions ignored |
| tracking_lin_vel | 10-30% | <5% = not learning to follow commands |
| tracking_ang_vel | 5-15% | <2% = not learning to turn |

**If alive fraction > 60%:** The policy is exploiting the alive bonus. Reduce alive scale.

### 5. KL Divergence

**Where:** `policy/kl_divergence` or `training/kl`

| Value | Meaning |
|-------|---------|
| 0.001-0.01 | Healthy — policy changing at good pace |
| < 0.001 | Policy barely changing — stuck, entropy likely collapsed |
| > 0.05 | Updates too large — risk of instability |

### 6. Policy Loss

**Where:** `training/policy_loss` or `losses/policy`

**Healthy pattern:** Noisy but with clear downward trend or stable range.

**Suspicious patterns:**
- Constant zero → policy not updating (learning rate=0? optimizer broken?)
- Suddenly spikes → gradient explosion (check grad norm)
- Oscillating wildly → LR too high or clipping epsilon too large

### 7. Gradient Norm

**Where:** `training/grad_norm`

**Healthy pattern:** Stable below the clip ceiling (0.5 in this project).

**Suspicious patterns:**
- Constantly at exactly 0.5 → gradients always being clipped. LR may be too high, or the loss landscape is very steep. Not necessarily bad, but worth watching.
- Spikes to clip ceiling then drops → normal during learning transitions
- Growing over time → potential instability

---

## Sanity Run Checklist (First 100K Steps)

After launching a training run, these are the minimum checks at 100K steps:

| Check | Expected | If Not Met |
|-------|----------|------------|
| No NaN in any metric | All finite | Stop immediately, debug |
| Entropy > 1.0 | Yes | entropy_cost too low |
| Episode length > 20 | Yes | Env or obs may be broken |
| Reward not constant | Varying | Reward function may be broken |
| KL > 0.0005 | Yes | Policy is actually updating |
| Loss is finite | Yes | Gradient/optimizer working |

If all checks pass at 100K → continue to 1M.
If any check fails → stop, diagnose, fix, restart.

---

## 1M Step Checkpoint Review

| Metric | Healthy | Concerning | Critical |
|--------|---------|------------|----------|
| Entropy | 0.8-1.5 | 0.3-0.8 | < 0.3 |
| Episode length | > 80 | 40-80 | < 40 |
| Episode reward | Trending up | Flat | Negative/constant |
| Alive fraction | < 60% | 60-75% | > 75% |
| Imitation fraction | > 10% | 5-10% | < 5% |

---

## Comparing Baseline vs Post-Fix Runs

### What to look for when comparing the 10M baseline (no value clipping) vs post-fix (clipping_epsilon_value=0.2):

| Metric | Baseline (pathological) | Healthy post-fix | Still broken if |
|--------|------------------------|------------------|-----------------|
| v_loss | 10^7 → 10^18 (11 OOM growth) | Stays within ~10× of initial, or stabilizes | Still grows by >3 OOM |
| policy_loss | ≈ 0 (frozen) | Nonzero, noisy with trend | Still stuck at ≈ 0 |
| KL | 0.00014 (constant) | > 0.001, varying | Still < 0.0005 |
| reward | -9.04 → -7.98 (noisy, marginal) | Clearer trend (up or down) | Same noise pattern |
| entropy | Check for collapse | Stable > 0.5 | Rapid collapse to 0 |

### How to tell whether the rerun is healthier

1. **v_loss:** The most important metric. If it no longer explodes, the intervention worked at the mechanistic level.
2. **KL divergence:** If KL moves above 0.001, the policy is actually updating — this means the frozen-policy pathology is broken.
3. **policy_loss:** Should show nonzero magnitude. Negative values mean the policy found improvement direction.
4. **Reward trend:** Even if reward doesn't improve dramatically in 10M steps, a clearer trend (less noise, directional movement) suggests the learning signal is reaching the policy.

### Actual Results (2026-03-16 post-fix rerun — FINAL, 15 eval points)

| Metric | Baseline (pathological) | v_clip=0.2 (FINAL) | Verdict |
|--------|------------------------|---------------------|---------|
| v_loss | 3.5×10^7 → 1.2×10^18 | 0.598 → 0.147 (range: 0.060–0.598) | **FIXED — stable, never re-explodes** |
| policy_loss | ≈ 0 (10^-6, frozen) | -0.013 → -0.020 | **FIXED — active gradient throughout** |
| KL | 0.00014 (constant) | 0.007 (stable, 50× higher) | **FIXED — policy updating** |
| reward | -9.04 → -7.98 (noisy, 12%) | -9.04 → -4.69 (directional, 48%) | **Clear improvement — 4× better** |
| imitation | -322 → -314 (flat, 2.5%) | -322 → -157 (51% reduction) | **Learning reference motion** |
| entropy | -0.446 (frozen) | -0.453 → -0.429 (gradual) | **Healthy — exploration maintained** |
| episode_length | ~53 (flat) | 54 → 35 (decreasing) | **Monitor — active locomotion signature** |

The value clipping intervention was an unambiguous success on all 5 priority metrics. Acceptance criteria: **7/7 met**.

### What metrics matter most for this comparison

Priority order for the value clipping comparison:
1. **v_loss trajectory** — did the fix address the root cause?
2. **KL divergence** — is the policy unfrozen?
3. **policy_loss** — is the policy gradient meaningful?
4. **reward** — is learning happening? (may need more steps to show)
5. **entropy** — did exploration survive?

---

## Common TensorBoard Pitfalls

1. **Smoothing hides problems.** TensorBoard's default smoothing can hide oscillations. Set smoothing to 0.0 periodically to see raw data.

2. **Eval vs training metrics differ.** Training metrics include exploration noise. Eval metrics use the deterministic policy. Always check eval metrics for true performance.

3. **Reward scale ≠ behavior quality.** A high reward number doesn't mean good walking. Always render video checkpoints to verify visually.

4. **Logging frequency matters.** If metrics are logged every 10K steps, you can't see what happened in between. For sanity runs, log more frequently (every 1K steps).
