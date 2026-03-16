# RL Fix Verification Audit — v2

**Date:** 2026-03-15 (updated)
**Auditor:** AIDOS technical audit
**Source document:** `RL_TRAINING_FIXES_V2.md` (robot_jarvis root, 322 lines, dated 2026-01-19)
**Training code location:** `C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground\`
**Upstream:** `https://github.com/apirrone/Open_Duck_Playground` (branch: main)

---

## Repository Structure Correction

### Why the v1 audit returned NOT FOUND

The first audit (2026-03-15, earlier session) searched only inside `robot_jarvis/`. The RL training code lives in a **separate repository** at `C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground\`, cloned from `apirrone/Open_Duck_Playground`. This repo was never symlinked or cloned into `robot_jarvis/`.

### What was missing

The entire training codebase:
- `playground/open_duck_mini_v2/joystick.py` — environment + reward function
- `playground/common/runner.py` — base training runner
- `playground/open_duck_mini_v2/runner.py` — robot-specific runner
- PPO config imported from `mujoco_playground.config.locomotion_params` (installed as PyPI package `playground`)

### How the structure is now corrected

The training repo has been located at its actual path. All 5 fixes have been verified against the actual source code. The fixes exist as **uncommitted local modifications** (visible via `git diff`), not as committed changes.

---

## Fix-by-Fix Verification

### Fix #1: Reward Clipping Bug

| Field | Value |
|-------|-------|
| **Intended change** | Change reward clip lower bound from `0.0` to `-10000.0` to allow negative rewards |
| **Target file** | `playground/open_duck_mini_v2/joystick.py` |
| **Target location** | Line 454 (current), was line 447 in original |
| **Status** | **VERIFIED APPLIED** |
| **Evidence quality** | HIGH — confirmed via `git diff` and direct file read |
| **Risk if wrong** | CRITICAL — root cause of freeze-and-fall behavior |

**Evidence (git diff):**
```python
# BEFORE (committed/upstream):
reward = jp.clip(sum(rewards.values()) * self.dt, 0.0, 10000.0)

# AFTER (local working copy):
reward = jp.clip(sum(rewards.values()) * self.dt, -10000.0, 10000.0)
```

**Classification: VERIFIED APPLIED** — exact match to fix doc specification.

---

### Fix #2: Reward Scale Rebalancing

| Field | Value |
|-------|-------|
| **Intended change** | Rebalance reward scales: alive 20→2, imitation 1→5, stand_still -0.2→-2, action_rate -0.5→-0.1, tracking_sigma 0.01→0.05 |
| **Target file** | `playground/open_duck_mini_v2/joystick.py` |
| **Target location** | Lines 78-94 (current), was lines 77-87 in original |
| **Status** | **APPLIED WITH DEVIATIONS** |
| **Evidence quality** | HIGH — confirmed via `git diff` and direct file read |
| **Risk if wrong** | CRITICAL — reward imbalance causes training to ignore task |

**Evidence — comparison of fix doc vs actual code:**

| Parameter | Fix doc target | Actual code | Match? |
|-----------|---------------|-------------|--------|
| `tracking_lin_vel` | 2.5 (unchanged) | **1.5** | **DEVIATED** — reduced further |
| `tracking_ang_vel` | 6.0 (unchanged) | **1.0** | **DEVIATED** — reduced 6×  |
| `torques` | -1e-3 (unchanged) | **-0.01** | **DEVIATED** — 10× stronger penalty |
| `action_rate` | -0.1 | -0.1 | MATCH |
| `stand_still` | -2.0 | -2.0 | MATCH |
| `alive` | 2.0 | **1.0** | **DEVIATED** — halved further |
| `imitation` | 5.0 | **2.0** | **DEVIATED** — less than specified |
| `tracking_sigma` | 0.05 | 0.05 | MATCH |

**Additional changes NOT in fix doc:**
- `orientation=-1.0` — **NEW** cost component added (penalizes tilting). Not in original fix doc.
- `push_config.enable=False` — **NEW** change. Pushes disabled during training.
- `cost_orientation` imported and added to `_get_reward()` return dict.

**Additional change NOT in fix doc — termination logic:**
- Original: `gravity_z < 0.0` (terminate at 90° tilt)
- Current: `torso_height < 0.08m` (height-based termination)
- This is a significant behavioral change not documented in the fix plan.

**Additional change NOT in fix doc — observation clipping:**
- Added `jp.clip(state, -100.0, 100.0)` and same for `privileged_state`
- Prevents normalizer explosion

**Classification: APPLIED WITH DEVIATIONS** — the spirit of Fix #2 is applied (alive reduced, stand_still increased, tracking_sigma loosened), but 5 of 7 parameters differ from the fix doc specification. Additional undocumented changes were also applied. The deviations appear to be iterative tuning beyond the original fix plan.

---

### Fix #3: Entropy Coefficient

| Field | Value |
|-------|-------|
| **Intended change** | Increase `entropy_cost` from 0.005 to 0.05 |
| **Target file** | `playground/common/runner.py` |
| **Target location** | Line 330 (current) |
| **Status** | **VERIFIED APPLIED** |
| **Evidence quality** | HIGH — confirmed via `git diff` and direct file read |
| **Risk if wrong** | HIGH — entropy collapse to -0.043 prevents exploration |

**Evidence (runner.py line 330):**
```python
self.ppo_params["entropy_cost"] = 0.05  # was 0.005 (10× increase)
```

**Classification: VERIFIED APPLIED** — exact match to fix doc.

---

### Fix #4: PPO Hyperparameters

| Field | Value |
|-------|-------|
| **Intended change** | clipping_epsilon 0.2→0.15, discounting 0.97→0.99, max_grad_norm 1.0→0.5 |
| **Target file** | `playground/common/runner.py` |
| **Target location** | Lines 331-333 (current) |
| **Status** | **VERIFIED APPLIED** |
| **Evidence quality** | HIGH — confirmed via `git diff` and direct file read |
| **Risk if wrong** | MEDIUM — suboptimal but not catastrophic |

**Evidence (runner.py lines 331-333):**
```python
self.ppo_params["clipping_epsilon"] = 0.15  # was 0.2 (25% reduction)
self.ppo_params["discounting"] = 0.99  # was 0.97 (longer horizon)
self.ppo_params["max_grad_norm"] = 0.5  # was 1.0 (tighter clipping)
```

**Classification: VERIFIED APPLIED** — exact match to fix doc.

---

### Fix #5: Learning Rate Schedule

| Field | Value |
|-------|-------|
| **Intended change** | Add warmup + cosine decay LR schedule via optax |
| **Target file** | `playground/common/runner.py` |
| **Target location** | After PPO param setup |
| **Status** | **NOT FOUND** |
| **Evidence quality** | HIGH — full file read, no optax import or schedule code |
| **Risk if wrong** | MEDIUM — constant LR can't escape local minima |

**Evidence:** `runner.py` does not import `optax`. No `warmup_cosine_decay_schedule` call exists. No `learning_rate` override in `ppo_params`. The training uses whatever default LR is in `locomotion_params.brax_ppo_config("BerkeleyHumanoidJoystickFlatTerrain")`.

**Classification: NOT FOUND** — Fix #5 was never applied.

---

## Summary Table

| Fix | Intended Change | Status | Evidence | Risk |
|-----|----------------|--------|----------|------|
| #1 | Allow negative rewards | **VERIFIED APPLIED** | git diff line 454 | CRITICAL if wrong |
| #2 | Rebalance reward scales | **APPLIED WITH DEVIATIONS** | git diff lines 78-94 | CRITICAL if wrong |
| #3 | Entropy coefficient 10× | **VERIFIED APPLIED** | git diff line 330 | HIGH if wrong |
| #4 | PPO hyperparams | **VERIFIED APPLIED** | git diff lines 331-333 | MEDIUM if wrong |
| #5 | LR warmup+cosine schedule | **NOT FOUND** | No optax import | MEDIUM if wrong |

---

## Critical Observations

### 1. Fixes are now COMMITTED (resolved 2026-03-16)

All changes were committed on branch `fixes/iao-v2-verified-2026-03-16`, commit `e93d2b9`.

**Risk: RESOLVED.** Fixes are preserved on a named branch. The `main` branch retains upstream state.

### 2. Fix #2 has significant deviations

The actual reward scales differ substantially from the fix doc. This means:
- The validation metrics in `RL_TRAINING_FIXES_V2.md` may not be accurate for the current config
- The predicted outcomes (alive ~35%, imitation ~35%) won't match current code (alive=1.0, imitation=2.0)
- Someone iterated beyond the original fix plan without updating the documentation

### 3. Undocumented changes were applied

Three changes not in any fix doc:
- `orientation` cost component added (tilting penalty)
- Push perturbations disabled
- Termination changed from gravity-based to height-based
- Observation clipping at ±100

These are potentially significant for training behavior and are not tracked in any fix document.

### 4. Fix #5 (LR schedule) was never applied

The most "advanced" fix was skipped. Training runs with constant learning rate from the upstream default config.

### 5. The `FIXES_APPLIED.md` in the training repo confirms intent

File `C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground\FIXES_APPLIED.md` (dated 2026-01-19 23:40) documents all 5 fixes as applied. But Fix #5 is not in the code. The document is aspirational, not fully accurate.

---

## Existing Training Runs

The training repo contains prior runs:

| Directory | Description |
|-----------|-------------|
| `checkpoints/` | Contains TFEvents files and checkpoint dirs |
| `training_runs/flat_1M_FIXED_v2` | Post-fix 1M step test |
| `training_runs/flat_HOSTILE_REVIEW_FIX` | Hostile review fix run |
| `training_runs/flat_IAO_v2_DYNAMIC` | IAO dynamic rebalancing run |
| `training_runs/flat_IAO_v2_DYNAMIC_restart` | Restart of above |
| `training_runs/overnight_21jan` | Overnight training (21 Jan) |
| `openduck_45M_demo.mp4` | 45M step demo video |
| `OpenDuck_FINAL_WORKING.ipynb` | Colab notebook |
| `OpenDuck_RL_Training_Colab.ipynb` | Colab notebook |
| `OpenDuck_Training_FINAL.ipynb` | Colab notebook |

These runs may contain TensorBoard data that could validate whether the fixes improved training.

---

## Preservation Status (updated 2026-03-16)

| Fix | Classification | Committed? | File(s) | Evidence Type | Remaining Risk |
|-----|---------------|-----------|---------|---------------|----------------|
| #1 | VERIFIED APPLIED | YES (e93d2b9) | joystick.py:454 | git diff + runtime test | LOW — negative reward confirmed at -1.74 |
| #2 | APPLIED WITH DEVIATIONS | YES (e93d2b9) | joystick.py:78-94 | git diff + code read | MEDIUM — deviation impact on training unknown |
| #3 | VERIFIED APPLIED | YES (e93d2b9) | runner.py:330 | git diff | LOW — committed |
| #4 | VERIFIED APPLIED | YES (e93d2b9) | runner.py:331-333 | git diff | LOW — committed |
| #5 | NOT APPLIED | N/A | N/A | full file read, no optax | MEDIUM — constant LR may limit convergence |

**Branch:** `fixes/iao-v2-verified-2026-03-16`
**Commit:** `e93d2b9`

## Undocumented Code Drift

Changes found in the working copy that are NOT in `RL_TRAINING_FIXES_V2.md`:

| Change | Classification | Risk |
|--------|---------------|------|
| `orientation=-1.0` cost added to reward | Likely beneficial — penalizes tilting, prevents fall exploit | LOW |
| `push_config.enable=False` | Needs review — disabling perturbations reduces robustness for sim-to-real | MEDIUM |
| Termination: gravity-based → height-based (0.08m) | Likely beneficial — allows dynamic tilts during walking | LOW |
| Observation clipping at ±100 | Likely beneficial — prevents normalizer explosion | LOW |
| `export_onnx.py` stubbed (TF/Windows issue) | Needs review — blocks ONNX export for deployment | MEDIUM (only at deploy time) |
| `pyproject.toml` CPU deps + loosened versions | Likely beneficial for local dev | LOW |
| Runner: video rendering support added | Likely beneficial — visual validation | LOW |
| `tracking_lin_vel` 2.5→1.5, `tracking_ang_vel` 6.0→1.0 | Unknown impact — significant deviation from fix plan | MEDIUM |
| `torques` -0.001→-0.01 (10× stronger) | Needs review — could over-penalize movement | MEDIUM |
| `alive` 2.0→1.0 (halved from fix plan) | Unknown impact — further reduces alive dominance | LOW |
| `imitation` 5.0→2.0 (less than fix plan) | Unknown impact — less imitation reward than planned | MEDIUM |

## Runtime Validation Results (2026-03-16)

Smoke test executed on local CPU (system Python 3.13.12, JAX 0.8.2, MuJoCo 3.4.0):

| Test | Result | Detail |
|------|--------|--------|
| Env construction | PASS | 6.9s (JIT compilation) |
| Env reset | PASS | 7.9s, obs shape (101,), no NaN |
| Single step (zero action) | PASS | 9.8s, reward=-0.371907 |
| Multi-step (10 random) | PASS | no NaN, obs range [-1.36, 16.65] |
| Negative reward (Fix #1) | PASS | min reward=-1.736498 in 100 bad steps |
| Action size | 14 (10 legs + 4 head) | Corrects prior doc error |
| Obs state size | 101 | Corrects prior doc error |

## Required Next Actions

1. ~~Commit or branch the fixes~~ DONE (e93d2b9)
2. **Decide on Fix #5** — apply LR schedule or explicitly defer with documented rationale
3. **Review TensorBoard logs** from existing Jan runs
4. **Re-enable push perturbations** before any sim-to-real transfer attempt
5. **Re-enable ONNX export** before deployment
