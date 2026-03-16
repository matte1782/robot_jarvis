# RL Codebase Map

**Date:** 2026-03-15
**Source:** `C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground\`
**Upstream:** `https://github.com/apirrone/Open_Duck_Playground` (branch: main)
**Status:** All files verified by direct read

---

## Repository Location

```
C:\Users\matte\OpenDuck_Workspace\
├── repos\
│   └── Open_Duck_Playground\          ← RL training repo (cloned from apirrone)
├── hardware\
├── models\
├── policies\
├── scripts\
└── OPENDUCK_V3_MASTER_REPORT.md
```

**Relation to robot_jarvis:** Separate workspace. robot_jarvis is the firmware/CAD/docs repo. OpenDuck_Workspace is the training/simulation workspace. They share no symlinks or submodules.

---

## Dependency Chain

```
google-deepmind/mujoco_playground (PyPI: "playground")
    ↑ imports
apirrone/Open_Duck_Playground (local clone, with local modifications)
    ↑ reads reference data from
apirrone/Open_Duck_reference_motion_generator
    ↓ exports ONNX to
apirrone/Open_Duck_Mini_Runtime (deployment on real robot)
```

---

## Training Code Map

### Core Environment

| File | Component | Role | Lines | Status |
|------|-----------|------|-------|--------|
| `playground/open_duck_mini_v2/joystick.py` | Environment | Main training env — obs, actions, rewards, termination, stepping | 749 | Modified (uncommitted) |
| `playground/open_duck_mini_v2/base.py` | Base env | MuJoCo model loading, floating base handling, backlash | ~400 | Unmodified |
| `playground/open_duck_mini_v2/constants.py` | Constants | Joint names, body names, XML paths, feet sites | ~80 | Unmodified |
| `playground/open_duck_mini_v2/standing.py` | Alt env | Standing task (not used for locomotion training) | ~700 | Unmodified |

### Reward System

| File | Component | Role | Lines | Status |
|------|-----------|------|-------|--------|
| `playground/common/rewards.py` | Shared rewards | tracking_lin_vel, tracking_ang_vel, cost_torques, cost_action_rate, cost_stand_still, cost_orientation, reward_alive, etc. | 242 | Unmodified |
| `playground/open_duck_mini_v2/custom_rewards.py` | Custom rewards | reward_imitation — matches joint poses/vels/contacts to reference motion | 149 | Unmodified |

**Reward components in current config (joystick.py lines 78-93):**

| Component | Scale | Sign | Source Function |
|-----------|-------|------|----------------|
| tracking_lin_vel | 1.5 | + | `rewards.reward_tracking_lin_vel()` |
| tracking_ang_vel | 1.0 | + | `rewards.reward_tracking_ang_vel()` |
| torques | -0.01 | - | `rewards.cost_torques()` |
| action_rate | -0.1 | - | `rewards.cost_action_rate()` |
| stand_still | -2.0 | - | `rewards.cost_stand_still()` |
| orientation | -1.0 | - | `rewards.cost_orientation()` |
| alive | 1.0 | + | `rewards.reward_alive()` (returns constant 1.0) |
| imitation | 2.0 | + | `custom_rewards.reward_imitation()` |

**Reward aggregation (line 454):**
```python
reward = jp.clip(sum(rewards.values()) * self.dt, -10000.0, 10000.0)
```

### Training Runner

| File | Component | Role | Lines | Status |
|------|-----------|------|-------|--------|
| `playground/common/runner.py` | Base runner | PPO training loop, checkpointing, TensorBoard, video rendering | 371 | Modified (uncommitted) |
| `playground/open_duck_mini_v2/runner.py` | Robot runner | Instantiates Joystick env, domain randomizer, parses CLI args | 80 | Modified (uncommitted) |

**Training entrypoint:**
```bash
python playground/open_duck_mini_v2/runner.py \
    --task flat_terrain \
    --num_timesteps 150000000 \
    --output_dir checkpoints
```

**PPO configuration (runner.py lines 325-333):**
```python
# Base config from upstream
self.ppo_params = locomotion_params.brax_ppo_config("BerkeleyHumanoidJoystickFlatTerrain")
# Local overrides (Fixes #3, #4)
self.ppo_params["entropy_cost"] = 0.05
self.ppo_params["clipping_epsilon"] = 0.15
self.ppo_params["discounting"] = 0.99
self.ppo_params["max_grad_norm"] = 0.5
```

### Domain Randomization

| File | Component | Role | Lines | Status |
|------|-----------|------|-------|--------|
| `playground/common/randomize.py` | Randomizer | Randomizes friction, mass, CoM, KP, armature, qpos0 per env instance | 147 | Unmodified |

**Randomized parameters:**
- Floor friction: U(0.5, 1.0)
- Static friction: x U(0.9, 1.1)
- Armature: x U(1.0, 1.05)
- Torso CoM: +U(-0.05, 0.05) xyz
- All body masses: x U(0.9, 1.1)
- Torso mass extra: +U(-0.1, 0.1)
- Initial qpos: +U(-0.03, 0.03)
- Actuator KP: x U(0.9, 1.1)

### Robot Model (MJCF)

| File | Component | Role |
|------|-----------|------|
| `playground/open_duck_mini_v2/xmls/open_duck_mini_v2.xml` | Base model | 14-DOF robot MJCF |
| `playground/open_duck_mini_v2/xmls/open_duck_mini_v2_backlash.xml` | Backlash model | Model with gear backlash simulation |
| `playground/open_duck_mini_v2/xmls/scene_flat_terrain.xml` | Flat scene | Training environment (flat floor) |
| `playground/open_duck_mini_v2/xmls/scene_flat_terrain_backlash.xml` | Flat + backlash | Flat floor with backlash model |
| `playground/open_duck_mini_v2/xmls/scene_rough_terrain_backlash.xml` | Rough terrain | Rough terrain variant |
| `playground/open_duck_mini_v2/xmls/assets/` | Mesh files | 30+ STL files for robot parts |

### Reference Motion Data

| File | Component | Role |
|------|-----------|------|
| `playground/open_duck_mini_v2/data/polynomial_coefficients.pkl` | Reference data | 3MB serialized file — polynomial coefficients for reference walking motions (generated by Open_Duck_reference_motion_generator) |

**Note:** This file uses Python serialization. It is from a trusted upstream source (apirrone). Do not load arbitrary serialized files from untrusted sources.

### Checkpointing and Export

| File | Component | Role |
|------|-----------|------|
| `playground/common/export_onnx.py` | ONNX export | Exports policy to ONNX format for deployment |
| `playground/common/onnx_infer.py` | ONNX inference | Tests ONNX model inference |

### Observation Vector Structure (from joystick.py lines 587-606)

**State observation (policy input):**

| Component | Dimensions | Description |
|-----------|-----------|-------------|
| noisy_gyro | 3 | Angular velocity with noise |
| noisy_accelerometer | 3 | Linear acceleration with noise |
| command | 3 | Commanded lin_vel_x, lin_vel_y, ang_vel_yaw |
| joint_angles - default | 10 | Joint position error from home pose |
| joint_vel x scale | 10 | Joint velocities x 0.05 |
| last_act | 10 | Previous action |
| last_last_act | 10 | Action 2 steps ago |
| last_last_last_act | 10 | Action 3 steps ago |
| motor_targets | 10 | Current motor position targets |
| contact | 2 | Foot contact binary |
| imitation_phase | 2 | cos/sin of imitation phase |
| **Total** | **73** | |

**Note:** Observations are clipped to [-100, 100] before return.

### Action Vector (10 dimensions)

| Index | Joint | Mapping |
|-------|-------|---------|
| 0-4 | Left leg | hip_yaw, hip_roll, hip_pitch, knee, ankle |
| 5-9 | Right leg | hip_yaw, hip_roll, hip_pitch, knee, ankle |

**Note:** Head joints are NOT actuated by the policy. The robot has 14 joints but only 10 legs are in the action space. Head commands appear in observations but are not controlled by the RL policy.

### Termination (joystick.py lines 490-502)

```python
TERMINATION_HEIGHT = 0.08  # meters
height_violation = data.qpos[2] < TERMINATION_HEIGHT  # torso z-position
nan_violation = jp.isnan(data.qpos).any() | jp.isnan(data.qvel).any()
return height_violation | nan_violation
```

---

## Existing Training Artifacts

| Path | Type | Description |
|------|------|-------------|
| `checkpoints/` | Checkpoints | TFEvents + checkpoint dirs |
| `training_runs/flat_1M_FIXED_v2/` | Run logs | Post-fix 1M step test |
| `training_runs/flat_HOSTILE_REVIEW_FIX/` | Run logs | Hostile review fix run |
| `training_runs/flat_IAO_v2_DYNAMIC/` | Run logs | IAO dynamic run |
| `training_runs/flat_IAO_v2_DYNAMIC_restart/` | Run logs | Restart |
| `training_runs/overnight_21jan/` | Run logs | Overnight 21 Jan |
| `openduck_45M_demo.mp4` | Video | 45M step demo |
| `OpenDuck_FINAL_WORKING.ipynb` | Notebook | Colab training |
| `OpenDuck_RL_Training_Colab.ipynb` | Notebook | Colab training |
| `OpenDuck_Training_FINAL.ipynb` | Notebook | Colab training |
| `FIXES_APPLIED.md` | Doc | Records fix application (partially inaccurate — claims Fix #5 applied) |
| `CRITICAL_ISSUES_ANALYSIS.md` | Doc | Analysis of training issues |
| `IAO_MASTER_PLAN.md` | Doc | Training plan |
| `TRAINING_QUICK_START.md` | Doc | Quick start guide |
