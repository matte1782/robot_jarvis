# Pin Assignment - Raspberry Pi Zero 2W

## GPIO Header Pinout

```
                    3.3V [1]  [2]  5V
           I2C SDA GPIO2 [3]  [4]  5V
           I2C SCL GPIO3 [5]  [6]  GND
                   GPIO4 [7]  [8]  GPIO14 UART TX
                     GND [9]  [10] GPIO15 UART RX
                  GPIO17 [11] [12] GPIO18 I2S BCLK
                  GPIO27 [13] [14] GND
                  GPIO22 [15] [16] GPIO23
                    3.3V [17] [18] GPIO24
          SPI MOSI GPIO10 [19] [20] GND
          SPI MISO GPIO9  [21] [22] GPIO25
          SPI SCLK GPIO11 [23] [24] GPIO8  SPI CE0
                     GND [25] [26] GPIO7  SPI CE1
         I2C EEPROM GPIO0 [27] [28] GPIO1  I2C EEPROM
                   GPIO5 [29] [30] GND
                   GPIO6 [31] [32] GPIO12
                  GPIO13 [33] [34] GND
          I2S LRCLK GPIO19 [35] [36] GPIO16
                  GPIO26 [37] [38] GPIO20 I2S DIN
                     GND [39] [40] GPIO21 I2S DOUT
```

## Pin Assignments for OpenDuck Mini V3

| Function | GPIO | Pin # | Notes |
|----------|------|-------|-------|
| **Power** |
| 5V Input | - | 2, 4 | From UBEC |
| 3.3V Output | - | 1, 17 | For sensors |
| GND | - | 6, 9, 14, 20, 25, 30, 34, 39 | Common ground |
| **Servo Bus (USB-UART)** |
| USB-UART Controller | USB | USB Port | FE-URT-1 via USB |
| **I2C Bus (Sensors)** |
| I2C SDA | GPIO2 | 3 | BNO085 IMU |
| I2C SCL | GPIO3 | 5 | BNO085 IMU |
| **I2S Audio** |
| I2S BCLK | GPIO18 | 12 | Audio bit clock |
| I2S LRCLK | GPIO19 | 35 | Audio L/R clock |
| I2S DIN | GPIO20 | 38 | Mic input (INMP441) |
| I2S DOUT | GPIO21 | 40 | Speaker output (MAX98357A) |
| **Ultrasonic Sensors** |
| HC-SR04 #1 Trig | GPIO17 | 11 | Front sensor |
| HC-SR04 #1 Echo | GPIO27 | 13 | Front sensor (via level shifter) |
| HC-SR04 #2 Trig | GPIO22 | 15 | Left sensor |
| HC-SR04 #2 Echo | GPIO23 | 16 | Left sensor (via level shifter) |
| HC-SR04 #3 Trig | GPIO24 | 18 | Right sensor |
| HC-SR04 #3 Echo | GPIO25 | 22 | Right sensor (via level shifter) |
| **Limit Switches (Foot Contact)** |
| Foot #1 (FL) | GPIO5 | 29 | Front-left foot |
| Foot #2 (FR) | GPIO6 | 31 | Front-right foot |
| Foot #3 (RL) | GPIO13 | 33 | Rear-left foot |
| Foot #4 (RR) | GPIO26 | 37 | Rear-right foot |
| **Camera** |
| CSI Camera | CSI | CSI Port | Pi AI Camera IMX500 |
| **Reserved** |
| GPIO4 | GPIO4 | 7 | Available |
| GPIO7 | GPIO7 | 26 | Available |
| GPIO8 | GPIO8 | 24 | Available |
| GPIO12 | GPIO12 | 32 | Available |
| GPIO16 | GPIO16 | 36 | Available |

## I2C Device Addresses

| Device | Address | Notes |
|--------|---------|-------|
| BNO085 IMU | 0x4A | Default, can be 0x4B with ADR pin |

## Level Shifter Connections (TXS0108E)

The HC-SR04 ultrasonic sensors operate at 5V logic. Use TXS0108E to shift:

| TXS0108E Side A (3.3V) | TXS0108E Side B (5V) | Function |
|------------------------|----------------------|----------|
| GPIO27 | HC-SR04 #1 Echo | Front echo |
| GPIO23 | HC-SR04 #2 Echo | Left echo |
| GPIO25 | HC-SR04 #3 Echo | Right echo |

Trigger pins (output from Pi) can drive 5V sensors directly via 3.3V GPIO.

## Notes

- All GPIO numbers are BCM numbering (not physical pin numbers)
- Echo pins MUST use level shifter to protect Pi GPIO from 5V
- Keep I2C wires short (<30cm) to avoid signal integrity issues
- Limit switches should use internal pull-up resistors
