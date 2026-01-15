# Security Policy

## Supported Versions

This project is in active development. Security updates are provided for the latest version only.

| Version | Supported          |
| ------- | ------------------ |
| Latest (main branch) | :white_check_mark: |
| Older commits | :x: |

## Scope

### In Scope

Security issues related to:
- **Firmware vulnerabilities** - Buffer overflows, code injection, privilege escalation
- **Hardware safety** - Battery management, emergency stop failures, thermal runaway
- **Network security** - If wireless features are added
- **Data privacy** - Sensor data handling, logging sensitive information
- **Physical safety** - Servo control failures, power management issues

### Out of Scope

- **General Li-ion battery risks** - See [SAFETY_WARNINGS.md](firmware/docs/SAFETY_WARNINGS.md)
- **3D printer safety** - See printer manufacturer documentation
- **Local development environment security** - User's responsibility
- **Hardware component defects** - Report to component manufacturer

## Reporting a Vulnerability

### Critical Security Issues (Report Privately)

**DO NOT create a public issue for critical security vulnerabilities.**

Critical issues include:
- Remote code execution vulnerabilities
- Privilege escalation bugs
- Battery management failures that could cause fires
- Emergency stop bypass vulnerabilities
- Data exfiltration vectors

**How to report:**
1. **DO NOT** open a public GitHub issue
2. Create a GitHub Security Advisory at: https://github.com/matte1782/robot_jarvis/security/advisories/new
3. Or email: security-openduck@proton.me (monitored weekly)
4. Use subject line: `[SECURITY] <Brief description>`
4. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)
   - Your contact information for follow-up

**Response timeline:**
- **Initial response**: Within 48 hours
- **Status update**: Within 7 days
- **Fix timeline**: Depends on severity
  - Critical: 7-14 days
  - High: 14-30 days
  - Medium: 30-60 days

### Non-Critical Security Issues (Public Issue OK)

Non-critical issues can be reported via GitHub issues:
- Code quality improvements
- Missing input validation (low impact)
- Documentation of security best practices
- Safety feature suggestions

Use the [Security Issue Template](.github/ISSUE_TEMPLATE/security.md)

## Security Best Practices

### For Users

#### Physical Safety

1. **Battery Safety** - Follow [SAFETY_WARNINGS.md](firmware/docs/SAFETY_WARNINGS.md) rigorously
2. **Emergency Stop** - Always have emergency stop accessible during operation
3. **Fire Extinguisher** - Keep Class D fire extinguisher nearby
4. **Supervision** - Never leave robot operating unattended
5. **Testing Environment** - Test in safe, controlled environment

#### Firmware Security

1. **Update Regularly** - Pull latest firmware updates for security fixes
2. **Secure Access** - If SSH is enabled, use strong passwords or key-based auth
3. **Network Isolation** - Keep robot on isolated network if wireless features added
4. **Log Review** - Regularly check logs for anomalies
5. **GPIO Protection** - Don't expose GPIO pins to untrusted inputs

#### Data Privacy

1. **Sensor Data** - Understand what data is collected (cameras, microphones)
2. **Logging** - Review what data is logged and where
3. **Network Traffic** - Monitor network connections if wireless features enabled
4. **Credentials** - Never hardcode passwords or API keys in code

### For Contributors

#### Code Security

1. **Input Validation** - Validate all inputs (GPIO, I2C, network)
2. **Buffer Bounds** - Check array bounds, prevent buffer overflows
3. **Error Handling** - Handle errors gracefully, don't expose sensitive info
4. **Resource Limits** - Implement timeouts, rate limiting
5. **Least Privilege** - Run with minimum required permissions

#### Hardware Safety

1. **Voltage Checks** - Validate voltage ranges before applying power
2. **Current Limiting** - Implement over-current protection
3. **Thermal Protection** - Monitor component temperatures
4. **Fail-Safe Design** - System should fail safely (stop movement, cut power)
5. **Emergency Stop** - Hardware-level emergency stop, not software-only

#### Testing

1. **Security Tests** - Include security test cases
2. **Fuzz Testing** - Test with invalid/malicious inputs
3. **Hardware Limits** - Test behavior at voltage/current limits
4. **Failure Modes** - Test emergency stop, power loss, sensor failures
5. **Code Review** - All PRs reviewed for security issues

## Known Security Considerations

### Current Implementation (v1.0)

#### Strengths

- **No network connectivity** - Air-gapped by default, no remote attack surface
- **Hardware emergency stop** - GPIO-based interrupt, fast response
- **BMS protection** - Battery management prevents over-charge/discharge
- **Read-only filesystem** - Can be configured for production deployments
- **Minimal attack surface** - Simple firmware, few external dependencies

#### Limitations

- **No authentication** - No user authentication (not multi-user system)
- **No encryption** - Data not encrypted at rest or in transit
- **Physical access** - Physical access = full control (by design for single-user robot)
- **GPIO exposure** - GPIO pins directly accessible (feature, not bug)
- **No secure boot** - Raspberry Pi doesn't verify firmware signature

### Future Security Enhancements

Planned for future versions:
- **Wireless safety** - Encrypted wireless emergency stop
- **Firmware signing** - Verify firmware integrity
- **Secure telemetry** - Encrypted sensor data transmission
- **Access control** - Multi-user support with authentication
- **Audit logging** - Tamper-evident audit logs

## Disclosure Policy

### Responsible Disclosure

We follow responsible disclosure principles:

1. **Private notification** - Reporter notifies us privately
2. **Acknowledgment** - We acknowledge receipt within 48 hours
3. **Investigation** - We investigate and develop fix
4. **Coordination** - We coordinate disclosure timeline with reporter
5. **Public disclosure** - After fix is released, we publish advisory

### Public Advisory Format

After fix is released, we publish:
- **CVE number** (if applicable)
- **Vulnerability description** - What was the issue?
- **Impact** - What could an attacker do?
- **Affected versions** - Which versions are vulnerable?
- **Fixed version** - Which version contains the fix?
- **Workarounds** - Temporary mitigations if fix not yet applied
- **Credits** - Acknowledgment to reporter (if desired)

## Security Hall of Fame

We acknowledge security researchers who responsibly disclose vulnerabilities:

<!-- Security researchers will be listed here -->

*No vulnerabilities reported yet.*

## Security Updates

Subscribe to security updates:
- **Watch this repository** - Enable notifications for security advisories
- **GitHub Security Advisories** - Check [Security tab](https://github.com/matte1782/robot_jarvis/security)
- **CHANGELOG.md** - Security fixes noted as `[SECURITY]` entries

## Additional Resources

- [SAFETY_WARNINGS.md](firmware/docs/SAFETY_WARNINGS.md) - Battery and hardware safety
- [CONTRIBUTING.md](CONTRIBUTING.md) - Secure coding guidelines
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Debugging without compromising security

## Contact

**For critical security issues only:**
- GitHub Security Advisory: https://github.com/matte1782/robot_jarvis/security/advisories/new (preferred)
- Email: security-openduck@proton.me (monitored weekly)

**For general security questions:** Open a GitHub issue with `[security-question]` label at https://github.com/matte1782/robot_jarvis/issues

---

**Remember:** Security is everyone's responsibility. When in doubt, report it.

**Last Updated:** 15 January 2026
