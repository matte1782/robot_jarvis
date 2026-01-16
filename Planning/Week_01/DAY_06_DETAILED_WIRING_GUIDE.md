# Day 6 - Guida Dettagliata Cablaggio PCA9685
## 16 Gennaio 2026

---

## 🎯 OBIETTIVO TASK 1
Collegare **UN SOLO** PCA9685 al Raspberry Pi 4 per test I2C.

**Perché solo uno?**
- Per Day 6 testing basta 1 PCA9685
- Il secondo lo useremo in Week 02 per 16+ canali
- Più semplice debuggare con un solo device

---

## 📦 COMPONENTI ESATTI (da Order Tracking)

### 1. Raspberry Pi 4 Model B (4GB)
- **Ordine:** #406-6313983-4881969
- **Consegnato:** 14 gennaio 2026
- **Prezzo:** €76.60
- **Identificazione:** Board verde con logo Raspberry Pi
- **GPIO Header:** 40 pin (2 file da 20)

### 2. PCA9685 PWM Controller (Prendi UNO dei due)
- **Marca:** TECNOIOT
- **Quantità ricevuta:** 2 pezzi
- **Ordine:** #406-5517512-1738718
- **Consegnato:** 16 gennaio 2026
- **Prezzo:** €10.09 (per 2pcs)
- **Identificazione:**
  - Board blu/viola scura
  - Chip grande quadrato (PCA9685)
  - 2 file di pin header (16 canali PWM)
  - 4 pin per I2C (VCC, GND, SDA, SCL)
  - Connettori servo a 3 pin (non li usiamo oggi)

### 3. Cavi Dupont Femmina-Femmina
- **Marca:** ELEGOO
- **Quantità:** 120pcs kit
- **Ordine:** #406-5517512-1738718
- **Consegnato:** 14 gennaio 2026
- **Prezzo:** €8.99
- **Identificazione:**
  - Cavi multicolore con connettori neri alle estremità
  - Lunghezza: 20cm circa
  - **Servono 4 cavi:** Rosso, Nero, Blu (o Verde), Giallo (o Arancione)

### 4. Alimentatore USB-C Raspberry Pi
- **Marca:** RASPBERRY Official
- **Modello:** KSA-15E-051300HE
- **Ordine:** #406-5517512-1738718
- **Consegnato:** 16 gennaio 2026
- **Spec:** 5.1V 3A
- **Prezzo:** €13.25
- **Identificazione:** Alimentatore bianco con logo Raspberry Pi, cavo USB-C

---

## 🔍 IDENTIFICAZIONE VISIVA COMPONENTI

### PCA9685 Board Layout (Vista Dall'Alto)

```
┌─────────────────────────────────────────────────────┐
│  TECNOIOT PCA9685 16-Channel PWM Servo Driver       │
│                                                      │
│  I2C Connection (4 pin):                            │
│  ┌──────────────────┐                               │
│  │ VCC  GND SDA SCL │ ← QUESTI pin vanno al Pi     │
│  └──────────────────┘                               │
│                                                      │
│  ┌──────────────┐  ← Chip principale PCA9685       │
│  │  PCA9685     │                                   │
│  │   CHIP       │                                   │
│  └──────────────┘                                   │
│                                                      │
│  Servo Channels (NON usare oggi):                   │
│  [0] [1] [2] [3] ... [15]                          │
│  ┆┆┆ ┆┆┆ ┆┆┆ ┆┆┆       ┆┆┆  ← 3 pin per canale    │
│                                                      │
│  V+ GND (Power, NON collegare oggi)                │
│  ┌────┐                                             │
│  │ V+ │  ← NON TOCCARE (servo power rail)          │
│  │GND │  ← NON TOCCARE                             │
│  └────┘                                             │
└─────────────────────────────────────────────────────┘
```

### Raspberry Pi 4 GPIO Header (Vista Dall'Alto)

```
         USB Ports
            ↓↓
    ┌──────────────────────┐
    │   Raspberry Pi 4     │
    │                      │
    │  GPIO Header (40 pin)│
    │  ┌──────────────┐    │
    │  │1  3.3V  [●]  │ ←──┼── Pin 1: 3.3V (ROSSO)
    │  │2  5V    [●]  │    │
    │  │3  GPIO2 [●]  │ ←──┼── Pin 3: SDA (BLU)
    │  │4  5V    [●]  │    │
    │  │5  GPIO3 [●]  │ ←──┼── Pin 5: SCL (GIALLO)
    │  │6  GND   [●]  │ ←──┼── Pin 6: GND (NERO)
    │  │7  GPIO4 [●]  │    │
    │  │8  GPIO14[●]  │    │
    │  │9  GND   [●]  │    │
    │  │10 GPIO15[●]  │    │
    │  │...          │    │
    │  └──────────────┘    │
    │                      │
    │  [USB-C Power]       │
    └──────────────────────┘
```

---

## 🔌 CABLAGGIO STEP-BY-STEP

### ⚠️ FASE PREPARATORIA (OBBLIGATORIA!)

#### Checkpoint 1: Raspberry Pi SPENTO
```
[ ] Raspberry Pi completamente spento
[ ] USB-C power supply SCOLLEGATO
[ ] Nessun LED acceso sul Pi
```

**Perché?** Collegare componenti con il Pi acceso può causare danni!

#### Checkpoint 2: Workspace Preparato
```
[ ] Superficie non conduttiva (tavolo in legno/plastica, NO metallo)
[ ] Luce adeguata per vedere i pin
[ ] Componenti identificati e pronti:
    [ ] Raspberry Pi 4
    [ ] 1x PCA9685 (ne hai 2, prendi uno qualsiasi)
    [ ] 4x cavi Dupont F-F (Rosso, Nero, Blu, Giallo)
    [ ] Alimentatore USB-C
```

---

### 📍 STEP 1: Preparazione Cavi

**Trova questi 4 cavi dal kit ELEGOO 120pcs:**

1. **Cavo ROSSO** (Femmina-Femmina, 20cm)
   - Funzione: Alimentazione 3.3V
   - Da: PCA9685 VCC → A: Pi Pin 1

2. **Cavo NERO** (Femmina-Femmina, 20cm)
   - Funzione: Ground
   - Da: PCA9685 GND → A: Pi Pin 6

3. **Cavo BLU o VERDE** (Femmina-Femmina, 20cm)
   - Funzione: I2C Data (SDA)
   - Da: PCA9685 SDA → A: Pi Pin 3

4. **Cavo GIALLO o ARANCIONE** (Femmina-Femmina, 20cm)
   - Funzione: I2C Clock (SCL)
   - Da: PCA9685 SCL → A: Pi Pin 5

**Se non hai i colori giusti:**
- Usa 4 cavi qualsiasi
- Metti un pezzetto di scotch colorato o etichetta su ogni cavo
- IMPORTANTE: Annota quale cavo è quale!

```
Checklist Cavi:
[ ] 4 cavi Dupont femmina-femmina pronti
[ ] Colori identificati (o etichettati)
[ ] Nessun cavo danneggiato (fili esposti)
```

---

### 📍 STEP 2: Collegamento I2C (PCA9685 → Raspberry Pi)

**RICORDA: Raspberry Pi DEVE essere SPENTO!**

#### Connessione 1: VCC (Alimentazione)
```
PCA9685 Board          Cavo         Raspberry Pi
┌─────────┐                        ┌────────────┐
│  VCC    │◄────[ROSSO]────────────│ Pin 1 (3.3V)
└─────────┘                        └────────────┘
```

**Procedura:**
1. Prendi il cavo ROSSO
2. Collega un'estremità al pin **VCC** del PCA9685 (primo pin del gruppo I2C)
3. Collega l'altra estremità al **Pin 1** del Raspberry Pi (3.3V)
4. Verifica che il connettore sia inserito completamente (nessun metallo visibile)

```
[ ] Cavo ROSSO collegato: PCA9685 VCC → Pi Pin 1
```

#### Connessione 2: GND (Ground)
```
PCA9685 Board          Cavo         Raspberry Pi
┌─────────┐                        ┌────────────┐
│  GND    │◄────[NERO]─────────────│ Pin 6 (GND)
└─────────┘                        └────────────┘
```

**Procedura:**
1. Prendi il cavo NERO
2. Collega un'estremità al pin **GND** del PCA9685 (secondo pin del gruppo I2C)
3. Collega l'altra estremità al **Pin 6** del Raspberry Pi (GND)
4. Verifica inserimento completo

```
[ ] Cavo NERO collegato: PCA9685 GND → Pi Pin 6
```

#### Connessione 3: SDA (I2C Data)
```
PCA9685 Board          Cavo         Raspberry Pi
┌─────────┐                        ┌────────────┐
│  SDA    │◄────[BLU]──────────────│ Pin 3 (GPIO2)
└─────────┘                        └────────────┘
```

**Procedura:**
1. Prendi il cavo BLU (o VERDE)
2. Collega un'estremità al pin **SDA** del PCA9685 (terzo pin del gruppo I2C)
3. Collega l'altra estremità al **Pin 3** del Raspberry Pi (GPIO2/SDA)
4. Verifica inserimento completo

```
[ ] Cavo BLU collegato: PCA9685 SDA → Pi Pin 3
```

#### Connessione 4: SCL (I2C Clock)
```
PCA9685 Board          Cavo         Raspberry Pi
┌─────────┐                        ┌────────────┐
│  SCL    │◄────[GIALLO]───────────│ Pin 5 (GPIO3)
└─────────┘                        └────────────┘
```

**Procedura:**
1. Prendi il cavo GIALLO (o ARANCIONE)
2. Collega un'estremità al pin **SCL** del PCA9685 (quarto pin del gruppo I2C)
3. Collega l'altra estremità al **Pin 5** del Raspberry Pi (GPIO3/SCL)
4. Verifica inserimento completo

```
[ ] Cavo GIALLO collegato: PCA9685 SCL → Pi Pin 5
```

---

### 📍 STEP 3: VERIFICA COMPLETA PRE-ACCENSIONE

**Questo step è CRITICO! Non saltarlo!**

#### Checklist Visiva:
```
[ ] 4 cavi collegati (VCC, GND, SDA, SCL)
[ ] Tutti i connettori inseriti completamente
[ ] Nessun filo esposto che tocca altri pin
[ ] Nessun cavo allentato
[ ] V+ e GND (servo power) del PCA9685 VUOTI
[ ] Raspberry Pi ancora SPENTO
```

#### Verifica Pin per Pin:

**Sul PCA9685:**
```
[ ] VCC  ← Cavo ROSSO collegato
[ ] GND  ← Cavo NERO collegato
[ ] SDA  ← Cavo BLU collegato
[ ] SCL  ← Cavo GIALLO collegato
[ ] V+   ← VUOTO (nessun cavo)
[ ] GND  ← VUOTO (nessun cavo)
```

**Sul Raspberry Pi:**
```
[ ] Pin 1 (3.3V)   ← Cavo ROSSO collegato
[ ] Pin 3 (GPIO2)  ← Cavo BLU collegato
[ ] Pin 5 (GPIO3)  ← Cavo GIALLO collegato
[ ] Pin 6 (GND)    ← Cavo NERO collegato
```

#### Verifica Sicurezza:
```
[ ] NO cortocircuiti (cavi che si toccano)
[ ] NO pin piegati sul PCA9685 o Pi
[ ] Workspace pulito (no oggetti metallici vicino)
```

---

### 📍 STEP 4: ACCENSIONE SISTEMA

**Procedura Power-On:**

1. **Doppia verifica finale**
   ```
   [ ] Tutti i 4 cavi correttamente collegati
   [ ] Nessun errore visibile
   [ ] Pi in posizione stabile (non pendente)
   ```

2. **Collega alimentazione**
   ```
   [ ] Prendi l'alimentatore USB-C (RASPBERRY KSA-15E-051300HE)
   [ ] Collega il connettore USB-C al Raspberry Pi
   [ ] Inserisci la spina nella presa elettrica
   ```

3. **Osserva il boot**
   ```
   [ ] LED rosso Pi si accende (power)
   [ ] LED verde Pi lampeggia (attività SD card)
   [ ] Pi boota normalmente (20-30 secondi)
   [ ] PCA9685: Piccolo LED potrebbe accendersi (se presente)
   ```

**⚠️ SEGNALI DI PERICOLO - SPEGNI IMMEDIATAMENTE SE:**
- ⚠️ Fumo o odore strano
- ⚠️ Componenti che si scaldano eccessivamente
- ⚠️ LED che lampeggiano in modo anomalo
- ⚠️ Rumori strani (sibili, click)

**Se tutto OK:**
```
[ ] Pi booted (LED verde smette di lampeggiare)
[ ] Nessun odore/fumo
[ ] Sistema stabile
[ ] Pronto per test I2C
```

---

## 🎯 STATO FINALE ATTESO

### Vista Completa Sistema:
```
    ┌─────────────────┐
    │  PCA9685 Board  │
    │                 │
    │  VCC GND SDA SCL│
    │   │   │   │   │ │
    └───┼───┼───┼───┼─┘
        │   │   │   │
     [ROSSO│BLU│GIALLO
        │ [NERO] │
        │   │   │   │
    ┌───┼───┼───┼───┼──────────┐
    │   1   3   5   6          │
    │ [●] [●] [●] [●]  GPIO    │
    │                          │
    │   Raspberry Pi 4         │
    │                          │
    │   [USB-C Power] ●────────┼─── Alimentatore
    └──────────────────────────┘
```

### Checklist Finale Successo:
```
✅ PCA9685 collegato al Pi via I2C
✅ 4 cavi: VCC, GND, SDA, SCL
✅ Pi booted correttamente
✅ Nessun problema di sicurezza
✅ Sistema pronto per sudo i2cdetect -y 1
```

---

## 🚨 TROUBLESHOOTING

### Problema: Pi non si accende
**Causa possibile:** Cortocircuito
**Soluzione:**
1. Scollega SUBITO l'alimentatore
2. Verifica che VCC e GND non si tocchino
3. Controlla che nessun cavo sia nel pin sbagliato

### Problema: PCA9685 no LED
**Causa possibile:** Normale (alcuni board non hanno LED)
**Soluzione:** Procedi comunque con test I2C

### Problema: Dubbio su un pin
**Soluzione:**
1. SPEGNI il Pi
2. Verifica con lo schema pinout
3. Conta i pin dall'angolo (Pin 1 è sempre 3.3V)

---

## ✅ TASK 1 COMPLETATA!

**Quando confermi che:**
- ✅ Tutti i 4 cavi collegati correttamente
- ✅ Pi acceso e funzionante
- ✅ Nessun problema di sicurezza

**Sei pronto per TASK 2: Test I2C Detection!**

---

**Creato:** 16 Gennaio 2026
**Per:** Day 6 Hardware Testing
**Versione:** 1.0 Ultra-Detailed
