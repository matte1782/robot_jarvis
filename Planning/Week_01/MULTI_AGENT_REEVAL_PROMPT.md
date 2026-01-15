# MULTI-AGENT WEEK 01 PLAN RE-EVALUATION PROMPT
**Created:** 2026-01-14
**Purpose:** Complete re-evaluation and rewrite of Week 01 roadmap accounting for hardware delays

---

## MISSION STATEMENT

Re-evaluate and rewrite the entire Week 01 plan (14-20 January 2026) for the OpenDuck Mini V3 robot project, accounting for the critical constraint that **the QIDI X-Max 3 3D printer has NOT arrived yet**.

The new plan must:
1. Focus on SOFTWARE-FIRST development with available components
2. Maximize productive work while waiting for hardware
3. Prepare for efficient assembly when printer arrives
4. Include realistic daily tasks with measurable outcomes
5. Identify true blockers vs artificial delays

---

## CRITICAL CONSTRAINTS (AS OF 14/01/2026)

### Hardware Status - REALITY CHECK

**COMPONENTS ACTUALLY RECEIVED (RICEVUTO):**
- [ ] Raspberry Pi 4 8GB (UNCERTAIN - needs verification in tracker)
- [x] PCA9685 PWM Driver (confirmed)
- [x] MG90S Servos (5x) (confirmed)
- [ ] WS2812B NeoPixel Ring 16-LED (UNCERTAIN - verify)
- [ ] MAX98357 I2S Amplifier (UNCERTAIN - verify)
- [ ] Other sensors/electronics (needs complete inventory check)

**ARRIVING THIS WEEK:**
- 15/01: INMP441 microphone, PCA9685, USB-C cable, aluminum case, heat shrink
- 16/01: Glass domes 50mm (2x)
- 19-22/01: BNO085 IMU, SD card, speakers, solder wire

**NOT AVAILABLE (CRITICAL BLOCKERS):**
- ❌ QIDI X-Max 3 3D Printer - NO ETA PROVIDED
- ❌ Molicel P30B batteries (4x) - NOT ORDERED YET
- ❌ Feetech STS3215 servos (16x) - NOT ORDERED YET (~€400, 7-10 day lead time)

### What Can Be Done NOW

**Software Development:**
- ✅ Firmware architecture design
- ✅ PCA9685 driver development
- ✅ Inverse kinematics solver
- ✅ Gait generation algorithms
- ✅ Testing harness creation
- ✅ Documentation

**Electronics Testing (if components available):**
- ✅ PCA9685 + MG90S servo bench test
- ✅ LED ring animation test (if available)
- ✅ Audio amplifier test (if available)
- ✅ Sensor characterization (if available)
- ✅ Power consumption measurements

**What CANNOT Be Done:**
- ❌ 3D printing (no printer)
- ❌ Full power testing (no batteries)
- ❌ Leg assembly (no servos, no printed parts)
- ❌ Complete robot integration

---

## AGENT TASK ASSIGNMENTS

### AGENT 1: "COMPONENT VERIFIER"
**Objective:** Establish ground truth of what's actually available NOW

**Tasks:**
1. Read `OPENDUCK_V3_FINAL_TRACKER.xlsx` completely
2. List EVERY component with status "RICEVUTO" (actually received)
3. Verify Raspberry Pi 4 8GB availability (critical for testing)
4. Check if LED rings, sensors, audio components are in hand
5. Create definitive "CAN USE TODAY" vs "WAITING FOR" lists
6. Flag any ambiguous status entries for user confirmation

**Output Format:**
```markdown
## COMPONENTS AVAILABLE FOR IMMEDIATE USE
- [Component name] - [Quantity] - [Purpose] - [Verified: YES/NO]

## COMPONENTS IN TRANSIT (ETA)
- [Component name] - [ETA date] - [Impact on plan]

## CRITICAL GAPS (Blocking factors)
- [Missing component] - [Why it blocks work] - [Action needed]
```

---

### AGENT 2: "SOFTWARE ARCHITECT"
**Objective:** Design complete firmware structure for 7-day development sprint

**Tasks:**
1. Read existing documentation:
   - `electronics/pin_assignment.md` (GPIO mapping)
   - `docs/` folder (hardware architecture)
   - Any existing code in `firmware/` or `repos/Open_Duck_Mini_Runtime`
2. Design modular firmware architecture:
   - Hardware abstraction layer (drivers)
   - Kinematics engine (IK solver)
   - Gait controller
   - Sensor fusion module
   - Safety/error handling
3. Create folder structure with detailed purpose for each module
4. Define interfaces between modules (APIs)
5. Specify testing strategy for each component
6. Estimate development time per module (realistic, not optimistic)

**Output Format:**
```markdown
## FIRMWARE ARCHITECTURE v1.0

### Folder Structure
[Complete tree with descriptions]

### Module Specifications
#### Module: [Name]
- **Purpose:**
- **Dependencies:**
- **Key Classes/Functions:**
- **Testing Strategy:**
- **Development Time:** X hours
- **Can Start:** YES/NO (if NO, why?)

### Development Priority Order
1. [Module] - [Why first]
2. [Module] - [Dependencies satisfied by #1]
...
```

---

### AGENT 3: "DAILY TASK PLANNER"
**Objective:** Create hour-by-hour task breakdown for Days 1-7

**Constraints:**
- User has ~4-6 hours productive time per day
- Must account for delivery reception windows
- No 3D printing tasks (printer not available)
- Focus on code development + available hardware testing
- Each task must have clear success criteria

**Tasks:**
1. Review Agent 1's component availability list
2. Review Agent 2's firmware architecture
3. Create day-by-day breakdown (14-20 January):
   - Morning block (2-3 hours)
   - Afternoon block (2-3 hours)
   - Evening block (optional, 1-2 hours)
4. Each task must specify:
   - Estimated time
   - Required components
   - Success criteria (measurable)
   - Output/deliverable
5. Include contingency tasks (if component not available, do X instead)

**Output Format:**
```markdown
## DAY 1 - Tuesday 14/01 (TODAY)
**Available time:** 5 hours
**Components needed:** [List]

### Block 1: Evening (19:00-21:00) - 2 hours
**Task:** [Name]
- **What to do:** [Specific actions]
- **Components needed:** [List]
- **Success criteria:** [Measurable outcome]
- **Deliverable:** [File/document/result]
- **If blocked:** [Alternative task]

[Repeat for each block and each day]
```

---

### AGENT 4: "HOSTILE REVIEWER - DEPENDENCIES"
**Objective:** Challenge all assumptions and dependencies ruthlessly

**Tasks:**
1. Review all three agents' outputs
2. For EVERY task, ask:
   - Can this actually be done with available components?
   - Are we SURE component X is available? Where's the proof?
   - Is this dependency real or artificial?
   - Why can't this start earlier?
   - What's the REAL blocker (not excuses)?
3. Identify false dependencies and artificial delays
4. Challenge optimistic time estimates
5. Flag vague success criteria
6. Verify that "can't do without printer" claims are valid

**Output Format:**
```markdown
## DEPENDENCY CHALLENGE REPORT

### Agent 1 (Components) - Issues Found: X
**Issue 1:** [Description]
- **Problem:** [Why this is wrong/uncertain]
- **Evidence:** [What makes me doubt this]
- **Action:** [What to verify/fix]

### Agent 2 (Architecture) - Issues Found: X
[Same structure]

### Agent 3 (Tasks) - Issues Found: X
[Same structure]

### CRITICAL FINDINGS
1. [Most serious issue that would derail the plan]
2. [Second most serious]
...

### RECOMMENDATIONS
- [Specific changes to make plan more realistic]
```

---

### AGENT 5: "HOSTILE REVIEWER - FEASIBILITY"
**Objective:** Verify technical feasibility and realistic time estimates

**Tasks:**
1. Review all agents' outputs
2. For each software module:
   - Is development time realistic? (challenge optimism)
   - Can this be tested without full hardware?
   - Is the architecture over-engineered or under-specified?
3. For each hardware test:
   - Is wiring/setup time included?
   - Are troubleshooting contingencies planned?
   - What if component doesn't work as expected?
4. Check for scope creep:
   - Is this task necessary for Week 01?
   - Can this wait until Week 02?
   - Are we adding "nice to have" features?
5. Verify success criteria are measurable and achievable

**Output Format:**
```markdown
## FEASIBILITY AUDIT REPORT

### Software Development Assessment
**Module:** [Name]
- **Estimated time:** [Agent 2's estimate]
- **Realistic time:** [Your challenge/validation]
- **Risk factors:** [What could go wrong]
- **Recommendation:** [Accept/Revise/Defer]

### Hardware Testing Assessment
[Same structure]

### Overall Plan Feasibility
- **Optimistic completion:** X%
- **Realistic completion:** Y%
- **High-risk items:** [List]
- **Should be deferred:** [List]

### TIME BUDGET REALITY CHECK
- **Total planned hours:** XX
- **Available hours:** YY
- **Buffer needed:** ZZ
- **Verdict:** OVERLOADED / BALANCED / CONSERVATIVE
```

---

## SYNTHESIS REQUIREMENTS

After all 5 agents complete their work:

1. **Consolidated Week 01 Roadmap v2.0:**
   - Incorporate all agent findings
   - Resolve conflicts between agents
   - Create final day-by-day task list
   - Include realistic success metrics
   - Document known risks and blockers

2. **Component Verification Checklist:**
   - List for user to physically verify what's available
   - Priority order (what to check first)

3. **Software Development Roadmap:**
   - Prioritized module development order
   - Testing strategy per module
   - Integration checkpoints

4. **48-Hour Action Plan (14-15 January):**
   - Immediate next steps
   - No ambiguity, only concrete actions
   - Checkbox format for tracking

---

## SUCCESS CRITERIA FOR THIS RE-EVALUATION

The new plan is successful if:

- [ ] Every task specifies EXACT components needed (verified available)
- [ ] No tasks depend on unavailable hardware (printer, batteries, leg servos)
- [ ] Software development path is clear and modular
- [ ] Daily time estimates are realistic (not optimistic)
- [ ] Success criteria are measurable (not "make progress")
- [ ] Blockers are clearly identified with mitigation plans
- [ ] User can start work TODAY with available components
- [ ] Plan accounts for delivery reception windows
- [ ] Hostile reviews identified and resolved critical issues
- [ ] Final plan is HONEST about constraints, not aspirational

---

## CONTEXT FILES TO READ

**Essential:**
- `Planning/Week_01/ROADMAP_WEEK_01.md` (current plan to replace)
- `OPENDUCK_V3_FINAL_TRACKER.xlsx` (component status)
- `electronics/power_budget.md` (power architecture)
- `electronics/pin_assignment.md` (GPIO mapping)

**Helpful:**
- `Planning/Week_01/SOFTWARE_FIRST_PLAN.md` (software development guide)
- `Planning/Week_01/ACTION_CHECKLIST_48H.md` (immediate tasks)
- `DUAL_UBEC_SETUP_SUMMARY.md` (power system design)
- `docs/` folder (architecture documentation)

**If exists:**
- `firmware/` or `repos/Open_Duck_Mini_Runtime` (existing code)

---

## OUTPUT DELIVERABLES

1. **Component_Verification_Report.md** (Agent 1)
2. **Firmware_Architecture_v1.0.md** (Agent 2)
3. **Week_01_Daily_Tasks_v2.0.md** (Agent 3)
4. **Hostile_Review_Dependencies.md** (Agent 4)
5. **Hostile_Review_Feasibility.md** (Agent 5)
6. **ROADMAP_WEEK_01_v2.0.md** (Final consolidated plan)
7. **IMMEDIATE_ACTION_14_01.md** (Next 24 hours, checkbox format)

---

## EXECUTION NOTES

- Agents must provide EVIDENCE for claims (file quotes, line numbers)
- No assumptions without verification
- Challenge everything, especially "can't do until X arrives"
- Focus on PRODUCTIVE work, not busy work
- Realistic > optimistic
- Honest > aspirational

---

*This prompt designed to produce a realistic, achievable Week 01 plan that maximizes progress despite hardware constraints.*
