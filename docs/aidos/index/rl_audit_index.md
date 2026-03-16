# RL Audit Index (v3)

**Date:** 2026-03-16 (updated after fix preservation + local validation)
**Scope:** All RL-related artifacts across robot_jarvis and OpenDuck_Workspace
**Preserved branch:** `fixes/iao-v2-verified-2026-03-16` (commit `e93d2b9`)

---

## Architecture

```
C:\Users\matte\
├── Desktop\...\robot_jarvis\           ← Firmware, CAD, docs, AIDOS audits
│   ├── docs\aidos\                     ← THIS audit structure
│   ├── firmware\                       ← Robot firmware (separate git)
│   ├── RL_TRAINING_FIXES_V2.md         ← Original fix plan
│   ├── MUJOCO_SIMULATION_DECISION_MATRIX.md
│   └── venv_rl\                        ← Python venv for RL deps
│
└── OpenDuck_Workspace\                 ← Training/simulation workspace
    └── repos\
        └── Open_Duck_Playground\       ← RL training code (apirrone fork)
            ├── playground\
            │   ├── common\             ← Base runner, rewards, randomize
            │   └── open_duck_mini_v2\  ← Environment, robot runner, MJCF
            ├── training_runs\          ← Prior run logs
            ├── checkpoints\            ← Model checkpoints
            └── *.ipynb                 ← Colab notebooks
```

---

## Reading Order

| # | Artifact | Path | Purpose | Status |
|---|----------|------|---------|--------|
| 1 | **HTML Summary** | `docs/aidos/learning/open_duck_rl_value_clipping_rerun_summary.html` | Visual summary: baseline vs post-fix, blocker state, next steps | **NEW — start here** |
| 2 | Decision Log | `docs/aidos/decisions/rl_current_state_decision_log.md` | GO for 50M decision, blocker state, action plan | **Active (v3)** |
| 3 | Experiment Plan | `docs/aidos/experiments/rl_next_experiment_plan.md` | Full 15-point trajectories, final comparison table | **Active (v3 — FINAL)** |
| 4 | Training Readiness | `docs/aidos/audits/rl_training_readiness.md` | Gate-by-gate: 7/7 criteria met, post-fix evidence | **Active (v3)** |
| 5 | Learning Guide | `docs/aidos/learning/how_rl_works_in_this_project.md` | RL pipeline + what the 10M run proved | **Active (v2)** |
| 6 | TensorBoard Guide | `docs/aidos/learning/how_to_read_tensorboard_for_rl.md` | Metrics reading + actual results from both runs | **Active (v2)** |
| 7 | Fix Verification | `docs/aidos/audits/rl_fix_verification.md` | 5-fix audit: 3 verified, 1 deviated, 1 missing | **Active (v2)** |
| 8 | Codebase Map | `docs/aidos/audits/rl_codebase_map.md` | Full map of training code, obs/action/reward | **Active** |
| 9 | Pipeline Infographic | `docs/aidos/learning/rl_pipeline_infographic.md` | Visual overview of training loop | **Active** |
| 10 | Glossary | `docs/aidos/learning/rl_glossary.md` | 23 terms in project context | **Active** |
| 11 | Failure Modes | `docs/aidos/learning/rl_failure_modes_cheatsheet.md` | 8 failure modes with diagnostics | **Active** |

---

## Artifacts in robot_jarvis Root (pre-existing)

| Artifact | Path | Recommendation |
|----------|------|----------------|
| `RL_TRAINING_FIXES_V2.md` | root | **KEEP** — original fix plan. Note: Fix #2 actual values deviate, Fix #5 never applied |
| `MUJOCO_SIMULATION_DECISION_MATRIX.md` | root | **KEEP** — V2/V3 compatibility reference |
| `OPENDUCK_V3_ENVIRONMENT_SETUP_PROMPT.md` | root | **KEEP but outdated** — references paths and setup from Day 17 |
| `venv_rl/` | root | **KEEP** — needs verification |

## Artifacts in OpenDuck_Workspace (training repo)

| Artifact | Path | Recommendation |
|----------|------|----------------|
| `FIXES_APPLIED.md` | Open_Duck_Playground root | **KEEP but inaccurate** — claims Fix #5 applied (it's not) |
| `CRITICAL_ISSUES_ANALYSIS.md` | Open_Duck_Playground root | **KEEP** — context for fixes |
| `IAO_MASTER_PLAN.md` | Open_Duck_Playground root | **KEEP** — training plan context |
| `TRAINING_QUICK_START.md` | Open_Duck_Playground root | **KEEP** — quick reference |
| `training_runs/` | Open_Duck_Playground | **KEEP** — prior run data (TensorBoard) |
| `checkpoints/` | Open_Duck_Playground | **KEEP** — model checkpoints |
| `*.ipynb` | Open_Duck_Playground | **KEEP** — Colab notebooks (3 files) |
| `openduck_45M_demo.mp4` | Open_Duck_Playground | **KEEP** — training result evidence |

## Redundancy Assessment

| Issue | Files | Recommendation |
|-------|-------|----------------|
| `RL_TRAINING_FIXES_V2.md` (robot_jarvis) vs `FIXES_APPLIED.md` (Open_Duck_Playground) | Overlapping content | Keep both — different perspectives (plan vs record). Note discrepancies in codebase map. |
| Learning guide obs/action details vs codebase map | Overlapping | Acceptable — learning guide explains "why", codebase map documents "what" |
| `OPENDUCK_V3_ENVIRONMENT_SETUP_PROMPT.md` partially overlaps experiment plan | Different scope | Keep both — setup prompt is broader |

---

## Key Discovery Summary

The training code was never missing — it lives at `C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground\` outside the robot_jarvis repo. Cloned 2026-01-14 from `apirrone/Open_Duck_Playground`.

## What Was Validated (2026-03-16 — cumulative)

| What | How | Result |
|------|-----|--------|
| Fixes preserved | git commit on named branch | e93d2b9 |
| All imports | runtime test, system Python 3.13 | PASS |
| Env construct/reset/step | runtime smoke test | PASS, no NaN |
| Fix #1 (negative rewards) | runtime test with bad actions | PASS, reward=-1.74 |
| Action/obs dimensions | runtime observation | 14-dim action, 101-dim obs |
| 10M baseline PPO run | full training run, 22.9M steps | PASS — pathological (v_loss divergent) |
| Value clipping fix (v_clip=0.2) | single-param change + 10M rerun | PASS — 7/7 criteria met |
| Checkpoint save (15 checkpoints) | post-fix run file count | PASS |
| Entropy/KL health | post-fix TensorBoard | PASS — KL=0.007, entropy gradual |

## What Remains Unvalidated

- PPO training beyond 22.9M steps (requires 50M run)
- Episode length recovery (needs 50M to assess)
- ONNX export (currently stubbed)
- Kaggle/Colab GPU runtime
- Domain randomization behavior under 50M training

## Post-fix 10M Run Artifacts (2026-03-16)

| Artifact | Location | Type |
|----------|----------|------|
| Training output | `C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground\training_runs\local_10M_vclip02_2026-03-16\` | TensorBoard events + checkpoints |
| HTML summary | `docs/aidos/learning/open_duck_rl_value_clipping_rerun_summary.html` | Visual summary (baseline vs post-fix) |
| Decision log update | `docs/aidos/decisions/rl_current_state_decision_log.md` | GO for 50M, final blocker state |
| Experiment plan update | `docs/aidos/experiments/rl_next_experiment_plan.md` | Full 15-point trajectories + final comparison |
| Training readiness update | `docs/aidos/audits/rl_training_readiness.md` | Post-fix evidence + 7/7 criteria |

## Artifacts Updated This Pass (2026-03-16 — final post-fix pass)

All under `docs/aidos/`:
- `audits/rl_fix_verification.md` — preservation status, runtime validation, undocumented drift
- `audits/rl_training_readiness.md` — post-preservation gates, corrected dimensions, post-fix evidence
- `decisions/rl_current_state_decision_log.md` — GO for 50M, final blocker reassessment
- `experiments/rl_next_experiment_plan.md` — full 15-point trajectories, baseline vs post-fix FINAL comparison
- `learning/how_rl_works_in_this_project.md` — section 11: what the 10M value clipping run proved
- `learning/how_to_read_tensorboard_for_rl.md` — actual results table updated with final numbers
- `learning/open_duck_rl_value_clipping_rerun_summary.html` — NEW: visual summary infographic
- `index/rl_audit_index.md` — this file (v4)
