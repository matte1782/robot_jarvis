# DAY 2 EVENING PLAN - 15 JANUARY 2026
## Corrected Reality-Based Execution Plan

**Created:** 15 January 2026, 19:00
**Status:** READY FOR EXECUTION
**Time Available:** 3 hours (19:00-22:00)

---

## 🎯 SITUATION REPORT

### **ASSETS AVAILABLE NOW:**
- ✅ **Raspberry Pi 4 Model B 4GB** - PHYSICALLY AVAILABLE
- ✅ MicroSD 64GB + SD Card Adapter
- ✅ Power System Components (BMS, UBEC, battery holder, XT30)
- ✅ MG90S Servos (5×)
- ✅ WS2812B LED Rings (2×)
- ✅ MAX98357A Amplifier
- ✅ INMP441 Microphone
- ✅ HC-SR04 Ultrasonic Sensors (3×)
- ✅ Soldering Station + Tools

### **ARRIVING TOMORROW (16 Jan):**
- 🚚 PCA9685 PWM Driver (2×)
- 🚚 USB-C Power Supply 5.1V 3A
- 🚚 Aluminum Case + Heatsink
- 🚚 Servo Extensions
- 🚚 Heat Shrink Tubing

### **ORDERED (Not Shipped):**
- 📦 Molicel P30B batteries (2×) - Will order tonight

---

## 📋 TONIGHT'S TASKS (Priority Order)

### **TASK 1: ORDER BATTERIES** ⚡ CRITICAL (20 min)

**Why Critical:** 3-5 day delivery, blocks all power testing

```
[ ] Go to: https://www.nkon.nl/
[ ] Search: "Molicel INR18650-P30B"
[ ] Add to cart: 2× batteries
[ ] Price: €7.98 (2 × €3.99)
[ ] Solder tags: GEEN (none)
[ ] Checkout and pay
[ ] Save confirmation email
[ ] Update tracker: Status ORDINATO, ETA 18-20 Jan
```

---

### **TASK 2: FLASH MICROSD + RASPBERRY PI SETUP** ⚡ (1h 30min)

**Complete Pi setup tonight so tomorrow = hardware only**

#### **Step 1: Download Raspberry Pi Imager** (5 min)
```
[ ] Go to: https://www.raspberrypi.com/software/
[ ] Download for Windows
[ ] Install Raspberry Pi Imager
```

#### **Step 2: Flash MicroSD** (25 min)
```
[ ] Insert microSD 64GB into PC (with adapter)
[ ] Open Raspberry Pi Imager
[ ] Select:
    - Device: Raspberry Pi 4
    - OS: Raspberry Pi OS (64-bit) - Lite recommended
    - Storage: Your 64GB microSD

[ ] Click ⚙️ Settings and configure:
    ✅ Hostname: openduck
    ✅ Enable SSH: YES (password authentication)
    ✅ Username: pi
    ✅ Password: [set secure password]
    ✅ WiFi (optional):
       - SSID: [your network]
       - Password: [wifi password]
       - Country: IT
    ✅ Locale:
       - Timezone: Europe/Rome
       - Keyboard: it

[ ] Click SAVE
[ ] Click YES to write
[ ] Wait 10-15 minutes (writing + verification)
[ ] Eject SD safely
```

#### **Step 3: First Boot** (10 min)
```
[ ] Insert microSD into Raspberry Pi 4
[ ] Connect HDMI monitor + USB keyboard (or prepare for SSH)
[ ] Power on Pi with ANY 5V USB-C charger (phone charger works)
[ ] Wait for first boot (30-60 seconds)
[ ] Login with username/password set earlier
[ ] Verify network connection: ping google.com
```

#### **Step 4: System Update** (30 min)
```bash
# Update package lists
sudo apt update

# Upgrade all packages (takes 15-20 min)
sudo apt upgrade -y

# Install essential tools
sudo apt install -y git python3-pip python3-dev

# Verify Python version
python3 --version  # Should be 3.9+
pip3 --version
```

#### **Step 5: Enable Hardware Interfaces** (10 min)
```bash
# Open raspi-config
sudo raspi-config

# Navigate:
# → Interface Options
#   → I2C → Enable → Yes
#   → SPI → Enable → Yes
#   → Exit

# Reboot
sudo reboot

# After reboot, verify I2C
ls /dev/i2c*  # Should show /dev/i2c-1
```

#### **Step 6: Install Python Dependencies** (15 min)
```bash
# Install CircuitPython libraries
sudo pip3 install adafruit-circuitpython-pca9685
sudo pip3 install adafruit-circuitpython-neopixel
sudo pip3 install adafruit-circuitpython-motor

# Install development tools
pip3 install numpy
pip3 install pytest
pip3 install pyyaml
pip3 install pylint
pip3 install black

# Verify installations
python3 -c "import numpy; print('NumPy OK')"
python3 -c "import pytest; print('Pytest OK')"
```

**Success Criteria:**
```
[ ] Pi boots successfully
[ ] SSH working (if configured)
[ ] System updated to latest
[ ] I2C enabled (/dev/i2c-1 exists)
[ ] SPI enabled
[ ] All Python dependencies installed
[ ] No errors in installation
```

---

### **TASK 3: GIT REPOSITORY INITIALIZATION** ⚡ (15 min)

```bash
# On Windows laptop
cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis\firmware"

# Initialize git
git init

# Check what we have
git status

# Add all files
git add .

# Create first commit
git commit -m "feat: Week 01 Day 1-2 firmware foundation

Complete firmware architecture:
- Modular structure (drivers, control, core, utils)
- README with project overview and hardware specs
- requirements.txt with all dependencies
- PCA9685 servo driver fully implemented
- ServoController high-level API
- Configuration system prepared
- Test structure ready

Hardware status:
- Raspberry Pi 4 4GB: Configured and ready
- PCA9685: Arriving 16 Jan
- Power system: Components available, assembly pending batteries
- Servos: 5× MG90S available for testing

Ready for Day 3 hardware integration testing."

# Verify commit
git log --oneline

# Check status (should be clean)
git status
```

**Success Criteria:**
```
[ ] Git initialized (.git folder created)
[ ] All files committed (no untracked files)
[ ] Commit message descriptive
[ ] Git log shows commit
[ ] Repository clean
```

---

### **TASK 4: CREATE DAY 2 COMPLETION REPORT** (20 min)

Create: `Planning/Week_01/Day_02_Completion_Report_15_Jan.md`

```markdown
# Day 2 Completion Report - 15 January 2026

## Summary
Completed Raspberry Pi 4 setup and firmware repository initialization.
Hardware testing deferred to Day 3 (awaiting PCA9685 delivery).

## Completed Tasks

### ✅ Hardware Setup
- Raspberry Pi 4 4GB fully configured
- System updated to latest packages
- I2C and SPI interfaces enabled
- All Python dependencies installed
- Ready for hardware testing tomorrow

### ✅ Software Development
- Git repository initialized
- Firmware architecture complete
- PCA9685 driver implemented (282 lines)
- ServoController high-level API ready
- Unit test structure prepared

### ✅ Procurement
- Molicel P30B batteries ordered (2×, €7.98)
- ETA: 18-20 January
- Tracking: [order number]

## Components Status

### Available Now:
- Raspberry Pi 4 4GB ✅
- Power components (BMS, UBEC, battery holder) ✅
- MG90S servos (5×) ✅
- LED rings (2×) ✅
- Audio components ✅
- Sensors (ultrasonic, microphone) ✅

### Arriving Tomorrow (16 Jan):
- PCA9685 PWM Driver (2×)
- USB-C power supply
- Aluminum case + heatsink
- Servo extensions
- Heat shrink tubing

### Ordered (ETA 18-20 Jan):
- Molicel P30B batteries (2×)

## Metrics

**Time Spent:**
- Battery ordering: 20 min
- Raspberry Pi setup: 1h 30min
- Git initialization: 15 min
- Documentation: 20 min
- **Total: 2h 25min**

**Lines of Code:**
- PCA9685 driver: 282 lines
- Total firmware: ~500 lines (with structure)

**Test Coverage:**
- Current: 0% (no tests run yet)
- Target Week 01: 40%

## Blockers Resolved
- ✅ MicroSD card acquired (64GB)
- ✅ Raspberry Pi available and configured
- ✅ Firmware repository structure complete

## Blockers Remaining
- ⏳ PCA9685 arriving tomorrow → Day 3 hardware testing
- ⏳ Batteries arriving 18-20 Jan → Power system testing Day 4-5

## Day 3 Plan (16 Jan)

**Morning:**
- Receive PCA9685 delivery
- Install Pi in aluminum case with heatsink
- Wire PCA9685 to Pi I2C bus

**Afternoon:**
- I2C detection test (0x40)
- Single servo test (MG90S)
- Multi-servo coordination test
- LED ring test (WS2812B)
- Document all tests with photos

**Success Criteria Day 3:**
- PCA9685 detected on I2C
- At least 1 servo responding to commands
- LED ring functional
- Power consumption measured

## Lessons Learned

**What Went Well:**
- Clear component status verification
- Raspberry Pi setup straightforward
- Firmware architecture solid

**What Could Improve:**
- Earlier verification of component arrival dates
- Better coordination between hardware/software tasks

## Week 01 Progress

**Overall:** 25% complete (Day 2 of 7)

**Hardware:** 20% (Pi ready, awaiting peripherals)
**Software:** 40% (architecture + driver complete)
**Documentation:** 30% (README + planning docs)
**Testing:** 0% (awaiting hardware)

---

**Report Created:** 15 January 2026, 22:00
**Next Review:** 16 January 2026, Day 3 completion
```

---

## 🎯 EXECUTION TIMELINE TONIGHT

```
19:00-19:20 (20 min)  → [1] Order batteries NKON ⚡
19:20-20:50 (1h 30m)  → [2] Flash SD + Pi setup ⚡
20:50-21:05 (15 min)  → [3] Git init ⚡
21:05-21:25 (20 min)  → [4] Day 2 report
21:25-22:00 (35 min)  → Buffer / Optional tasks

TOTAL: 2h 25min core work + 35min buffer
```

---

## ✅ SUCCESS CRITERIA DAY 2

**MUST COMPLETE:**
- [ ] Batteries ordered from NKON
- [ ] Raspberry Pi 4 configured and updated
- [ ] I2C enabled and verified
- [ ] Python dependencies installed
- [ ] Git repository initialized
- [ ] Day 2 report documented

**BONUS (if time permits):**
- [ ] Power system partially assembled
- [ ] Component inventory photos
- [ ] Unit test skeleton created

---

## 🚀 TOMORROW'S ADVANTAGES

Because we completed Pi setup tonight:
- ✅ No time wasted on OS installation
- ✅ All dependencies pre-installed
- ✅ Hardware testing starts immediately when PCA9685 arrives
- ✅ Can focus 100% on hardware validation

**Estimated time saved tomorrow:** 1h 30min

---

## 📊 RISK ASSESSMENT

**LOW RISK:**
- Raspberry Pi setup (straightforward, well documented)
- Git initialization (standard procedure)

**MEDIUM RISK:**
- PCA9685 delivery timing (expected tomorrow but not guaranteed)
- First I2C communication (may need troubleshooting)

**MITIGATION:**
- Pi setup tonight reduces tomorrow's dependencies
- PCA9685 driver already implemented (ready to test immediately)
- Backup: If PCA9685 delayed, continue with LED/audio testing

---

**Created:** 15 January 2026, 19:00
**Status:** READY FOR EXECUTION
**Next Update:** Day 3 plan (16 January 2026)
