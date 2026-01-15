# OpenDuck V3 - Simulation Dependencies
## Critical Missing Packages (Hostile Review Finding)

**Date:** 2026-01-14
**Status:** BLOCKING - Training cannot run until installed

---

## MISSING PACKAGES

### CRITICAL (Must Install)

| Package | Purpose | Install Command |
|---------|---------|-----------------|
| mujoco_playground | MJX environment base | `pip install git+https://github.com/google-deepmind/mujoco_playground.git` |
| brax | PPO training algorithm | `pip install brax` |
| flax | Neural network library | `pip install flax` |
| orbax-checkpoint | Model checkpointing | `pip install orbax-checkpoint` |
| ml-collections | Config management | `pip install ml-collections` |
| tensorboardX | Training logging | `pip install tensorboardX` |
| etils | Google utilities | `pip install etils` |

---

## INSTALLATION SCRIPT

Run this complete installation script:

```bash
# 1. Install mujoco_playground from source
pip install git+https://github.com/google-deepmind/mujoco_playground.git

# 2. Install training dependencies
pip install brax flax tensorboardX orbax-checkpoint ml-collections etils

# 3. Install Open_Duck_Playground in development mode
cd C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground
pip install -e .

# 4. Verify all imports work
python -c "import mujoco; from mujoco import mjx; import jax; import brax; from mujoco_playground._src import mjx_env; print('SUCCESS: All imports work'); print('JAX devices:', jax.devices())"
```

---

## JAX GPU STATUS

### Current Setup
- JAX Version: 0.8.2
- Backend: **CPU ONLY** (no NVIDIA GPU)
- Intel Arc: Not supported by JAX

### Training Time Estimates

| Backend | 150M Timesteps | 1M Timesteps (Test) |
|---------|----------------|---------------------|
| CPU | 2-4 weeks | 4-8 hours |
| GPU (CUDA) | 24-48 hours | 15-30 min |

### Recommendations for GPU Training

**Option A: WSL2 + Cloud GPU**
```bash
wsl -d Ubuntu
# Then use Google Colab, Lambda Labs, or RunPod for GPU
pip install jax[cuda12]
```

**Option B: Google Colab (Free)**
- Upload Open_Duck_Playground to Colab
- Use free T4 GPU
- Limit: 12 hour sessions

**Option C: RunPod/Lambda Labs (Paid)**
- ~$0.20-0.50/hour for A10/A100
- Full 150M timesteps: ~$10-25

---

## VERIFICATION CHECKLIST

After installation, verify each component:

```bash
# Test 1: MuJoCo model loads
python -c "import mujoco; m = mujoco.MjModel.from_xml_path('C:/Users/matte/OpenDuck_Workspace/repos/Open_Duck_Playground/playground/open_duck_mini_v2/xmls/scene_flat_terrain.xml'); print(f'Model loaded: {m.nu} actuators')"

# Test 2: Brax imports
python -c "from brax.training.agents.ppo import train as ppo; print('Brax PPO ready')"

# Test 3: Playground environment
python -c "from playground.open_duck_mini_v2.open_duck_env import OpenDuckEnv; print('Environment ready')"

# Test 4: JAX devices
python -c "import jax; print('JAX devices:', jax.devices())"
```

---

## SERVO COUNT CLARIFICATION

| Context | Servo Count | Notes |
|---------|-------------|-------|
| Simulation (scene_flat_terrain.xml) | 14 | 10 leg + 4 head/neck |
| Physical Robot (full) | 16 | +2 antennas |
| Training Mode | 14 | Antennas disabled |

The discrepancy between "14 actuators" and "16 servos" is correct:
- Training uses 14 servos (antennas not simulated)
- Physical robot has 16 servos (2 antennas added)

---

## QUICK START (After Dependencies Installed)

```bash
# Short CPU training test (1M timesteps)
cd C:\Users\matte\OpenDuck_Workspace\repos\Open_Duck_Playground
uv run playground/open_duck_mini_v2/runner.py --task flat_terrain --num_timesteps 1000000

# Full training (requires GPU)
uv run playground/open_duck_mini_v2/runner.py --task flat_terrain --num_timesteps 150000000
```

---

*Document created from Hostile Technical Review findings*
*Last updated: 2026-01-14*
