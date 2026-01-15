# 48-HOUR ACTION CHECKLIST
## 14-15 January 2026 - NO EXCUSES MODE

---

## TODAY (14/01) - EVENING SESSION
**Target: 5 hours of productive work**

### BLOCK 1: 3D Printing Startup (2 hours) - PRIORITY 1

- [ ] **Join OpenDuck Discord** (5 min)
  - Link: https://discord.gg/UtJZsgfQGe
  - Search pinned messages for CAD files

- [ ] **Download STL Files** (30 min)
  - Hip joint (left + right)
  - Torso frame section
  - Leg segment (tibia/femur)
  - Small bracket for test

- [ ] **Import to Slicer** (30 min)
  - Material: eSUN PLA+ Black
  - Nozzle: 210°C
  - Bed: 60°C
  - Speed: 50mm/s
  - Infill: 30% (structural parts)

- [ ] **Print Test Piece** (1 hour active + 1-2h print)
  - Start with smallest bracket
  - Verify first layer adhesion
  - Check dimensional accuracy with calipers

- [ ] **Queue Overnight Print** (30 min)
  - Hip joints OR torso frame section
  - Expected: 8-12 hours print time
  - Set up webcam/phone monitoring if available

**SUCCESS CRITERIA:**
- Printer running by end of evening
- First test piece completed or 50%+ done
- Overnight print queued

---

### BLOCK 2: Component Testing (2 hours) - PRIORITY 2

- [ ] **Test WS2812B LED Ring** (30 min)
  - Wire: GPIO 18 (data), 5V, GND
  - Install: `pip install rpi-ws281x adafruit-circuitpython-neopixel`
  - Run rainbow animation
  - Measure power: ____ mA at full brightness
  - Document findings in test log

- [ ] **Test MAX98357 Audio** (30 min)
  - Wire I2S: BCLK, LRCLK, DIN
  - Enable I2S in raspi-config
  - Play test WAV file
  - Verify output quality
  - Document volume levels

- [ ] **Test MG90S Servo** (1 hour)
  - Wire ONE servo: GPIO 18, 5V, GND
  - Software PWM test: 0-180° sweep
  - Measure current: ____ mA at stall
  - Verify torque with kitchen scale
  - Document: PWM frequency, pulse width range

**SUCCESS CRITERIA:**
- All 3 components tested and characterized
- Power consumption documented
- Any issues identified and logged

---

### BLOCK 3: Critical Orders (1 hour) - PRIORITY 1

- [ ] **Order Molicel Batteries** (30 min)
  - Call vape shops in Monza:
    - [ ] Shop 1: _____________ (phone: _______)
    - [ ] Shop 2: _____________ (phone: _______)
    - [ ] Shop 3: _____________ (phone: _______)
  - Ask: "Avete Molicel INR18650-P30B in stock?"
  - If YES: Drive and pick up TODAY
  - If NO: Order from TheBatteryShop.eu

- [ ] **Check Servo Order Status** (15 min)
  - Check email for Eckstein quotation
  - If received: Place order immediately
  - If not: Send follow-up email

- [ ] **Update Tracker** (15 min)
  - Mark batteries as ORDERED or RICEVUTO
  - Update servo order status
  - Log today's progress

**SUCCESS CRITERIA:**
- Batteries ordered or in hand
- Servo order placed or follow-up sent
- Tracker updated

---

## TOMORROW (15/01) - DELIVERY DAY
**Target: 6 hours productive work**

### MORNING (2 hours)

- [ ] **Receive Deliveries** (30 min)
  - [ ] INMP441 Microphone (AYWHP)
  - [ ] PCA9685 PWM Driver
  - [ ] USB-C Cable
  - [ ] Aluminum Case
  - [ ] Heat Shrink Tubing
  - Inventory parts, check for damage
  - Update tracker: Mark as RICEVUTO

- [ ] **Check Overnight Print** (30 min)
  - Inspect quality (layer adhesion, warping)
  - Measure dimensions with calipers
  - Compare to STL specs
  - Document any issues

- [ ] **Queue Next Print** (1 hour)
  - Slice torso frame OR leg segments
  - Start daytime print (6-8 hours)
  - Monitor first 15 minutes

---

### AFTERNOON (2 hours)

- [ ] **Test PCA9685 Board** (1 hour)
  - Wire I2C: SDA, SCL, VCC, GND
  - Install: `pip install adafruit-circuitpython-pca9685`
  - Connect ONE MG90S servo
  - Test multi-channel control
  - Verify 6V UBEC compatibility

- [ ] **Write Servo Control Library** (1 hour)
  - Create `firmware/src/servo_control/pca9685_driver.py`
  - Functions: set_angle(), set_speed(), get_position()
  - Test with 2-3 servos simultaneously
  - Document PWM calculations

---

### EVENING (2 hours)

- [ ] **Test INMP441 Microphone** (1 hour)
  - Wire I2S: SCK, WS, SD
  - Install I2S audio recording
  - Capture test audio
  - Verify quality, noise level

- [ ] **Firmware Repository Setup** (1 hour)
  - Create folder structure (see hostile review)
  - Initialize git repo
  - Write README with architecture overview
  - Commit initial structure

- [ ] **Queue Overnight Print** (if needed)
  - Next batch: Arms OR head shell
  - Expected: 10-14 hours

---

## SUCCESS METRICS (48 Hours)

### Must Have:
- [ ] 20+ hours of 3D printing completed or queued
- [ ] 5+ components tested and documented
- [ ] Batteries ordered/acquired
- [ ] Firmware repo initialized
- [ ] All Wed deliveries received

### Nice to Have:
- [ ] Servo order placed
- [ ] First assembled joint (test fit)
- [ ] Basic servo control library working
- [ ] Power consumption spreadsheet started

### Unacceptable:
- ❌ Printer still idle
- ❌ No component testing done
- ❌ Batteries not ordered
- ❌ Still "planning" instead of building

---

## RISK MITIGATION

### IF Print Fails:
1. Check bed leveling
2. Verify filament flow (extrusion test)
3. Try different part orientation
4. Ask Discord for help with photo
5. DO NOT STOP - try different part

### IF Component Doesn't Work:
1. Double-check wiring (GPIO pinout)
2. Verify power supply (voltage/current)
3. Check software (driver versions)
4. Test with different component if available
5. Document issue, continue other work

### IF Batteries Not Available:
1. Use bench power supply (5V/6V current-limited)
2. Test with old phone charger (5V 2A)
3. Order online (3-5 day lead time acceptable)
4. Continue with printing and software work

---

## EMERGENCY CONTACTS

**Technical Issues:**
- OpenDuck Discord: https://discord.gg/UtJZsgfQGe
- Raspberry Pi Forums: https://forums.raspberrypi.com

**Component Suppliers:**
- Eckstein Servos: info@eckstein-shop.de
- TheBatteryShop: info@thebatteryshop.eu

**Local Resources:**
- Vape shops Monza (search Google Maps)
- Electronics stores for emergency parts

---

## ACCOUNTABILITY

**At end of 48 hours, answer honestly:**

1. How many hours did 3D printer run? _____
2. How many components tested? _____
3. Did I order batteries? YES / NO
4. Did I create firmware repo? YES / NO
5. What blocked me that was TRULY unavoidable? ___________

**If answers are unsatisfactory:**
- [ ] Read hostile review again
- [ ] Identify REAL blocker (not excuses)
- [ ] Commit to different approach

---

## MOTIVATION

**You have:**
- Professional 3D printer (1200 EUR value)
- Raspberry Pi 4 with 8GB RAM
- 5kg+ of filament
- Quality components

**You're waiting for:**
- Parts that won't arrive for days/weeks
- "Perfect" conditions that don't exist
- Permission to start (you already have it)

**Truth:**
- Every day of delay pushes final assembly by 1 day
- 3D printing is SLOW (40-60 hours total) - start NOW
- Component testing takes 2-3 hours - do it TONIGHT
- Batteries cost 14 EUR - get them TOMORROW

**The robot won't build itself. Stop planning and START BUILDING.**

---

*Created: 2026-01-14*
*Deadline: 2026-01-15 23:59*
*No excuses. Only results.*
