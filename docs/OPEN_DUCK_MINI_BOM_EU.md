# Open Duck Mini + Custom Arms - Bill of Materials (EU)

**Last Verified**: 2026-01-11
**Project**: Open Duck Mini v2 with Custom 2-DOF Robotic Arms
**Budget Target**: €360 (recommended) / €460 (with tools)
**Status**: ✅ VERIFIED - All links and prices checked January 2026

---

## 📊 EXECUTIVE SUMMARY

### What You're Building:
A quadruped robot (4 legs) with 2-DOF robotic arms based on Open Duck Mini, featuring:
- 10 servo motors total (6 legs + 2 shoulders + 2 gripper servos)
- Raspberry Pi 4 brain with IMU sensor for balance
- 3S LiPo battery power system
- RGB LED strip for visual feedback
- Custom 3D-printed parts (body, legs, arms)

### Total Investment:
| Budget Level | Cost | What's Included |
|--------------|------|-----------------|
| **Minimum** | €310 | Basic robot, no TPU, basic sensors |
| **Recommended** | **€360** | **Full robot + PLA + TPU filament** ⭐ |
| **With Tools** | €460 | Everything + soldering kit, screwdrivers, etc. |

### Key Verified Changes (Jan 2026 vs Nov 2024):
- ✅ **Raspberry Pi 4 4GB**: IN STOCK on Amazon.it (€43-65)
- ✅ **Servo extension cables**: NOW AVAILABLE on Amazon.it (was problematic)
- ✅ **PCA9685 Driver**: Updated to 2-pack instead of 5-pack (€15)
- ❌ **MG90S servos**: Still NOT available → Use SG90 for all positions or upgrade shoulders to MG996R
- ❌ **INMP441 microphone**: Still NOT on Amazon.it → DigiKey.it or use USB mic
- ⚠️ **TPU filament added** (€26) - essential for flexible feet pads
- 📈 **Price increase**: +€60-70 overall due to component updates and filament costs

### Where to Buy:
1. **Amazon.it (Prime)**: 80% of components (€290-320) - fast shipping ✅
2. **Melopero.com**: BNO055 IMU sensor if needed (€28-32)
3. **DigiKey.it**: INMP441 microphone if needed (€8-10)

### Time Commitment:
- **3D Printing**: 40-60 hours print time
- **Assembly**: 15-20 hours
- **Programming**: 10-30 hours (depends on experience)
- **Total**: 8-12 weeks calendar time

### Prerequisites:
- Access to 3D printer or printing service (REQUIRED)
- Basic soldering skills (or use crimp connectors)
- Electronics experience helpful but not required
- Linux/Python knowledge recommended

---

## 🛒 COMPLETE COMPONENT LIST

### 📦 CATEGORIA 1: Compute & Controllo

| # | Componente | Qtà | Prezzo Unit. | Totale | Link Amazon.it / EU | Status |
|---|------------|-----|--------------|--------|---------------------|--------|
| 1 | **Raspberry Pi 4 Model B 4GB** | 1 | €43-65 | €60 | ✅ [Amazon.it RPI4-4GB](https://www.amazon.it/Raspberry-Pi-RAS-4-4G-Modelo-4GB/dp/B07TC2BK1X) | IN STOCK |
| 2 | **Scheda microSD 32GB Class 10 (SanDisk/Samsung)** | 1 | €7-10 | €8 | ✅ Cerca: "microSD 32GB SanDisk" su Amazon.it | Available |
| 3 | **PCA9685 16-CH PWM Servo Driver I2C** | 1 | €15 (2pcs) | €15 | ✅ [Amazon.it TECNOIOT 2pcs](https://www.amazon.it/PCA9685-Channel-Interface-Interfaccia-servoazionamento/dp/B07LH56QBZ) | IN STOCK |

**Subtotale Compute**: ~€83

**Note**:
- Raspberry Pi 4 4GB verified available with recent Jan 2026 reviews
- PCA9685 now comes in 2-pack (updated from 5-pack listing), price adjusted
- MicroSD: SanDisk Ultra or Samsung EVO Plus recommended

---

### ⚡ CATEGORIA 2: Alimentazione

| # | Componente | Qtà | Prezzo Unit. | Totale | Link Amazon.it / EU | Status |
|---|------------|-----|--------------|--------|---------------------|--------|
| 4 | **Batteria LiPo 11.1V 3S 3000mAh XT60** | 1 | €18-25 | €22 | ✅ Cerca: "3S 3000mAh XT60" su Amazon.it | Available |
| 5 | **UBEC Step-Down 5V 3A DC-DC** | 1 | €6-9 | €8 | ✅ Cerca: "UBEC 5V 3A" su Amazon.it | Available |
| 6 | **Caricabatterie LiPo Balance 2S-3S (IMAX B6)** | 1 | €18-28 | €25 | ✅ Cerca: "IMAX B6 LiPo charger" su Amazon.it | Available |
| 7 | **Cavi bilanciamento 3S XT60** | 1 | €5-7 | €6 | ✅ Cerca: "cavi bilanciamento 3S XT60" su Amazon.it | Available |

**Subtotale Alimentazione**: ~€61

**Note**:
- LiPo batteries: Look for brands like OVONIC, HRB, Zeee with 30C+ discharge rate
- UBEC: Adafruit or generic 5V 3A step-down converters work well
- Charger: IMAX B6 clone or SkyRC recommended for safe charging
- **SAFETY**: Never leave LiPo batteries charging unattended!

---

### 🦾 CATEGORIA 3: Servomotori

| # | Componente | Qtà | Prezzo Unit. | Totale | Link Amazon.it / EU | Status |
|---|------------|-----|--------------|--------|---------------------|--------|
| 8 | **SG90 Micro Servo 9g (legs: 6pcs)** | 1 pack | €12-15 (6pcs) | €15 | ✅ Cerca: "SG90 servo 6pcs" su Amazon.it | IN STOCK |
| 9 | **SG90 Servo (arms shoulders: 2pcs)** | 2 | €2.50 | €5 | ✅ Same as #8 or buy 10-pack | IN STOCK |
| 10 | **SG90 Servo (gripper claws: 2pcs)** | 2 | €2.50 | €5 | ✅ Same as #8 or separate 2-pack | IN STOCK |
| 11 | **Servo Arms/Horns Kit** | 1 set | €5-8 | €6 | ✅ Cerca: "servo horn arm kit" su Amazon.it | Available |

**Subtotale Servomotori**: ~€31

**⚠️ IMPORTANT SERVO NOTES**:
- **MG90S Metal Gear**: NOT available on Amazon.it in Jan 2026
- **ALTERNATIVE 1**: Use SG90 for all positions (cheaper, less durable but works)
- **ALTERNATIVE 2**: Upgrade shoulders to **MG996R** (€5 each, high torque) - recommended for arm strength
- **ALTERNATIVE 3**: **SERVOMY SDS1601** - upgraded SG90 replacement with metal gears (Amazon.com ships to EU)
- **Total servo count**: 10 servos needed (6 legs + 2 shoulders + 2 grippers)
- **Recommendation**: Buy 10-pack SG90 (€20-25) for cost efficiency + spares

---

### 🧠 CATEGORIA 4: Sensori & I/O

| # | Componente | Qtà | Prezzo Unit. | Totale | Link Amazon.it / EU | Status |
|---|------------|-----|--------------|--------|---------------------|--------|
| 12 | **BNO055 9-DOF IMU Sensor (Adafruit)** | 1 | €28-35 | €30 | ⚠️ Cerca Amazon.it o [Melopero.com](https://www.melopero.com) | Limited Stock |
| 13 | **WS2812B LED Strip 1m 60 LED/m 5V** | 1 | €12-18 | €15 | ✅ Cerca: "WS2812B 1m 60" su Amazon.it | IN STOCK |
| 14 | **Mini Speaker 8Ω 2-5W** | 1 | €5-8 | €6 | ✅ Cerca: "speaker 8 ohm 3W" su Amazon.it | Available |
| 15 | **Microfono I2S MEMS INMP441** | 1 | €8-12 | €10 | ⚠️ NOT on Amazon.it - [DigiKey.it](https://www.digikey.it) or Amazon.com | Special Order |

**Subtotale Sensori**: ~€61

**Note**:
- **BNO055**: Adafruit part #2472 or #4646 (STEMMA QT version). Alternative: MPU6050 (€5, less accurate)
- **WS2812B LED**: BTF-LIGHTING brand recommended, IP30 (indoor) or IP65 (waterproof)
- **INMP441 Microphone**: DigiKey/Mouser or Amazon.com ships to EU. Alternative: use USB mic
- **Speaker**: JST connector or solder directly to amplifier board

---

### 🔩 CATEGORIA 5: Hardware Meccanico

| # | Componente | Qtà | Prezzo Unit. | Totale | Link Amazon.it / EU | Status |
|---|------------|-----|--------------|--------|---------------------|--------|
| 16 | **Kit Viti M2/M3 + Distanziali 300pcs** | 1 | €10-15 | €12 | ✅ Cerca: "kit viti M2 M3 distanziali" su Amazon.it | IN STOCK |
| 17 | **Cuscinetti a sfera 608ZZ (8x22x7mm)** | 8pcs | €6-10 (8pcs) | €8 | ✅ Cerca: "608ZZ bearing" su Amazon.it | IN STOCK |
| 18 | **Cavi Servo Extension 30cm JR (25pcs kit)** | 1 kit | €10-15 | €12 | ✅ [Amazon.it Servo Extension](https://www.amazon.it/Prolunga-Servocomando-Estensione-Connettore-Telecomandato/dp/B0925FT1RF) | IN STOCK |

**Subtotale Hardware**: ~€32

**Note**:
- **M2/M3 screws**: Get assortment kit with hex nuts and standoffs for Raspberry Pi and servo mounting
- **608ZZ bearings**: Standard skateboard bearings, use for leg joints and rotating parts
- **Servo cables**: 25pcs kit includes multiple lengths (10cm/15cm/30cm/50cm/60cm), JR connector compatible

---

### 🖨️ CATEGORIA 6: Stampa 3D

| # | Componente | Qtà | Prezzo Unit. | Totale | Link Amazon.it / EU | Status |
|---|------------|-----|--------------|--------|---------------------|--------|
| 19 | **Filamento PLA 1.75mm 1kg** | 1-2 | €16-22 | €20 | ✅ Cerca: "SUNLU PLA+ 1kg" su Amazon.it | IN STOCK |
| 20 | **Filamento TPU 95A 1kg (flexible, for feet)** | 1 | €22-30 | €26 | ✅ [SUNLU TPU 95A](https://www.amazon.it/SUNLU-Filamento-Flessibile-Precisione-Dimensionale/dp/B0BXNWK6NS) or OVERTURE | IN STOCK |

**Subtotale Stampa 3D**: ~€46

**Note**:
- **PLA filament**: SUNLU PLA+, eSUN PLA+, or Prusament recommended. Need ~800g for full robot
- **TPU filament**: For flexible feet pads and shock absorption. Shore 95A hardness ideal
- **Colors**: White/Grey for body, Black for details, or your choice
- **Print settings**: 0.2mm layer height, 20% infill for structural parts

**⚠️ If you don't have a 3D printer**:
- **Online print service**: Treatstock, 3DHubs (~€35-60 for complete set)
- **Local makerspace**: Often €5-10/hour printer time
- **Buy printer**: Bambu Lab A1 Mini (€250), Creality Ender 3 V3 (€200) on Amazon.it

---

### 🔌 CATEGORIA 7: Cavi & Connettori

| # | Componente | Qtà | Prezzo Unit. | Totale | Link Amazon.it / EU | Status |
|---|------------|-----|--------------|--------|---------------------|--------|
| 21 | **Alimentatore USB-C 5V 3A per Pi 4** | 1 | €8-12 | €10 | ✅ Cerca: "USB-C 5V 3A Raspberry Pi" su Amazon.it | IN STOCK |
| 22 | **Cavi Dupont F-F, F-M, M-M (120pcs kit)** | 1 | €6-9 | €7 | ✅ Cerca: "cavi dupont 120pcs" su Amazon.it | IN STOCK |
| 23 | **Connettori JST-PH 2.0 (per speaker/LED)** | 1 set | €5-8 | €6 | ✅ Cerca: "JST 2.0 connettori" su Amazon.it | Available |
| 24 | **Heat Shrink Tubing Kit** | 1 | €5-8 | €6 | ✅ Cerca: "guaina termorestringente" su Amazon.it | Available |

**Subtotale Cavi**: ~€29

**Note**:
- **USB-C Power**: Official Raspberry Pi power supply recommended (5.1V 3A)
- **Dupont cables**: 20cm length ideal for internal wiring
- **JST connectors**: For clean removable connections on sensors
- **Heat shrink**: Essential for protecting solder joints

---

### 🛠️ CATEGORIA 8: Tools & Assembly (if not owned)

| # | Componente | Qtà | Prezzo Unit. | Totale | Link Amazon.it / EU | Status |
|---|------------|-----|--------------|--------|---------------------|--------|
| 25 | **Soldering Iron Kit 60W Temperature Control** | 1 | €18-30 | €25 | ✅ Cerca: "soldering iron kit 60W" su Amazon.it | IN STOCK |
| 26 | **Precision Screwdriver Set (Phillips + Hex)** | 1 | €12-20 | €15 | ✅ Cerca: "Wera precision screwdriver" su Amazon.it | IN STOCK |
| 27 | **Hex Key Set Metric (1.5mm-6mm)** | 1 | €8-15 | €10 | ✅ Cerca: "Wiha hex key set" su Amazon.it | IN STOCK |
| 28 | **Wire Stripper/Cutter** | 1 | €8-12 | €10 | ✅ Cerca: "wire stripper cutter" su Amazon.it | Available |
| 29 | **Helping Hands with Magnifier** | 1 | €12-18 | €15 | ✅ Cerca: "helping hands soldering" su Amazon.it | Available |
| 30 | **Digital Multimeter** | 1 | €15-25 | €20 | ✅ Cerca: "digital multimeter" su Amazon.it | Available |

**Subtotale Tools**: ~€95 (skip if you already own these)

**Note**:
- **Soldering iron**: 60W adjustable temp (200-450°C), comes with tips, stand, sponge
- **Screwdrivers**: Precision set for small electronics, magnetic tips recommended
- **Hex keys**: Needed for M2/M3 socket head screws, ball-end type preferred
- **Multimeter**: For debugging power issues, checking servo signals
- **These are ONE-TIME purchases** - reusable for future projects

---

## 💰 TOTALI

### Build BASE (Robot Only - No Tools)

| Categoria | Totale EUR |
|-----------|------------|
| 1. Compute & Controllo | €83 |
| 2. Alimentazione | €61 |
| 3. Servomotori (10x SG90) | €31 |
| 4. Sensori & I/O | €61 |
| 5. Hardware Meccanico | €32 |
| 6. Stampa 3D (PLA + TPU) | €46 |
| 7. Cavi & Connettori | €29 |
| **SUBTOTALE COMPONENTI** | **€343** |
| **Shipping buffer (~5%)** | **€17** |
| **TOTALE BUILD BASE** | **~€360** |

### Build COMPLETO (with Tools)

| Categoria | Totale EUR |
|-----------|------------|
| Robot Components (1-7) | €343 |
| 8. Tools & Assembly | €95 |
| **SUBTOTALE COMPLETO** | **€438** |
| **Shipping buffer (~5%)** | **€22** |
| **TOTALE CON TOOLS** | **~€460** |

**Note**: Tools are ONE-TIME purchase, skip if you already own soldering equipment and screwdrivers

---

### UPGRADE OPZIONALI

| # | Componente | Qtà | Prezzo | Note | Status |
|---|------------|-----|--------|------|--------|
| 31 | **Webcam USB (Logitech C270 HD)** | 1 | €35-45 | Computer vision, object tracking | ✅ Available |
| 32 | **MG996R High Torque Servo (for shoulders)** | 2 | €10-12 | 11kg.cm torque vs 1.8kg.cm SG90 | ✅ Available |
| 33 | **LiPo 3S 5000mAh XT60 (extended runtime)** | 1 | €28-35 | 2x battery life (~2hrs vs 1hr) | ✅ Available |
| 34 | **Raspberry Pi Camera Module v3** | 1 | €35-40 | Better than USB cam, native ribbon | ✅ Available |
| 35 | **MPU6050 IMU (cheaper BNO055 alternative)** | 1 | €5-8 | 6-axis instead of 9-axis | ✅ Available |
| 36 | **Neopixel Ring 16 LED WS2812B** | 1 | €6-10 | Head LED ring for expressions | ✅ Available |

**Totale Upgrade (pick what you need)**: ~€45-95 depending on choices

---

## 🚨 ITEMS REQUIRING SPECIAL ATTENTION (January 2026)

| Componente | Status | Best Solution |
|------------|--------|---------------|
| **MG90S Metal Gear Servo** | ❌ NOT AVAILABLE on Amazon.it | ✅ **Use SG90 for all positions** (works fine, slightly less durable)<br>OR upgrade shoulders to MG996R (€5 each, high torque) |
| **INMP441 I2S MEMS Microphone** | ❌ NOT on Amazon.it | ✅ Order from [DigiKey.it](https://www.digikey.it) or Amazon.com<br>OR use USB microphone (cheaper, easier) |
| **BNO055 IMU Sensor** | ⚠️ LIMITED STOCK | ✅ Check [Melopero.com](https://www.melopero.com)<br>OR use MPU6050 (€5, less accurate but works) |
| **Servo Extension Cables 30cm** | ✅ NOW AVAILABLE | ✅ [25pcs kit on Amazon.it](https://www.amazon.it/Prolunga-Servocomando-Estensione-Connettore-Telecomandato/dp/B0925FT1RF) verified |

---

## 📋 PURCHASE STRATEGY (Updated Jan 2026)

### 🛒 ORDINE 1: Amazon.it (Prime) - ~€290-320

✅ **PRIORITY ITEMS** (get these first):

**Electronics & Control:**
1. ✅ Raspberry Pi 4 4GB (€60) - [Direct Link](https://www.amazon.it/Raspberry-Pi-RAS-4-4G-Modelo-4GB/dp/B07TC2BK1X)
2. ✅ PCA9685 Servo Driver 2pcs (€15) - [Direct Link](https://www.amazon.it/PCA9685-Channel-Interface-Interfaccia-servoazionamento/dp/B07LH56QBZ)
3. ✅ SG90 Servos 10-pack (€20-25) - Search: "SG90 10pcs"
4. ✅ microSD 32GB Class 10 (€8) - Search: "SanDisk Ultra 32GB"

**Power:**
5. ✅ LiPo 3S 3000mAh XT60 (€22) - Search: "3S 3000mAh XT60"
6. ✅ UBEC 5V 3A (€8) - Search: "UBEC 5V 3A step down"
7. ✅ LiPo Charger IMAX B6 (€25) - Search: "IMAX B6 charger"
8. ✅ USB-C Power Supply 5V 3A (€10) - Search: "Raspberry Pi power supply"

**Sensors & LEDs:**
9. ✅ WS2812B LED Strip 1m 60LED (€15) - Search: "WS2812B 1m 60"
10. ✅ Speaker 8Ω 3W (€6) - Search: "speaker 8 ohm 3W"

**Hardware:**
11. ✅ M2/M3 Screw Kit (€12) - Search: "kit viti M2 M3"
12. ✅ 608ZZ Bearings 8pcs (€8) - Search: "608ZZ bearing"
13. ✅ Servo Extension Cable Kit (€12) - [Direct Link](https://www.amazon.it/Prolunga-Servocomando-Estensione-Connettore-Telecomandato/dp/B0925FT1RF)
14. ✅ Dupont Cables 120pcs (€7) - Search: "cavi dupont 120"

**3D Printing:**
15. ✅ PLA Filament 1kg (€20) - Search: "SUNLU PLA+"
16. ✅ TPU 95A Filament 1kg (€26) - [Direct Link](https://www.amazon.it/SUNLU-Filamento-Flessibile-Precisione-Dimensionale/dp/B0BXNWK6NS)

**Advantage**: Amazon Prime free shipping, 1-2 day delivery, easy returns

---

### 📦 ORDINE 2: Specialized EU Suppliers - ~€40-50

**Melopero.com** (Italy):
- ✅ BNO055 IMU Sensor (€28-32) - if not found on Amazon.it
- Component selection and Arduino/Pi accessories

**DigiKey.it** or **Mouser.it**:
- ✅ INMP441 I2S Microphone (€8-10) - professional electronics distributor
- Fast EU shipping from local warehouses

**Alternative**: Skip INMP441, use USB microphone (€10-15 on Amazon.it)

---

### 🛠️ ORDINE 3: Tools (if needed) - ~€95

Order from Amazon.it:
- Soldering iron kit 60W (€25)
- Precision screwdriver set (€15)
- Hex key set (€10)
- Wire stripper (€10)
- Helping hands (€15)
- Multimeter (€20)

**Note**: Skip this order if you already have electronics tools

---

## 🎯 ALTERNATIVE ITALIANE

### Se Amazon.it non ha stock:

| Categoria | Fornitore Alternativo IT/EU |
|-----------|------------------------------|
| **Raspberry Pi** | Melopero.com, RobotStore.it, RS Components IT |
| **Servomotori** | Futura Elettronica, RobotStore.it, Conrad.it |
| **Elettronica** | Futura Elettronica, Elettronica In (elettronicain.it) |
| **Sensori** | Melopero.com, RobotShop EU |
| **Filamento PLA** | 3DItaly.it, Filoalfa.com (produttore italiano!) |

---

## ✅ CHECKLIST PRE-ORDINE

Prima di procedere all'acquisto, verifica:

- [ ] **Stampante 3D disponibile** (o servizio stampa prenotato)
- [ ] **Account Amazon.it Prime** (per spedizione gratuita)
- [ ] **Alimentatore USB-C 5V 3A** per Raspberry Pi 4 (se non già posseduto)
- [ ] **PC/laptop** per programmazione e flash microSD
- [ ] **Cacciavite set** (Phillips + Torx) per assemblaggio
- [ ] **Saldatore** (opzionale, per connessioni robuste)

---

## 📊 BUDGET COMPARISON (January 2026)

| Configuration | Total EUR | What's Included |
|---------------|-----------|-----------------|
| **Minimum Build** | ~€310 | Robot only, no tools, no TPU filament, basic components |
| **Recommended Build** | **~€360** | **Full robot + PLA + TPU, no tools** |
| **Complete Build** | ~€460 | Robot + all tools (one-time investment) |
| **With 3D Printer** | ~€560-660 | Add Creality Ender 3 V3 (€200) or Bambu A1 Mini (€250) |
| **Premium Build** | ~€500 | Robot + tools + upgrades (MG996R servos, extra battery, webcam) |

**Price Changes vs Nov 2024**:
- Overall +€60-70 increase (mainly filament, servos, and updated components)
- Raspberry Pi 4 stable at €43-65
- Servo extension cables now available on Amazon.it (was problematic before)
- TPU filament added (€26) - essential for flexible feet

---

## 🔗 LINK UTILI

### Documentazione Progetto
- **Open Duck Mini GitHub**: https://github.com/apirrone/Open_Duck_Mini
- **CAD OnShape**: https://cad.onshape.com/documents/64074dfcfa379b37d8a47762
- **LittleBot Gripper (braccio reference)**: https://www.instructables.com/3D-Printed-Robot-Gripper-LittleBot-Gripper/

### Fornitori Principali
- **Amazon.it**: https://www.amazon.it
- **Melopero Elettronica**: https://www.melopero.com
- **RobotStore.it**: https://www.robotstore.it
- **Futura Elettronica**: https://www.futurashop.it
- **Mouser Italia**: https://www.mouser.it
- **DigiKey Italia**: https://www.digikey.it

---

## 📝 IMPORTANT NOTES (January 2026)

### ✅ Verified January 2026:
- All Amazon.it links checked and working
- Prices updated to current market rates
- Stock availability verified where possible
- Direct product links provided for critical components

### ⚠️ Before You Order:

1. **Prices are current as of Jan 11, 2026** - Always verify current price before purchasing
2. **Stock varies daily** - Raspberry Pi 4 and some sensors may have limited availability
3. **Alternatives provided** - Almost every component has a working alternative listed
4. **Consolidate orders** - Use Amazon.it for most items to minimize shipping costs
5. **Assembly time**: Budget 8-12 weeks for complete build (see project timeline docs)

### 🔧 Critical Success Factors:

- **3D Printer Access**: You MUST have access to a 3D printer or printing service
- **Soldering Skills**: Basic soldering required for some connections (or use crimp connectors)
- **LiPo Safety**: Never leave LiPo batteries charging unattended, use fireproof bag
- **Patience**: This is an advanced project - expect troubleshooting and iterations

---

**READY TO ORDER? 🚀**

### Quick Start Guide:

1. **START HERE**: Order from Amazon.it first (€290-320)
   - Get all components from ORDINE 1 list above
   - Use Amazon Prime for free fast shipping

2. **THEN**: Order specialty items (€40-50)
   - BNO055 from Melopero.com (if not on Amazon.it)
   - INMP441 microphone from DigiKey.it (optional)

3. **OPTIONAL**: Order tools if needed (€95)
   - Only if you don't already own electronics tools
   - These are reusable for future projects

4. **VERIFY** before finalizing:
   - Check current Amazon.it prices
   - Confirm stock availability
   - Read recent reviews (Jan 2026)
   - Calculate total with shipping

### 💡 Money-Saving Tips:

- Buy SG90 servos in 10-pack instead of individual purchases
- Skip INMP441 microphone, use USB mic instead (-€10)
- Use MPU6050 instead of BNO055 IMU (-€23)
- Print with PLA only, skip TPU for first build (-€26)
- **Minimum viable build**: ~€285-310

---

## 📋 QUICK REFERENCE SUMMARY

**Total Components Needed:**
- 1x Raspberry Pi 4 4GB
- 1x PCA9685 servo driver
- 10x SG90 servos (6 legs + 2 shoulders + 2 grippers)
- 1x LiPo 3S 3000mAh + charger + UBEC
- 1x BNO055 IMU (or MPU6050 alternative)
- 1x WS2812B LED strip 1m
- 1x microSD 32GB
- Various cables, screws, bearings
- ~800g PLA filament + optional TPU

**Estimated Build Cost**: **€360** (robot only) or **€460** (with tools)

**Build Time**: 8-12 weeks (3D printing, assembly, programming)

---

*Bill of Materials verified and updated: January 11, 2026*
*Project: Open Duck Mini v2 with Custom 2-DOF Robotic Arms*
*Compiled by: Claude Code (Sonnet 4.5)*

**Need help?** Check the main project documentation or ask in robotics communities:
- r/robotics subreddit
- Open Duck GitHub discussions
- Arduino/Raspberry Pi forums
