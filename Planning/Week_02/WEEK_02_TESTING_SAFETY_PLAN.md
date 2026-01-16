# Week 02 Testing & Safety Plan
## OpenDuck Mini V3 - Quality & Safety Engineering
### Boston Dynamics Standards - Senior Systems Engineer Review

**Document Version:** 1.0
**Created:** 17 January 2026
**Author:** Quality & Safety Systems Engineering
**Classification:** Safety-Critical

---

## Executive Summary

This document defines the testing strategy and safety validation procedures for Week 02 of the OpenDuck Mini V3 project. With servos arriving mid-week and batteries at week's end, we must ensure all software safety mechanisms are validated BEFORE hardware activation.

**Current State:**
- 452 tests, 98.2% pass rate (444 passed, 8 hardware-dependent errors)
- Safety systems: EmergencyStop, CurrentLimiter, ServoWatchdog implemented
- 113 safety tests passing
- Hardware validated: PCA9685 (I2C 0x40), WS2812B LED ring (16/16 pixels)

**Week 02 Critical Timeline:**
- **Days 8-10:** Software-only (BNO085, animation system)
- **Days 11-12 (Mid-Week):** SERVOS ARRIVE - Power-limited testing
- **Days 13-14 (End of Week):** BATTERIES ARRIVE - Full power testing

---

## Section 1: Test Coverage Expansion Strategy

### 1.1 Current Test Distribution

| Module | Tests | Coverage | Status |
|--------|-------|----------|--------|
| `drivers/servo/pca9685.py` | 45 | ~85% | Good |
| `safety/emergency_stop.py` | 43 | ~90% | Good |
| `safety/current_limiter.py` | 45 | ~88% | Good |
| `safety/watchdog.py` | 25 | ~80% | Needs expansion |
| `core/safety_coordinator.py` | 45 | ~85% | Good |
| `core/robot.py` | 41 | ~82% | Needs expansion |
| `kinematics/arm_kinematics.py` | 80 | ~92% | Excellent |

### 1.2 Week 02 Test Targets

| Day | Focus Area | New Tests | Cumulative | Target Coverage |
|-----|------------|-----------|------------|-----------------|
| Day 8 | BNO085 IMU + Animation Timing | +50 | 502 | 85% |
| Day 9 | Easing Functions + LED Patterns | +45 | 547 | 87% |
| Day 10 | Emotion State Machine | +40 | 587 | 89% |
| Day 11 | Head Controller + Servo Safety | +35 | 622 | 91% |
| Day 12 | Integration Tests | +30 | 652 | 93% |
| Day 13 | Edge Cases + Stress Tests | +20 | 672 | 95% |
| Day 14 | Hardware Validation Tests | +25 | 697 | 95% |

### 1.3 Test Category Requirements

#### Unit Tests (70% of new tests)
```python
# Every new class must have:
- __init__ parameter validation tests
- Public method happy path tests
- Error condition tests
- Boundary value tests
- Thread safety tests (if applicable)
```

#### Integration Tests (20% of new tests)
```python
# Component interaction tests:
- SafetyCoordinator + EmergencyStop integration
- Robot + SafetyCoordinator + CurrentLimiter
- AnimationPlayer + HeadController + ServoDriver
- EmotionManager + LEDController + AnimationPlayer
```

#### Hardware Validation Tests (10% of new tests)
```python
# Tests that run on actual Pi hardware:
- I2C device detection (PCA9685, BNO085)
- GPIO interrupt latency measurement
- PWM signal generation verification
- Servo movement under load (BATTERY DAY ONLY)
```

---

## Section 2: Hardware Safety Validation Procedures

### 2.1 Servo Bring-up Safety Checklist

**PRE-POWER VERIFICATION (MANDATORY)**

```
[ ] 2.1.1 MECHANICAL INSPECTION
    [ ] All servo horns properly seated
    [ ] No obstructions in servo range of motion
    [ ] Mounting hardware secure (no loose screws)
    [ ] Cables routed away from moving parts

[ ] 2.1.2 ELECTRICAL VERIFICATION
    [ ] V+ rail voltage: 6.0V +/- 0.1V (from UBEC)
    [ ] No shorts between V+, GND, or signal lines
    [ ] All connections secure (no loose Dupont cables)
    [ ] PCA9685 detected at 0x40 (i2cdetect -y 1)

[ ] 2.1.3 SOFTWARE SAFETY CHECK
    [ ] emergency_stop.py loaded and functional
    [ ] Watchdog timeout configured (500ms)
    [ ] Current limiter initialized
    [ ] All safety tests passing (113/113)

[ ] 2.1.4 ENVIRONMENT
    [ ] Clear workspace (no tools in robot area)
    [ ] Emergency stop button accessible
    [ ] Fire extinguisher nearby (LiPo safety)
    [ ] Multimeter ready for voltage verification
```

### 2.2 Servo Power-On Sequence

**CRITICAL: Follow this exact sequence to prevent servo damage.**

```python
# STEP 1: Pre-flight (software running, no power to V+)
python3 scripts/hardware_validation.py --i2c --gpio

# STEP 2: Enable safety systems FIRST
safety_coordinator.start()
assert safety_coordinator.is_safe == True

# STEP 3: Connect single servo to channel 0 (still no V+ power)
# Physical connection only - servo unpowered

# STEP 4: Apply V+ power to PCA9685
# IMMEDIATELY verify voltage: 6.0V on V+ rail

# STEP 5: Center servo (90 degrees)
robot.set_servo_angle(channel=0, angle=90)
# VISUALLY VERIFY: Servo moves to center
# LISTEN: No grinding, clicking, or stalling sounds

# STEP 6: Test range of motion (slow sweep)
robot.sweep_servo(channel=0, start=45, end=135, steps=10, delay=0.5)
# VISUALLY VERIFY: Smooth movement
# WATCH: Current draw should be <300mA per servo

# STEP 7: Verify emergency stop
# PRESS PHYSICAL E-STOP BUTTON
# VERIFY: Servo immediately releases (no holding torque)
# VERIFY: robot.state == RobotState.E_STOPPED
```

### 2.3 Multi-Servo Activation Protocol

**Only proceed after single-servo validation is complete.**

```
CHANNEL ACTIVATION ORDER (by risk):
1. Channel 0 (already validated)
2. Channel 1 (second lowest load)
3. Channel 2
4. Channel 3
5. Channel 4

After EACH new servo:
[ ] Verify current draw < 1.5A total
[ ] Test emergency stop functionality
[ ] Test watchdog timeout (disconnect command loop)
[ ] Verify no brownouts or voltage drops
```

### 2.4 Battery Integration Safety Protocol

**HIGHEST RISK PHASE - Execute with extreme caution.**

```
[ ] 2.4.1 BATTERY INSPECTION
    [ ] No physical damage to cells
    [ ] No puffing or swelling
    [ ] Voltage per cell: 3.0V - 4.2V (reject if outside range)
    [ ] Pack voltage: 7.0V - 8.4V

[ ] 2.4.2 BMS VERIFICATION
    [ ] BMS installed between battery and UBEC
    [ ] Balance leads connected (if applicable)
    [ ] Over-discharge protection active (cutoff at 6.0V)
    [ ] Over-current protection active (20A limit)

[ ] 2.4.3 CHARGING SAFETY
    [ ] Never charge unattended
    [ ] Charge in fireproof container (LiPo safe bag)
    [ ] Charge rate: 1C maximum (3000mAh = 3A max)
    [ ] Stop charging if any cell exceeds 4.25V

[ ] 2.4.4 FIRST BATTERY POWER TEST
    [ ] All servos disconnected initially
    [ ] Monitor voltage under no load for 60 seconds
    [ ] Verify UBEC output: 6.0V stable
    [ ] Reconnect servos one at a time
    [ ] Monitor for voltage sag (>0.5V drop = problem)
```

---

## Section 3: Hostile Review Schedule

### 3.1 Mandatory Review Triggers

| Trigger | Review Level | Deadline |
|---------|--------------|----------|
| Any new file >50 lines | Level 2 (Standard) | Before commit |
| Safety-critical code change | Level 3 (Deep) | Before any testing |
| Hardware interface code | Level 3 (Deep) | Before hardware test |
| Integration test failures | Level 2 (Standard) | Before next session |
| Any servo movement code | Level 3 (Deep) | Before powered test |

### 3.2 Week 02 Review Schedule

```
Day 8 (Wed):
  [x] Morning: BNO085 driver review (Level 2)
  [x] Afternoon: Animation timing review (Level 2)
  [x] Evening: Integration review (Level 2)

Day 9 (Thu):
  [x] Morning: Easing functions review (Level 1)
  [x] Afternoon: LED patterns review (Level 2)

Day 10 (Fri):
  [x] Full day: Emotion system review (Level 3)
      - State machine correctness
      - Thread safety analysis
      - Memory leak check

Day 11 (Sat) - SERVO ARRIVAL:
  [!!!] MANDATORY: Servo command review (Level 3)
  [!!!] MANDATORY: Power sequencing review (Level 3)
  [ ] Head controller review (Level 2)

Day 12 (Sun):
  [ ] Integration test review (Level 2)
  [ ] Performance review (control loop timing)

Day 13 (Mon) - BATTERY ARRIVAL:
  [!!!] MANDATORY: Power management review (Level 3)
  [!!!] MANDATORY: Current limiting review (Level 3)
  [ ] Full system review (Level 3)

Day 14 (Tue):
  [ ] Final hostile review (Level 3 - all Week 02 code)
  [ ] Sign-off for v0.2.0 tag
```

### 3.3 Hostile Review Prompts for Safety Code

**Servo Command Review:**
```
You are reviewing SAFETY-CRITICAL servo control code for a robotics project.

Hardware constraints:
- MG90S servos: 0-180 degree range, stall at ~900mA
- STS3215 servos: Continuous rotation, 7.4V nominal
- PCA9685: 16 channels, 50Hz PWM
- Emergency stop: GPIO 26, active LOW

CRITICAL CHECKS:
1. Every servo angle MUST be clamped to [0, 180] BEFORE sending to driver
2. Emergency stop MUST NOT be disabled, bypassed, or ignored anywhere
3. Watchdog MUST be fed in every control loop iteration
4. Current estimates MUST be updated on every movement command
5. Stall detection MUST trigger E-stop within 300ms

Any violation of these rules is CRITICAL severity.

Code to review:
[CODE HERE]
```

**Power Management Review:**
```
You are reviewing power management code for a LiPo-powered robot.

Hardware constraints:
- 2S LiPo: 7.4V nominal, 6.0V cutoff, 8.4V max
- BMS: 20A over-current protection
- UBEC: 6V 3A output to servos
- Total servo current budget: 2.5A max

CRITICAL CHECKS:
1. Low voltage warning at 7.0V, emergency shutdown at 6.5V
2. Total current estimation must not exceed 2.5A
3. Brownout detection must trigger E-stop
4. Never command more than 4 servos simultaneously under load
5. Thermal protection must limit duty cycle during stalls

Any violation that could damage batteries is CRITICAL severity.

Code to review:
[CODE HERE]
```

---

## Section 4: Integration Test Design

### 4.1 Integration Test Categories

#### 4.1.1 Safety System Integration Tests

```python
# tests/test_integration/test_safety_integration.py

class TestSafetySystemIntegration:
    """Full integration tests for safety systems working together."""

    def test_estop_disables_all_safety_systems(self):
        """E-stop trigger disables watchdog, servos, and updates state."""
        robot = Robot(mock_driver)
        robot.start()

        # Trigger E-stop
        robot.emergency_stop(source="integration_test")

        # Verify ALL safety actions taken
        assert robot.state == RobotState.E_STOPPED
        assert robot.safety.watchdog.is_running == False
        assert robot._servo_driver.disable_all_calls >= 1
        assert robot.safety.estop_state == SafetyState.RESET_REQUIRED

    def test_watchdog_timeout_triggers_estop(self):
        """Watchdog timeout triggers full E-stop sequence."""
        robot = Robot(mock_driver, watchdog_timeout_ms=100)
        robot.start()

        # Stop feeding watchdog
        time.sleep(0.2)  # 200ms > 100ms timeout

        assert robot.state == RobotState.E_STOPPED

    def test_stall_detection_triggers_estop(self):
        """Servo stall detection triggers E-stop."""
        robot = Robot(mock_driver)
        robot.start()
        robot.set_servo_angle(0, 90)

        # Simulate stall (position not changing)
        for _ in range(10):
            robot.safety.check_stall(0, target_angle=90, current_position=45)
            time.sleep(0.05)  # 500ms total > 300ms timeout

        # Should trigger E-stop
        assert robot.state == RobotState.E_STOPPED

    def test_recovery_sequence(self):
        """Full recovery from E-stop state."""
        robot = Robot(mock_driver)
        robot.start()
        robot.emergency_stop(source="test")

        # Attempt recovery
        result = robot.reset_from_estop()

        # Should be in INIT state, requiring explicit start()
        assert result == True
        assert robot.state == RobotState.INIT

        # Re-start
        robot.start()
        assert robot.state == RobotState.READY
```

#### 4.1.2 Control Loop Integration Tests

```python
# tests/test_integration/test_control_loop.py

class TestControlLoopIntegration:
    """Tests for the main control loop with all components."""

    def test_control_loop_feeds_watchdog(self):
        """Control loop correctly feeds watchdog each iteration."""
        robot = Robot(mock_driver, watchdog_timeout_ms=1000)
        robot.start()

        # Run control loop for 500ms
        start = time.monotonic()
        while time.monotonic() - start < 0.5:
            result = robot.step()
            assert result == True

        # Should still be running (watchdog fed)
        assert robot.state == RobotState.READY

    def test_control_loop_timing(self):
        """Control loop maintains 50Hz timing."""
        robot = Robot(mock_driver, control_rate_hz=50)
        robot.start()

        timestamps = []
        for _ in range(100):
            robot.step()
            timestamps.append(time.monotonic())

        # Calculate actual rate
        deltas = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        avg_delta = sum(deltas) / len(deltas)
        expected_delta = 1.0 / 50  # 20ms

        # Should be within 10% of target
        assert abs(avg_delta - expected_delta) < expected_delta * 0.1

    def test_control_loop_handles_slow_commands(self):
        """Control loop handles slow I2C operations gracefully."""
        mock_driver.i2c_delay_ms = 10  # Simulate slow I2C
        robot = Robot(mock_driver, control_rate_hz=50)
        robot.start()

        # Should not crash even with slow I2C
        for _ in range(50):
            robot.step()

        assert robot.state == RobotState.READY
```

#### 4.1.3 Animation System Integration Tests

```python
# tests/test_integration/test_animation_integration.py

class TestAnimationIntegration:
    """Tests for animation system integration with servos."""

    def test_animation_respects_servo_limits(self):
        """Animation keyframes are clamped to servo limits."""
        animator = AnimationPlayer(mock_driver)
        animator.set_servo_limits(0, min_angle=30, max_angle=150)

        # Create animation that exceeds limits
        animation = AnimationSequence("test")
        animation.add_keyframe(0, {'servo_0': 0})    # Below min
        animation.add_keyframe(1000, {'servo_0': 180})  # Above max

        # Play and verify clamping
        animator.play(animation)

        # Should have been clamped
        assert 30 <= mock_driver.last_angle[0] <= 150

    def test_animation_aborts_on_estop(self):
        """Animation stops immediately on E-stop."""
        robot = Robot(mock_driver)
        robot.start()

        # Start long animation
        animation = AnimationSequence("long_sweep")
        animation.add_keyframe(0, {'head_pan': 0})
        animation.add_keyframe(5000, {'head_pan': 180})  # 5 second animation

        robot.animator.play(animation)
        time.sleep(0.1)  # Let animation start

        # Trigger E-stop
        robot.emergency_stop(source="test")

        # Animation should abort
        assert robot.animator.is_playing == False

    def test_emotion_transition_animation(self):
        """Emotion changes trigger appropriate LED and head animations."""
        robot = Robot(mock_driver)
        robot.start()

        # Change emotion
        robot.emotion.set_emotion(EmotionState.HAPPY)

        # Verify LED pattern changed
        assert robot.led.current_pattern == 'sparkle'

        # Verify head animation started
        assert robot.animator.is_playing == True
```

### 4.2 Hardware Integration Tests

```python
# tests/test_hardware/test_hardware_integration.py
# These tests require actual Raspberry Pi hardware

@pytest.mark.hardware
class TestHardwareIntegration:
    """Tests that run on actual Raspberry Pi hardware."""

    def test_pca9685_i2c_communication(self):
        """Verify PCA9685 I2C communication."""
        import board
        import busio

        i2c = busio.I2C(board.SCL, board.SDA)
        devices = i2c.scan()

        assert 0x40 in devices, "PCA9685 not found at 0x40"

    def test_gpio_interrupt_latency(self):
        """Measure GPIO interrupt latency."""
        import RPi.GPIO as GPIO

        latencies = []

        def callback(channel):
            latencies.append(time.perf_counter())

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(26, GPIO.FALLING, callback=callback)

        # Trigger interrupt programmatically or via button
        # Measure latency

        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        assert avg_latency < 0.005, f"GPIO latency {avg_latency*1000}ms > 5ms"

    @pytest.mark.servo
    def test_servo_movement_accuracy(self):
        """Test servo reaches commanded position."""
        driver = PCA9685Driver()

        # Command 90 degrees
        driver.set_servo_angle(0, 90)
        time.sleep(0.5)  # Allow servo to reach position

        # This would require external measurement (visual or encoder)
        # For now, verify no exceptions
        assert True

    @pytest.mark.battery
    def test_voltage_under_load(self):
        """Test voltage stability under servo load."""
        # This test requires ADC for voltage measurement
        # Placeholder for when ADS1115 is integrated
        pass
```

---

## Section 5: Failure Mode Analysis (FMEA)

### 5.1 Servo Failure Modes

| Failure Mode | Severity | Probability | Detection | Mitigation |
|--------------|----------|-------------|-----------|------------|
| Servo stall (blocked) | HIGH | Medium | Position monitoring, current spike | E-stop after 300ms, disable channel |
| Servo overheat | HIGH | Low | Thermal estimation, duty cycle | Limit duty to 70%, rest periods |
| Servo gear strip | CRITICAL | Low | Sudden position jump, no load | Replace servo, add soft limits |
| PWM signal loss | MEDIUM | Low | Watchdog timeout | E-stop, re-initialize PCA9685 |
| I2C bus hang | HIGH | Low | Transaction timeout | Bus reset, E-stop |

### 5.2 Power System Failure Modes

| Failure Mode | Severity | Probability | Detection | Mitigation |
|--------------|----------|-------------|-----------|------------|
| Battery undervoltage | CRITICAL | Medium | Voltage monitoring | Warning at 7.0V, shutdown at 6.5V |
| Battery overcurrent | CRITICAL | Low | BMS trip | E-stop on BMS disconnect |
| UBEC failure | HIGH | Low | Voltage drop | E-stop, visual LED indicator |
| Brownout (sag) | HIGH | Medium | Voltage monitoring | Limit simultaneous movements |
| LiPo fire | CRITICAL | Very Low | Smoke, heat | Fire extinguisher, outdoor testing |

### 5.3 Software Failure Modes

| Failure Mode | Severity | Probability | Detection | Mitigation |
|--------------|----------|-------------|-----------|------------|
| Control loop crash | HIGH | Low | Watchdog timeout | E-stop, servo release |
| Memory leak | MEDIUM | Low | Resource monitoring | Bounded event history (100 max) |
| Deadlock | CRITICAL | Low | Watchdog timeout | RLock usage, lock ordering |
| Race condition | HIGH | Low | Inconsistent state | Comprehensive locking |
| GPIO interrupt miss | MEDIUM | Low | State inconsistency | Pin state verification |

### 5.4 Mitigation Priority Matrix

```
         HIGH PROBABILITY          LOW PROBABILITY
        +--------------------+--------------------+
 HIGH   | Servo stall        | I2C bus hang       |
SEVERITY| Battery undervolt  | Gear strip         |
        | Brownout           | UBEC failure       |
        +--------------------+--------------------+
 LOW    | Control loop       | Memory leak        |
SEVERITY| timing drift       | GPIO miss          |
        +--------------------+--------------------+

        PRIORITY: HIGH SEVERITY + HIGH PROBABILITY = CRITICAL
                  Address these FIRST before hardware testing
```

---

## Section 6: Safety Interlocks for Servo Power

### 6.1 Software Interlocks

```python
# firmware/src/safety/servo_interlocks.py

class ServoInterlocks:
    """Software interlocks that MUST pass before servo power is enabled."""

    # Interlock 1: Watchdog must be running
    @staticmethod
    def check_watchdog(safety: SafetyCoordinator) -> Tuple[bool, str]:
        if not safety.watchdog.is_running:
            return False, "INTERLOCK FAIL: Watchdog not running"
        return True, ""

    # Interlock 2: E-stop must be in RUNNING state
    @staticmethod
    def check_estop(safety: SafetyCoordinator) -> Tuple[bool, str]:
        if safety.estop_state != SafetyState.RUNNING:
            return False, f"INTERLOCK FAIL: E-stop in {safety.estop_state.name}"
        return True, ""

    # Interlock 3: No stalled channels
    @staticmethod
    def check_stalls(limiter: CurrentLimiter) -> Tuple[bool, str]:
        diagnostics = limiter.get_system_diagnostics()
        stalled = diagnostics.get('stalled_channels', [])
        if stalled:
            return False, f"INTERLOCK FAIL: Stalled channels {stalled}"
        return True, ""

    # Interlock 4: Current budget available
    @staticmethod
    def check_current_budget(limiter: CurrentLimiter) -> Tuple[bool, str]:
        total = limiter.get_total_current()
        max_budget = 2500  # 2.5A max
        if total > max_budget * 0.9:  # 90% threshold
            return False, f"INTERLOCK FAIL: Current {total}mA > 90% of budget"
        return True, ""

    # Interlock 5: Thermal limits not exceeded
    @staticmethod
    def check_thermal(limiter: CurrentLimiter) -> Tuple[bool, str]:
        diagnostics = limiter.get_system_diagnostics()
        limited = diagnostics.get('thermal_limited_channels', [])
        if limited:
            return False, f"INTERLOCK FAIL: Thermal limited channels {limited}"
        return True, ""

    @classmethod
    def check_all(cls, safety: SafetyCoordinator) -> Tuple[bool, List[str]]:
        """Run all interlocks, return (all_pass, list_of_failures)."""
        failures = []

        checks = [
            cls.check_watchdog(safety),
            cls.check_estop(safety),
            cls.check_stalls(safety._current_limiter),
            cls.check_current_budget(safety._current_limiter),
            cls.check_thermal(safety._current_limiter),
        ]

        for passed, message in checks:
            if not passed:
                failures.append(message)

        return len(failures) == 0, failures
```

### 6.2 Hardware Interlocks

```
PHYSICAL SAFETY REQUIREMENTS:

1. EMERGENCY STOP BUTTON
   - Must be within arm's reach during all testing
   - Must immediately cut V+ power to PCA9685
   - Software E-stop (GPIO 26) is BACKUP, not primary

2. POWER ISOLATION
   - Main power switch between battery and BMS
   - Can cut all power within 1 second
   - Labeled clearly: "MAIN POWER"

3. VISUAL INDICATORS
   - LED on when servos powered (power indicator)
   - LED blink pattern for E-stop state
   - Different colors for different states

4. CURRENT LIMITING
   - UBEC rated for 3A continuous
   - Fuse on battery positive: 5A
   - Polyfuse on servo rail: 3A (resettable)
```

### 6.3 Interlock Test Verification

```python
# tests/test_safety/test_interlocks.py

class TestServoInterlocks:
    """Tests for servo power interlocks."""

    def test_all_interlocks_pass_normal_operation(self):
        """All interlocks pass in normal READY state."""
        robot = Robot(mock_driver)
        robot.start()

        passed, failures = ServoInterlocks.check_all(robot.safety)

        assert passed == True
        assert len(failures) == 0

    def test_watchdog_interlock_fails_when_stopped(self):
        """Watchdog interlock fails when watchdog stopped."""
        robot = Robot(mock_driver)
        robot.start()
        robot.safety._watchdog.stop()

        passed, msg = ServoInterlocks.check_watchdog(robot.safety)

        assert passed == False
        assert "Watchdog not running" in msg

    def test_estop_interlock_fails_when_triggered(self):
        """E-stop interlock fails after E-stop triggered."""
        robot = Robot(mock_driver)
        robot.start()
        robot.emergency_stop(source="test")

        passed, msg = ServoInterlocks.check_estop(robot.safety)

        assert passed == False
        assert "E-stop in" in msg

    def test_stall_interlock_blocks_power(self):
        """Stall interlock prevents servo power."""
        robot = Robot(mock_driver)
        robot.start()

        # Simulate stall
        robot.safety._current_limiter._channel_states[0].stall_condition = StallCondition.CONFIRMED

        passed, msg = ServoInterlocks.check_stalls(robot.safety._current_limiter)

        assert passed == False
        assert "Stalled channels" in msg
```

---

## Section 7: Day-by-Day Testing Work Breakdown

### Day 8 (Wednesday) - BNO085 + Animation Timing

**Morning (3 hours):**
```
[ ] 09:00 - BNO085 hardware connection
    [ ] Wire to I2C bus (shared with PCA9685)
    [ ] Verify detection: i2cdetect -y 1 shows 0x4A
    [ ] Run: python3 scripts/test_bno085.py

[ ] 10:00 - BNO085 driver TDD
    [ ] Write tests FIRST (25 tests)
    [ ] Implement driver to pass tests
    [ ] Hostile review: Level 2

[ ] 12:00 - BNO085 integration
    [ ] Add to I2CBusManager
    [ ] Test concurrent PCA9685 + BNO085 access
```

**Afternoon (3 hours):**
```
[ ] 14:00 - Animation timing system TDD
    [ ] Keyframe tests (15 tests)
    [ ] Interpolation tests (10 tests)

[ ] 16:00 - Implementation
    [ ] AnimationSequence class
    [ ] Linear and ease-in-out interpolation
    [ ] Hostile review: Level 2

[ ] 18:00 - Integration tests
    [ ] Animation + mock servo
    [ ] Timing accuracy verification
```

**Evening (1 hour):**
```
[ ] 20:00 - Documentation
    [ ] Update CHANGELOG
    [ ] Commit: "feat: BNO085 IMU + animation timing"
    [ ] Test count target: 502
```

---

### Day 9 (Thursday) - Easing + LED Patterns

**Morning (2 hours):**
```
[ ] 09:00 - Easing functions TDD
    [ ] Test all easing curves (20 tests)
    [ ] Implement 5 easing functions
    [ ] Verify mathematical properties

[ ] 11:00 - Hostile review: Level 1
```

**Afternoon (4 hours):**
```
[ ] 12:00 - LED pattern TDD
    [ ] BreathingPattern tests (8 tests)
    [ ] PulsePattern tests (8 tests)
    [ ] SpinPattern tests (8 tests)
    [ ] SparklePattern tests (8 tests)

[ ] 14:00 - Implementation
    [ ] Pattern base class
    [ ] All 4 patterns
    [ ] Hardware test on LED ring

[ ] 16:00 - Hostile review: Level 2
    [ ] Performance check (50Hz render budget)
    [ ] Memory allocation check

[ ] 18:00 - Integration
    [ ] LED patterns + animation system
    [ ] Test count target: 547
```

---

### Day 10 (Friday) - Emotion State Machine

**Full Day (6 hours):**
```
[ ] 09:00 - Emotion system design review
    [ ] State transition diagram
    [ ] 8 emotion configurations

[ ] 10:00 - TDD for EmotionManager
    [ ] State transition tests (15 tests)
    [ ] Invalid transition tests (10 tests)
    [ ] LED integration tests (8 tests)
    [ ] Animation trigger tests (7 tests)

[ ] 14:00 - Implementation
    [ ] EmotionState enum
    [ ] EmotionConfig dataclass
    [ ] EmotionManager class
    [ ] VALID_TRANSITIONS dict

[ ] 17:00 - Hostile review: Level 3
    [ ] State machine correctness
    [ ] Thread safety
    [ ] Memory bounds

[ ] 19:00 - Hardware demo
    [ ] Run emotion showcase on LED ring
    [ ] Test count target: 587
```

---

### Day 11 (Saturday) - SERVO ARRIVAL

**CRITICAL: Servo safety validation takes priority.**

**Morning (3 hours):**
```
[ ] 09:00 - Pre-servo preparation
    [ ] Review Section 2 of this document
    [ ] Complete PRE-POWER VERIFICATION checklist
    [ ] Hostile review: ALL servo command code (Level 3)

[ ] 11:00 - Head controller TDD (mock only)
    [ ] look_at() tests (12 tests)
    [ ] random_glance() tests (8 tests)
    [ ] Safety integration tests (15 tests)
```

**Afternoon (3 hours) - POWERED TESTING:**
```
[!!!] 14:00 - Servo bring-up (Section 2.2)
    [ ] Single servo test (channel 0)
    [ ] Emergency stop verification
    [ ] Current measurement

[!!!] 16:00 - Multi-servo activation (Section 2.3)
    [ ] One channel at a time
    [ ] E-stop test after each
    [ ] Current budget verification

[ ] 18:00 - Head controller with real servos
    [ ] Pan/tilt movement
    [ ] Smooth animation test
    [ ] Test count target: 622
```

---

### Day 12 (Sunday) - Integration + Polish

**Morning (3 hours):**
```
[ ] 09:00 - Idle behavior implementation
    [ ] Random glances
    [ ] Blinking patterns
    [ ] Background animation

[ ] 11:00 - Full integration tests
    [ ] Emotion + LED + Head
    [ ] Control loop timing
    [ ] Resource leak check
```

**Afternoon (3 hours):**
```
[ ] 14:00 - Stress testing
    [ ] Rapid emotion changes (100 changes/second)
    [ ] Long-running test (1 hour)
    [ ] Memory monitoring

[ ] 17:00 - Hostile review: Integration
    [ ] All Day 11-12 code
    [ ] Test count target: 652
```

---

### Day 13 (Monday) - BATTERY ARRIVAL

**CRITICAL: Power safety validation takes priority.**

**Morning (3 hours):**
```
[ ] 09:00 - Battery inspection
    [ ] Complete Section 2.4.1-2.4.3 checklists
    [ ] Hostile review: Power management code (Level 3)

[!!!] 11:00 - First battery power test
    [ ] No-load voltage test
    [ ] UBEC output verification
    [ ] Servo connection one-by-one
```

**Afternoon (3 hours):**
```
[ ] 14:00 - Full power testing
    [ ] All servos powered
    [ ] Stress test (continuous movement)
    [ ] Current monitoring

[ ] 16:00 - Edge case testing
    [ ] Low battery simulation
    [ ] Brownout recovery
    [ ] E-stop under load

[ ] 18:00 - Documentation
    [ ] Power budget measurements
    [ ] Voltage profiles
    [ ] Test count target: 672
```

---

### Day 14 (Tuesday) - Final Validation

**Morning (2 hours):**
```
[ ] 09:00 - Full test suite
    [ ] pytest tests/ -v --tb=short
    [ ] All 672+ tests must pass

[ ] 10:00 - Coverage report
    [ ] pytest --cov=src --cov-report=html
    [ ] Target: 95% overall coverage

[ ] 11:00 - Hardware validation script
    [ ] Run all hardware tests
    [ ] Document results
```

**Afternoon (3 hours):**
```
[ ] 13:00 - Final hostile review
    [ ] All Week 02 code (Level 3)
    [ ] Sign-off required for v0.2.0

[ ] 15:00 - Demo run
    [ ] Full system demonstration
    [ ] All emotions, animations, movements
    [ ] Record video for documentation

[ ] 17:00 - Week 02 closure
    [ ] Update CHANGELOG
    [ ] Git tag v0.2.0
    [ ] Week 02 completion report
    [ ] Test count target: 697
```

---

## Section 8: Coverage Targets by Module

### 8.1 Week 02 Coverage Requirements

| Module | Current | Target | Priority |
|--------|---------|--------|----------|
| `safety/emergency_stop.py` | 90% | 95% | HIGH |
| `safety/current_limiter.py` | 88% | 95% | HIGH |
| `safety/watchdog.py` | 80% | 90% | HIGH |
| `core/safety_coordinator.py` | 85% | 95% | HIGH |
| `core/robot.py` | 82% | 90% | MEDIUM |
| `drivers/servo/pca9685.py` | 85% | 90% | MEDIUM |
| `drivers/sensor/imu/bno085.py` | NEW | 90% | HIGH |
| `animation/timing.py` | NEW | 90% | MEDIUM |
| `animation/easing.py` | NEW | 95% | LOW |
| `animation/emotions.py` | NEW | 90% | MEDIUM |
| `animation/head_controller.py` | NEW | 85% | MEDIUM |
| `led/patterns.py` | NEW | 85% | LOW |

### 8.2 Critical Path Coverage

**These modules MUST have 95%+ coverage before servo power-on:**

1. `safety/emergency_stop.py` - Controls E-stop functionality
2. `safety/current_limiter.py` - Prevents servo damage
3. `core/safety_coordinator.py` - Orchestrates all safety systems

**Rationale:** A bug in safety code could cause hardware damage or injury. 95% coverage ensures comprehensive testing of all code paths.

---

## Section 9: Success Criteria Summary

### 9.1 Test Metrics

| Metric | Target | Actual (EOW) |
|--------|--------|--------------|
| Total Tests | 697 | _____ |
| Pass Rate | 98%+ | _____ |
| Safety Tests | 150+ | _____ |
| Integration Tests | 50+ | _____ |
| Hardware Tests | 25+ | _____ |

### 9.2 Safety Metrics

| Metric | Target | Actual (EOW) |
|--------|--------|--------------|
| E-stop Latency | <5ms | _____ |
| Watchdog Response | <100ms | _____ |
| Stall Detection | <300ms | _____ |
| Hostile Reviews | 10+ | _____ |
| Critical Issues Fixed | 100% | _____ |

### 9.3 Hardware Validation

| Test | Status | Notes |
|------|--------|-------|
| PCA9685 I2C | PASSED (Day 6) | 0x40 detected |
| BNO085 I2C | _____ | Day 8 |
| Single Servo | _____ | Day 11 |
| Multi-Servo | _____ | Day 11 |
| E-Stop Hardware | _____ | Day 11 |
| Battery Power | _____ | Day 13 |
| Full System | _____ | Day 14 |

---

## Appendix A: Emergency Procedures

### A.1 Servo Runaway

**Symptoms:** Servo moves uncontrollably, won't stop
**Response:**
1. PRESS PHYSICAL E-STOP BUTTON
2. If no response: DISCONNECT BATTERY (pull XT60)
3. Wait 10 seconds for capacitors to discharge
4. Investigate cause before power-on

### A.2 Battery Thermal Event

**Symptoms:** Smoke, heat, bulging, unusual smell
**Response:**
1. DO NOT TOUCH BATTERY
2. EVACUATE AREA (outdoors if possible)
3. Call fire department if flames
4. Let battery cool for 1 hour minimum
5. Dispose properly (battery recycling center)

### A.3 I2C Bus Hang

**Symptoms:** Commands not responding, timeout errors
**Response:**
1. Software E-stop: `robot.emergency_stop(source="i2c_hang")`
2. Power cycle PCA9685 (disconnect V+, wait 5s, reconnect)
3. Reset I2C bus: `sudo rmmod i2c_bcm2835 && sudo modprobe i2c_bcm2835`
4. Re-run i2cdetect to verify recovery

---

## Appendix B: Quick Reference Cards

### B.1 Daily Test Commands

```bash
# Run all tests
cd firmware && pytest tests/ -v --tb=short

# Run safety tests only
pytest tests/test_safety/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run hardware tests (on Pi only)
pytest tests/ -v -m hardware

# Run single test file
pytest tests/test_safety/test_emergency_stop.py -v
```

### B.2 Safety State Quick Reference

```
INIT         - System initialized, not running, servos disabled
RUNNING      - Normal operation, servos enabled, monitoring active
E_STOP       - Emergency stop triggered, servos disabled
RESET_REQ    - E-stop acknowledged, manual reset required

Valid Transitions:
INIT -> RUNNING (start())
INIT -> E_STOP (trigger() for safety during init)
RUNNING -> E_STOP (trigger())
E_STOP -> RESET_REQ (auto)
RESET_REQ -> INIT (reset() with auto_reset=False)
RESET_REQ -> RUNNING (reset() with auto_reset=True)
```

### B.3 Hostile Review Severity Quick Reference

```
CRITICAL - Immediate failure, safety hazard, hardware damage
           MUST fix before ANY testing. BLOCKS commit.

HIGH     - Failure under specific conditions, security vuln
           MUST fix before merge. BLOCKS commit.

MEDIUM   - Degraded behavior, maintenance problems
           SHOULD fix. May defer with justification.

LOW      - Cosmetic, preferences
           MAY fix. Often auto-fixable.
```

---

**Document Approval:**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | Quality & Safety Engineering | 17 Jan 2026 | _____ |
| Reviewer | Boston Dynamics Standards | _____ | _____ |
| Approver | Project Lead | _____ | _____ |

---

**Document Version History:**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 17 Jan 2026 | Initial release | QA/Safety |

---

*This document is MANDATORY reading for all personnel involved in Week 02 hardware testing.*
