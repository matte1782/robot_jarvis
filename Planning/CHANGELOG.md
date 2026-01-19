# Planning CHANGELOG - OpenDuck Mini V3
## Cronologia delle Modifiche al Piano di Sviluppo

**Progetto:** OpenDuck Mini V3
**Inizio:** 15 Gennaio 2026
**Scopo:** Tracciare tutte le modifiche significative al piano dovute a ritardi hardware, ripianificazioni e decisioni strategiche.

---

## Legenda

- **[DELAY]** - Ritardo hardware/spedizione
- **[REPLAN]** - Ripianificazione delle attività
- **[PIVOT]** - Cambio strategico significativo
- **[SCOPE]** - Modifica dello scope
- **[HW-STATUS]** - Aggiornamento stato hardware

---

## Week 01 (15-21 Gennaio 2026)

### 15 Gennaio 2026 - Day 1

**[DELAY] microSD Card**
- Previsto: 15-17 Gennaio
- Reale: 19-22 Gennaio (Amazon)
- Impatto: Impossibile configurare Pi senza microSD
- Risoluzione: Acquisto locale il giorno dopo

**[REPLAN] Piano Day 1**
- Originale: Hardware testing + software
- Modificato: Solo software (firmware repo, driver PCA9685)
- Motivo: microSD non disponibile

**[SCOPE] Riduzione Scope Week 01**
- Rimosso: Leg kinematics, gaits, balance controller
- Rimosso: Voltage monitoring (richiede ADS1115)
- Target ridotto: 70-80% → 55-60%
- Motivo: Hostile review ha identificato sovraccarico timeline (50h → 32h disponibili)

### 16-17 Gennaio 2026 - Days 2-3

**[HW-STATUS] Consegne Massive**
- Ricevuti: Raspberry Pi 4, PCA9685 x2, MG90S x5, UBEC x2, LED rings x3, INMP441 x6, MAX98357A, BMS x5
- Totale: ~€530 di componenti consegnati
- Ancora mancante: Batterie 18650, BNO085 IMU

**[DELAY] Batterie 18650**
- Status: Non ordinate (ricerca negozi vape)
- Impatto: Impossibile testare servo/LED con potenza reale
- Risoluzione: Continuare sviluppo software-only

### 18-19 Gennaio 2026 - Days 6-7

**[HW-STATUS] LED Ring Validation**
- GPIO 18 conflict identificato (LED Ring 1 vs I2S Audio)
- Workaround: Script disable_i2s_audio.sh
- LED Ring 1: GPIO 18 (Pin 12) - VALIDATO
- LED Ring 2: GPIO 13 (Pin 33) - VALIDATO
- Entrambi i ring funzionanti quando I2S disabilitato

**[PIVOT] Weekend Work**
- Originale: Hardware integration
- Modificato: Software-only (Option B)
- Motivo: Batterie ancora non arrivate

---

## Week 02 (15-19 Gennaio 2026) - Days 8-14

### Piano Originale vs Reale

| Day | Piano Originale | Piano Reale | Motivo |
|-----|----------------|-------------|--------|
| Day 8 | BNO085 + Batterie | Animation timing (software) | Batterie non arrivate |
| Day 9 | Servo testing | Easing + LED patterns | Batterie non arrivate |
| Day 10 | Full system test | Emotion system | Batterie non arrivate |
| Day 11-14 | Integration | Software-only development | Batterie non arrivate |

**[SCOPE] Week 02 Software-Only**
- Tutto lo sviluppo hardware rinviato a Week 03
- Focus: Animation system, emotion engine, LED patterns
- Risultato: 50,501 LOC, 1,377 tests, 95% achievement

**[HW-STATUS] BNO085 IMU**
- Ordine: Adafruit BNO085 (STEMMA QT/Qwiic, 4754)
- Status: IN TRANSITO
- ETA: Day 16 (21 Gennaio 2026)
- Note: NON ANCORA VALIDATO - test previsto Day 16

**[DELAY] Batterie - Ancora Mancanti**
- Status: Ordinate da NKON
- ETA: Week 03
- Impatto: Tutti i test servo/LED con potenza reale rinviati

---

## Week 03 (20-26 Gennaio 2026) - Days 15-21

### 20 Gennaio 2026 - Day 15

**[REPLAN] Day 15**
- Piano originale: Battery power-up, system test
- Piano reale: INMP441 audio driver (software-only)
- Motivo: Batterie ancora non arrivate, BNO085 arriva domani

**[PIVOT] Audio Driver Anticipato**
- Originale: Day 18 (Audio In)
- Reale: Day 15 (software driver completo)
- Deliverable: 2,599 LOC, 147 tests, 95/100 hostile review
- Note: Test hardware su Pi pianificato per Day 16

**[HW-STATUS] Componenti Week 03**

| Componente | Status | ETA | Note |
|------------|--------|-----|------|
| 18650 Batterie | IN TRANSITO | Week 03 | CRITICO per servo/LED |
| BNO085 IMU | IN TRANSITO | Day 16 (21 Gen) | Per test orientamento |
| AI Camera | IN TRANSITO | Week 03 | Per visione |
| FE-URT-1 | IN TRANSITO | Week 03 | Controller servo |

### 21 Gennaio 2026 - Day 16 (Pianificato)

**[REPLAN] Day 16 Priorità**
1. **PRIMA:** Test hardware INMP441 su Pi (USB power)
2. **SECONDA:** Test BNO085 IMU (se arrivato)
3. Software: Continuare sviluppo se hardware non disponibile

**Wiring INMP441 per test:**
```
INMP441 → Pi Zero 2W (I2S)
VDD     → Pin 1 (3.3V)
GND     → Pin 6 (GND)
SCK     → Pin 12 (GPIO 18)
WS      → Pin 35 (GPIO 19)
SD      → Pin 38 (GPIO 20)
```

**Note:** LED Ring 1 NON connesso durante test audio (conflitto GPIO 18)

---

## Riepilogo Ritardi Hardware

### Componenti Critici - Status Attuale (20 Gen 2026)

| Componente | Ordinato | ETA Originale | ETA Reale | Impatto |
|------------|----------|---------------|-----------|---------|
| microSD 32GB | Amazon | 15-17 Gen | 19-22 Gen | Delay Day 1-2 |
| Batterie 18650 | NKON | Week 01 | Week 03 | CRITICO - No servo/LED test |
| BNO085 IMU | Adafruit | Week 02 | Day 16 | IMU test delayed |
| AI Camera | - | Week 03 | Week 03 | On track |
| FE-URT-1 | AliExpress | ~25 Gen | ~25 Gen | On track |

### Impatto Cumulativo dei Ritardi

- **Week 01:** -15% efficienza (microSD delay)
- **Week 02:** -20% hardware testing (batterie mancanti)
- **Week 03:** In corso - dipende da arrivo batterie

### Strategia di Mitigazione

1. **Software-First:** Sviluppare tutto il software possibile senza hardware
2. **Mock Testing:** 100% test coverage con hardware mockato
3. **USB Power:** Testare componenti low-power (mic, IMU) con alimentazione USB
4. **Deferred Integration:** Test integrazione completa quando batterie arrivano

---

## Decisioni Chiave

### 1. Option B - Software Only (Weekend, Day 15)
- **Decisione:** Continuare sviluppo software senza batterie
- **Pro:** Nessun tempo perso, codebase avanza
- **Contro:** Test hardware rinviati
- **Risultato:** Week 02 completata al 95%

### 2. GPIO 18 Conflict Resolution
- **Problema:** LED Ring 1 e I2S Audio condividono GPIO 18
- **Soluzione Temporanea:** Disabilitare I2S durante test LED
- **Soluzione Permanente (Pianificata):** Spostare LED Ring 1 a GPIO 10

### 3. Audio Driver Anticipato
- **Decisione:** Sviluppare INMP441 driver in Day 15 invece che Day 18
- **Motivo:** Batterie non arrivate, audio driver non richiede potenza
- **Risultato:** 2,599 LOC, 147 tests, pronto per test hardware Day 16

---

**Ultimo Aggiornamento:** 20 Gennaio 2026, 23:00
**Prossimo Milestone:** Day 16 - BNO085 arrivo + INMP441 Pi test
