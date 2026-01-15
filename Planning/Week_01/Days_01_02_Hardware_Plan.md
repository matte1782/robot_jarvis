# DAYS 1-2 HARDWARE TESTING PLAN (14-15 JANUARY 2026)
**Robot**: OpenDuck Mini V3
**Phase**: Week 01 - Hardware Validation
**Agent**: HARDWARE TESTING SPECIALIST
**Status**: ACTIVE - READY TO EXECUTE

---

## EXECUTIVE SUMMARY

**What We Have Now (14 Jan Evening)**:
- Raspberry Pi 4 Model B (4GB)
- 5× MG90S Servos
- 2× WS2812B LED Rings (16-LED)
- MAX98357A I2S Amplifier
- UBEC 5V/6V 3A
- 3× HC-SR04 Ultrasonic Sensors
- BMS 2S 20A + Battery Holder
- Complete wiring kit
- Soldering station

**Arriving Tomorrow (15 Jan)**:
- 2× PCA9685 PWM Driver (CRITICAL for servo control)
- INMP441 Microphone (6 pcs)
- UBEC 6V 3A (second unit)
- USB-C Power Supply 5.1V 3A

**Mission Objectives**:
- Day 1 (Tonight): 4-5 hours - Pi setup, LED testing, power assembly, documentation
- Day 2 (Tomorrow): 6-7 hours - PCA9685 testing, servo control, audio system, integration

---

## DAY 1: TONIGHT (14 JANUARY) - 4-5 HOURS

**Start Time**: 20:00
**End Time**: 24:00-01:00
**Priority**: Get Pi operational, test basic peripherals, prepare for servo testing tomorrow

---

### HOUR 1-2 (20:00-22:00): RASPBERRY PI 4 SETUP ⚡ CRITICAL

#### Task 1.1: Unbox and Inventory (15 minutes)

**Checklist**:
- [ ] Open Raspberry Pi 4 package
- [ ] Verify model: Pi 4 Model B 4GB RAM
- [ ] Find microSD card (32GB minimum)
- [ ] Check for USB-C cable (temporary power from laptop until PSU arrives)
- [ ] Verify HDMI cable available (for initial setup if needed)

**Photo Documentation**:
Take clear photos of:
1. Pi 4 board (show model number)
2. All accessories laid out
3. Serial number on board (for warranty tracking)

---

#### Task 1.2: OS Installation (30 minutes)

**Step-by-Step Process**:

1. **Download Raspberry Pi Imager**:
   ```bash
   # On Windows laptop
   # Visit: https://www.raspberrypi.com/software/
   # Download and install "Raspberry Pi Imager"
   ```

2. **Flash OS to microSD**:
   - Insert microSD card into laptop card reader
   - Launch Raspberry Pi Imager
   - Choose OS: "Raspberry Pi OS Lite (64-bit)" (Debian Bookworm)
   - Choose Storage: Your microSD card
   - Click gear icon (⚙️) for advanced options:
     ```
     Hostname: openduck-pi4
     Enable SSH: YES
     Username: pi
     Password: openduck2026
     Configure WiFi: YES
       SSID: [Your WiFi Name]
       Password: [Your WiFi Password]
       Country: IT (Italy)
     Locale: Europe/Rome
     Keyboard: it (Italian)
     ```
   - Click "WRITE" and confirm

3. **Verify Flash**:
   - Wait for "Write Successful" message
   - Safely eject SD card
   - Visual inspection: SD card not damaged

**Expected Duration**: 20-25 minutes (depending on SD card speed)

---

#### Task 1.3: First Boot and SSH Connection (20 minutes)

**Hardware Setup**:
```
Raspberry Pi 4 Connections:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
microSD Card    →  SD card slot (underside)
USB-C Power     →  Power port (use laptop USB-C or phone charger 5V 2A minimum)
(Optional) HDMI →  Micro-HDMI port 0 (if SSH fails)
```

**Boot Process**:
1. Insert microSD card into Pi 4
2. Connect USB-C power (laptop or phone charger)
3. **Watch for activity LED**: Green LED should blink (SD card activity)
4. Wait 90 seconds for first boot
5. On Windows laptop, open PowerShell

**SSH Connection**:
```powershell
# Method 1: Try hostname (if mDNS works)
ssh pi@openduck-pi4.local

# Method 2: Find IP address (if Method 1 fails)
# Check router admin page for "openduck-pi4" device
# Then connect via IP
ssh pi@192.168.1.XXX

# Password: openduck2026
```

**Troubleshooting SSH**:
- **Can't find hostname**: Check router DHCP client list for "openduck-pi4"
- **Connection refused**: Wait another 60 seconds, Pi still booting
- **Wrong password**: Re-flash SD card, verify credentials in Imager settings
- **No response**: Connect HDMI + keyboard, check boot process

**Success Criteria**:
- [ ] SSH connection established
- [ ] Can run commands: `ls`, `pwd`, `uname -a`
- [ ] Verify OS: Should show "Linux openduck-pi4 6.1.0-rpi7-rpi-v8 aarch64"

---

#### Task 1.4: System Configuration (30 minutes)

**Run System Configuration**:
```bash
# Update package lists first
sudo apt update

# Launch configuration tool
sudo raspi-config
```

**Configuration Menu Steps**:

1. **System Options** (S):
   - S4 Hostname: Already set to "openduck-pi4" (verify)
   - S5 Boot/Auto Login: B1 Console (no desktop needed)

2. **Interface Options** (I):
   - I2 SSH: Already enabled (verify)
   - I3 VNC: Disable (not needed for headless)
   - I4 SPI: **ENABLE** (for LED ring alternative driver)
   - I5 I2C: **ENABLE** (for future IMU BNO085)
   - I6 Serial Port: Disable login shell, Enable serial hardware
   - I7 1-Wire: Disable (not needed)
   - I8 Remote GPIO: Disable (security risk)

3. **Performance Options** (P):
   - P2 GPU Memory: Set to 128MB (default, camera will need this)

4. **Localisation Options** (L):
   - L1 Locale: en_US.UTF-8 UTF-8 (verify)
   - L2 Timezone: Europe/Rome (verify)
   - L3 Keyboard: Generic 105-key PC, Italian layout
   - L4 WLAN Country: IT Italy (verify)

5. **Advanced Options** (A):
   - A1 Expand Filesystem: **YES** (use full SD card)
   - A3 Memory Split: 128MB (already set in Performance)

**Finish**: Select "Finish", **REBOOT** when prompted

---

#### Task 1.5: System Update and Python Setup (30 minutes)

**After reboot, reconnect via SSH**:
```bash
ssh pi@openduck-pi4.local
```

**Update System Packages**:
```bash
# Full system update (will take 10-15 minutes)
sudo apt update && sudo apt upgrade -y

# Install essential development tools
sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    vim \
    htop \
    i2c-tools \
    python3-smbus \
    libgpiod2 \
    libportaudio2 \
    libasound2-dev

# Verify Python version
python3 --version
# Expected: Python 3.11.x

# Verify pip
pip3 --version
# Expected: pip 23.x
```

**Create Virtual Environment** (Best Practice):
```bash
# Create project directory
mkdir -p ~/openduck_firmware
cd ~/openduck_firmware

# Create virtual environment
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Upgrade pip in venv
pip install --upgrade pip
```

**Install Python Libraries**:
```bash
# GPIO and hardware libraries
pip install RPi.GPIO==0.7.1
pip install gpiod==2.1.3
pip install adafruit-circuitpython-neopixel==6.3.11
pip install rpi-ws281x==5.0.0
pip install adafruit-circuitpython-pca9685==3.4.8
pip install adafruit-circuitpython-motor==3.4.3

# Sensor libraries (for tomorrow)
pip install smbus2==0.4.3
pip install adafruit-circuitpython-bno08x==1.2.4

# Audio libraries (for tomorrow)
pip install pyaudio==0.2.14

# Development tools
pip install pytest==7.4.4
pip install black==23.12.1
pip install pylint==3.0.3

# Utilities
pip install pyyaml==6.0.1
pip install numpy==1.26.3
pip install colorama==0.4.6
```

**Verify Installation**:
```bash
# List installed packages
pip list

# Test GPIO import
python3 -c "import RPi.GPIO as GPIO; print('GPIO OK')"

# Test gpiod import
python3 -c "import gpiod; print('gpiod OK')"
```

**Success Criteria**:
- [ ] All packages installed without errors
- [ ] Python imports work
- [ ] Virtual environment active

---

#### Task 1.6: GPIO Basic Test (15 minutes)

**Create Test Script**:
```bash
cd ~/openduck_firmware
nano test_gpio_basic.py
```

**Test Code**:
```python
#!/usr/bin/env python3
"""
Basic GPIO Test - Raspberry Pi 4
Tests: LED blink on GPIO 17
"""

import RPi.GPIO as GPIO
import time
import sys

# Configuration
LED_PIN = 17  # BCM numbering (Physical pin 11)
BLINK_COUNT = 10
BLINK_DELAY = 0.5

def test_gpio_led():
    """Test GPIO with LED or oscilloscope"""
    print("=" * 50)
    print("GPIO BASIC TEST - LED BLINK")
    print("=" * 50)
    print(f"Testing GPIO{LED_PIN} (Physical Pin 11)")
    print(f"Connect LED: Anode -> GPIO{LED_PIN}, Cathode -> GND (via 220Ω resistor)")
    print()

    try:
        # Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(LED_PIN, GPIO.OUT)

        print(f"Blinking {BLINK_COUNT} times...")
        for i in range(BLINK_COUNT):
            print(f"Blink {i+1}/{BLINK_COUNT}: HIGH", end='\r')
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(BLINK_DELAY)

            print(f"Blink {i+1}/{BLINK_COUNT}: LOW ", end='\r')
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(BLINK_DELAY)

        print()
        print("✓ GPIO test PASSED")
        return True

    except KeyboardInterrupt:
        print("\n⚠ Test interrupted by user")
        return False

    except Exception as e:
        print(f"\n✗ GPIO test FAILED: {e}")
        return False

    finally:
        GPIO.cleanup()
        print("GPIO cleanup complete")

if __name__ == "__main__":
    success = test_gpio_led()
    sys.exit(0 if success else 1)
```

**Run Test**:
```bash
# Make executable
chmod +x test_gpio_basic.py

# Run test (with external LED if available, or observe with multimeter)
python3 test_gpio_basic.py
```

**Expected Output**:
```
==================================================
GPIO BASIC TEST - LED BLINK
==================================================
Testing GPIO17 (Physical Pin 11)
Connect LED: Anode -> GPIO17, Cathode -> GND (via 220Ω resistor)

Blinking 10 times...
Blink 10/10: LOW
✓ GPIO test PASSED
GPIO cleanup complete
```

**Measurement Points** (if have multimeter):
- Physical Pin 11 (GPIO17): Should toggle between 0V and 3.3V
- Frequency: 1 Hz (0.5s HIGH, 0.5s LOW)

**Success Criteria**:
- [ ] Script runs without errors
- [ ] No "Permission denied" errors (if yes, add user to gpio group)
- [ ] Multimeter shows 3.3V HIGH, 0V LOW (if checking)
- [ ] Ready for more complex GPIO tasks

---

### HOUR 2-3 (22:00-23:00): LED RING TESTING ⚡ HIGH PRIORITY

#### Task 2.1: WS2812B Wiring (15 minutes)

**Component Specs**:
- **LED Ring**: WS2812B 16-LED (5V addressable RGB)
- **Current Draw**: ~960mA at 100% white (60mA per LED), ~200mA at typical colors 50% brightness
- **Protocol**: One-wire serial (800 kHz)

**Wiring Diagram**:
```
WS2812B 16-LED Ring Connections
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LED Ring Pin        →  Raspberry Pi 4 Pin         Notes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIN (Data In)       →  GPIO 18 (Physical Pin 12)  PWM0 channel
5V (VCC)            →  5V (Physical Pin 4)        WARNING: Max 500mA from Pi!
GND                 →  GND (Physical Pin 6)       Common ground

IMPORTANT NOTES:
1. For testing: Power from Pi 5V rail (keep brightness <30%)
2. For production: Use external 5V from UBEC (up to 1A available)
3. Use GPIO18 (PWM0) for best performance
4. Keep wires short (<30cm) to avoid signal integrity issues
```

**Physical Wiring Steps**:

1. **Prepare Jumper Wires**:
   - Red wire (15cm): 5V power
   - Black wire (15cm): Ground
   - Yellow/White wire (15cm): Data signal

2. **Connect to LED Ring**:
   - Identify LED ring pins: Usually marked "5V", "GND", "DIN" or "DI"
   - Solder or use JST connectors if ring has them
   - **Verify polarity before connecting**

3. **Connect to Raspberry Pi**:
   ```
   Pi Physical Pin Layout (relevant section):
   ┌─────────────────────────────────────┐
   │  5V  [2] [4]  5V       ← VCC here   │
   │ GND  [6] [8]  GPIO14   ← GND here   │
   │GPIO18[12][14] GND                    │
   │      └─ DIN here                     │
   └─────────────────────────────────────┘
   ```

4. **Safety Check**:
   - [ ] No exposed wire touching other pins
   - [ ] Power wire (red) goes to 5V, NOT 3.3V
   - [ ] Ground connected to GND pin, not any GPIO
   - [ ] Data wire to GPIO18 only

**Power Consideration**:
- Pi 4 can source ~500mA from 5V rail (shared with USB peripherals)
- LED ring at 30% brightness ≈ 200mA → **SAFE**
- LED ring at 100% brightness ≈ 960mA → **EXCEEDS PI LIMIT**
- **Mitigation**: Set `brightness=0.3` in software (hardcoded limit)

---

#### Task 2.2: NeoPixel Library Test (30 minutes)

**Create Test Script**:
```bash
nano ~/openduck_firmware/test_led_ring.py
```

**Test Code**:
```python
#!/usr/bin/env python3
"""
WS2812B LED Ring Test - Raspberry Pi 4
Hardware: 16-LED WS2812B ring on GPIO18
"""

import board
import neopixel
import time
import sys

# Configuration
NUM_PIXELS = 16
PIXEL_PIN = board.D18  # GPIO 18 (PWM0)
ORDER = neopixel.GRB   # WS2812B uses GRB order
BRIGHTNESS = 0.3       # 30% max (SAFETY LIMIT)

def wheel(pos):
    """
    Generate rainbow colors across 0-255 positions.
    Returns (R, G, B) tuple.
    """
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def test_all_leds_white(pixels):
    """Test 1: All LEDs white (verify all work)"""
    print("\n[Test 1] All LEDs WHITE (5 seconds)")
    pixels.fill((255, 255, 255))
    pixels.show()
    time.sleep(5)
    pixels.fill((0, 0, 0))
    pixels.show()
    print("✓ Test 1 complete")

def test_individual_leds(pixels):
    """Test 2: Individual LED control (verify addressing)"""
    print("\n[Test 2] Individual LED sweep (clockwise)")
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue

    for led_id in range(NUM_PIXELS):
        color = colors[led_id % 3]
        pixels[led_id] = color
        pixels.show()
        print(f"  LED {led_id:2d}/15: {color}", end='\r')
        time.sleep(0.2)

    pixels.fill((0, 0, 0))
    pixels.show()
    print("\n✓ Test 2 complete")

def test_rainbow_cycle(pixels, cycles=2):
    """Test 3: Rainbow animation (verify smooth color transitions)"""
    print(f"\n[Test 3] Rainbow cycle ({cycles} rotations)")

    for cycle in range(cycles):
        for j in range(255):
            for i in range(NUM_PIXELS):
                pixel_index = (i * 256 // NUM_PIXELS) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(0.002)  # 2ms per frame (~500 FPS)
        print(f"  Cycle {cycle+1}/{cycles} complete", end='\r')

    pixels.fill((0, 0, 0))
    pixels.show()
    print("\n✓ Test 3 complete")

def test_primary_colors(pixels):
    """Test 4: Primary color accuracy"""
    print("\n[Test 4] Primary colors (RGB test)")

    colors = [
        ("RED", (255, 0, 0)),
        ("GREEN", (0, 255, 0)),
        ("BLUE", (0, 0, 255)),
        ("YELLOW", (255, 255, 0)),
        ("CYAN", (0, 255, 255)),
        ("MAGENTA", (255, 0, 255))
    ]

    for name, color in colors:
        print(f"  Showing {name}...")
        pixels.fill(color)
        pixels.show()
        time.sleep(2)

    pixels.fill((0, 0, 0))
    pixels.show()
    print("✓ Test 4 complete")

def test_brightness_levels(pixels):
    """Test 5: Brightness control"""
    print("\n[Test 5] Brightness levels")

    levels = [0.1, 0.3, 0.5, 0.7, 1.0]

    for level in levels:
        pixels.brightness = level
        pixels.fill((255, 255, 255))  # White
        pixels.show()
        print(f"  Brightness: {level*100:.0f}%")
        time.sleep(2)

    pixels.brightness = BRIGHTNESS  # Reset to safe level
    pixels.fill((0, 0, 0))
    pixels.show()
    print("✓ Test 5 complete")

def main():
    """Main test sequence"""
    print("=" * 60)
    print("WS2812B LED RING TEST")
    print("=" * 60)
    print(f"Hardware: {NUM_PIXELS}-LED ring on GPIO{PIXEL_PIN._pin.id}")
    print(f"Brightness: {BRIGHTNESS*100:.0f}% (safety limit)")
    print(f"Color order: {ORDER}")
    print()

    try:
        # Initialize NeoPixel strip
        print("Initializing NeoPixel...")
        pixels = neopixel.NeoPixel(
            PIXEL_PIN,
            NUM_PIXELS,
            brightness=BRIGHTNESS,
            auto_write=False,
            pixel_order=ORDER
        )
        print("✓ NeoPixel initialized")

        # Run test sequence
        test_all_leds_white(pixels)
        time.sleep(1)

        test_individual_leds(pixels)
        time.sleep(1)

        test_rainbow_cycle(pixels, cycles=2)
        time.sleep(1)

        test_primary_colors(pixels)
        time.sleep(1)

        test_brightness_levels(pixels)

        # Final cleanup
        pixels.fill((0, 0, 0))
        pixels.show()
        pixels.deinit()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return True

    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        pixels.fill((0, 0, 0))
        pixels.show()
        pixels.deinit()
        return False

    except Exception as e:
        print(f"\n\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

**Run Test**:
```bash
chmod +x test_led_ring.py
sudo python3 test_led_ring.py
# NOTE: sudo required for GPIO access to PWM
```

**Expected Output**:
```
============================================================
WS2812B LED RING TEST
============================================================
Hardware: 16-LED ring on GPIO18
Brightness: 30% (safety limit)
Color order: GRB

Initializing NeoPixel...
✓ NeoPixel initialized

[Test 1] All LEDs WHITE (5 seconds)
✓ Test 1 complete

[Test 2] Individual LED sweep (clockwise)
  LED 15/15: (0, 0, 255)
✓ Test 2 complete

[Test 3] Rainbow cycle (2 rotations)
  Cycle 2/2 complete
✓ Test 3 complete

[Test 4] Primary colors (RGB test)
  Showing RED...
  Showing GREEN...
  Showing BLUE...
  Showing YELLOW...
  Showing CYAN...
  Showing MAGENTA...
✓ Test 4 complete

[Test 5] Brightness levels
  Brightness: 10%
  Brightness: 30%
  Brightness: 50%
  Brightness: 70%
  Brightness: 100%
✓ Test 5 complete

============================================================
ALL TESTS PASSED ✓
============================================================
```

---

#### Task 2.3: LED Ring Validation and Documentation (15 minutes)

**Visual Inspection**:
- [ ] All 16 LEDs illuminate (no dead pixels)
- [ ] Colors accurate (red is red, not orange)
- [ ] Brightness smooth across all levels
- [ ] No flickering or random colors
- [ ] Rainbow animation smooth (no jumps)

**Measurements** (if have multimeter):
```bash
# While running test at 30% brightness
# Measure current draw on 5V rail

Expected values:
- Idle (all LEDs off): ~0mA
- 30% brightness white: ~200-250mA
- 100% brightness white: ~900-1000mA (DO NOT RUN from Pi!)
```

**Create Test Report**:
```bash
nano ~/openduck_firmware/test_reports/led_ring_report.txt
```

**Report Template**:
```
WS2812B LED RING TEST REPORT
Date: 2026-01-14
Hardware: 16-LED WS2812B ring
GPIO: GPIO18 (Physical Pin 12)

RESULTS:
[ ] All 16 LEDs functional
[ ] Rainbow animation smooth
[ ] Primary colors accurate (Red, Green, Blue)
[ ] Brightness control working (10%-100%)
[ ] No flickering observed
[ ] Current draw: _____ mA at 30% brightness

ISSUES:
(List any problems observed)

NOTES:
- Brightness limited to 30% for Pi 5V rail safety
- Production will use external UBEC 5V (1A available)
- Consider adding capacitor (1000µF) for power stability

APPROVED: [YES / NO]
Signature: ___________
```

**Success Criteria**:
- [ ] All tests passed
- [ ] Test report created
- [ ] Ready for second LED ring testing (if needed)
- [ ] Documented for production integration

---

### HOUR 3 (23:00-00:00): POWER SYSTEM ASSEMBLY ⚡ HIGH PRIORITY

**SAFETY WARNING**: DO NOT CONNECT BATTERIES YET (not acquired until tomorrow)

#### Task 3.1: Component Inspection (10 minutes)

**Verify Components**:
- [ ] UBEC 5V/6V 3A (ZHITING or similar)
- [ ] BMS 2S 20A (HW-131 or similar)
- [ ] Battery Holder 2S (holds 2× 18650 cells)
- [ ] XT30 Connectors (male/female pairs)
- [ ] Silicon Wire 16AWG (red/black)
- [ ] Heat shrink tubing (various sizes)
- [ ] Soldering iron + solder

**Read Component Datasheets**:
```
UBEC Specifications:
- Input: 6-26V (2S-6S LiPo)
- Output: 5V or 6V (jumper selectable)
- Current: 3A continuous, 5A peak
- Efficiency: ~85%

BMS Specifications:
- Cells: 2S (7.4V nominal)
- Charge Current: 20A max
- Discharge Current: 20A max
- Protection: Overcharge, overdischarge, overcurrent, short circuit
- Balance: Yes (automatic cell balancing during charge)
```

---

#### Task 3.2: BMS to Battery Holder Wiring (30 minutes)

**Wiring Diagram**:
```
Battery Holder (2S) → BMS → Power Output
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Battery Holder:
  Cell 1 (-)  ──┐
  Cell 1 (+)  ──┼─── Mid-point (balance wire)
  Cell 2 (-)  ──┤
  Cell 2 (+)  ──┘

BMS Connections:
  B- (Battery Negative)  ← Cell 1 (-)
  B1 (Balance Wire 1)    ← Cell 1 (+) / Cell 2 (-)
  B+ (Battery Positive)  ← Cell 2 (+)

  P- (Load Negative)     → To UBEC (-)
  P+ (Load Positive)     → To UBEC (+)
```

**Detailed Wiring Steps**:

1. **Prepare Wires** (15 minutes):
   ```bash
   Cut wires:
   - Battery (-) to BMS B-: 10cm black 16AWG
   - Battery mid to BMS B1: 10cm red 16AWG
   - Battery (+) to BMS B+: 10cm red 16AWG
   - BMS P- to XT30: 15cm black 16AWG
   - BMS P+ to XT30: 15cm red 16AWG
   ```

2. **Solder Battery Holder to BMS** (10 minutes):
   ```
   WARNING: DOUBLE CHECK POLARITY BEFORE SOLDERING

   Battery Holder → BMS:
   [Black wire, Cell 1 (-)]  → BMS B- pad
   [Red wire, Cell 1 (+)]    → BMS B1 pad (balance)
   [Red wire, Cell 2 (+)]    → BMS B+ pad

   Soldering Tips:
   - 350°C iron temperature
   - Tin both pad and wire first
   - Solder joint should be shiny, not grainy
   - Hold for 2-3 seconds, let cool naturally
   ```

3. **Add Heat Shrink** (5 minutes):
   - Cut heat shrink: 2cm pieces for each solder joint
   - Slide over wire BEFORE soldering (don't forget!)
   - After soldering: Slide over joint, apply heat gun/lighter
   - Verify: No exposed wire visible

4. **Solder XT30 to BMS Output** (15 minutes):
   ```
   BMS P+/P- → XT30 Male Connector:

   BMS P+ → XT30 Male (+) [Red wire, larger pad]
   BMS P- → XT30 Male (-) [Black wire, smaller pad]

   XT30 Connector Notes:
   - Male connector goes on BMS side (output)
   - Female connector goes on UBEC side (input)
   - Polarized: Impossible to reverse if done correctly
   ```

5. **Label Wires**:
   ```bash
   Use label maker or masking tape + marker:
   - "BATT (+) 7.4V" on battery holder positive
   - "BATT (-) GND" on battery holder negative
   - "BMS OUT (+)" on XT30 male positive
   - "BMS OUT (-)" on XT30 male negative
   ```

**Quality Checks**:
- [ ] All solder joints shiny (not cold/grainy)
- [ ] Heat shrink covers all exposed wire
- [ ] No shorts between (+) and (-) (check with multimeter continuity)
- [ ] Wires secured (gentle tug test)
- [ ] Labels applied and readable

---

#### Task 3.3: UBEC Input Wiring (20 minutes)

**Wiring Steps**:

1. **Prepare XT30 Female for UBEC**:
   ```
   XT30 Female Connector → UBEC Input:

   XT30 Female (+) [Red wire] → UBEC Input (+) [Red wire]
   XT30 Female (-) [Black wire] → UBEC Input (-) [Black wire]

   Wire Length: 10cm (allows some movement)
   ```

2. **Solder XT30 to UBEC Input Wires**:
   - Strip UBEC input wires 5mm
   - Tin both XT30 pads and UBEC wires
   - Solder XT30 female to UBEC input wires
   - **VERIFY POLARITY**: Red to red, black to black
   - Apply heat shrink

3. **Set UBEC Output Voltage**:
   ```
   UBEC Jumper Settings:
   - Locate voltage selection jumper (usually 3-pin header)
   - Position options: 5V | 6V | 7.4V
   - Set to 5V position (for Day 1 testing)

   Verification:
   - Visual: Check jumper position
   - Multimeter: Measure output with 9V battery test (optional)
   ```

4. **Prepare UBEC Output Wires**:
   ```
   UBEC Output → Raspberry Pi (via Dupont connectors):

   UBEC 5V (+) [Red] → Add female Dupont connector
   UBEC GND (-) [Black] → Add female Dupont connector

   Note: We'll connect to Pi tomorrow after confirming voltage
   ```

**Safety Test** (WITHOUT BATTERY):
- [ ] Continuity test: BMS OUT to UBEC IN (should have continuity)
- [ ] Isolation test: (+) to (-) (should be open circuit, infinite resistance)
- [ ] Polarity test: Visual inspection, all red wires on (+), black on (-)
- [ ] Wiggle test: Gentle tugging on connections, nothing loose

---

#### Task 3.4: Power System Documentation (15 minutes)

**Create Power System Diagram**:
```bash
nano ~/openduck_firmware/docs/power_system_day1.txt
```

**Diagram Content**:
```
OPENDUCK MINI V3 - POWER SYSTEM ARCHITECTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATUS: Day 1 - Assembled, NOT powered (no batteries yet)

┌─────────────────────────────────────────────────────────┐
│                    2S BATTERY PACK                      │
│                  (2× Molicel P30B)                      │
│              7.4V Nominal, 3000mAh                      │
│                                                         │
│   Cell 1 (3.7V)  [NOT INSTALLED]                       │
│   Cell 2 (3.7V)  [NOT INSTALLED]                       │
└───┬─────────────────────────────────────────────────┬───┘
    │                                                 │
    │ (+) Red 16AWG                  (-) Black 16AWG │
    │                                                 │
┌───▼─────────────────────────────────────────────────▼───┐
│               BMS 2S 20A (HW-131)                       │
│  Protection: Overcharge, Overdischarge, Overcurrent     │
│  Balance: Automatic during charge                       │
│                                                         │
│  B-  ──── Cell 1 (-)                                   │
│  B1  ──── Cell 1 (+) / Cell 2 (-) [Balance]           │
│  B+  ──── Cell 2 (+)                                   │
│                                                         │
│  P-  ──── Load (-)  [XT30 Male installed]             │
│  P+  ──── Load (+)  [XT30 Male installed]             │
└───┬─────────────────────────────────────────────────┬───┘
    │                                                 │
    │ XT30 Male Connector (output)                    │
    │                                                 │
    │ XT30 Female Connector (input)                   │
    │                                                 │
┌───▼─────────────────────────────────────────────────▼───┐
│            UBEC 5V/6V 3A (ZHITING)                      │
│  Input: 6-26V (2S-6S compatible)                        │
│  Output: 5V @ 3A (jumper set to 5V)                    │
│  Efficiency: ~85%                                       │
│                                                         │
│  IN (+) ◄─── XT30 Female (+)                           │
│  IN (-) ◄─── XT30 Female (-)                           │
│                                                         │
│  OUT 5V (+) ──► [Dupont connector] → Pi 5V (Pin 4)    │
│  OUT GND (-) ──► [Dupont connector] → Pi GND (Pin 6)   │
└─────────────────────────────────────────────────────────┘

MEASUREMENTS TAKEN (Day 1):
- Continuity BMS to UBEC: [   ] Ω (expected <0.5Ω)
- Isolation (+) to (-): ∞ Ω (open circuit) ✓

NEXT STEPS (Day 2):
1. Acquire Molicel P30B batteries (2× cells)
2. Charge cells to 3.7V (storage voltage) before first connection
3. Install cells in holder (observe polarity!)
4. Test voltage at BMS output: Expect 7.4V ± 0.2V
5. Test voltage at UBEC output: Expect 5.0V ± 0.1V
6. Connect to Pi and measure under load

SAFETY NOTES:
⚠ Never connect batteries without BMS installed
⚠ Always verify polarity before connecting
⚠ Keep BMS wires organized (don't short B+ to B-)
⚠ Discharge cells to 3.2V before long-term storage
```

**Take Photos**:
- Photo 1: Full power system layout (BMS + UBEC + battery holder)
- Photo 2: Close-up of BMS connections (label each wire in photo)
- Photo 3: Close-up of XT30 connector (show polarity)
- Photo 4: UBEC input/output connections

**Success Criteria**:
- [ ] Power system fully assembled
- [ ] All connections soldered and heat-shrunk
- [ ] Continuity and isolation tests passed
- [ ] Documentation complete with photos
- [ ] Ready for battery installation tomorrow

---

### HOUR 4 (00:00-01:00): FIRMWARE REPOSITORY AND PLANNING

#### Task 4.1: Create Firmware Directory Structure (20 minutes)

**On Development Laptop** (Windows):
```powershell
# Navigate to project
cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis"

# Create firmware directory structure
mkdir firmware
cd firmware

# Create subdirectories
mkdir src
mkdir src\drivers
mkdir src\drivers\led
mkdir src\drivers\servo
mkdir src\drivers\sensor
mkdir src\drivers\audio
mkdir src\control
mkdir src\core
mkdir src\utils
mkdir config
mkdir tests
mkdir tests\unit
mkdir tests\integration
mkdir docs
mkdir logs

# Create __init__.py files for Python packages
New-Item src\__init__.py
New-Item src\drivers\__init__.py
New-Item src\drivers\led\__init__.py
New-Item src\drivers\servo\__init__.py
New-Item src\drivers\sensor\__init__.py
New-Item src\drivers\audio\__init__.py
New-Item src\control\__init__.py
New-Item src\core\__init__.py
New-Item src\utils\__init__.py
New-Item tests\__init__.py
New-Item tests\unit\__init__.py
New-Item tests\integration\__init__.py
```

---

#### Task 4.2: Create Base Configuration Files (20 minutes)

**requirements.txt**:
```bash
# File: firmware/requirements.txt
# Raspberry Pi 4 Model B (4GB) - Python 3.11+

# GPIO Libraries
RPi.GPIO==0.7.1
gpiod==2.1.3

# LED Control
adafruit-circuitpython-neopixel==6.3.11
rpi-ws281x==5.0.0

# Servo Control
adafruit-circuitpython-pca9685==3.4.8
adafruit-circuitpython-motor==3.4.3
adafruit-circuitpython-servokit==1.3.14

# Sensors
smbus2==0.4.3
adafruit-circuitpython-bno08x==1.2.4

# Audio
pyaudio==0.2.14

# Utilities
numpy==1.26.3
pyyaml==6.0.1
colorama==0.4.6

# Development
pytest==7.4.4
black==23.12.1
pylint==3.0.3
```

**config/hardware_config.yaml**:
```yaml
# Hardware Configuration - OpenDuck Mini V3
# Date: 2026-01-14
# Status: Day 1 - Basic setup

system:
  name: "OpenDuck Mini V3"
  version: "0.1.0-dev"
  hardware_revision: "v3.0"
  board: "Raspberry Pi 4 Model B 4GB"

gpio:
  numbering_mode: "BCM"  # BCM pin numbering
  warnings: false

led:
  ws2812b_rings:
    count: 2
    pixels_per_ring: 16
    gpio_pin: 18  # PWM0
    color_order: "GRB"
    brightness_default: 0.3
    brightness_max: 1.0  # Use external power if >0.5

servo:
  pca9685:
    i2c_address: 0x40
    frequency: 50  # Hz (standard for servos)
    channels: 16

  mg90s_arms:
    count: 5
    voltage: 5.0  # V (from UBEC)
    min_pulse: 500  # µs
    max_pulse: 2500  # µs
    default_angle: 90

power:
  battery:
    type: "2S Li-ion"
    cells: 2
    nominal_voltage: 7.4
    capacity_mah: 3000

  ubec_main:
    input_voltage_min: 6.0
    input_voltage_max: 26.0
    output_voltage: 5.0
    max_current: 3.0

safety:
  voltage_warning_threshold: 6.8  # V
  voltage_critical_threshold: 6.0  # V
  servo_stall_timeout_ms: 300
  max_concurrent_moving_servos: 3
```

**README.md**:
```markdown
# OpenDuck Mini V3 Firmware

**Version**: 0.1.0-dev
**Status**: Week 01 - Hardware Testing Phase
**Board**: Raspberry Pi 4 Model B (4GB)

## Project Structure

```
firmware/
├── src/
│   ├── drivers/          # Hardware abstraction layer
│   │   ├── led/          # WS2812B LED control
│   │   ├── servo/        # PCA9685 + MG90S servo control
│   │   ├── sensor/       # HC-SR04, BNO085, etc.
│   │   └── audio/        # MAX98357A + INMP441
│   ├── control/          # Motion control and kinematics
│   ├── core/             # Main robot logic
│   └── utils/            # Helper functions
├── config/               # YAML configuration files
├── tests/                # Pytest test suite
├── docs/                 # Documentation
└── logs/                 # Runtime logs

## Quick Start

### On Raspberry Pi:

```bash
# Clone repository
git clone <repo_url>
cd firmware

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run main program (when ready)
python3 src/core/robot.py
```

## Hardware Setup - Day 1 Status

**Completed**:
- ✓ Raspberry Pi 4 configured with OS
- ✓ GPIO library tested
- ✓ WS2812B LED ring tested (16 LEDs on GPIO18)
- ✓ Power system assembled (BMS + UBEC, awaiting batteries)

**Pending** (Day 2):
- ⏳ PCA9685 PWM driver (arriving 15 Jan)
- ⏳ MG90S servo testing
- ⏳ Audio amplifier (MAX98357A)
- ⏳ Microphone (INMP441)

## Development Guidelines

- Use `black` for code formatting
- Use `pylint` for linting
- Write unit tests for all drivers
- Document hardware connections in docstrings
- Log all hardware operations

## Safety Features

- Voltage monitoring (prevent brownout)
- Servo stall detection (300ms timeout)
- Current limiting (max 3 servos moving concurrently)
- Emergency stop functionality

## License

MIT License (pending)

## Authors

- Matteo (Project Lead)
- Hardware Testing Specialist (AI Agent)

---

**Last Updated**: 2026-01-14
**Next Milestone**: Day 2 - PCA9685 and servo testing
```

---

#### Task 4.3: Git Repository Initialization (15 minutes)

**Initialize Git** (on laptop):
```powershell
cd firmware

# Initialize repo
git init

# Create .gitignore
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/

# IDE
.vscode/
.idea/

# Logs
logs/*.log
*.log

# OS
.DS_Store
Thumbs.db

# Hardware specific
*.bin
*.hex
*.elf

# Test
.pytest_cache/
htmlcov/
.coverage
"@ | Out-File -FilePath .gitignore -Encoding utf8

# Add files
git add .

# First commit
git commit -m "Initial firmware structure

- Created modular architecture (drivers, control, core)
- Added hardware_config.yaml
- Added requirements.txt with Pi 4 dependencies
- Documented Day 1 hardware testing status
- Ready for Week 01 development

Hardware tested:
- Raspberry Pi 4 (4GB)
- WS2812B LED ring (16 LEDs on GPIO18)
- GPIO basic functionality

Pending (Day 2):
- PCA9685 PWM driver
- MG90S servo testing
- Audio system"

# View commit
git log --oneline
git status
```

**Success Criteria**:
- [ ] Firmware directory structure created
- [ ] Configuration files written
- [ ] Git repository initialized
- [ ] First commit created
- [ ] Ready for Day 2 development

---

#### Task 4.4: Tomorrow's Checklist and Documentation (10 minutes)

**Create Day 2 Preparation File**:
```bash
nano ~/openduck_firmware/docs/day2_checklist.txt
```

**Content**:
```
DAY 2 CHECKLIST (15 JANUARY 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MORNING (08:00-09:00): DELIVERIES AND SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Receive Amazon delivery
    [ ] 2× PCA9685 PWM Driver boards
    [ ] INMP441 Microphone (6 pcs)
    [ ] UBEC 6V 3A (second unit)
    [ ] USB-C Power Supply 5.1V 3A
    [ ] Heat shrink tubing
    [ ] Aluminum case for Pi 4

[ ] Unbox and inventory all components
[ ] Install Pi 4 in aluminum case (better cooling)
[ ] Replace laptop USB-C power with proper 5.1V 3A PSU
[ ] Test Pi boots with new PSU (verify stable 5V)

BLOCK 1 (09:00-11:00): PCA9685 SETUP AND TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Wire PCA9685 to Raspberry Pi 4:
    [ ] VCC (PCA9685) → 3.3V (Pi Pin 1)
    [ ] GND (PCA9685) → GND (Pi Pin 9)
    [ ] SDA (PCA9685) → GPIO2 (Pi Pin 3)
    [ ] SCL (PCA9685) → GPIO3 (Pi Pin 5)
    [ ] V+ (PCA9685) → UBEC 5V output (external power for servos)

[ ] Install I2C tools and scan for device:
    sudo apt install i2c-tools
    i2cdetect -y 1
    # Expected: Device at 0x40

[ ] Install PCA9685 Python library:
    pip install adafruit-circuitpython-pca9685
    pip install adafruit-circuitpython-servokit

[ ] Run PCA9685 test script (verify PWM output)
[ ] Measure PWM signal with oscilloscope/logic analyzer (optional)

BLOCK 2 (11:00-13:00): SINGLE SERVO TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Connect 1× MG90S servo to PCA9685 Channel 0:
    [ ] Brown wire → GND
    [ ] Red wire → V+ (5V from UBEC)
    [ ] Orange wire → PWM Channel 0

[ ] Test servo sweep (0° to 180°)
[ ] Measure current draw during movement
[ ] Test holding torque
[ ] Test stall current (block servo, measure timeout)
[ ] Verify servo responds to angle commands

BLOCK 3 (14:00-16:00): MULTI-SERVO COORDINATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Connect 3× MG90S servos (Channels 0, 1, 2)
[ ] Test simultaneous movement (all 3 servos)
[ ] Test sequential movement (one at a time)
[ ] Measure peak current draw (verify <3A limit)
[ ] Implement current limiting software (max 3 concurrent)

BLOCK 4 (16:00-18:00): AUDIO SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Wire MAX98357A amplifier to Pi:
    [ ] VIN → 5V (Pi Pin 2)
    [ ] GND → GND (Pi Pin 6)
    [ ] BCLK → GPIO18 (Pi Pin 12)
    [ ] LRCLK → GPIO19 (Pi Pin 35)
    [ ] DIN → GPIO21 (Pi Pin 40)

[ ] Configure I2S audio in /boot/config.txt
[ ] Test audio playback (test tone, WAV file)
[ ] Measure current draw during playback

[ ] Wire INMP441 microphone:
    [ ] VDD → 3.3V (Pi Pin 1)
    [ ] GND → GND (Pi Pin 9)
    [ ] SCK → GPIO18 (shared with amp)
    [ ] WS → GPIO19 (shared with amp)
    [ ] SD → GPIO20 (Pi Pin 38)

[ ] Test microphone recording
[ ] Test simultaneous record + playback

BLOCK 5 (18:00-20:00): INTEGRATION TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Test full system:
    [ ] LED ring + Servos
    [ ] LED ring + Audio
    [ ] Servos + Audio
    [ ] All three simultaneously

[ ] Measure total current draw at 5V rail
[ ] Verify no voltage sag below 4.8V
[ ] Check for interference (audio noise during servo movement?)

[ ] Document all test results
[ ] Update firmware with working drivers
[ ] Create integration test suite

OPTIONAL (IF TIME):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Test HC-SR04 ultrasonic sensors
[ ] Begin BNO085 IMU integration (if have level shifters)
[ ] Test all 5 servos simultaneously (with current limiting)

BATTERY ACQUISITION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] If acquired batteries tonight: Test power system with battery
[ ] Charge batteries to 3.7V (storage voltage)
[ ] Measure voltage at BMS output (expect 7.4V)
[ ] Test UBEC output under load (expect 5.0V ±0.1V)
[ ] Measure battery runtime under typical load

SUCCESS CRITERIA FOR DAY 2:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ PCA9685 communicating via I2C
✓ 1-3 MG90S servos responding to commands
✓ Audio playback working (MAX98357A)
✓ Microphone recording working (INMP441)
✓ Total 5V rail current <2.5A during normal operation
✓ All test reports documented
✓ Firmware drivers created for all components
```

---

### HOUR 5 (Optional - If Time): URGENT ORDERS

#### Task 5.1: Molicel P30B Battery Acquisition (20 minutes)

**Option A: Local Acquisition (TONIGHT)**:

1. **Google Search**:
   ```
   Search: "vape shop Monza" OR "batterie 18650 Monza"
   ```

2. **Phone Call Script** (Italian):
   ```
   "Buonasera, cerco batterie Molicel INR18650-P30B.
   Avete 2 o 4 celle disponibili?"

   If YES:
   "Ottimo, quando chiudete stasera? Passo a ritirare."

   If NO:
   "Va bene, conosci altri negozi nella zona? Grazie."
   ```

3. **Purchase**:
   - Buy 4× cells (2S pack + 2 spares)
   - Expected price: €14-20 (€3.50-5 per cell)
   - Verify: Authentic Molicel (check serial number, weight ~45g)

4. **Safety**:
   - Store at room temperature
   - Keep away from metal objects (no shorting!)
   - Charge to 3.7V before first use (storage voltage)

**Option B: Online Order (If Local Fails)**:

1. **TheBatteryShop.eu**:
   - Product: Molicel INR18650-P30B
   - Quantity: 4 cells
   - Shipping: Express (2-3 days)
   - Price: ~€16-18 + shipping

2. **Nkon.nl** (Alternative):
   - Same product, faster EU shipping
   - Usually 2-4 day delivery to Italy

3. **Amazon.it** (Last Resort):
   - Higher price (~€25 for 4 cells)
   - BUT: Next-day delivery available
   - Risk: Counterfeits (check seller reviews)

**Documentation**:
```bash
# Record order details
nano ~/openduck_firmware/docs/battery_order.txt

# Content:
Molicel P30B Battery Order
Date: 2026-01-14
Quantity: 4 cells (2S pack + 2 spares)
Supplier: [Name]
Order Number: [Number]
Expected Delivery: [Date]
Price: €[XX.XX]

Cells received: [ ] YES [ ] NO
Date received: _______
Serial numbers: _____________
Initial voltage test: ___ V (cell 1), ___ V (cell 2)
```

---

#### Task 5.2: FE-URT-1 Servo Controller Order (10 minutes)

**Product**: FE-URT-1 Feetech Serial Servo Controller

**Specifications**:
- Supports: STS series servos (STS3215 for legs)
- Interface: USB-UART
- Channels: 254 servos (overkill, but standard)
- Voltage: 6-12V
- Baud rate: 1M (1Mbps)

**Where to Order**:

1. **AliExpress** (Recommended):
   ```
   Search: "FE-URT-1 servo controller" OR "Feetech USB controller"
   Filters:
   - Ships from: China (15-25 days) OR Spain/Poland (7-12 days)
   - Price: €40-50
   - Seller rating: >95%

   Look for:
   - "Official Feetech Store" (if available)
   - Sellers with >1000 orders
   - Reviews with photos
   ```

2. **Purchase Process**:
   - Add to cart
   - Select shipping: Standard (free) or ePacket (€3-5, faster)
   - Pay via PayPal (buyer protection)
   - Save tracking number

3. **Documentation**:
   ```bash
   nano ~/openduck_firmware/docs/feetech_order.txt

   # Content:
   FE-URT-1 Controller Order
   Date: 2026-01-14
   Supplier: AliExpress
   Seller: [Name]
   Order Number: [Number]
   Price: €[XX.XX]
   Shipping: [Method]
   Expected Delivery: [Date range]
   Tracking: [Number]

   Status: [ ] Ordered [ ] Shipped [ ] Delivered
   ```

**Alternative Suppliers** (if AliExpress unavailable):
- RobotShop.com (EU warehouse, faster but expensive)
- ServoCity.com (USA, long shipping but reliable)
- Direct from Feetech.com.cn (manufacturer, but complex order process)

---

## DAY 1 COMPLETION CHECKLIST

**Core Tasks** (MUST COMPLETE):
- [ ] Raspberry Pi 4 set up with OS and SSH working
- [ ] Python environment configured with all libraries
- [ ] GPIO test passed (LED blink on GPIO17)
- [ ] WS2812B LED ring tested (all 16 LEDs, rainbow animation)
- [ ] Power system assembled (BMS + UBEC + battery holder wired)
- [ ] Firmware repository initialized with git
- [ ] Molicel batteries ordered or acquisition plan confirmed
- [ ] FE-URT-1 controller ordered

**Nice to Have** (If Time Permits):
- [ ] HC-SR04 ultrasonic sensor tested
- [ ] Component inventory photos taken
- [ ] Second LED ring tested
- [ ] Power system tested with bench power supply (if available)

**End of Day Report**:
```
DAY 1 REPORT (14 JANUARY 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIME SPENT: ___ hours (target: 4-5 hours)

COMPLETED TASKS:
1. [ ] Raspberry Pi 4 setup
2. [ ] LED ring testing
3. [ ] Power system assembly
4. [ ] Firmware repository
5. [ ] Component orders

ISSUES ENCOUNTERED:
(List any problems and how they were resolved)

DEFERRED TO DAY 2:
(List tasks moved to tomorrow)

READINESS FOR DAY 2:
[ ] Ready to proceed with PCA9685 testing
[ ] All tools and components organized
[ ] Day 2 checklist printed/accessible

NOTES:
(Additional observations, ideas, concerns)

NEXT SESSION START TIME: ______ (15 Jan)
```

---

---

## DAY 2: 15 JANUARY - 6-7 HOURS

**Start Time**: 09:00
**End Time**: 16:00-17:00
**Priority**: PCA9685 servo control, audio system, full integration

---

### BLOCK 1 (09:00-11:00): PCA9685 PWM DRIVER SETUP ⚡ CRITICAL

**Expected Delivery**: Morning (track package)

#### Task 1.1: PCA9685 Hardware Setup (30 minutes)

**Component Specifications**:
- **PCA9685**: 16-channel 12-bit PWM driver
- **I2C Address**: 0x40 (default), adjustable via solder jumpers
- **PWM Frequency**: 40-1000 Hz (50 Hz standard for servos)
- **Power**: 2.3-5.5V logic (VCC), separate servo power (V+)

**Wiring Diagram**:
```
PCA9685 PWM Driver → Raspberry Pi 4 + Power
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PCA9685 Pin         →  Connection                  Notes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VCC (Logic Power)   →  Pi 3.3V (Pin 1)            PCA9685 logic power
GND (Logic Ground)  →  Pi GND (Pin 9)             Common ground
SDA (I2C Data)      →  Pi GPIO2 (Pin 3)           I2C data line
SCL (I2C Clock)     →  Pi GPIO3 (Pin 5)           I2C clock line

V+ (Servo Power)    →  UBEC 5V Output (+)         Servo power rail
GND (Servo Ground)  →  UBEC GND (-)               Servo ground

IMPORTANT:
- VCC is 3.3V (logic level) - DO NOT connect to 5V!
- V+ is 5V (servo power) - Separate from VCC!
- V+ and VCC grounds must be connected together (common ground)
```

**Physical Wiring Steps**:

1. **Prepare Jumper Wires**:
   ```
   Cut 4× female-female jumpers (15cm each):
   - Red: VCC (3.3V)
   - Black: GND
   - Yellow: SDA
   - Blue: SCL
   ```

2. **Connect to Raspberry Pi**:
   ```
   Pi Header (40-pin) - Left Side:
   ┌──────────────────────────────┐
   │ 3.3V  [1] [2]  5V            │ ← VCC to Pin 1 (3.3V)
   │ SDA   [3] [4]  5V            │ ← SDA to Pin 3 (GPIO2)
   │ SCL   [5] [6]  GND           │ ← SCL to Pin 5 (GPIO3)
   │       [7] [8]  GPIO14        │
   │ GND   [9][10]  GPIO15        │ ← GND to Pin 9
   └──────────────────────────────┘
   ```

3. **Connect Power Rail**:
   ```
   UBEC 5V Output:
   (+) Red wire  → PCA9685 V+ terminal (screw terminal or pin header)
   (-) Black wire → PCA9685 GND terminal (adjacent to V+)

   CRITICAL: V+ is HIGH CURRENT (up to 3A for 5 servos)
   Use 16AWG wire, not jumpers!
   ```

4. **Verify Connections**:
   - [ ] VCC to 3.3V (NOT 5V!)
   - [ ] GND from Pi and UBEC connected to PCA9685 (common ground)
   - [ ] SDA and SCL to correct GPIO pins
   - [ ] V+ from UBEC to PCA9685 servo power rail

---

#### Task 1.2: I2C Configuration and Testing (20 minutes)

**Enable I2C** (should already be enabled from Day 1):
```bash
sudo raspi-config
# Navigate to: Interface Options → I5 I2C → Enable
# Reboot if changed
```

**Install I2C Tools**:
```bash
sudo apt install -y i2c-tools python3-smbus
```

**Scan I2C Bus**:
```bash
# Scan I2C bus 1 (standard on Pi 4)
i2cdetect -y 1
```

**Expected Output**:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --    ← PCA9685 detected!
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- 77
```

**Troubleshooting**:
- **No device at 0x40**: Check wiring (SDA/SCL swapped? VCC connected?)
- **Multiple devices**: Check for solder jumper on PCA9685 (address selection)
- **Bus error**: I2C not enabled in raspi-config
- **UU instead of 40**: Device already claimed by kernel driver (okay, can still use)

**Success Criteria**:
- [ ] Device detected at 0x40
- [ ] No I2C errors
- [ ] Ready for Python library testing

---

#### Task 1.3: PCA9685 Python Driver Test (40 minutes)

**Install Adafruit Library**:
```bash
source ~/openduck_firmware/venv/bin/activate
pip install adafruit-circuitpython-pca9685
pip install adafruit-circuitpython-servokit
```

**Create Test Script**:
```bash
nano ~/openduck_firmware/test_pca9685_pwm.py
```

**Test Code**:
```python
#!/usr/bin/env python3
"""
PCA9685 PWM Driver Test - Raspberry Pi 4
Tests PWM output on all 16 channels (without servo connected)
"""

import time
import sys
from adafruit_pca9685 import PCA9685
import board
import busio

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

def test_pca9685_init():
    """Test 1: Initialize PCA9685"""
    print("\n[Test 1] Initializing PCA9685...")
    try:
        pca = PCA9685(i2c, address=0x40)
        pca.frequency = 50  # 50 Hz for servos
        print(f"✓ PCA9685 initialized at 0x40")
        print(f"✓ Frequency set to {pca.frequency} Hz")
        return pca
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return None

def test_single_channel_pwm(pca, channel=0):
    """Test 2: Single channel PWM sweep"""
    print(f"\n[Test 2] Channel {channel} PWM sweep")
    print("Testing PWM duty cycle 0% → 100% → 0%")

    try:
        # Sweep up
        for duty in range(0, 0xFFFF, 0x1000):
            pca.channels[channel].duty_cycle = duty
            percent = (duty / 0xFFFF) * 100
            print(f"  Duty cycle: {percent:.1f}%", end='\r')
            time.sleep(0.05)

        # Sweep down
        for duty in range(0xFFFF, 0, -0x1000):
            pca.channels[channel].duty_cycle = duty
            percent = (duty / 0xFFFF) * 100
            print(f"  Duty cycle: {percent:.1f}%", end='\r')
            time.sleep(0.05)

        # Turn off
        pca.channels[channel].duty_cycle = 0
        print()
        print(f"✓ Channel {channel} PWM sweep complete")
        return True

    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        return False

def test_all_channels(pca):
    """Test 3: All 16 channels simultaneously"""
    print("\n[Test 3] All 16 channels @ 50% duty cycle")

    try:
        mid_duty = 0xFFFF // 2

        for ch in range(16):
            pca.channels[ch].duty_cycle = mid_duty
            print(f"  Channel {ch:2d}: ON", end='\r')
            time.sleep(0.1)

        print()
        print("All channels active for 3 seconds...")
        time.sleep(3)

        # Turn off all
        for ch in range(16):
            pca.channels[ch].duty_cycle = 0

        print("✓ All channels test complete")
        return True

    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_servo_pulse_range(pca, channel=0):
    """Test 4: Servo-specific pulse widths"""
    print(f"\n[Test 4] Servo pulse range on Channel {channel}")
    print("Testing 500µs, 1500µs, 2500µs pulses (servo range)")

    try:
        # At 50 Hz, period = 20ms = 20000µs
        # 12-bit resolution: 4096 steps
        # Each step = 20000µs / 4096 = 4.88µs

        pulse_widths = [
            ("MIN (500µs)", int(500 / 4.88)),
            ("CENTER (1500µs)", int(1500 / 4.88)),
            ("MAX (2500µs)", int(2500 / 4.88))
        ]

        for name, pulse_value in pulse_widths:
            pca.channels[channel].duty_cycle = pulse_value * 16  # Convert to 16-bit
            print(f"  {name}: {pulse_value} (12-bit value)")
            time.sleep(2)

        # Turn off
        pca.channels[channel].duty_cycle = 0
        print("✓ Servo pulse range test complete")
        return True

    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def main():
    """Main test sequence"""
    print("=" * 60)
    print("PCA9685 PWM DRIVER TEST")
    print("=" * 60)
    print("Hardware: PCA9685 16-channel PWM driver")
    print("I2C Address: 0x40")
    print("Frequency: 50 Hz (servo standard)")
    print()

    try:
        # Test 1: Initialize
        pca = test_pca9685_init()
        if not pca:
            return False

        time.sleep(1)

        # Test 2: Single channel
        if not test_single_channel_pwm(pca, channel=0):
            return False

        time.sleep(1)

        # Test 3: All channels
        if not test_all_channels(pca):
            return False

        time.sleep(1)

        # Test 4: Servo pulses
        if not test_servo_pulse_range(pca, channel=0):
            return False

        # Cleanup
        pca.deinit()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        print("\nNEXT STEP: Connect MG90S servo to Channel 0")
        return True

    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        return False

    except Exception as e:
        print(f"\n\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

**Run Test**:
```bash
chmod +x test_pca9685_pwm.py
python3 test_pca9685_pwm.py
```

**Expected Output**:
```
============================================================
PCA9685 PWM DRIVER TEST
============================================================
Hardware: PCA9685 16-channel PWM driver
I2C Address: 0x40
Frequency: 50 Hz (servo standard)

[Test 1] Initializing PCA9685...
✓ PCA9685 initialized at 0x40
✓ Frequency set to 50 Hz

[Test 2] Channel 0 PWM sweep
  Duty cycle: 93.8%
✓ Channel 0 PWM sweep complete

[Test 3] All 16 channels @ 50% duty cycle
All channels active for 3 seconds...
✓ All channels test complete

[Test 4] Servo pulse range on Channel 0
  MIN (500µs): 102 (12-bit value)
  CENTER (1500µs): 307 (12-bit value)
  MAX (2500µs): 512 (12-bit value)
✓ Servo pulse range test complete

============================================================
ALL TESTS PASSED ✓
============================================================

NEXT STEP: Connect MG90S servo to Channel 0
```

**Measurement** (if have oscilloscope):
- Connect probe to PCA9685 Channel 0 output pin
- Set scope to 5ms/div, 2V/div
- Observe:
  - Frequency: 50 Hz (20ms period)
  - Pulse width: 500µs to 2500µs range
  - Voltage: 3.3V high, 0V low (logic level)

**Success Criteria**:
- [ ] All tests passed
- [ ] PWM output verified (visually or with scope)
- [ ] Ready for servo connection

---

### BLOCK 2 (11:00-13:00): MG90S SERVO TESTING ⚡ CRITICAL

#### Task 2.1: Single Servo Connection and Test (45 minutes)

**Safety First**:
```
⚠ WARNING: Servo Power Requirements
- MG90S draws 100-400mA during movement
- UBEC 5V output: 3A max
- Start with 1 servo to verify power system
```

**Wiring Diagram**:
```
MG90S Servo → PCA9685 Channel 0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Servo Wire Color    →  PCA9685 Connection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Brown (GND)         →  GND rail (near V+)
Red (Power)         →  V+ rail (5V from UBEC)
Orange (Signal)     →  Channel 0 PWM output pin

NOTES:
- Keep servo wires short (<30cm) to minimize voltage drop
- Ensure V+ and GND rails are connected to UBEC
- Do NOT power servo from Pi GPIO (insufficient current)
```

**Physical Connection**:
1. Locate PCA9685 Channel 0 (usually labeled on board)
2. Insert servo connector (3-pin, correct orientation)
3. Verify colors: Brown-Red-Orange from left to right
4. Gently tug servo connector (ensure seated properly)

**Create Servo Test Script**:
```bash
nano ~/openduck_firmware/test_servo_single.py
```

**Test Code**:
```python
#!/usr/bin/env python3
"""
MG90S Single Servo Test - Raspberry Pi 4 + PCA9685
Tests: Position control, speed, holding torque
"""

import time
import sys
from adafruit_servokit import ServoKit

# Configuration
SERVO_CHANNEL = 0
MIN_ANGLE = 0
MAX_ANGLE = 180
CENTER_ANGLE = 90

def initialize_servo():
    """Initialize ServoKit and configure servo"""
    print("\n[Setup] Initializing PCA9685 and ServoKit...")
    try:
        # Initialize PCA9685 (16 channels, 12-bit)
        kit = ServoKit(channels=16, address=0x40)

        # Configure servo parameters for MG90S
        kit.servo[SERVO_CHANNEL].set_pulse_width_range(500, 2500)

        print(f"✓ ServoKit initialized (I2C 0x40)")
        print(f"✓ Servo {SERVO_CHANNEL} configured")
        print(f"  - Pulse range: 500-2500 µs")
        print(f"  - Angle range: {MIN_ANGLE}° to {MAX_ANGLE}°")
        return kit

    except Exception as e:
        print(f"✗ FAILED: {e}")
        return None

def test_center_position(kit):
    """Test 1: Move to center position"""
    print(f"\n[Test 1] Move to center ({CENTER_ANGLE}°)")
    try:
        kit.servo[SERVO_CHANNEL].angle = CENTER_ANGLE
        print(f"  Command sent: {CENTER_ANGLE}°")
        print("  Waiting 1 second for movement...")
        time.sleep(1)
        print("✓ Servo should be at center position")
        input("  Press Enter to continue...")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_full_sweep(kit):
    """Test 2: Full range sweep (0° to 180° to 0°)"""
    print(f"\n[Test 2] Full range sweep ({MIN_ANGLE}° → {MAX_ANGLE}° → {MIN_ANGLE}°)")
    try:
        # Move to min
        print(f"  Moving to {MIN_ANGLE}°...")
        kit.servo[SERVO_CHANNEL].angle = MIN_ANGLE
        time.sleep(1)

        # Move to max
        print(f"  Moving to {MAX_ANGLE}°...")
        kit.servo[SERVO_CHANNEL].angle = MAX_ANGLE
        time.sleep(1)

        # Return to center
        print(f"  Returning to {CENTER_ANGLE}°...")
        kit.servo[SERVO_CHANNEL].angle = CENTER_ANGLE
        time.sleep(1)

        print("✓ Full sweep complete")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_smooth_sweep(kit, step=10, delay=0.1):
    """Test 3: Smooth sweep with small steps"""
    print(f"\n[Test 3] Smooth sweep (step={step}°, delay={delay}s)")
    try:
        # Sweep up
        print(f"  Sweeping {MIN_ANGLE}° → {MAX_ANGLE}°...")
        for angle in range(MIN_ANGLE, MAX_ANGLE + 1, step):
            kit.servo[SERVO_CHANNEL].angle = angle
            print(f"  Angle: {angle:3d}°", end='\r')
            time.sleep(delay)

        print()

        # Sweep down
        print(f"  Sweeping {MAX_ANGLE}° → {MIN_ANGLE}°...")
        for angle in range(MAX_ANGLE, MIN_ANGLE - 1, -step):
            kit.servo[SERVO_CHANNEL].angle = angle
            print(f"  Angle: {angle:3d}°", end='\r')
            time.sleep(delay)

        print()

        # Return to center
        kit.servo[SERVO_CHANNEL].angle = CENTER_ANGLE
        print("✓ Smooth sweep complete")
        return True
    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        return False

def test_discrete_positions(kit):
    """Test 4: Move to discrete positions"""
    print("\n[Test 4] Discrete position test")
    positions = [0, 45, 90, 135, 180, 90]

    try:
        for pos in positions:
            print(f"  Moving to {pos}°...")
            kit.servo[SERVO_CHANNEL].angle = pos
            time.sleep(0.8)

        print("✓ Discrete position test complete")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_holding_torque(kit):
    """Test 5: Holding torque (manual test)"""
    print("\n[Test 5] Holding torque test (MANUAL)")
    print("Servo will move to 90° and hold position")
    print("Try to manually rotate the servo arm")
    print("You should feel resistance (holding torque)")

    try:
        kit.servo[SERVO_CHANNEL].angle = 90
        input("\nPress Enter after testing holding torque...")
        print("✓ Holding torque test complete")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_speed_measurement(kit):
    """Test 6: Measure servo speed"""
    print("\n[Test 6] Speed measurement (60° movement)")
    print("MG90S spec: 0.1s/60° @ 4.8V, 0.08s/60° @ 6V")
    print("Expected @ 5V: ~0.09s/60°")

    try:
        # Prepare
        kit.servo[SERVO_CHANNEL].angle = 45
        time.sleep(1)

        # Time a 60° movement
        print("  Timing 60° movement (45° → 105°)...")
        start = time.time()
        kit.servo[SERVO_CHANNEL].angle = 105
        time.sleep(0.5)  # Wait for completion
        elapsed = time.time() - start

        print(f"  Measured time: {elapsed:.3f}s")
        print(f"  Expected: ~0.09s (command) + 0.09s (movement) = 0.18s")
        print("✓ Speed measurement complete")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def main():
    """Main test sequence"""
    print("=" * 60)
    print("MG90S SINGLE SERVO TEST")
    print("=" * 60)
    print(f"Hardware: MG90S servo on PCA9685 Channel {SERVO_CHANNEL}")
    print("Power: 5V from UBEC (via PCA9685 V+ rail)")
    print("Control: I2C @ 0x40, 50 Hz PWM")
    print()
    print("SAFETY CHECKS:")
    print("  ✓ Servo connected to Channel 0?")
    print("  ✓ V+ rail powered from UBEC 5V?")
    print("  ✓ Common ground between Pi, PCA9685, UBEC?")
    print("  ✓ Servo arm free to move (no obstructions)?")
    print()
    input("Press Enter to start tests...")

    try:
        # Initialize
        kit = initialize_servo()
        if not kit:
            return False

        # Run test sequence
        tests = [
            test_center_position,
            test_full_sweep,
            test_smooth_sweep,
            test_discrete_positions,
            test_holding_torque,
            test_speed_measurement
        ]

        for test in tests:
            if not test(kit):
                print("\n⚠ Test failed, aborting sequence")
                return False
            time.sleep(1)

        # Return to center and finish
        kit.servo[SERVO_CHANNEL].angle = CENTER_ANGLE
        time.sleep(0.5)

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        print("\nNEXT STEP: Test multiple servos simultaneously")
        return True

    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        # Safety: return to center
        try:
            kit.servo[SERVO_CHANNEL].angle = CENTER_ANGLE
        except:
            pass
        return False

    except Exception as e:
        print(f"\n\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

**Run Test**:
```bash
chmod +x test_servo_single.py
python3 test_servo_single.py
```

**Manual Verification Checklist**:
- [ ] Servo moves to center (90°) smoothly
- [ ] Full sweep (0° to 180°) completes without stalling
- [ ] Smooth sweep has no jerky movements
- [ ] Servo holds position when force applied (holding torque)
- [ ] Speed matches datasheet (~0.1s/60°)
- [ ] No unusual noise (grinding, buzzing)

**Current Measurement**:
```bash
# While servo is running, measure current on 5V rail
# Use multimeter in series with UBEC 5V output

Expected current draw:
- Idle (holding position): 100-120mA
- Moving (60° sweep): 300-400mA
- Stalled (blocked): 900-1200mA (DO NOT SUSTAIN)
```

---

#### Task 2.2: Multi-Servo Testing (45 minutes)

**Connect 3 Servos**:
```
MG90S Servo Connections:
Channel 0: Left shoulder
Channel 1: Left gripper
Channel 2: Right shoulder
```

**Create Multi-Servo Test**:
```bash
nano ~/openduck_firmware/test_servo_multi.py
```

**Test Code** (abbreviated, full version similar to single servo):
```python
#!/usr/bin/env python3
"""
MG90S Multi-Servo Test - 3 servos simultaneously
Tests: Current limiting, coordination, power stability
"""

import time
import sys
from adafruit_servokit import ServoKit

SERVO_CHANNELS = [0, 1, 2]
CENTER_ANGLE = 90

def test_sequential_movement(kit):
    """Test 1: Move servos one at a time (low current)"""
    print("\n[Test 1] Sequential movement (one servo at a time)")
    try:
        for ch in SERVO_CHANNELS:
            print(f"  Moving servo {ch} to 0°...")
            kit.servo[ch].angle = 0
            time.sleep(0.5)

        for ch in SERVO_CHANNELS:
            print(f"  Moving servo {ch} to 180°...")
            kit.servo[ch].angle = 180
            time.sleep(0.5)

        for ch in SERVO_CHANNELS:
            kit.servo[ch].angle = CENTER_ANGLE
            time.sleep(0.5)

        print("✓ Sequential movement complete")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_simultaneous_movement(kit):
    """Test 2: Move all servos at once (high current)"""
    print("\n[Test 2] Simultaneous movement (all servos)")
    print("  ⚠ MONITORING: Watch for voltage sag or Pi brownout")

    try:
        # All to 0°
        print("  All servos → 0°...")
        for ch in SERVO_CHANNELS:
            kit.servo[ch].angle = 0
        time.sleep(1)

        # All to 180°
        print("  All servos → 180°...")
        for ch in SERVO_CHANNELS:
            kit.servo[ch].angle = 180
        time.sleep(1)

        # All to center
        print("  All servos → 90°...")
        for ch in SERVO_CHANNELS:
            kit.servo[ch].angle = CENTER_ANGLE
        time.sleep(1)

        print("✓ Simultaneous movement complete")
        print("  If no brownout occurred, power system is adequate")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_wave_pattern(kit):
    """Test 3: Wave pattern (coordinated movement)"""
    print("\n[Test 3] Wave pattern (coordinated movement)")
    try:
        for cycle in range(2):
            print(f"  Cycle {cycle+1}/2...")
            # Wave right
            for ch in SERVO_CHANNELS:
                kit.servo[ch].angle = 180
                time.sleep(0.3)
            # Wave left
            for ch in reversed(SERVO_CHANNELS):
                kit.servo[ch].angle = 0
                time.sleep(0.3)

        # Return to center
        for ch in SERVO_CHANNELS:
            kit.servo[ch].angle = CENTER_ANGLE
        time.sleep(0.5)

        print("✓ Wave pattern complete")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def main():
    print("=" * 60)
    print("MG90S MULTI-SERVO TEST (3 SERVOS)")
    print("=" * 60)
    print(f"Hardware: MG90S servos on Channels {SERVO_CHANNELS}")
    print("Expected current: 1.0-1.2A simultaneous movement")
    print("UBEC capacity: 3.0A")
    print()
    input("Press Enter to start tests...")

    try:
        kit = ServoKit(channels=16, address=0x40)
        for ch in SERVO_CHANNELS:
            kit.servo[ch].set_pulse_width_range(500, 2500)

        # Run tests
        if not test_sequential_movement(kit):
            return False
        time.sleep(2)

        if not test_simultaneous_movement(kit):
            return False
        time.sleep(2)

        if not test_wave_pattern(kit):
            return False

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return True

    except KeyboardInterrupt:
        print("\n⚠ Interrupted")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

**Run Test**:
```bash
python3 test_servo_multi.py
```

**Monitor During Test**:
- [ ] Pi does not reboot (no brownout)
- [ ] Servos move smoothly (no stuttering)
- [ ] No unusual smells (overheating)
- [ ] Current draw stays below 2.5A (measure with multimeter)

**Success Criteria**:
- [ ] All 3 servos respond correctly
- [ ] Simultaneous movement works without issues
- [ ] No power system problems
- [ ] Ready for 5-servo testing (if UBEC handles 3 servos well)

---

### BLOCK 3 (14:00-16:00): AUDIO SYSTEM TESTING

#### Task 3.1: MAX98357A Audio Amplifier Setup (45 minutes)

**Component Specs**:
- **MAX98357A**: Class D I2S audio amplifier
- **Power**: 5V, max 300mA @ max volume
- **Interface**: I2S (3-wire)
- **Output**: 3W mono (4Ω speaker) or 1.4W (8Ω speaker)

**Wiring Diagram**:
```
MAX98357A → Raspberry Pi 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MAX98357A Pin       →  Pi Pin                     Notes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIN                 →  5V (Pin 2 or Pin 4)        Power
GND                 →  GND (Pin 6)                Ground
BCLK (Bit Clock)    →  GPIO18 (Pin 12)            I2S bit clock
LRCLK (LR Clock)    →  GPIO19 (Pin 35)            I2S word select
DIN (Data In)       →  GPIO21 (Pin 40)            I2S data
SD (Shutdown)       →  Leave floating (always on)  Optional gain control

Speaker Out (+/-)   →  8Ω 2W speaker              Red/Black wires
```

**I2S Configuration**:
```bash
# Edit boot config
sudo nano /boot/config.txt

# Add at end of file (if not already present):
dtparam=audio=on
dtoverlay=i2s-mmap
dtoverlay=hifiberry-dac

# Save and reboot
sudo reboot
```

**After Reboot, Test Audio Device**:
```bash
# List audio devices
aplay -l

# Expected output should show:
# card 0: bcm2835 [bcm2835 ALSA], device 0: ...
# OR
# card 0: sndrpii2s [snd_rpi_i2s], device 0: ...
```

**Test Audio Playback**:
```bash
# Generate test tone
speaker-test -c 2 -t wav

# You should hear voice saying "Front Left, Front Right" from speaker
# If silent: Check wiring, volume level, speaker connection
```

**Create Audio Test Script**:
```bash
nano ~/openduck_firmware/test_audio_playback.py
```

**Test Code**:
```python
#!/usr/bin/env python3
"""
MAX98357A Audio Test - Raspberry Pi 4
Tests: Tone generation, WAV playback, volume control
"""

import numpy as np
import wave
import os
import sys
import subprocess

def generate_test_tone(filename, frequency=440, duration=2, sample_rate=44100):
    """Generate a test tone WAV file"""
    print(f"\n[Setup] Generating {frequency} Hz test tone ({duration}s)...")

    # Generate sine wave
    t = np.linspace(0, duration, int(sample_rate * duration))
    waveform = np.sin(2 * np.pi * frequency * t)

    # Convert to 16-bit PCM
    waveform_int = np.int16(waveform * 32767)

    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(waveform_int.tobytes())

    print(f"✓ Test tone saved to {filename}")

def test_playback(filename):
    """Play audio file using aplay"""
    print(f"\n[Test] Playing {filename}...")
    try:
        subprocess.run(['aplay', filename], check=True)
        print("✓ Playback complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Playback failed: {e}")
        return False

def main():
    print("=" * 60)
    print("MAX98357A AUDIO AMPLIFIER TEST")
    print("=" * 60)
    print("Hardware: MAX98357A on I2S (GPIO18, 19, 21)")
    print("Output: 8Ω 2W speaker")
    print()

    # Generate test files
    test_files = [
        ("tone_440hz.wav", 440, 2),   # A4 note
        ("tone_880hz.wav", 880, 1),   # A5 note
        ("tone_220hz.wav", 220, 2),   # A3 note
    ]

    for filename, freq, duration in test_files:
        generate_test_tone(filename, freq, duration)

    input("\nPress Enter to start playback tests...")

    # Play test tones
    for filename, freq, duration in test_files:
        print(f"\nPlaying {freq} Hz tone...")
        if not test_playback(filename):
            print("⚠ Playback failed, check audio configuration")
            return False
        input("Press Enter to continue...")

    # Cleanup
    for filename, _, _ in test_files:
        os.remove(filename)

    print("\n" + "=" * 60)
    print("AUDIO TEST COMPLETE ✓")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

**Run Test**:
```bash
python3 test_audio_playback.py
```

**Troubleshooting**:
- **No sound**: Check speaker polarity, volume (may be muted)
- **Distorted sound**: Lower volume, check power supply stability
- **Crackling**: I2S timing issue, check wiring

---

#### Task 3.2: INMP441 Microphone Setup (45 minutes)

**Wiring Diagram**:
```
INMP441 Microphone → Raspberry Pi 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INMP441 Pin         →  Pi Pin                     Notes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VDD                 →  3.3V (Pin 1)               Power (NOT 5V!)
GND                 →  GND (Pin 9)                Ground
SCK (Serial Clock)  →  GPIO18 (Pin 12)            Shared with amp
WS (Word Select)    →  GPIO19 (Pin 35)            Shared with amp
SD (Serial Data)    →  GPIO20 (Pin 38)            Mic data input
L/R                 →  GND (left channel)         Or 3.3V (right channel)
```

**Note**: INMP441 and MAX98357A share BCLK (GPIO18) and LRCLK (GPIO19). This is intentional for I2S half-duplex operation.

**Configure I2S Recording**:
```bash
# Edit boot config (add if not present)
sudo nano /boot/config.txt

# Add:
dtoverlay=i2s-mmap
dtparam=i2s=on

# Save and reboot
sudo reboot
```

**Install PyAudio**:
```bash
sudo apt install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Create Microphone Test**:
```bash
nano ~/openduck_firmware/test_microphone.py
```

**Test Code**:
```python
#!/usr/bin/env python3
"""
INMP441 Microphone Test - Raspberry Pi 4
Tests: Recording, playback, noise level
"""

import pyaudio
import wave
import sys

# Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Mono
RATE = 16000  # 16 kHz (good for voice)
CHUNK = 1024
RECORD_SECONDS = 5
OUTPUT_FILENAME = "test_recording.wav"

def test_record():
    """Test 1: Record audio from INMP441"""
    print("\n[Test 1] Recording 5 seconds of audio...")
    print("  Speak into microphone: 'Testing, one, two, three'")

    try:
        audio = pyaudio.PyAudio()

        # Open stream
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        print("  Recording...")
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            progress = (i + 1) / (RATE / CHUNK * RECORD_SECONDS) * 100
            print(f"  Progress: {progress:.0f}%", end='\r')

        print()
        print("  Recording complete")

        # Stop stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save to WAV file
        with wave.open(OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        print(f"✓ Recording saved to {OUTPUT_FILENAME}")
        return True

    except Exception as e:
        print(f"✗ Recording failed: {e}")
        return False

def test_playback():
    """Test 2: Play back recorded audio"""
    print(f"\n[Test 2] Playing back {OUTPUT_FILENAME}...")

    try:
        import subprocess
        subprocess.run(['aplay', OUTPUT_FILENAME], check=True)
        print("✓ Playback complete")
        return True
    except Exception as e:
        print(f"✗ Playback failed: {e}")
        return False

def main():
    print("=" * 60)
    print("INMP441 MICROPHONE TEST")
    print("=" * 60)
    print("Hardware: INMP441 I2S microphone on GPIO18, 19, 20")
    print("Sample rate: 16 kHz (voice optimized)")
    print()

    input("Press Enter to start recording test...")

    # Record
    if not test_record():
        return False

    input("\nPress Enter to play back recording...")

    # Playback
    if not test_playback():
        return False

    print("\n" + "=" * 60)
    print("MICROPHONE TEST COMPLETE ✓")
    print("=" * 60)
    print("\nDid you hear your voice clearly? [y/n]")
    response = input().lower()

    if response == 'y':
        print("✓ Microphone working correctly")
        return True
    else:
        print("⚠ Microphone may need adjustment")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

**Run Test**:
```bash
python3 test_microphone.py
```

---

### BLOCK 4 (16:00-17:00): INTEGRATION AND DOCUMENTATION

#### Task 4.1: Full System Integration Test (30 minutes)

**Test all components simultaneously**:
```python
#!/usr/bin/env python3
"""
Full System Integration Test - Day 2
Tests: LED + Servo + Audio simultaneously
"""

import time
from adafruit_servokit import ServoKit
import board
import neopixel
import subprocess

def test_integration():
    """Test all systems together"""
    print("=" * 60)
    print("FULL SYSTEM INTEGRATION TEST")
    print("=" * 60)

    # Initialize components
    print("\n[Setup] Initializing components...")
    kit = ServoKit(channels=16)
    pixels = neopixel.NeoPixel(board.D18, 16, brightness=0.3, auto_write=False)

    # Test sequence
    print("\n[Test] Running integrated sequence...")

    # 1. LED + Servo
    print("  1. LED ring + Servo movement")
    pixels.fill((255, 0, 0))  # Red
    pixels.show()
    kit.servo[0].angle = 0
    time.sleep(1)

    pixels.fill((0, 255, 0))  # Green
    pixels.show()
    kit.servo[0].angle = 180
    time.sleep(1)

    pixels.fill((0, 0, 255))  # Blue
    pixels.show()
    kit.servo[0].angle = 90
    time.sleep(1)

    # 2. Audio + LED
    print("  2. Audio playback + LED animation")
    # (Play audio file while animating LEDs)

    # 3. All three
    print("  3. All systems active")
    # (Complex integration)

    # Cleanup
    pixels.fill((0, 0, 0))
    pixels.show()
    pixels.deinit()

    print("\n✓ Integration test complete")
    return True

if __name__ == "__main__":
    test_integration()
```

---

#### Task 4.2: Day 2 Final Report (20 minutes)

**Create comprehensive report**:
```
DAY 2 REPORT (15 JANUARY 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIME SPENT: ___ hours (target: 6-7 hours)

COMPONENTS TESTED:
[ ] PCA9685 PWM Driver (I2C communication, PWM output)
[ ] MG90S Servo (single servo control, position accuracy)
[ ] Multiple Servos (3× simultaneous, current measurement)
[ ] MAX98357A Audio Amp (playback, volume, speaker output)
[ ] INMP441 Microphone (recording, quality, noise level)

MEASUREMENTS RECORDED:
- 5V rail current @ idle: _____ mA
- 5V rail current @ 1 servo moving: _____ mA
- 5V rail current @ 3 servos moving: _____ mA
- Audio current @ max volume: _____ mA
- Total current (all active): _____ mA

POWER SYSTEM STATUS:
[ ] UBEC 5V output stable: _____ V (expected 5.0 ± 0.1V)
[ ] No voltage sag during peak load
[ ] No Pi brownouts observed
[ ] Temperature acceptable (<60°C)

ISSUES ENCOUNTERED:
(List problems and resolutions)

SUCCESS CRITERIA MET:
[ ] PCA9685 communicating via I2C (0x40)
[ ] Servos responding accurately to angle commands
[ ] Audio playback clear, no distortion
[ ] Microphone recording voice clearly
[ ] Total current <2.5A during normal operation
[ ] All test scripts created and working

NEXT STEPS (Day 3+):
[ ] Test all 5 MG90S servos
[ ] Implement servo current limiting software
[ ] Test HC-SR04 ultrasonic sensors
[ ] Begin firmware driver development
[ ] Plan mechanical assembly (when printer arrives)

APPROVED: [YES / NO]
Date: 2026-01-15
```

---

## SUCCESS CRITERIA SUMMARY

### Day 1 (14 Jan) - MUST COMPLETE:
- [x] Raspberry Pi 4 operational (OS, SSH, Python)
- [x] GPIO tested (basic functionality)
- [x] WS2812B LED ring working (16 LEDs, animations)
- [x] Power system assembled (BMS + UBEC wired, tested for continuity)
- [x] Firmware repository initialized (structure, git)
- [x] Batteries ordered or acquisition plan in place

### Day 2 (15 Jan) - MUST COMPLETE:
- [x] PCA9685 PWM driver working (I2C detected @ 0x40)
- [x] 1-3 MG90S servos controlled successfully
- [x] Audio playback functional (MAX98357A)
- [x] Microphone recording functional (INMP441)
- [x] Full system integration tested (no power issues)
- [x] All test reports documented

### Failure Conditions (ABORT if):
- Pi won't boot after 3 attempts → Re-flash SD card
- PCA9685 not detected on I2C → Check wiring, try second board
- Servo draws >3A → Reduce concurrent servos, verify UBEC rating
- UBEC voltage sag below 4.5V → Need second UBEC (order immediately)
- Pi brownouts during operation → Power system insufficient

---

## TROUBLESHOOTING GUIDE

### Raspberry Pi Issues:
```
Problem: Won't boot (no activity LED)
Solutions:
1. Check power supply (need 5V 2.5A minimum)
2. Re-seat SD card
3. Re-flash SD card with known-good image
4. Try different power cable

Problem: Can't SSH
Solutions:
1. Check WiFi credentials in Imager settings
2. Find IP on router, connect directly
3. Connect HDMI + keyboard, fix network manually
4. Reflash SD with correct settings
```

### PCA9685 Issues:
```
Problem: Not detected on I2C
Solutions:
1. Run i2cdetect -y 1 to scan bus
2. Check wiring: SDA → GPIO2, SCL → GPIO3, VCC → 3.3V
3. Verify I2C enabled in raspi-config
4. Try lowering I2C speed: /boot/config.txt add dtparam=i2c_baudrate=50000
5. Test with second PCA9685 board

Problem: Servo jitter
Solutions:
1. Ensure V+ powered from UBEC (not Pi)
2. Add 1000µF capacitor across V+ and GND
3. Check for ground loops
4. Lower PWM frequency slightly (40-50 Hz)
```

### Power Issues:
```
Problem: Voltage sag during servo movement
Solutions:
1. Measure voltage at UBEC output under load
2. Check wire gauge (use 16AWG minimum)
3. Verify UBEC rated for load
4. Add second UBEC for servos (6V rail)
5. Implement software current limiting

Problem: Pi brownout (unexpected reboot)
Solutions:
1. Use proper 5V 3A power supply
2. Separate servo power from Pi power
3. Add bulk capacitance (1000-4700µF)
4. Reduce concurrent servo movements
5. Monitor voltage in software
```

---

## SAFETY WARNINGS

**ELECTRICAL SAFETY**:
- Never connect/disconnect components while powered
- Always verify polarity before connecting batteries
- Use proper wire gauge (16AWG for high current)
- Insulate all exposed connections with heat shrink

**BATTERY SAFETY**:
- Store Li-ion cells at 3.7V (storage voltage), not fully charged
- Never short circuit battery terminals
- Monitor temperature during charging (<45°C)
- Use proper 2S Li-ion charger with balance connector

**SERVO SAFETY**:
- Never block servo for >1 second (stall current damages motor)
- Keep servo movements clear of obstructions
- Monitor temperature during extended use
- Implement software stall detection

**GENERAL**:
- Work in well-ventilated area (soldering fumes)
- Keep liquids away from electronics
- Have fire extinguisher accessible (Li-ion fire risk)
- Take breaks every 90 minutes (avoid fatigue errors)

---

## CONTACT INFORMATION

**Component Suppliers**:
- AliExpress: www.aliexpress.com (FE-URT-1 controller)
- Amazon.it: www.amazon.it (batteries, UBEC, components)
- TheBatteryShop.eu: www.thebatteryshop.eu (Molicel batteries)

**Technical Resources**:
- Raspberry Pi Documentation: www.raspberrypi.com/documentation
- Adafruit Learn: learn.adafruit.com (PCA9685, NeoPixel guides)
- MG90S Datasheet: Search "TowerPro MG90S datasheet PDF"
- PCA9685 Datasheet: Search "NXP PCA9685 datasheet PDF"

**Emergency Contacts**:
- Local electronics shop: [Phone number]
- Battery supplier: [Phone number]
- Backup support: [Contact info]

---

**Document Version**: 1.0
**Created**: 2026-01-14
**Author**: Hardware Testing Specialist Agent
**Status**: READY FOR EXECUTION
**Estimated Total Time**: 10-12 hours (Day 1: 4-5h, Day 2: 6-7h)

---

**FINAL NOTE**: This plan is aggressive but achievable. Prioritize core functionality (Pi setup, PCA9685, servo control) over optional features. If blocked, document the issue and move to next task rather than spending hours debugging. Real-world hardware testing always has surprises - budget 20% time buffer for troubleshooting.

**START WITH DAY 1 HOUR 1 (RASPBERRY PI SETUP) NOW.**
