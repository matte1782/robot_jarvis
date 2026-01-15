# MICROSD CARD BLOCKER - RESOLUTION GUIDE
## 14 January 2026 Evening - CRITICAL ISSUE

**Status:** 🚨 BLOCKS ALL RASPBERRY PI WORK
**Impact:** Cannot execute Block 1 (Pi Setup) from tonight's plan
**ETA for Delivery:** Friday 16 January 2026 (2 days from now)

---

## THE PROBLEM

**Original Plan (TONIGHT_ACTION_PLAN_CORRECTED.md):**
- Block 1 (90 minutes): Setup Raspberry Pi 4 with OS, SSH, Python, GPIO testing
- Prerequisite: MicroSD card with Raspberry Pi OS flashed
- **Reality:** SanDisk Ultra 32GB microSD arriving **Friday 16 Jan** (not available now)

**What This Blocks:**
- ❌ Raspberry Pi 4 setup (no SD = cannot boot)
- ❌ LED ring testing (requires Pi GPIO)
- ❌ Ultrasonic sensor testing (requires Pi GPIO)
- ❌ All GPIO/I2C/I2S work
- ❌ Audio amplifier testing
- ❌ Tomorrow's PCA9685 servo testing (requires configured Pi)

**Time Impact:** Loses 2 days if waiting for Friday delivery

---

## SOLUTION OPTIONS

### OPTION A: BUY MICROSD LOCALLY TONIGHT ⚡ RECOMMENDED

**What:** Purchase microSD card from local electronics store tonight
**Time:** 30-60 minutes (drive + purchase)
**Cost:** €8-15 for 32GB microSD card
**Impact:** UNBLOCKS all Pi work, can start tonight as planned

**Where to Buy (Monza Area):**

1. **MediaWorld Monza**
   - Address: Centro Commerciale Auchan, Via Borgazzi
   - Hours: Usually open until 21:00
   - Products: SanDisk, Samsung, Kingston microSD 32GB
   - Price: €10-15

2. **Unieuro Monza**
   - Address: Multiple locations in Monza
   - Hours: Check Google Maps
   - Products: Various brands 16GB-64GB
   - Price: €8-12

3. **Euronics**
   - Check nearest location
   - Usually stocks SanDisk/Samsung microSD

4. **Decathlon** (if open late)
   - Sports camera section often has microSD cards
   - Cheaper than electronics stores

**What to Buy:**
- Minimum: 16GB microSD card (Class 10 or better)
- Recommended: 32GB microSD card (A1/A2 rating preferred)
- Brands: SanDisk, Samsung, Kingston, Lexar (avoid no-name brands)
- **DO NOT** buy full-size SD card, must be **microSD**

**Advantage:** Can start Pi setup tonight (saves 2 days)

---

### OPTION B: CHECK FOR EXISTING SD CARDS

**What:** Search your home for any existing microSD cards

**Where to Look:**
- Old smartphones (Samsung, Xiaomi, etc.)
- Digital cameras
- Raspberry Pi projects from before
- Nintendo Switch (if you have one)
- Drone cameras
- Dashcam
- Old Android tablets

**Requirements:**
- Minimum 8GB (16GB+ recommended)
- Will be completely erased during OS flashing
- Any data on it will be lost

**How to Check:**
1. Find microSD card
2. Verify it's microSD (not full-size SD)
3. Insert into laptop SD reader
4. Check capacity (8GB minimum)
5. Backup any important data (will be erased)

**Advantage:** FREE, immediate availability if found

---

### OPTION C: USE EXISTING FULL-SIZE SD WITH ADAPTER

**What:** If you have full-size SD card, use microSD adapter

**Check if you have:**
- Old digital camera SD cards
- Camcorder SD cards
- Professional camera SD cards

**Requirement:** MicroSD adapter (small plastic shell that converts microSD to SD)
- Most microSD cards come with adapters
- Can buy adapter for €2-3 if needed

**Note:** This is backwards - you need microSD for Pi, but if you have SD card, you could potentially use it with adapter in laptop, then need microSD adapter for Pi (NOT RECOMMENDED, confusing)

**Advantage:** Might have available at home

---

### OPTION D: WAIT UNTIL FRIDAY (16 JAN) - DEFER PI WORK

**What:** Continue with non-Pi tasks tonight, wait for Friday delivery

**Impact:**
- Loses 2 days of Pi work (14-15 Jan)
- Can still do: Power assembly, firmware repo, component orders
- Cannot do: Any electronics testing until Friday

**Revised Schedule:**
- **Tonight (14 Jan):** Power system assembly, firmware repo, orders (2 hours)
- **Tomorrow (15 Jan):** Software development, mock drivers, kinematics (4-5 hours)
- **Friday (16 Jan):** MicroSD arrives, setup Pi, test electronics (6-8 hours)
- **Weekend (18-19 Jan):** Catch up on hardware testing

**Advantage:** No additional cost, no rushing
**Disadvantage:** 2-day delay on hardware validation

---

## ASUS ZENBOOK SD CARD READER - VERIFICATION

**Your Question:** "can i do it with my asus dual zenbook? i have ssd nvme adaptor not sure if sd"

### Step 1: Check if Your Laptop Has SD Card Reader

**ASUS Dual Zenbook (most models have SD reader):**

1. **Look at laptop sides:**
   - Check left side for SD card slot (usually labeled with SD icon)
   - Check right side if not on left
   - Slot is about 24mm wide, 2-3mm tall
   - Often has spring-loaded mechanism

2. **Check laptop specifications:**
   - Google: "ASUS Dual Zenbook [your model number] SD card reader"
   - Model number usually on bottom of laptop or in Settings > System > About
   - Example models: UX482, UX8402, UX435 (most have SD readers)

3. **Visual Guide:**
   ```
   SD Card Slot looks like:
   ┌─────────────┐
   │ ─────       │  ← This is the slot opening
   └─────────────┘
   Usually has text: SD or SD/MMC or card symbol
   ```

**If YES (has SD reader):**
- ✅ You can flash microSD cards directly
- ✅ Can use Raspberry Pi Imager on Windows
- ✅ Ready to flash OS once you have microSD

**If NO (no SD reader):**
- You'll need USB SD card reader (€5-10 from same stores)
- OR use SSD NVMe adapter if it has SD slot (unlikely)

---

### Step 2: About Your "SSD NVMe Adapter"

**What is it?**
- NVMe adapter = for M.2 NVMe SSDs (internal storage drives)
- **NOT the same as SD card reader**
- Used for upgrading laptop storage, not for SD cards

**Confusion clarification:**
- SSD NVMe adapter: For M.2 solid-state drives (internal PC component)
- SD card adapter: For SD/microSD memory cards (camera cards, Pi cards)
- These are DIFFERENT devices

**If your adapter is USB NVMe enclosure:**
- Cannot use for SD cards
- Need separate SD card reader

**If your adapter has SD slot (rare):**
- Some multi-function adapters have both NVMe and SD slots
- Check the adapter for SD card slot opening
- If yes, can use it

---

## HOW TO FLASH RASPBERRY PI OS (ONCE YOU HAVE MICROSD)

### Requirements:
- Windows laptop (ASUS Zenbook) ✅ You have this
- MicroSD card (16GB+, Class 10+) ❌ Need to acquire
- SD card reader (built-in or USB) ❓ Need to verify
- Internet connection ✅ Assumed available

### Step-by-Step Process:

**STEP 1: Download Raspberry Pi Imager (5 minutes)**

1. Open web browser
2. Go to: https://www.raspberrypi.com/software/
3. Click "Download for Windows"
4. Save file: `imager_latest.exe`
5. Run installer (double-click downloaded file)
6. Follow installation wizard (click Next, Next, Install, Finish)

**STEP 2: Insert MicroSD Card**

1. If built-in SD reader:
   - Insert microSD into SD slot on laptop side
   - Should click into place
   - Windows will detect it (may ask to format - click Cancel)

2. If USB SD reader:
   - Insert microSD into USB reader
   - Plug USB reader into laptop USB port
   - Windows will detect it

3. Verify detection:
   - Open File Explorer (Windows key + E)
   - Check if new drive appears (e.g., "D:", "E:", etc.)
   - Note the drive letter

**STEP 3: Flash Raspberry Pi OS (10 minutes)**

1. Launch Raspberry Pi Imager (from Start Menu)

2. Click "CHOOSE DEVICE"
   - Select: Raspberry Pi 4
   - (Your model: Pi 4 Model B 4GB)

3. Click "CHOOSE OS"
   - Select: "Raspberry Pi OS (64-bit)"
   - **Recommended:** "Raspberry Pi OS Lite (64-bit)" for headless (no desktop)
   - OR "Raspberry Pi OS (64-bit)" if you want desktop GUI

4. Click "CHOOSE STORAGE"
   - Select your microSD card
   - **CAREFUL:** Select correct drive (all data will be erased!)
   - Should show size (e.g., "32 GB SD Card")

5. Click gear icon ⚙️ (Advanced Options) **IMPORTANT - DO THIS**
   - Set hostname: `openduck` (or `raspberrypi`)
   - ✅ Enable SSH
     - Select: "Use password authentication"
   - Set username: `pi`
   - Set password: `openduck` (or your choice, remember it!)
   - ✅ Configure wireless LAN
     - SSID: Your WiFi network name
     - Password: Your WiFi password
     - Country: IT (Italy)
   - Set locale:
     - Timezone: Europe/Rome
     - Keyboard: it (Italian)
   - Click "SAVE"

6. Click "WRITE"
   - Confirm: "All existing data will be erased"
   - Click "YES"
   - Wait 5-10 minutes (downloads OS + writes to card)
   - Progress bar will show status

7. When complete:
   - "Write Successful" message appears
   - Click "CONTINUE"
   - Windows may say "format disk" - click Cancel/Dismiss
   - Safely eject SD card:
     - Right-click drive in File Explorer
     - Click "Eject"
     - Wait for "Safe to remove" message
     - Remove microSD from reader

**STEP 4: Insert into Raspberry Pi 4**

1. Locate microSD slot on Pi 4:
   - On underside of board
   - Opposite side from USB ports
   - Push-push mechanism (push in to insert, push again to eject)

2. Insert microSD card:
   - Metal contacts facing UP (toward PCB)
   - Push until clicks into place

3. Power on Pi:
   - Connect USB-C power (5V 3A minimum)
   - Red LED lights up (power)
   - Green LED blinks (activity, reading SD card)
   - Wait 30-60 seconds for first boot

4. Connect via SSH:
   - Open Command Prompt or PowerShell on laptop
   - Type: `ssh pi@openduck.local`
   - OR find IP from router, use: `ssh pi@192.168.x.x`
   - Accept fingerprint (type `yes`)
   - Enter password: `openduck` (or what you set)
   - You should see: `pi@openduck:~ $`

**Success!** Pi is ready for development.

---

## REVISED TONIGHT PLAN (WITHOUT PI)

**If you cannot acquire microSD tonight, here's what you CAN do:**

### BLOCK 1: POWER SYSTEM ASSEMBLY (45 minutes) ✅ NO PI NEEDED

**Components:**
- BMS 2S 20A (delivered)
- UBEC 5V/6V 3A (delivered)
- Battery holder 2S (delivered)
- XT30 connectors (delivered)
- Silicon wire 16AWG (delivered)
- Soldering station (delivered)

**Tasks:**
1. Solder BMS to battery holder:
   - Red wire: Battery + to BMS B+
   - Black wire: Battery - to BMS B-
2. Add XT30 male connector to BMS output (P+/P-)
3. Solder XT30 female to UBEC input
4. Set UBEC output to 5V (check jumper settings)
5. Heat shrink all connections
6. Label with tape: "BMS OUT", "UBEC IN", polarity markers

**Success:** Power system ready for battery insertion (when batteries acquired)

---

### BLOCK 2: FIRMWARE REPOSITORY INITIALIZATION (30 minutes) ✅ NO PI NEEDED

**Tasks:**
1. Create `firmware/` directory structure:
   ```bash
   cd "C:\Users\matte\Desktop\Desktop OLD\AI\Università AI\courses\personal_project\robot_jarvis"
   mkdir firmware
   cd firmware
   mkdir -p src/drivers/servo src/drivers/led src/drivers/audio src/drivers/sensor
   mkdir -p src/control src/core/safety src/utils
   mkdir -p config tests
   ```

2. Create README.md (copy from TONIGHT_ACTION_PLAN_CORRECTED.md)

3. Create requirements.txt (copy from plan)

4. Initialize git:
   ```bash
   git init
   git add .
   git commit -m "Initial firmware structure for OpenDuck Mini V3"
   ```

**Success:** Firmware foundation ready for development

---

### BLOCK 3: CRITICAL COMPONENT ORDERS (60 minutes) ✅ NO PI NEEDED

**Order 1: Molicel P30B Batteries (30 min)**

Option A: Call vape shops (Google: "Vape shop Monza")
- Ask: "Avete batterie Molicel INR18650-P30B?"
- If yes: Drive and buy 4 cells (€14-16)

Option B: Order online
- TheBatteryShop.eu
- 4× Molicel P30B
- Express shipping

**Order 2: FE-URT-1 Controller (10 min)**
- AliExpress: Search "FE-URT-1"
- Order 1 unit (~€45)
- Standard shipping (15-25 days OK)

**Order 3: Email Eckstein for STS3215 Quote (10 min)**
- Email: info@eckstein-shop.de
- Request quote for 16× Feetech STS3215 servos

**Success:** All critical path items ordered, no future delays

---

### BLOCK 4: COMPONENT INVENTORY & PHOTOS (30 minutes) ✅ NO PI NEEDED

**Tasks:**
1. Locate all delivered components
2. Take photos of each item
3. Create inventory document
4. Verify quantities match orders
5. Check for any damage
6. Organize workspace for tomorrow

**Success:** Know exactly what's available, photo documentation created

---

## REVISED TIMELINE

### OPTION A: Acquire MicroSD Tonight
- **Tonight (14 Jan, 20:00-23:30):**
  - 20:00-20:30: Drive to MediaWorld/Unieuro, buy microSD
  - 20:30-21:00: Return home, flash Raspberry Pi OS
  - 21:00-22:30: Pi setup, LED test, GPIO test
  - 22:30-23:00: Power assembly
  - 23:00-23:30: Orders (batteries, FE-URT-1)
- **Result:** ON SCHEDULE, all hardware validated by end of tomorrow

---

### OPTION B: Wait for Friday Delivery
- **Tonight (14 Jan, 20:00-22:00):**
  - 20:00-20:45: Power system assembly
  - 20:45-21:15: Firmware repo initialization
  - 21:15-22:00: Orders + component inventory
- **Tomorrow (15 Jan, 9:00-14:00):**
  - Software development (mock drivers, kinematics)
  - Documentation and architecture
- **Friday (16 Jan, when SD arrives):**
  - Morning: Flash OS, setup Pi
  - Afternoon: Full hardware testing marathon
- **Result:** 2-DAY DELAY on hardware, but software progresses

---

## RECOMMENDATION

**IF you can get to MediaWorld/Unieuro before they close tonight:**
→ **DO IT.** Spend €10-15 on microSD, unblock all Pi work, stay on schedule.

**IF stores are closed or too far:**
→ **Accept 2-day delay.** Focus on power assembly, firmware repo, orders tonight. Do software work tomorrow. Hardware blitz on Friday.

**DO NOT:**
- ❌ Wait around hoping SD arrives early (it won't)
- ❌ Try to jury-rig other storage methods (won't work with Pi)
- ❌ Delay orders (batteries, FE-URT-1) - order tonight regardless

---

## BOTTOM LINE

**The MicroSD blocker is REAL but SOLVABLE:**

1. **Best option:** Buy microSD locally tonight (€10-15, 30-60 min effort)
2. **Free option:** Search home for existing microSD card
3. **Wait option:** Accept 2-day delay, do non-Pi work tonight

**What NOT to stress about:**
- The plan is still solid
- Software work can proceed without Pi
- 2-day delay is manageable (still 70%+ Week 01 completion possible)
- Your Amazon order is fine, just arriving Friday

**What to DO right now:**
1. Check ASUS Zenbook for SD card slot (30 seconds)
2. If yes + stores open → drive and buy microSD (saves 2 days)
3. If no/stores closed → execute OPTION B revised plan above

**Remember:** Progress > Perfection. Getting SOMETHING done tonight beats waiting for perfect conditions.

---

*Created: 2026-01-14 Evening*
*Priority: CRITICAL - Blocks 80% of Week 01 hardware work*
*Decision needed: Next 30 minutes*
