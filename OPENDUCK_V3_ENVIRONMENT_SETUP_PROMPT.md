# OPENDUCK MINI V3 - ENVIRONMENT SETUP MASTER PROMPT
## Boston Dynamics-Grade Physical AI Development Laboratory

---

## MISSION STATEMENT

Configura un ambiente di sviluppo robotico professionale per l'OpenDuck Mini V3, un robot bipede di ~42cm basato sul design Disney BDX. L'obiettivo e creare un laboratorio virtuale che replichi le capacita di un team Boston Dynamics/Physical Intelligence, con pipeline Sim2Real verificata, automazione completa e workflow infallibile.

**Hardware Target:**
- 16x Servo Feetech STS3215 (19kg/cm, 7.4V, TTL Bus, Magnetic Encoder)
- Raspberry Pi Zero 2W (onboard compute)
- ASUS Zenbook Dual Screen (development workstation)
- Stampante 3D (per parti meccaniche)

---

## PHASE 0: CRITICAL RESEARCH AND VERIFICATION

### 0.1 Repository Ufficiali da Clonare e Analizzare

```bash
# Core OpenDuck Repositories
git clone https://github.com/apirrone/Open_Duck_Mini
git clone https://github.com/apirrone/Open_Duck_Playground
git clone https://github.com/apirrone/Open_Duck_reference_motion_generator
git clone https://github.com/apirrone/Open_Duck_Mini_Runtime

# MuJoCo Ecosystem
git clone https://github.com/google-deepmind/mujoco
git clone https://github.com/google-deepmind/mujoco_menagerie

# Reference Implementations
git clone https://github.com/unitreerobotics/unitree_mujoco
```

### 0.2 HOST CHECKPOINT 1 - Repository Verification
```
[VERIFICA OBBLIGATORIA]
[ ] Tutti i repository clonati con successo?
[ ] Versioni compatibili verificate (Python 3.10+, MuJoCo 3.x)?
[ ] Open_Duck_Playground contiene modelli MJCF per v2?
[ ] Licenze verificate (MIT/Apache)?

WARNING: NON PROCEDERE se qualsiasi check fallisce. Risolvi prima.
```

---

## PHASE 1: MCP SERVER CONFIGURATION

### 1.1 MCP Servers Essenziali per Robotica

Aggiungi al file `~/.claude/mcp.json` (o equivalente Windows):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "C:/Users/matte/Desktop/Desktop OLD/AI/Universita AI/courses/personal_project/robot_jarvis",
               "C:/Users/matte/OpenDuck_Workspace"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "ros2-mcp": {
      "command": "python",
      "args": ["-m", "ros2_mcp_server"],
      "env": {
        "ROS_DOMAIN_ID": "42"
      }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

### 1.2 MCP Server per CAD/Blender Integration

```json
{
  "blender-mcp": {
    "command": "python",
    "args": ["-m", "blender_mcp"],
    "env": {
      "BLENDER_PATH": "C:/Program Files/Blender Foundation/Blender 4.x/blender.exe"
    }
  },
  "autocad-mcp": {
    "command": "python",
    "args": ["-m", "autocad_mcp_server"],
    "comment": "Requires AutoCAD 2018+ with COM interface"
  }
}
```

### 1.3 HOST CHECKPOINT 2 - MCP Verification
```
[VERIFICA OBBLIGATORIA]
[ ] `claude mcp list` mostra tutti i server configurati?
[ ] GitHub MCP puo accedere ai repo OpenDuck?
[ ] Filesystem MCP ha accesso alla directory di lavoro?
[ ] Test comando: "List files in robot_jarvis directory"

WARNING: Esegui test di connettivita per ogni MCP prima di procedere.
```

---

## PHASE 2: PYTHON ENVIRONMENT SETUP

### 2.1 Conda/Mamba Environment

```bash
# Crea environment dedicato
mamba create -n openduck_v3 python=3.11 -y
mamba activate openduck_v3

# Core Dependencies
pip install mujoco>=3.0.0
pip install mujoco-mjx  # JAX-accelerated MuJoCo
pip install jax[cuda12]  # GPU acceleration (se disponibile)
pip install torch torchvision torchaudio
pip install gymnasium[mujoco]
pip install stable-baselines3
pip install onnx onnxruntime

# MuJoCo Playground (Google DeepMind)
pip install playground

# Servo Control
pip install feetech-servo-sdk
pip install pyserial

# Visualization and Logging
pip install tensorboard
pip install wandb
pip install matplotlib
pip install trimesh

# Robot Model Conversion
pip install mjcf-urdf-simple-converter

# Development Tools
pip install uv  # Fast package manager (used by Open_Duck_Playground)
pip install black isort mypy
pip install pytest pytest-cov
```

### 2.2 Verifica Installazione MuJoCo

```python
# test_mujoco_installation.py
import mujoco
import mujoco.viewer

print(f"MuJoCo version: {mujoco.__version__}")

# Test basic simulation
xml = """
<mujoco>
  <worldbody>
    <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
    <geom type="plane" size="1 1 0.1" rgba=".9 .9 .9 1"/>
    <body pos="0 0 1">
      <joint type="free"/>
      <geom type="box" size=".1 .1 .1" rgba="1 0 0 1"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)

print("MuJoCo basic test PASSED")

# Test MJX (JAX acceleration)
try:
    import mujoco.mjx as mjx
    print("MuJoCo MJX available")
except ImportError:
    print("MuJoCo MJX not available - GPU training will be slower")
```

### 2.3 HOST CHECKPOINT 3 - Environment Verification
```
[VERIFICA OBBLIGATORIA]
[ ] `python test_mujoco_installation.py` passa?
[ ] `python -c "import jax; print(jax.devices())"` mostra GPU (se presente)?
[ ] `pip show feetech-servo-sdk` mostra versione installata?
[ ] `uv --version` funziona?

WARNING: Problemi JAX/CUDA sono comuni - documenta workaround se necessario.
```

---

## PHASE 3: OPENDUCK WORKSPACE SETUP

### 3.1 Struttura Directory

```
C:/Users/matte/OpenDuck_Workspace/
├── repos/                      # Cloned repositories
│   ├── Open_Duck_Mini/
│   ├── Open_Duck_Playground/
│   ├── Open_Duck_Mini_Runtime/
│   └── Open_Duck_reference_motion_generator/
├── models/                     # MJCF/URDF models
│   ├── open_duck_mini_v2.xml
│   ├── open_duck_mini_v3_custom.xml  # Le nostre modifiche
│   └── meshes/
├── policies/                   # Trained RL policies
│   ├── checkpoints/
│   ├── onnx/
│   └── logs/
├── sim/                        # Simulation configs
│   ├── terrains/
│   ├── domain_randomization/
│   └── reward_configs/
├── hardware/                   # Hardware-related
│   ├── servo_configs/
│   ├── calibration_data/
│   └── wiring_diagrams/
├── docs/                       # Documentation
│   ├── assembly_guide.md
│   ├── troubleshooting.md
│   └── research_notes/
└── scripts/                    # Utility scripts
    ├── servo_test.py
    ├── model_viewer.py
    └── sim2real_transfer.py
```

### 3.2 Script di Setup Automatico

```python
# setup_workspace.py
import os
import subprocess
from pathlib import Path

WORKSPACE = Path("C:/Users/matte/OpenDuck_Workspace")

REPOS = [
    ("https://github.com/apirrone/Open_Duck_Mini", "Open_Duck_Mini"),
    ("https://github.com/apirrone/Open_Duck_Playground", "Open_Duck_Playground"),
    ("https://github.com/apirrone/Open_Duck_Mini_Runtime", "Open_Duck_Mini_Runtime"),
    ("https://github.com/apirrone/Open_Duck_reference_motion_generator", "reference_motion_generator"),
]

DIRECTORIES = [
    "models/meshes",
    "policies/checkpoints",
    "policies/onnx",
    "policies/logs",
    "sim/terrains",
    "sim/domain_randomization",
    "sim/reward_configs",
    "hardware/servo_configs",
    "hardware/calibration_data",
    "hardware/wiring_diagrams",
    "docs/research_notes",
    "scripts",
]

def main():
    # Create workspace
    WORKSPACE.mkdir(parents=True, exist_ok=True)

    # Create directory structure
    for dir_path in DIRECTORIES:
        (WORKSPACE / dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created {dir_path}")

    # Clone repositories
    repos_dir = WORKSPACE / "repos"
    repos_dir.mkdir(exist_ok=True)

    for url, name in REPOS:
        target = repos_dir / name
        if not target.exists():
            print(f"Cloning {name}...")
            subprocess.run(["git", "clone", url, str(target)], check=True)
        else:
            print(f"{name} already exists")

    print("\nWorkspace setup complete!")
    print(f"  Location: {WORKSPACE}")

if __name__ == "__main__":
    main()
```

---

## PHASE 4: SIMULATION PIPELINE (MuJoCo Playground)

### 4.1 Test Modello OpenDuck Mini V2

```python
# test_openduck_model.py
import mujoco
import mujoco.viewer
from pathlib import Path

WORKSPACE = Path("C:/Users/matte/OpenDuck_Workspace")
MODEL_PATH = WORKSPACE / "repos/Open_Duck_Playground/playground/open_duck_mini_v2/scene.xml"

def test_model():
    # Load model
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    print(f"Model loaded: {MODEL_PATH.name}")
    print(f"  nq (generalized positions): {model.nq}")
    print(f"  nv (generalized velocities): {model.nv}")
    print(f"  nu (actuators): {model.nu}")
    print(f"  nbody: {model.nbody}")

    # List actuators
    print("\nActuators:")
    for i in range(model.nu):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)
        print(f"  [{i}] {name}")

    # Launch viewer
    print("\nLaunching viewer... (press ESC to exit)")
    mujoco.viewer.launch(model, data)

if __name__ == "__main__":
    test_model()
```

### 4.2 Training con MuJoCo Playground

```bash
# Dalla directory Open_Duck_Playground
cd C:/Users/matte/OpenDuck_Workspace/repos/Open_Duck_Playground

# Training flat terrain (baseline)
uv run playground/open_duck_mini_v2/runner.py \
    --task flat_terrain \
    --num_timesteps 50000000 \
    --seed 42

# Training con rough terrain (generalization)
uv run playground/open_duck_mini_v2/runner.py \
    --task rough_terrain \
    --num_timesteps 100000000 \
    --seed 42

# Monitoraggio con TensorBoard
uv run tensorboard --logdir=./logs
```

### 4.3 Domain Randomization Config

```python
# domain_randomization_config.py
"""
Domain Randomization parameters per Sim2Real transfer robusto.
Basato su best practices Boston Dynamics e Google DeepMind.
"""

RANDOMIZATION_PARAMS = {
    # Physics
    "gravity_range": [-10.5, -9.5],  # m/s^2 (nominal: -9.81)
    "friction_range": [0.5, 1.5],     # coefficient
    "damping_scale": [0.8, 1.2],      # multiplier

    # Actuator
    "motor_strength_scale": [0.85, 1.15],
    "motor_backlash_deg": [0.0, 2.0],  # degrees
    "control_delay_ms": [0, 20],        # milliseconds

    # Observation Noise
    "joint_position_noise_deg": 0.5,
    "joint_velocity_noise_deg_s": 1.0,
    "imu_accel_noise": 0.1,
    "imu_gyro_noise": 0.02,

    # Mass/Inertia
    "link_mass_scale": [0.9, 1.1],
    "com_offset_range_mm": [-5, 5],  # mm

    # External Disturbances
    "push_force_range_N": [0, 5],
    "push_interval_steps": [100, 500],
}
```

### 4.4 HOST CHECKPOINT 4 - Simulation Verification
```
[VERIFICA OBBLIGATORIA]
[ ] `test_openduck_model.py` carica il modello correttamente?
[ ] Viewer MuJoCo mostra il robot con tutte le parti visibili?
[ ] Numero di actuator corrisponde a 16 (o expected)?
[ ] Training baseline avvia senza errori?
[ ] TensorBoard mostra curve di reward?

WARNING: Problemi comuni: path meshes errati, versione MuJoCo incompatibile.
```

---

## PHASE 5: SERVO HARDWARE INTERFACE

### 5.1 Test Connessione Servo STS3215

```python
# servo_connection_test.py
"""
Test connessione e comunicazione con servo Feetech STS3215.
Richiede: USB-to-TTL adapter (es. Waveshare Bus Servo Adapter)
"""
from feetech_servo_sdk import *
import time

# Configuration
DEVICE_PORT = "COM3"  # Cambia in base al tuo sistema
BAUDRATE = 1000000    # 1Mbps (default STS3215)
SERVO_ID = 1          # ID del servo da testare

def main():
    # Initialize port handler
    port_handler = PortHandler(DEVICE_PORT)
    packet_handler = PacketHandler()

    # Open port
    if not port_handler.openPort():
        print(f"Failed to open port {DEVICE_PORT}")
        return

    print(f"Port {DEVICE_PORT} opened")

    # Set baudrate
    if not port_handler.setBaudRate(BAUDRATE):
        print(f"Failed to set baudrate {BAUDRATE}")
        return

    print(f"Baudrate set to {BAUDRATE}")

    # Ping servo
    model_number, result, error = packet_handler.ping(port_handler, SERVO_ID)

    if result != COMM_SUCCESS:
        print(f"Failed to ping servo {SERVO_ID}: {packet_handler.getTxRxResult(result)}")
        return

    print(f"Servo {SERVO_ID} found! Model: {model_number}")

    # Read current position
    position, result, error = packet_handler.read2ByteTxRx(port_handler, SERVO_ID, 56)
    if result == COMM_SUCCESS:
        print(f"Current position: {position}")

    # Close port
    port_handler.closePort()
    print("\nServo test complete!")

if __name__ == "__main__":
    main()
```

### 5.2 Calibrazione Multi-Servo

```python
# servo_calibration.py
"""
Calibrazione di tutti i 16 servo per OpenDuck Mini V3.
"""
from feetech_servo_sdk import *
import json
from pathlib import Path

DEVICE_PORT = "COM3"
BAUDRATE = 1000000
NUM_SERVOS = 16

# Mapping servo ID -> joint name
SERVO_MAP = {
    1: "left_hip_yaw",
    2: "left_hip_roll",
    3: "left_hip_pitch",
    4: "left_knee",
    5: "left_ankle_pitch",
    6: "left_ankle_roll",
    7: "right_hip_yaw",
    8: "right_hip_roll",
    9: "right_hip_pitch",
    10: "right_knee",
    11: "right_ankle_pitch",
    12: "right_ankle_roll",
    13: "head_yaw",
    14: "head_pitch",
    15: "left_arm",
    16: "right_arm",
}

def scan_servos(port_handler, packet_handler):
    """Scan per tutti i servo presenti sul bus."""
    found = []
    for servo_id in range(1, 254):
        model, result, _ = packet_handler.ping(port_handler, servo_id)
        if result == COMM_SUCCESS:
            found.append((servo_id, model))
            print(f"  Found servo ID {servo_id} (model: {model})")
    return found

def calibrate_center(port_handler, packet_handler, servo_id):
    """Imposta la posizione corrente come centro (2048)."""
    result, error = packet_handler.write1ByteTxRx(
        port_handler, servo_id,
        47,  # Calibration register
        1    # Trigger calibration
    )
    return result == COMM_SUCCESS

def read_limits(port_handler, packet_handler, servo_id):
    """Legge i limiti min/max del servo."""
    min_pos, _, _ = packet_handler.read2ByteTxRx(port_handler, servo_id, 9)
    max_pos, _, _ = packet_handler.read2ByteTxRx(port_handler, servo_id, 11)
    return min_pos, max_pos

def main():
    port_handler = PortHandler(DEVICE_PORT)
    packet_handler = PacketHandler()

    if not port_handler.openPort():
        print(f"Failed to open {DEVICE_PORT}")
        return

    port_handler.setBaudRate(BAUDRATE)

    print("Scanning for servos...")
    servos = scan_servos(port_handler, packet_handler)
    print(f"\nFound {len(servos)} servos")

    # Calibration data
    calibration = {}

    for servo_id, model in servos:
        joint_name = SERVO_MAP.get(servo_id, f"unknown_{servo_id}")
        min_pos, max_pos = read_limits(port_handler, packet_handler, servo_id)

        calibration[joint_name] = {
            "id": servo_id,
            "model": model,
            "min_position": min_pos,
            "max_position": max_pos,
            "center": 2048,
        }

    # Save calibration
    output_path = Path("C:/Users/matte/OpenDuck_Workspace/hardware/calibration_data/servo_calibration.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(calibration, f, indent=2)

    print(f"\nCalibration saved to {output_path}")
    port_handler.closePort()

if __name__ == "__main__":
    main()
```

### 5.3 HOST CHECKPOINT 5 - Hardware Verification
```
[VERIFICA OBBLIGATORIA]
[ ] USB-TTL adapter riconosciuto dal sistema (check Device Manager)?
[ ] `servo_connection_test.py` trova almeno 1 servo?
[ ] Tutti i 16 servo rispondono al ping?
[ ] Nessun conflitto ID tra servo?
[ ] File calibration JSON generato correttamente?

WARNING: Problemi comuni: driver CH340 mancante, baudrate errato, alimentazione insufficiente.
```

---

## PHASE 6: SIM2REAL TRANSFER PIPELINE

### 6.1 Export Policy to ONNX

```python
# export_to_onnx.py
"""
Esporta policy trainata in formato ONNX per deploy su Raspberry Pi.
"""
import torch
import onnx
from pathlib import Path

def export_policy(checkpoint_path: Path, output_path: Path):
    """
    Esporta un checkpoint PyTorch in formato ONNX.
    """
    # Load checkpoint
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    model = checkpoint["model"]
    model.set_mode_inference()

    # Get input dimensions from model
    obs_dim = model.obs_dim

    # Create dummy input
    dummy_input = torch.randn(1, obs_dim)

    # Export
    torch.onnx.export(
        model,
        dummy_input,
        str(output_path),
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=["observation"],
        output_names=["action"],
        dynamic_axes={
            "observation": {0: "batch_size"},
            "action": {0: "batch_size"}
        }
    )

    # Verify
    onnx_model = onnx.load(str(output_path))
    onnx.checker.check_model(onnx_model)

    print(f"Policy exported to {output_path}")
    return output_path

if __name__ == "__main__":
    checkpoint = Path("C:/Users/matte/OpenDuck_Workspace/policies/checkpoints/best_model.pt")
    output = Path("C:/Users/matte/OpenDuck_Workspace/policies/onnx/walking_policy.onnx")

    export_policy(checkpoint, output)
```

### 6.2 Deploy Script per Raspberry Pi

```python
# deploy_to_rpi.py
"""
Script per deploy della policy sul Raspberry Pi Zero 2W.
"""
import subprocess
from pathlib import Path

RPI_HOST = "openduck.local"  # o IP address
RPI_USER = "pi"
RPI_TARGET_DIR = "/home/pi/openduck"

LOCAL_FILES = [
    "policies/onnx/walking_policy.onnx",
    "hardware/calibration_data/servo_calibration.json",
    "scripts/runtime_controller.py",
]

def deploy():
    workspace = Path("C:/Users/matte/OpenDuck_Workspace")

    # Create target directory on RPi
    subprocess.run([
        "ssh", f"{RPI_USER}@{RPI_HOST}",
        f"mkdir -p {RPI_TARGET_DIR}"
    ], check=True)

    # Copy files
    for file_path in LOCAL_FILES:
        local = workspace / file_path
        if local.exists():
            print(f"Copying {file_path}...")
            subprocess.run([
                "scp", str(local),
                f"{RPI_USER}@{RPI_HOST}:{RPI_TARGET_DIR}/"
            ], check=True)
        else:
            print(f"File not found: {local}")

    print("\nDeploy complete!")
    print(f"  SSH into {RPI_HOST} and run:")
    print(f"  cd {RPI_TARGET_DIR} and python runtime_controller.py")

if __name__ == "__main__":
    deploy()
```

### 6.3 HOST CHECKPOINT 6 - Sim2Real Verification
```
[VERIFICA OBBLIGATORIA]
[ ] Policy ONNX esportata senza errori?
[ ] ONNX model passa il check (onnx.checker)?
[ ] SSH connection al Raspberry Pi funziona?
[ ] ONNXRuntime installato sul Pi (`pip install onnxruntime`)?
[ ] Test inferenza ONNX sul Pi < 20ms per step?

WARNING: Se inferenza troppo lenta, considera quantizzazione INT8.
```

---

## PHASE 7: CUSTOM SLASH COMMANDS (SKILLS)

### 7.1 Skill: /openduck-sim

Crea file `~/.claude/skills/openduck-sim/SKILL.md`:

```markdown
# OpenDuck Simulation Skill

## Description
Lancia e gestisce simulazioni MuJoCo per OpenDuck Mini V3.

## Commands
- `sim start [terrain]` - Avvia simulazione (flat/rough)
- `sim visualize` - Apre viewer MuJoCo
- `sim train [steps]` - Avvia training RL
- `sim export` - Esporta policy in ONNX
- `sim status` - Mostra stato training corrente

## Usage
/openduck-sim start flat
/openduck-sim train 10000000
/openduck-sim export
```

### 7.2 Skill: /openduck-hardware

```markdown
# OpenDuck Hardware Skill

## Description
Gestisce interfaccia hardware con servo e sensori.

## Commands
- `hw scan` - Scansiona servo sul bus
- `hw calibrate [id]` - Calibra servo specifico
- `hw test [id]` - Test movimento servo
- `hw status` - Stato tutti i servo
- `hw deploy` - Deploy su Raspberry Pi

## Safety
WARNING: Tutti i comandi hardware richiedono conferma esplicita.
```

### 7.3 Skill: /openduck-docs

```markdown
# OpenDuck Documentation Skill

## Description
Genera e gestisce documentazione del progetto.

## Commands
- `docs bom` - Mostra Bill of Materials
- `docs assembly` - Guida assemblaggio
- `docs wiring` - Schema cablaggio
- `docs troubleshoot [issue]` - Risoluzione problemi

## Auto-Update
Documentazione sincronizzata con stato attuale del progetto.
```

---

## PHASE 8: VERIFICATION PIPELINE

### 8.1 Automated Test Suite

```python
# run_verification.py
"""
Suite di test automatici per verificare l'intero setup.
Esegui prima di ogni milestone.
"""
import subprocess
import sys
from pathlib import Path

TESTS = [
    ("Python Environment", "python --version"),
    ("MuJoCo Import", "python -c \"import mujoco; print(mujoco.__version__)\""),
    ("JAX Devices", "python -c \"import jax; print(jax.devices())\""),
    ("Feetech SDK", "python -c \"import feetech_servo_sdk; print('OK')\""),
    ("ONNX Runtime", "python -c \"import onnxruntime; print(onnxruntime.__version__)\""),
    ("Playground Import", "python -c \"import playground; print('OK')\""),
    ("OpenDuck Model", "python test_openduck_model.py --no-viewer"),
]

def run_verification():
    results = []

    for name, cmd in TESTS:
        print(f"Testing: {name}...")
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            success = result.returncode == 0
            output = result.stdout.strip() if success else result.stderr.strip()
        except Exception as e:
            success = False
            output = str(e)

        status = "PASS" if success else "FAIL"
        results.append((name, success, output))
        print(f"  {status} {name}: {output[:50]}")

    # Summary
    passed = sum(1 for _, s, _ in results if s)
    total = len(results)

    print(f"\n{'='*50}")
    print(f"VERIFICATION RESULTS: {passed}/{total} passed")

    if passed < total:
        print("\nFAILED TESTS:")
        for name, success, output in results:
            if not success:
                print(f"  - {name}: {output}")
        return False

    print("\nAll verifications passed!")
    return True

if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
```

### 8.2 HOST CHECKPOINT FINALE
```
[VERIFICA FINALE - TUTTI I CHECK DEVONO PASSARE]

ENVIRONMENT:
[ ] Python 3.11+ installato e attivo
[ ] MuJoCo 3.x funzionante con viewer
[ ] JAX configurato (GPU se disponibile)
[ ] Tutti i requirements installati

MCP SERVERS:
[ ] GitHub MCP connesso
[ ] Filesystem MCP con accesso workspace
[ ] Memory MCP attivo

SIMULATION:
[ ] Modello OpenDuck carica correttamente
[ ] Training baseline completa almeno 1M steps
[ ] TensorBoard mostra metriche
[ ] Export ONNX funziona

HARDWARE (quando disponibile):
[ ] USB-TTL adapter riconosciuto
[ ] Almeno 1 servo risponde al ping
[ ] Calibrazione completata

DOCUMENTAZIONE:
[ ] Workspace structure creata
[ ] Scripts di utility presenti
[ ] Troubleshooting guide iniziata

BLOCCO: Non procedere alla produzione se qualsiasi check fallisce!
```

---

## PHASE 9: ROADMAP OPERATIVA

### 9.1 Milestone Timeline

```
MILESTONE 1: Environment Ready
├── [M1.1] Repository clonati e verificati
├── [M1.2] MCP servers configurati
├── [M1.3] Python environment funzionante
└── [M1.4] Test MuJoCo passati

MILESTONE 2: Simulation Validated
├── [M2.1] Modello OpenDuck V2 caricato
├── [M2.2] Training baseline completato
├── [M2.3] Domain randomization configurato
└── [M2.4] Export ONNX verificato

MILESTONE 3: Hardware Interface
├── [M3.1] Servo scan completo (16/16)
├── [M3.2] Calibrazione individuale
├── [M3.3] Test movimento coordinato
└── [M3.4] Protocollo sicurezza definito

MILESTONE 4: Custom Model (V3)
├── [M4.1] Modifiche MJCF per V3
├── [M4.2] Re-training con nuove specs
├── [M4.3] Validazione in sim
└── [M4.4] Confronto V2 vs V3

MILESTONE 5: Sim2Real Transfer
├── [M5.1] Deploy su Raspberry Pi
├── [M5.2] Test statico (no movimento)
├── [M5.3] Test dinamico controllato
└── [M5.4] Fine-tuning in real world

MILESTONE 6: Production Ready
├── [M6.1] Stampa 3D parti custom
├── [M6.2] Assemblaggio meccanico
├── [M6.3] Integration test completo
└── [M6.4] Documentation finale
```

### 9.2 Researcher Roles

```
HOST (Tu - Project Lead)
├── Decision making finale
├── Approvazione checkpoint
├── Resource allocation
└── Risk assessment

REVIEWER (Claude Code)
├── Verifica tecnica automatica
├── Code review
├── Documentation check
└── Best practices enforcement

SPECIALIST AGENTS:
├── Sim Agent: Training and optimization
├── Hardware Agent: Servo interface
├── CAD Agent: Model modifications
└── Deploy Agent: Raspberry Pi ops
```

---

## APPENDIX A: TROUBLESHOOTING

### A.1 Problemi Comuni

```
PROBLEMA: MuJoCo viewer non si apre
SOLUZIONE:
  - Windows: Installa Visual C++ Redistributable
  - Verifica: pip install mujoco --force-reinstall

PROBLEMA: JAX non trova GPU
SOLUZIONE:
  - Verifica CUDA toolkit installato
  - pip install jax[cuda12] -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

PROBLEMA: Servo non risponde
SOLUZIONE:
  - Verifica alimentazione (7.4V minimo)
  - Check baudrate (default 1Mbps)
  - Prova baudrate alternativi: 115200, 500000

PROBLEMA: ONNX export fallisce
SOLUZIONE:
  - Verifica versione PyTorch compatibile
  - Usa opset_version=11 o 12
  - Rimuovi operazioni non supportate
```

### A.2 Risorse Esterne

- Open Duck Discord: https://discord.gg/UtJZsgfQGe
- MuJoCo Documentation: https://mujoco.readthedocs.io/
- MuJoCo Playground: https://playground.mujoco.org/
- Feetech STS3215 Manual: https://www.waveshare.com/wiki/ST3215_Servo
- Boston Dynamics RL Blog: https://bostondynamics.com/blog/starting-on-the-right-foot-with-reinforcement-learning/

---

## EXECUTION INSTRUCTIONS

Quando esegui questo prompt in una nuova istanza Claude Code:

1. **LEGGI** l'intero documento prima di agire
2. **ESEGUI** ogni fase in ordine sequenziale
3. **VERIFICA** ogni checkpoint HOST prima di procedere
4. **DOCUMENTA** problemi e soluzioni trovate
5. **NON SALTARE** verifiche anche se sembrano ridondanti

**Comando di avvio:**
```
Inizia l'esecuzione del setup OpenDuck Mini V3.
Procedi con Phase 0 e riporta lo stato di ogni checkpoint.
```

---

*Prompt generato il 2026-01-14 per OpenDuck Mini V3 Project*
*Basato su ricerche: MuJoCo Playground, Open Duck Repositories, Boston Dynamics RL, Physical AI best practices*
