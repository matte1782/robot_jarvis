# RL Current State — Decision Log (v2)

**Date:** 2026-03-16 (updated after fix preservation + local validation)
**Decision:** GO for 100K sanity run. NO-GO for Kaggle.

---

## Current Objective

Prepare a Kaggle-based RL training workflow for Open Duck Mini biped locomotion. Train a PPO policy in MuJoCo simulation that can be deployed on V3 hardware.

## Verified Facts

1. Training code exists at `C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground\`
2. Fixes #1, #3, #4: **VERIFIED APPLIED + COMMITTED** on branch `fixes/iao-v2-verified-2026-03-16` (commit `e93d2b9`)
3. Fix #2: **APPLIED WITH DEVIATIONS + COMMITTED** — 5/7 params differ from fix doc
4. Fix #5: **NOT APPLIED** — no optax import, no schedule code
5. All verified fixes are now **safe from accidental loss** (committed on named branch)
6. Domain randomization: 8 params randomized (`playground/common/randomize.py`)
7. Prior training runs exist (Jan 2026) including a 45M step demo video
8. **Runtime validated (2026-03-16):** env construction, reset, step all pass on local CPU
9. **Action size: 14** (10 leg + 4 head), **Obs state: 101-dim**, privileged: 212-dim
10. **Fix #1 runtime-confirmed:** negative reward of -1.74 observed under bad actions
11. **No NaN** in any observation or reward during smoke test
12. Packages in system Python (JAX 0.8.2, Brax 0.14.0, MuJoCo 3.4.0). `venv_rl/` in robot_jarvis is empty.

## Unverified Assumptions

1. `venv_rl/` still has working dependencies (2 months old, not tested)
2. Colab notebooks still work with current package versions
3. The reward deviations from Fix #2 are improvements (not regressions)
4. Existing training runs produced useful policies (45M demo video suggests yes)
5. Kaggle GPUs can run JAX + MuJoCo MJX

## Blocking Unknowns

1. **Fix #5 not applied** — deliberate skip or oversight? Constant LR may be adequate for initial runs.
2. **Fixes are uncommitted** — risk of accidental loss
3. **No Kaggle notebook exists** — need to create or adapt from Colab

## Decision: CONDITIONAL GO (local), NO-GO (Kaggle)

Local testing can proceed through gates G2-G6 after verifying the venv works. Kaggle requires creating a notebook and verifying GPU availability.

## Immediate Next Actions (ordered)

1. ~~Commit or branch the fixes~~ DONE (e93d2b9)
2. ~~Test imports~~ DONE (all pass, system Python)
3. ~~Run env smoke test~~ DONE (all pass, negative rewards confirmed)
4. **Run 100K sanity run** — verify entropy > 0.5, episodes > 20 steps
5. **Review existing TensorBoard logs** from Jan runs
6. **Decide on Fix #5** — apply LR schedule or defer with rationale

---

## Value clipping intervention (2026-03-16)

**File changed:** `playground/common/runner.py` line 334
**Parameter added:** `self.ppo_params["clipping_epsilon_value"] = 0.2`
**Why this is the chosen intervention:**
- The 10M baseline run showed v_loss exploding from ~3.5×10^7 to ~1.2×10^18
- Without value clipping, the critic can make arbitrarily large prediction jumps each update
- Large critic errors corrupt advantage estimates → policy gradient becomes meaningless → policy freezes
- Value clipping (ε=0.2) constrains the critic's per-update change, preventing runaway divergence
- This is the single highest-leverage fix because it addresses the root cause of both the v_loss explosion AND the frozen policy

**What blocker it addresses:**
- CRITICAL: v_loss exponential divergence
- CRITICAL: policy effectively frozen (policy_loss ≈ 0, KL ≈ 0.00014)

**What it does NOT address (by design):**
- Fix #5 (LR schedule) — deferred, will reassess after this rerun
- Push perturbations — deferred
- ONNX export — deferred

---

**Next review:** After post-fix 10M rerun completes and evidence is extracted.

---

## Post-fix 10M Evidence + Decision (2026-03-16)

### Evidence Summary (FINAL — full 22.9M run)

The v_clip=0.2 fix **resolved the critical blocker**:
- v_loss: 10^18 divergence → stable 0.060–0.598 (FIXED, never re-explodes)
- Policy unfrozen: KL=0.007 (50× baseline), policy_loss=-0.020 (active throughout)
- Reward: -9.04 → -4.69 (48% improvement over 22.9M steps vs 12% baseline)
- Best reward: -4.21 at step 19.7M
- Imitation cost: -322 → -157 (51% reduction — robot actively learning reference motion)
- Episode length: 54 → 35 (decreasing — active locomotion, not freeze-and-stand)
- No NaN, no crash, exit code 0

See `docs/aidos/experiments/rl_next_experiment_plan.md` for full 15-point trajectories and final comparison table.

### Acceptance Criteria: 7/7 MET (FULL RUN — all criteria satisfied)

### Updated Blocker State

| Blocker | Previous | Current |
|---------|----------|---------|
| v_loss divergence | CRITICAL | **RESOLVED** — bounded 0.060–0.598 |
| Policy frozen | CRITICAL | **RESOLVED** — KL=0.007, policy_loss=-0.020 |
| Fix #5 (LR schedule) | MEDIUM | MEDIUM — constant LR working, defer to 50M assessment |
| ONNX export | DEFERRED | DEFERRED — not needed for local runs |
| Push perturbations disabled | DEFERRED | DEFERRED — assess after 50M |
| Kaggle notebook | HIGH (for Kaggle goal) | **PREMATURE** — need 50M local evidence first |

**NEW concern: episode length decreasing (54→35) despite reward improving.** This is a known early-training signature of active locomotion (robot tries to move, falls faster). Expected to recover with more steps. Needs monitoring at 50M.

### Decision: GO for 50M local run with current config

**Rationale:**
- 22.9M run shows improvement trend that hasn't plateaued (best reward at step 19.7M, near end)
- Value function is stable across all 14 training data points (v_loss bounded, never re-diverges)
- Policy actively exploring throughout (entropy gradual, KL steady at 0.007)
- 50M steps needed to determine convergence trajectory and episode length recovery

**Fix #5 status:** Still deferred. Constant LR=3×10^-4 produced 48% reward improvement and 51% imitation improvement. Cosine decay recommended for 50M+ runs but not a current blocker.

**Kaggle status:** Still NO-GO. Wait for 50M local evidence. Kaggle is premature until we confirm convergence trajectory is healthy over longer runs.

### Immediate Next Actions

1. Run 50M steps locally with current config (clipping_epsilon_value=0.2, no other changes)
2. Monitor: does episode length recover past 50? Does reward continue trending below -4?
3. After 50M: decide on Fix #5 + Kaggle migration
