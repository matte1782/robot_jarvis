# Troubleshooting Guide - OpenDuck Mini V3

## Common Issues and Solutions

### Raspberry Pi Issues

#### Pi Won't Boot
- **Check:** Red LED on, green LED off
- **Solution:** SD card not formatted correctly. Reflash with Raspberry Pi Imager
- **Prevention:** Always verify SD card write completed successfully

#### Can't Connect via SSH
- **Check:** `ping openduck.local` works?
- **Solution:** WiFi credentials incorrect in config. Reflash SD with correct SSID/password
- **Debug:** Connect monitor + keyboard to see boot messages

#### Pi Boots But No Network
- **Check:** Green LED flashing pattern?
- **Solution:** WiFi network out of range or 5GHz network (Pi 4 supports 5GHz but config may be wrong)

### Firmware Issues

#### I2C Devices Not Detected
- **Check:** `i2cdetect -y 1` shows devices?
- **Solution:** Enable I2C in raspi-config: `sudo raspi-config` → Interface Options → I2C → Enable
- **Hardware:** Verify 3.3V power and SDA/SCL connections

#### Servo Not Moving
- **Check:** PCA9685 address correct (default 0x40)?
- **Solution:** Verify PCA9685 powered separately (servos draw too much current for Pi GPIO)
- **Test:** Run `python -m firmware.tests.test_drivers.test_pca9685`

### Battery Safety Issues

⚠️ **DANGER:** If battery is hot, swelling, or smoking, see [SAFETY_WARNINGS.md](firmware/docs/SAFETY_WARNINGS.md) IMMEDIATELY.

#### Battery Won't Charge
- **Check:** BMS protection triggered (over-discharge)?
- **Solution:** Use balance charger to slowly bring voltage above 6.0V
- **Prevention:** Never discharge below 6.0V (2S pack minimum)

### Build Issues

#### Tests Failing
- **Check:** All dependencies installed? `pip install -r requirements.txt`
- **Solution:** Verify Python 3.9+: `python --version`
- **Mock Hardware:** Tests use mocks for hardware - no real I2C needed

#### Import Errors
- **Check:** PYTHONPATH includes firmware directory?
- **Solution:** Run tests from firmware/: `cd firmware && pytest tests/`

## Getting Help

1. Check this troubleshooting guide first
2. Review [firmware/README.md](firmware/README.md) for configuration
3. Search GitHub issues: (Add your repo URL)
4. Create new issue with:
   - Error message (full traceback)
   - Steps to reproduce
   - Python version, OS, hardware details

## Security Issues

For security vulnerabilities, see [SECURITY.md](SECURITY.md) for responsible disclosure process.
**DO NOT create public issues for security bugs.**
