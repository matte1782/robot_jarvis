# JARVIS Project - EU/Italy Hardware BOM (Bill of Materials)

**Last Updated:** January 2025
**Research by:** Agent A - EU Hardware Scout
**Currency:** EUR (Euro)

---

## Executive Summary

This document provides a complete Bill of Materials for building a desk AI assistant in EU/Italy, organized in two tiers:
- **Balanced Tier:** EUR 300-600 total
- **Pro Tier:** EUR 600-1200 total

---

## 1. COMPUTE OPTIONS

### Understanding LLM Hardware Requirements

Before selecting hardware, it's important to understand what local LLM inference requires:

| Model Size | Minimum RAM | Recommended VRAM | Notes |
|------------|-------------|------------------|-------|
| 7B models  | 16GB        | 8GB              | Entry-level, good for basic tasks |
| 13B models | 32GB        | 12GB             | Better quality, reasonable speed |
| 32B models | 64GB        | 16-24GB          | High quality, slower on CPU |
| 70B models | 128GB       | 48GB+            | Requires high-end hardware |

**Key insight:** Memory bandwidth is the primary bottleneck for LLM inference, not raw compute power.

---

### BALANCED TIER: Budget Mini PCs (EUR 150-350)

These are suitable for:
- Running small models (7B quantized) on CPU
- Acting as orchestration hub with cloud API calls
- General computing tasks
- Always-on operation with low power consumption

| Item | Specs | EU Price | EU Store | Alternatives | Stock | Notes |
|------|-------|----------|----------|--------------|-------|-------|
| **GMKtec NucBox G3** | Intel N100, 8GB DDR4, 256GB SSD | EUR 116-150 | [GMKtec EU](https://de.gmktec.com) | Minisforum UN100P, Beelink EQ12 | In Stock | Best budget option, fanless available |
| **Minisforum UN100P** | Intel N100, 16GB DDR4, 512GB SSD | EUR 195-256 | [Amazon.it](https://www.amazon.it) | GMKtec G3, ASUS PN42 | In Stock | Good balance of RAM and storage |
| **ASUS ExpertCenter PN42** | Intel N100/N200, Barebone | EUR 227-280 | [Trovaprezzi.it](https://www.trovaprezzi.it) | Minisforum UN100, Beelink Mini S12 | In Stock | Enterprise grade, fanless design |
| **Beelink Mini S12** | Intel N100, 16GB DDR4, 500GB SSD | EUR 180-220 | [Amazon.it](https://www.amazon.it) | EQ12, GMKtec G3 | Variable | Good brand reputation |

**Recommended for Balanced Tier:** Minisforum UN100P (EUR 195-256) - Best RAM/storage for the price.

---

### PRO TIER: Performance Mini PCs (EUR 450-900)

These are suitable for:
- Running 7B-13B models locally at reasonable speed
- Integrated GPU (AMD Radeon 780M) for acceleration
- Future-proof with 32GB+ RAM
- Professional workloads

| Item | Specs | EU Price | EU Store | Alternatives | Stock | Notes |
|------|-------|----------|----------|--------------|-------|-------|
| **Beelink SER8** | AMD Ryzen 7 8845HS, 32GB DDR5, 1TB NVMe | EUR 600-720 | [Amazon.it](https://www.amazon.it/Beelink-SER8-8845HS-1TB-PCIe4-0/dp/B0D44K41PC) | SER7, Minisforum UM790 Pro | In Stock | Best AMD option, NPU for AI |
| **Beelink SER7** | AMD Ryzen 7 7840HS, 32GB DDR5, 1TB NVMe | EUR 550-670 | [Amazon.it](https://www.amazon.it) | SER8, UM790 Pro | Variable | Previous gen, still excellent |
| **Minisforum UM790 Pro** | AMD Ryzen 9 7940HS, 32GB DDR5, 1TB SSD | EUR 623-700 | [Amazon.it](https://www.amazon.it/MINIS-FORUM-UM790-Pro-connessione/dp/B0CJ38BT9Q), [Idealo.it](https://www.idealo.it) | UM780 XTX, Beelink SER8 | In Stock | Top AMD APU, Cold Wave 2.0 cooling |
| **Intel NUC 13 Pro** | Intel Core i5-1340P/i7-1360P, Barebone | EUR 485-690 | [Idealo.it](https://www.idealo.it), [Amazon.it](https://www.amazon.it/NUC13ANHi5-16GB-512GB-processore-preinstallato/dp/B0C1S9XFJQ) | ASUS NUC 13, Minisforum | In Stock | Thunderbolt 4 for eGPU |
| **ASUS NUC 13 Pro** | Intel Core i5/i7 13th Gen, Barebone | EUR 355-830 | [Idealo.it](https://www.idealo.it) | Intel NUC 13, Beelink | In Stock | Enterprise warranty |

**Recommended for Pro Tier:** Beelink SER8 or Minisforum UM790 Pro (EUR 600-720) - Best local LLM performance with AMD Radeon 780M iGPU.

---

## 2. MICROPHONES

### BALANCED TIER: Budget USB Microphones (EUR 25-70)

| Item | Type | EU Price | EU Store | Alternatives | Stock | Notes |
|------|------|----------|----------|--------------|-------|-------|
| **Fifine K669B** | USB Condenser | EUR 30-40 | [Amazon.it](https://www.amazon.it/FIFINE-Microfoni-Microfono-Registrazione-condensazione/dp/B07QC5W7G9) | Fifine T669, K688 | In Stock | Best budget, plug-and-play |
| **Blue Yeti Nano** | USB Condenser | EUR 66-90 | [Amazon.it](https://www.amazon.it/Microfono-Registrazione-Streaming-Condensatore-Monitoraggio/dp/B07DTTGZ7M) | Yeti X, Snowball | In Stock | Compact, great quality |
| **Fifine K669 Kit** | USB Condenser + Arm | EUR 45-55 | [Amazon.it](https://www.amazon.it/FIFINE-Microfono-Condensatore-Registrazione-Professionale/dp/B09BHJRZZB) | Standalone + arm | In Stock | All-in-one solution |

**Recommended for Balanced Tier:** Fifine K669B (EUR 30-40) or Blue Yeti Nano (EUR 66-90)

---

### PRO TIER: Quality Microphones (EUR 80-150)

| Item | Type | EU Price | EU Store | Alternatives | Stock | Notes |
|------|------|----------|----------|--------------|-------|-------|
| **RODE NT-USB Mini** | USB Condenser | EUR 90-110 | [Thomann.it](https://www.thomann.it/rode_nt_usb_mini.htm), [Amazon.it](https://www.amazon.it/Rode-Microphones-NTUSBMINI-NT-USB-Mini/dp/B084P1CXFD) | AT2020USB+, Yeti | In Stock | Studio quality, compact |
| **Blue Yeti** | USB Condenser | EUR 85-120 | [Amazon.it](https://www.amazon.it/Blue-Microphones-Yeti-Microfono-USB/dp/B002VA464S) | Yeti X, NT-USB Mini | In Stock | 4 polar patterns |
| **Samson Q2U** | USB/XLR Dynamic | EUR 70-90 | [Amazon.it](https://www.amazon.it/Samson-Q2U-Microfono-dinamico-registrazione/dp/B0876TR1ZS) | AT2100x, Shure MV7 | In Stock | Dual connectivity, upgrade path |
| **Audio-Technica ATR2500x-USB** | USB Condenser | EUR 90-120 | [Amazon.it](https://www.amazon.it/Audio-Technica-ATR2500x-USB-MICROFONO-TRASMETTERE-REGISTRAZIONI/dp/B086CV7FX8) | AT2020USB+, RODE | In Stock | 24-bit/192kHz |

**Recommended for Pro Tier:** RODE NT-USB Mini (EUR 90-110) - Best overall quality for desk use.

---

## 3. SPEAKERS

### BALANCED TIER: Budget Desktop Speakers (EUR 15-50)

| Item | Config | EU Price | EU Store | Alternatives | Stock | Notes |
|------|--------|----------|----------|--------------|-------|-------|
| **Creative Pebble** | 2.0 USB | EUR 20-25 | [Amazon.it](https://www.amazon.it/Sistema-altoparlanti-desktop-Creative-alimentazione/dp/B0791H74NT) | Pebble V2, Trust Arys | In Stock | Minimalist design |
| **Creative Pebble Plus** | 2.1 USB + Sub | EUR 35-45 | [Amazon.it](https://www.amazon.it) | Pebble V3, Logitech Z200 | In Stock | Good bass with subwoofer |
| **Trust Arys** | 2.0 Soundbar | EUR 15-25 | [Amazon.it](https://www.amazon.it) | Trust Remo, GXT 620 | In Stock | Compact soundbar |
| **Amazon Basics Speakers** | 2.0 USB | EUR 15-20 | [Amazon.it](https://www.amazon.it) | Trust, Creative | In Stock | Basic but functional |

**Recommended for Balanced Tier:** Creative Pebble Plus (EUR 35-45) - Good sound with subwoofer.

---

### PRO TIER: Quality Desktop Speakers (EUR 70-150)

| Item | Config | EU Price | EU Store | Alternatives | Stock | Notes |
|------|--------|----------|----------|--------------|-------|-------|
| **Edifier R1280T** | 2.0 Powered | EUR 89-100 | [Amazon.it](https://www.amazon.it/Edifier-R1280T-Sistemi-altoparlanti-marrone/dp/B00GBN50SC) | R1280DB, R1380DB | In Stock | Studio monitor quality |
| **Creative Pebble Pro** | 2.0 USB-C + BT | EUR 55-70 | [Amazon.it](https://www.amazon.it/CREATIVE-Altoparlanti-Bluetooth-illuminazione-personalizzabile/dp/B0BD89JTRK) | Pebble V3, X Plus | In Stock | RGB, Bluetooth 5.3 |
| **Creative Pebble V3** | 2.0 USB-C + BT | EUR 40-50 | [Amazon.it](https://www.amazon.it/CREATIVE-Pebble-Altoparlante-convertitore-USB/dp/B09HGXDLX2) | Pebble Pro, V2 | In Stock | Clear Dialog tech |
| **Edifier R1280DB** | 2.0 Powered + BT | EUR 120-150 | [Amazon.it](https://www.amazon.it/Edifier-R1280DB-Altoparlanti-Notebook-Smartphone/dp/B01NCTGH9M) | R1280T, R1380DB | In Stock | Bluetooth + optical |

**Recommended for Pro Tier:** Edifier R1280T (EUR 89-100) - Best audio quality for the price.

---

## 4. WEBCAM (Optional - Future Robot Integration)

| Item | Resolution | EU Price | EU Store | Alternatives | Stock | Notes |
|------|------------|----------|----------|--------------|-------|-------|
| **Logitech C920 HD Pro** | 1080p/30fps | EUR 53-80 | [Amazon.it](https://www.amazon.it/Logitech-HD-Pro-Webcam-C920/dp/B006H967FA), [Idealo.it](https://www.idealo.it) | C922, C920S | In Stock | Industry standard |
| **Logitech C920S HD Pro** | 1080p/30fps | EUR 64-80 | [Amazon.it](https://www.amazon.it/Logitech-Videochiamate-Registrazione-Copriobiettivo-Acquisizione/dp/B07MM4V7NR) | C920, C922 | In Stock | With privacy shutter |
| **Logitech C922 Pro Stream** | 1080p/60fps | EUR 80-100 | [Amazon.it](https://www.amazon.it) | Brio, StreamCam | In Stock | Better for streaming |

**Recommended:** Logitech C920S HD Pro (EUR 64-80) - Best value with privacy shutter.

---

## 5. ACCESSORIES

### Microphone Boom Arms

| Item | Load Capacity | EU Price | EU Store | Alternatives | Stock | Notes |
|------|---------------|----------|----------|--------------|-------|-------|
| **Aokeo AK-35** | 1.8kg | EUR 15-25 | [Amazon.it](https://www.amazon.it/Microfono-Aokeo-Sospensione-Supporto-Snowball/dp/B01MZ99Y67) | TONOR, Amazon Basics | In Stock | Budget option |
| **Amazon Basics Boom Arm** | 1.5kg | EUR 25-35 | [Amazon.it](https://www.amazon.it/Amazon-Basics-Supporto-microfono-antipop/dp/B0B1Q3BKNC) | Aokeo, TONOR | In Stock | Includes pop filter |
| **TONOR T20LP** | 1.5kg | EUR 30-40 | [Amazon.it](https://www.amazon.it) | Elgato Wave Arm | In Stock | Low profile design |
| **Elgato Wave Mic Arm LP** | 2kg | EUR 80-100 | [Amazon.it](https://www.amazon.it/Elgato-Wave-Mic-Arm-Profile/dp/B097376LKF) | Shure, RODE PSA1 | In Stock | Premium, cable management |

---

### USB Hubs (Powered)

| Item | Ports | EU Price | EU Store | Alternatives | Stock | Notes |
|------|-------|----------|----------|--------------|-------|-------|
| **Anker 7-in-1 USB-C Hub** | 7 ports | EUR 24-30 | [Amazon.it](https://www.amazon.it) | UGREEN, Sabrent | In Stock | Includes HDMI |
| **RSHTECH USB 3.0 Hub** | 7 ports | EUR 34-37 | [Amazon.it](https://www.amazon.it) | DIGITUS, Anker | In Stock | Individual switches |
| **DIGITUS USB 3.0 Hub** | 7 ports | EUR 34-40 | [Amazon.it](https://www.amazon.it) | RSHTECH, Anker | In Stock | Aluminum, powered |

**Recommended:** RSHTECH or DIGITUS 7-port (EUR 34-40) - Individual switches are useful.

---

### UPS (Uninterruptible Power Supply)

| Item | Capacity | EU Price | EU Store | Alternatives | Stock | Notes |
|------|----------|----------|----------|--------------|-------|-------|
| **VulTech UPS800VA-LITE** | 800VA/440W | EUR 49-55 | [Amazon.it](https://www.amazon.it) | NJOY Keen 800 | In Stock | Best budget |
| **NJOY Keen 800** | 800VA/480W | EUR 55-62 | [Amazon.it](https://www.amazon.it) | Trust Maxxon, Tecnoware | In Stock | 3-year warranty |
| **Green Cell UPS 800VA** | 800VA/480W | EUR 60-75 | [Amazon.it](https://www.amazon.it/Green-Cell-UPS-600VA-800VA-Approximated/dp/B07NS2DPLW) | NJOY, APC | In Stock | LCD display |
| **Tecnoware Era Plus 800** | 800VA/560W | EUR 65-80 | [Amazon.it](https://www.amazon.it) | APC, Eaton | In Stock | Higher wattage |

**Recommended:** NJOY Keen 800 (EUR 55-62) - Good balance of price and reliability.

---

### Optional: USB DAC (for better audio)

| Item | Features | EU Price | EU Store | Alternatives | Stock | Notes |
|------|----------|----------|----------|--------------|-------|-------|
| **FiiO BTR13** | BT/USB DAC | EUR 55-70 | [Amazon.it](https://www.amazon.it) | BTR7, E10K | In Stock | Portable option |
| **Topping DX3 Pro+** | DAC + Amp | EUR 199 | [Amazon.it](https://www.amazon.it) | E30 II, FiiO K5 Pro | In Stock | Desktop, Bluetooth |
| **Topping E30 II** | DAC only | EUR 149 | [Amazon.it](https://www.amazon.it) | D10s, SMSL | In Stock | Pure DAC |

---

## COMPLETE BUILD CONFIGURATIONS

### BALANCED BUILD (EUR 350-500)

| Component | Selected Item | Price |
|-----------|---------------|-------|
| Compute | Minisforum UN100P (16GB/512GB) | EUR 220 |
| Microphone | Fifine K669B | EUR 35 |
| Speakers | Creative Pebble Plus | EUR 40 |
| USB Hub | RSHTECH 7-port | EUR 35 |
| Mic Arm | Aokeo AK-35 | EUR 20 |
| **TOTAL** | | **EUR 350** |

**Optional additions:**
- UPS NJOY Keen 800: +EUR 60
- Webcam C920S: +EUR 70
- **With all options: EUR 480**

---

### PRO BUILD (EUR 750-1000)

| Component | Selected Item | Price |
|-----------|---------------|-------|
| Compute | Beelink SER8 (32GB/1TB) | EUR 650 |
| Microphone | RODE NT-USB Mini | EUR 100 |
| Speakers | Edifier R1280T | EUR 95 |
| USB Hub | DIGITUS 7-port | EUR 38 |
| Mic Arm | TONOR T20LP | EUR 35 |
| UPS | NJOY Keen 800 | EUR 60 |
| **TOTAL** | | **EUR 978** |

**Optional additions:**
- Webcam C922 Pro: +EUR 90
- Elgato Wave Arm: +EUR 50 (instead of TONOR)
- **With all options: EUR 1118**

---

## SUPPLY CHAIN ANALYSIS

### Risk Assessment

| Component | Risk Level | Notes |
|-----------|------------|-------|
| Mini PCs (Beelink, Minisforum) | LOW | Multiple sellers, good EU availability |
| Intel N100 devices | LOW | Widely available, multiple brands |
| AMD Ryzen devices | MEDIUM | Some models may have limited stock |
| RODE microphones | LOW | EU distribution center in Germany |
| Fifine microphones | LOW | Available on Amazon with Prime |
| Logitech webcams | LOW | Well-established EU distribution |
| UPS units | LOW | Multiple brands, local availability |

### Lead Times (Italy)

| Vendor | Typical Delivery |
|--------|------------------|
| Amazon.it (Prime) | 1-2 days |
| Amazon.it (Non-Prime) | 3-5 days |
| Thomann.it | 2-4 days |
| Official brand stores (Minisforum, Beelink) | 5-10 days |
| Idealo.it partners | Varies (2-7 days) |

---

## RECOMMENDED PURCHASE ORDER

### Phase 1: Core System (Week 1)
1. **Mini PC** - Order first, longest shipping from some vendors
2. **USB Hub** - Needed for connecting peripherals

### Phase 2: Audio (Week 1-2)
3. **Microphone** - Essential for voice input
4. **Speakers** - Essential for voice output
5. **Mic Arm** (optional) - Better positioning

### Phase 3: Stability & Future (Week 2-3)
6. **UPS** - Protects against power issues
7. **Webcam** - For future robot vision integration

---

## SOURCES

### Price Comparison Sites
- [Idealo.it](https://www.idealo.it) - Best for price comparison
- [Trovaprezzi.it](https://www.trovaprezzi.it) - Italian price aggregator

### Retailers
- [Amazon.it](https://www.amazon.it) - Prime delivery, easy returns
- [Amazon.de](https://www.amazon.de) - Often cheaper, ships to Italy
- [Thomann.it](https://www.thomann.it) - Best for audio equipment

### Official Stores
- [Beelink Official](https://www.bee-link.com)
- [Minisforum EU](https://store.minisforum.de)
- [GMKtec EU](https://de.gmktec.com)

### Research Sources
- [NotebookCheck](https://www.notebookcheck.net) - Mini PC reviews
- [HDBlog.it](https://www.hdblog.it) - Italian tech news
- [Local LLM Hardware Guide](https://www.localai.computer/learn/llm-hardware-guide)
- [PC Build Advisor](https://www.pcbuildadvisor.com/best-mini-pcs-for-ai-server-the-ultimate-server-mini-pcs-for-2026-new-models-included/)

---

## NOTES FOR FUTURE UPGRADES

### External GPU Options (for serious LLM work)
If you need more GPU power for larger models, consider:
- **Thunderbolt 4 eGPU enclosure** + NVIDIA RTX 3060/4060
- Intel NUC 13 Pro supports Thunderbolt 4 for this purpose
- Budget: EUR 300-500 for enclosure + EUR 300-400 for GPU

### RAM Upgrades
- Beelink SER8 supports up to 64GB DDR5
- Minisforum UM790 Pro supports up to 64GB DDR5
- Consider 64GB if running 13B+ models locally

### Storage Upgrades
- Both recommended Pro tier PCs support 2x NVMe drives
- Consider 2TB+ for model storage (7B models are 4-8GB, 70B models are 40-70GB)

---

*Document compiled January 2025. Prices may vary. Always verify current prices before purchasing.*
