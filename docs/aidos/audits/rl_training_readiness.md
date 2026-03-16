# RL Training Readiness Gates — v2

**Date:** 2026-03-15 (updated)
**Auditor:** AIDOS technical audit
**Depends on:** `docs/aidos/audits/rl_fix_verification.md` (v2)

---

## Repository Structure Correction

### Why the v1 audit was all NO-GO

The v1 audit searched only inside `robot_jarvis/`. The training code lives at `C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground\`, a separate clone of `apirrone/Open_Duck_Playground`. This repo contains the environment, reward function, training runner, and prior training runs with checkpoints.

### Current state after discovery

- Training code: **FOUND** at external path
- 4 of 5 fixes: **VERIFIED APPLIED** (uncommitted local modifications)
- Fix #5 (LR schedule): **NOT APPLIED**
- Prior training runs: **EXIST** (multiple runs from Jan 2026)
- Colab notebooks: **EXIST** (3 notebooks)
- 45M step demo video: **EXISTS**

---

## Gate Summary

| Gate | Status | Blocking Condition |
|------|--------|-------------------|
| G1: Code inspection complete | **CONDITIONAL GO** | Code found, fixes verified, but uncommitted + Fix #5 missing |
| G2: Local import test | **CONDITIONAL GO** | `venv_rl/` exists, but deps not verified. Prior runs prove it worked on 2026-01-21. |
| G3: Kaggle dependency install | **NO-GO** | No Kaggle notebook exists (Colab notebooks exist, not Kaggle) |
| G4: Env reset/step smoke test | **CONDITIONAL GO** | Prior runs prove env works, but current state not tested |
| G5: Short sanity run (100K) | **CONDITIONAL GO** | Must verify G2+G4 first on current machine state |
| G6: 1M-step run | **CONDITIONAL GO** | Prior 1M runs exist (`flat_1M_FIXED_v2`), but on CPU (~8h) |
| G7: Long Kaggle run (50M+) | **NO-GO** | No Kaggle infra set up. Colab notebooks may work. |

**Overall: CONDITIONAL GO for local testing (G1-G6). NO-GO for Kaggle deployment (G3, G7).**

---

## Gate Details

### G1: Code Inspection Complete
- **Status:** CONDITIONAL GO
- **Why:** All training code found and inspected. 4/5 fixes verified applied. Reward function, PPO config, domain randomization, reference motions all present.
- **Conditions:**
  1. Fix #5 (LR schedule) must be decided: apply or explicitly defer
  2. Uncommitted changes must be preserved (commit or branch)
  3. Deviations from Fix #2 must be documented and accepted
- **Evidence:** `docs/aidos/audits/rl_fix_verification.md` v2

### G2: Local Import Test
- **Status:** CONDITIONAL GO
- **Why:** `venv_rl/` exists in `robot_jarvis/`. Prior training runs (up to 2026-01-21) prove the dependencies worked. However, 2 months have passed — packages may have been broken by updates or the venv may be stale.
- **What must happen:**
  ```bash
  source "C:/Users/matte/Desktop/Desktop OLD/AI/.../robot_jarvis/venv_rl/Scripts/activate"
  python -c "import jax; import brax; import mujoco; print('OK')"
  ```
- **Blocking on:** Nothing (can test now)

### G3: Kaggle Dependency Install
- **Status:** NO-GO
- **Why:** No Kaggle notebook or Kaggle config exists. Three Colab notebooks exist but haven't been tested:
  - `OpenDuck_FINAL_WORKING.ipynb`
  - `OpenDuck_RL_Training_Colab.ipynb`
  - `OpenDuck_Training_FINAL.ipynb`
- **What must happen:** Either adapt a Colab notebook for Kaggle or create a new Kaggle notebook. Verify GPU runtime availability.
- **Alternative:** Use Colab instead of Kaggle if GPUs are available there.

### G4: Env Reset/Step Smoke Test
- **Status:** CONDITIONAL GO
- **Why:** Prior training runs prove the env can reset and step. But the reward function has been modified (deviations from Fix #2, added orientation cost, changed termination). Current config hasn't been tested end-to-end.
- **What must happen:** Run a minimal env test:
  ```python
  from playground.open_duck_mini_v2.joystick import Joystick
  import jax
  env = Joystick(task="flat_terrain")
  state = env.reset(jax.random.PRNGKey(0))
  print(f"Obs shape: {state.obs['state'].shape}")
  action = jax.numpy.zeros(env.action_size)
  next_state = env.step(state, action)
  print(f"Reward: {next_state.reward}, can be negative: {next_state.reward < 0}")
  ```
- **Blocking on:** G2 pass

### G5: Short Sanity Run (100K)
- **Status:** CONDITIONAL GO
- **Why:** The training command is known and has worked before:
  ```bash
  cd C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground
  python playground/open_duck_mini_v2/runner.py --task flat_terrain --num_timesteps 100000
  ```
- **What must happen:** G2+G4 pass. Run 100K steps. Check entropy > 0.5, episode length > 20, no NaN.
- **Blocking on:** G2, G4

### G6: 1M-Step Run
- **Status:** CONDITIONAL GO
- **Why:** A `flat_1M_FIXED_v2` training run already exists. New run needed with current config (which has further deviations). CPU runtime ~4-8 hours.
- **What must happen:** G5 pass with healthy metrics.
- **Blocking on:** G5

### G7: Long Kaggle Run (50M+)
- **Status:** NO-GO
- **Why:** No Kaggle infrastructure. Colab notebooks exist but GPU availability is uncertain. The `openduck_45M_demo.mp4` suggests a long run was done, but unclear where (local CPU? Colab?).
- **What must happen:**
  1. Test a Colab notebook
  2. Verify GPU availability
  3. Verify checkpoint save/resume works in cloud
  4. OR: set up Kaggle notebook from scratch
- **Blocking on:** Colab/Kaggle infra verification

---

## Post-Preservation Readiness (2026-03-16)

| Gate | Status | Evidence |
|------|--------|----------|
| Fixes committed | **GO** | Branch `fixes/iao-v2-verified-2026-03-16`, commit `e93d2b9` |
| Local imports | **GO** | All imports pass (JAX 0.8.2, Brax 0.14.0, MuJoCo 3.4.0, system Python 3.13.12) |
| Env smoke test | **GO** | Construct, reset, step all pass. Obs (101,), action (14), no NaN, negative rewards work |
| Very short sanity run | **GO** | Env validated, ready for 100K step run |
| 10M baseline run | **COMPLETE** | PPO mechanically alive but pathological (v_loss divergent, policy frozen) |
| Post-fix 10M (value clipping) | **COMPLETE — SUCCESS (7/7)** | v_loss stable (0.060–0.598), reward -9.04→-4.69, policy active (KL=0.007), ALL 7 acceptance criteria met |
| Kaggle eligibility | **NO-GO** | Deferred until 50M local run validates convergence |

### Corrected Technical Details (from runtime validation)
- **Action size: 14** (10 leg + 4 head joints) — not 10 as previously documented
- **Obs state size: 101** — not 73 as previously estimated
- **Privileged state size: 212**
- **JIT compilation time on CPU:** 7-10s per operation (env construction, reset, step)
- **venv_rl in robot_jarvis is EMPTY** — packages are in system Python, not the venv

---

## Immediate Blocker Summary

| Blocker | Severity | Resolution |
|---------|----------|------------|
| ~~Fixes uncommitted~~ | ~~HIGH~~ | RESOLVED — committed on branch e93d2b9 |
| ~~v_loss divergence~~ | ~~CRITICAL~~ | **RESOLVED** — v_loss stable at 0.08-0.14 with clipping_epsilon_value=0.2 |
| ~~Policy frozen~~ | ~~CRITICAL~~ | **RESOLVED** — KL=0.007, policy_loss=-0.02, policy actively learning |
| Fix #5 not applied | MEDIUM | Deferred — reassess after value clipping rerun |
| No Kaggle notebook | HIGH (for Kaggle goal) | Depends on post-fix rerun evidence |

---

## Post-fix 10M run evidence (FINAL)

**Run:** `training_runs/local_10M_vclip02_2026-03-16/` — 7h04m, 22.9M env steps, 15/15 eval+checkpoints, exit 0

### Verified by execution
- Run completed without error (exit code 0, no NaN at any eval point)
- 15 eval points and 15 checkpoints produced (criterion 5 FULLY MET)
- All metrics finite throughout: v_loss, policy_loss, KL, entropy, reward, imitation, episode_length
- Reward trajectory: -9.04 → -4.69 (48% improvement; best -4.21 at step 19.7M)
- v_loss trajectory: 0.598 → 0.147 (bounded 0.060–0.598; never re-diverges)
- Imitation cost: -322 → -157 (51% reduction over full run)
- Policy active: KL=0.007 (50× baseline), policy_loss=-0.020 (nonzero throughout)

### Inferred from data
- Policy is learning active locomotion (reward improves while episode_length decreases 54→35)
- Decreasing episode_length with improving reward = robot switched from freeze-and-stand to attempting movement
- Imitation cost halving = robot is progressively matching reference motion trajectories
- No plateau visible at 22.9M — improvement trend ongoing at end of run

### Still unknown (requires 50M run)
- Whether convergence continues and at what rate beyond 22.9M
- Whether episode_length recovers (expected: yes, as policy stabilizes)
- Whether LR schedule (Fix #5) would improve convergence speed or final quality
- Whether reward continues trending below -4.0 toward positive values

---

## Post-fix 10M acceptance criteria (2026-03-16)

These criteria determine whether the value clipping intervention was successful:

| # | Criterion | Threshold | How to verify |
|---|-----------|-----------|---------------|
| 1 | v_loss no longer explodes by many orders of magnitude | v_loss final < 10× v_loss initial (not 10^11× as baseline) | Read TensorBoard event files |
| 2 | policy_loss is no longer frozen near zero | abs(policy_loss) > 0.001 at any point after step 0 | TensorBoard |
| 3 | KL shows policy movement | KL > 0.001 at some eval point | TensorBoard |
| 4 | Reward/episode metrics more interpretable | Reward trend clearer (less noisy or directional) | Stdout log + TensorBoard |
| 5 | Logging and checkpointing work | 15 eval points, 15 checkpoints | File count in output dir |
| 6 | No NaN/crash | Exit code 0, no NaN in metrics | Stdout log |
| 7 | Evidence strength | At least 3 of criteria 1-4 met | Composite judgment |

**GO for Kaggle requires:** Criteria 1, 2, 3, 5, 6 all met AND criterion 7 met.
**Another local fix required if:** Criteria 1 not met (v_loss still diverging) OR 3+ criteria fail.
