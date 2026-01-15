# TONIGHT ACTION PLAN - 14 JANUARY 2026 (CORRECTED)
## Based on ACTUAL Component Availability

**Created:** 2026-01-14 Evening (Post-Delivery Reality Check)
**Status:** READY TO EXECUTE NOW
**Components Available:** Raspberry Pi 4, MG90S servos (5×), LED rings, audio amp, sensors, power components

---

## 🎉 REALITY CHECK: EVERYTHING ARRIVED TODAY!

**Previous agent assumption:** Only printer available, electronics in transit
**ACTUAL REALITY:** Massive Amazon delivery TODAY with 90% of electronics!

**What you have RIGHT NOW:**
- ✅ Raspberry Pi 4 Model B (4GB) - DELIVERED
- ✅ MG90S Servos (5×) - DELIVERED
- ✅ WS2812B LED Rings (2×) - DELIVERED
- ✅ MAX98357A Audio Amplifier - DELIVERED
- ✅ UBEC 5V/6V 3A - DELIVERED
- ✅ HC-SR04 Ultrasonic Sensors (3×) - DELIVERED
- ✅ Complete wiring kit (jumpers, silicon wire, XT30) - DELIVERED
- ✅ Soldering station - DELIVERED
- ✅ 4+ spools of filament (PLA+, PLA PRO, Silk, TPU) - DELIVERED

**Arriving TOMORROW (15 Jan):**
- PCA9685 PWM Driver (for servo control)
- INMP441 Microphone
- Second UBEC 6V 3A
- Heat shrink tubing

**Still Missing:**
- Molicel P30B batteries (order tonight)
- QIDI printer (arriving "couple days, worst case next week")

---

## TONIGHT: 3-4 HOURS OF PRODUCTIVE WORK

### BLOCK 1: RASPBERRY PI SETUP (90 minutes) ⚡ HIGHEST PRIORITY

**Goal:** Get Pi 4 operational with OS and basic testing

**Tasks:**
1. **Unbox and Inventory (10 min)**
   - [ ] Open Raspberry Pi 4 package
   - [ ] Verify: Pi 4 Model B 4GB RAM
   - [ ] Locate power supply (USB-C, 5.1V 3A - arriving tomorrow)
   - [ ] Find microSD card (or use spare if have one)

2. **Install Raspberry Pi OS (30 min)**
   - [ ] Download Raspberry Pi Imager: https://www.raspberrypi.com/software/
   - [ ] Flash microSD with "Raspberry Pi OS Lite (64-bit)"
   - [ ] Enable SSH in settings (username: pi, password: openduck)
   - [ ] Configure WiFi credentials
   - [ ] Eject SD card

3. **First Boot and Configuration (30 min)**
   - [ ] Insert SD card into Pi 4
   - [ ] Power via laptop USB-C (temporary, until PSU arrives tomorrow)
   - [ ] SSH into Pi: `ssh pi@raspberrypi.local` (or find IP on router)
   - [ ] Run: `sudo raspi-config`
     - [ ] Enable I2C (Interface Options)
     - [ ] Enable I2S (Interface Options)
     - [ ] Enable SPI (Interface Options)
     - [ ] Set timezone
     - [ ] Expand filesystem
   - [ ] Update system: `sudo apt update && sudo apt upgrade -y`

4. **Install Python Dependencies (20 min)**
```bash
# Core GPIO library
sudo apt install python3-pip python3-dev -y

# GPIO and hardware libraries
pip3 install RPi.GPIO
pip3 install adafruit-circuitpython-neopixel
pip3 install rpi-ws281x
pip3 install smbus2

# Audio (for tomorrow's MAX98357)
sudo apt install libportaudio2 -y

# Development tools
pip3 install pytest black
```

5. **GPIO Test (10 min)**
```python
# test_gpio.py
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Test with built-in LED or external LED on GPIO 17
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

print("Blinking LED...")
for i in range(5):
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.5)

GPIO.cleanup()
print("GPIO test PASSED")
```

**Success Criteria:**
- [x] Pi 4 boots successfully
- [x] SSH connection working
- [x] Python 3 with pip operational
- [x] GPIO test passes

---

### BLOCK 2: LED RING TESTING (45 minutes) ⚡ HIGH PRIORITY

**Goal:** Test WS2812B LED rings with Pi 4

**Hardware Setup:**
- WS2812B LED Ring (16 LEDs)
- Pi 4 GPIO 10 (not GPIO 18 - avoid I2S conflict!)
- 5V power (from UBEC if available, or Pi 5V rail for testing)
- GND (common ground)

**Wiring:**
```
WS2812B Pin      →  Connection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIN (Data In)    →  Pi GPIO 10 (physical pin 19)
5V (VCC)         →  Pi 5V (physical pin 2) OR UBEC 5V out
GND              →  Pi GND (physical pin 6)
```

**Code:**
```python
# test_neopixel.py
import board
import neopixel
import time

# Configure
NUM_PIXELS = 16
PIXEL_PIN = board.D10  # GPIO 10
ORDER = neopixel.GRB

# Initialize
pixels = neopixel.NeoPixel(
    PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def wheel(pos):
    # Input 0-255, output RGB tuple
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

# Test
print("Testing NeoPixel ring...")
rainbow_cycle(0.001)  # Fast rainbow
pixels.fill((0, 0, 0))
pixels.show()
print("Test complete!")
```

**Tests to Run:**
1. [ ] Rainbow animation (verify all 16 LEDs work)
2. [ ] Individual LED control (test each LED 0-15)
3. [ ] Brightness test (10%, 50%, 100%)
4. [ ] Color accuracy (pure red, green, blue)
5. [ ] Power consumption measurement (if have multimeter)

**Success Criteria:**
- [x] All 16 LEDs light up
- [x] Rainbow animation smooth
- [x] No flickering or color issues
- [x] Current draw documented (~200mA at 50% brightness)

---

### BLOCK 3: POWER SYSTEM ASSEMBLY (45 minutes) ⚡ HIGH PRIORITY

**Goal:** Wire up UBEC, battery holder, BMS for power testing tomorrow

**Components:**
- UBEC 5V/6V 3A (DELIVERED)
- BMS 2S 20A (DELIVERED)
- Battery Holder 2S (DELIVERED)
- XT30 Connectors (DELIVERED)
- Silicon Wire 16AWG (DELIVERED)

**System Architecture:**
```
[Battery Holder 2S]
       │
       ├─── [Positive +] → BMS B+
       └─── [Negative -] → BMS B-
                │
                └─── BMS P+ → Main Power Switch → UBEC Input (+)
                └─── BMS P- → GND → UBEC Input (-)
                                      │
                                      ├─── UBEC 5V Out → Pi 4 GPIO 5V rail
                                      └─── UBEC GND → Pi GND
```

**Wiring Steps:**
1. **BMS to Battery Holder (30 min)**
   - [ ] Solder red wire: Battery + to BMS B+
   - [ ] Solder black wire: Battery - to BMS B-
   - [ ] Add XT30 male connector to BMS P+/P-
   - [ ] Heat shrink all solder joints
   - [ ] Label wires with tape

2. **UBEC Input (15 min)**
   - [ ] Solder XT30 female to UBEC input wires
   - [ ] Verify polarity (red = +, black = -)
   - [ ] Set UBEC jumper to 5V output (check manual)
   - [ ] Test continuity with multimeter

3. **SAFETY CHECK (NO BATTERIES YET)**
   - [ ] Visual inspection: No exposed wire
   - [ ] Continuity test: BMS to UBEC
   - [ ] Polarity verification: Red = +, Black = -
   - [ ] Insulation check: No shorts to ground

**DO NOT CONNECT BATTERIES YET** - Wait until acquired tomorrow

**Success Criteria:**
- [x] All connections soldered properly
- [x] Heat shrink applied
- [x] Polarity verified
- [x] Ready for battery insertion (when acquired)

---

### BLOCK 4: FIRMWARE REPOSITORY INIT (30 minutes)

**Goal:** Create firmware folder structure and git repo

**Execute:**
```bash
cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis"

# Create firmware directory
mkdir firmware
cd firmware

# Create structure
mkdir -p src/drivers/{servo,led,audio,sensor}
mkdir -p src/control
mkdir -p src/core/safety
mkdir -p src/utils
mkdir -p config
mkdir -p tests/{test_drivers,test_control,test_core}

# Initialize git
git init

# Create README
echo "# OpenDuck Mini V3 Firmware
Version: 0.1.0-dev
Status: Week 01 Development - Hardware Testing Phase

## Structure
- src/drivers/: Hardware abstraction layer
- src/control/: Kinematics and control
- src/core/: Main robot logic
- tests/: Pytest test suite

## Quick Start
pip install -r requirements.txt
python src/core/robot.py
" > README.md

# Create requirements.txt
echo "# Raspberry Pi Dependencies
RPi.GPIO==0.7.1
adafruit-circuitpython-neopixel==6.3.8
rpi-ws281x==5.0.0
smbus2==0.4.2

# Development
pytest==7.4.3
black==23.11.0

# Utilities
pyyaml==6.0.1
numpy==1.24.3
" > requirements.txt

# First commit
git add .
git commit -m "Initial firmware structure

- Created modular architecture (drivers, control, core)
- Added README and requirements
- Ready for Week 01 development (hardware testing)
"
```

**Success Criteria:**
- [x] Folder structure created
- [x] Git repository initialized
- [x] README and requirements.txt written
- [x] First commit made

---

### BLOCK 5: URGENT ORDERS (30 minutes) ⚡ CRITICAL

**Task 5.1: Molicel P30B Batteries (20 min)**

**Option A: Local Vape Shop (TONIGHT)**
1. Google Maps: "Vape shop Monza"
2. Call 3-5 shops, ask: "Avete Molicel INR18650-P30B?"
3. If YES: Drive and buy 4 cells (€14-16)
4. If NO: Order online (Option B)

**Option B: Online Order (3-5 days)**
- TheBatteryShop.eu
- Search: "Molicel INR18650-P30B"
- Order 4 cells
- Express shipping if available

**Task 5.2: FE-URT-1 Controller (10 min)**
- AliExpress.com
- Search: "FE-URT-1 servo controller"
- Order 1 unit (€45, 15-25 day lead time)
- Save tracking number

**Success Criteria:**
- [x] Batteries ordered or acquired
- [x] FE-URT-1 ordered
- [x] Tracker updated with order info

---

## OPTIONAL TONIGHT (If Time Remaining)

### BONUS 1: Ultrasonic Sensor Test (20 min)
```python
# test_hcsr04.py
import RPi.GPIO as GPIO
import time

TRIG_PIN = 23
ECHO_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Test
for i in range(10):
    dist = measure_distance()
    print(f"Distance: {dist} cm")
    time.sleep(0.5)

GPIO.cleanup()
```

### BONUS 2: Component Photos (15 min)
- Take photos of all received components
- Create inventory document with photos
- Useful for documentation and troubleshooting

---

## TOMORROW MORNING (15 Jan)

### Expected Deliveries:
- [ ] PCA9685 PWM Driver (2×) - CRITICAL for servo control
- [ ] INMP441 Microphone (6 pcs)
- [ ] ZHITING UBEC 6V 3A (second power rail)
- [ ] USB-C Power Supply 5.1V 3A (proper Pi power)
- [ ] Aluminum case for Pi 4
- [ ] Heat shrink tubing

### Immediate Actions (15 Jan Morning):
1. **Install USB-C PSU** - Power Pi 4 properly (not laptop USB)
2. **Install PCA9685** - Wire I2C (SDA, SCL) to Pi
3. **Test 1 MG90S Servo** - Connect to PCA9685, run sweep test
4. **Develop PCA9685 Driver** - Python class for servo control
5. **Battery Acquisition Check** - If local shop has them, acquire TODAY

---

## SUCCESS METRICS FOR TONIGHT

**Must Complete (Core Work):**
- [x] Raspberry Pi 4 set up with OS and SSH
- [x] Python environment configured
- [x] GPIO test passed (LED blink)
- [x] NeoPixel LED ring tested (rainbow animation)
- [x] Power system wired (BMS + UBEC + battery holder)
- [x] Firmware repository initialized with git
- [x] Batteries ordered or acquisition plan confirmed
- [x] FE-URT-1 controller ordered

**Nice to Have (If Time):**
- [ ] HC-SR04 ultrasonic sensor tested
- [ ] Component inventory photos taken
- [ ] Audio amp wired (test tomorrow with proper PSU)
- [ ] Servo extension cables organized

**Unacceptable:**
- ❌ Pi 4 still in box
- ❌ No LED testing done
- ❌ Batteries not ordered
- ❌ No firmware repo created

---

## CONTINGENCY PLANS

### If Pi 4 won't boot:
1. Try different microSD card
2. Reflash with different OS image
3. Power from different source (wall adapter, not laptop)
4. Check for physical damage

### If LED ring doesn't work:
1. Verify wiring (DIN to GPIO 10, not 18)
2. Check 5V power supply adequate
3. Test with lower brightness (0.1)
4. Try second LED ring (you have 2!)

### If can't find batteries locally:
1. Order online immediately
2. Continue with USB-powered testing (low current only)
3. Plan full power tests for Weekend (18-19 Jan)

---

## ESTIMATED COMPLETION TIME

**Realistic Schedule:**
- Block 1 (Pi Setup): 90 minutes
- Block 2 (LED Test): 45 minutes
- Block 3 (Power Wiring): 45 minutes
- Block 4 (Firmware Repo): 30 minutes
- Block 5 (Orders): 30 minutes

**Total: 3.5 hours** (achievable tonight)

**If start at 20:00 → finish by 23:30**

---

## FINAL WORD

**Previous plan was based on WRONG assumptions.**

**NEW REALITY:**
- You have Raspberry Pi 4 4GB RIGHT NOW
- You have 5× MG90S servos RIGHT NOW
- You have LED rings, sensors, power components RIGHT NOW
- You have complete wiring kit RIGHT NOW
- Only waiting for PCA9685 (arriving tomorrow) to test servos

**TONIGHT'S IMPACT:**
- 80% of electronics validation can be completed
- Firmware foundation can be started
- Power system can be assembled
- Batteries can be ordered/acquired

**Tomorrow (15 Jan) when PCA9685 arrives:**
- Full servo control testing
- Multi-servo coordination
- Hardware validation essentially complete

**The multi-agent review methodology was CORRECT, but input data was WRONG.**

**START WITH BLOCK 1 (Pi Setup) NOW. You have everything needed.**

---

*Created: 2026-01-14 Evening*
*Based on: Actual Amazon delivery confirmations*
*Corrected assumption: Components available NOW, not in transit*
