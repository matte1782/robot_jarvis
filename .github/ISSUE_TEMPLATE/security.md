---
name: Security Vulnerability Report
about: Report a security vulnerability (for non-critical issues only)
title: '[SECURITY] '
labels: security
assignees: ''
---

## ⚠️ CRITICAL VULNERABILITIES - DO NOT USE THIS TEMPLATE

**If you've found a critical security vulnerability:**
- **DO NOT** create a public issue
- Use GitHub Security Advisory: https://github.com/matte1782/robot_jarvis/security/advisories/new
- Or email: security-openduck@proton.me

**Critical vulnerabilities include:**
- Remote code execution
- Privilege escalation
- Battery management failures (fire risk)
- Emergency stop bypass
- Data exfiltration

---

## Non-Critical Security Issue

**For non-critical security improvements only** (code quality, documentation, best practices)

### Issue Type
<!-- Check all that apply -->
- [ ] Code quality improvement
- [ ] Missing input validation (low impact)
- [ ] Documentation of security best practices
- [ ] Safety feature suggestion
- [ ] Security test coverage improvement
- [ ] Other (describe below)

### Description
<!-- Clear description of the security concern -->

**What is the security concern?**


**Why is this important?**


### Affected Components
<!-- Check all that apply -->
- [ ] Firmware (Raspberry Pi)
- [ ] Servo drivers
- [ ] Sensor drivers
- [ ] Battery management
- [ ] Network configuration
- [ ] Documentation
- [ ] Build scripts
- [ ] Other:

### Impact Assessment

**Severity:**
<!-- Choose one: Low / Medium / High / Critical -->
<!-- If Critical, DO NOT use this template - use private reporting -->

**Likelihood:**
<!-- How likely is this to be exploited? -->

**Potential consequences:**
<!-- What could happen if this is exploited? -->

### Steps to Reproduce (if applicable)
<!-- How to demonstrate this issue -->

1.
2.
3.

### Suggested Solution
<!-- Optional: Your ideas for fixing this -->

### Environment
<!-- If relevant -->
- Firmware version:
- Hardware version:
- Raspberry Pi OS version:
- Python version:

### Additional Context
<!-- Screenshots, logs, references -->

### Checklist
<!-- Confirm before submitting -->
- [ ] I have verified this is NOT a critical security vulnerability
- [ ] I have searched existing issues to avoid duplicates
- [ ] I have not included sensitive information (passwords, API keys, etc.)
- [ ] I understand this issue will be public

---

## References

- [SECURITY.md](https://github.com/matte1782/robot_jarvis/blob/main/SECURITY.md) - Full security policy
- [SAFETY_WARNINGS.md](https://github.com/matte1782/robot_jarvis/blob/main/firmware/docs/SAFETY_WARNINGS.md) - Hardware safety
- [Security Advisories](https://github.com/matte1782/robot_jarvis/security/advisories) - Published vulnerabilities

Thank you for helping keep OpenDuck Mini V3 secure!
