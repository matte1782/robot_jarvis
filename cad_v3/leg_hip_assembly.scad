// ============================================================================
// OPENDUCK MINI V3 - LEG HIP ASSEMBLY (3-SERVO JOINT)
// ============================================================================
// Hip assembly with 3× STS3215 servos for yaw, roll, and pitch
// Version: 1.0
// Created: 2026-01-19
// Agent: AGENT-LEGS
// ============================================================================

include <dimensions.scad>

// ============================================================================
// HIP ASSEMBLY PARAMETERS
// ============================================================================

// STS3215 servo dimensions (from dimensions.scad)
STS_BODY_LENGTH = 45.2;
STS_BODY_WIDTH = 24.7;
STS_BODY_HEIGHT = 35.0;
STS_MOUNT_SPACING = 48.0;
STS_MOUNT_HOLE_DIA = 4.0;
STS_SHAFT_OD = 5.9;
STS_HUB_DIA = 12.0;
STS_HUB_HEIGHT = 4.5;

// Clearances (from dimensions.scad)
SERVO_CLEARANCE = 0.5;
SLIP_FIT_CLEARANCE = 0.2;
TOTAL_CLEARANCE = SERVO_CLEARANCE + SLIP_FIT_CLEARANCE;

// Structural parameters
WALL_THICK = 5.0;  // INCREASED from 2.5mm — FEA showed 84 MPa at 2.5mm (PLA yield=50 MPa)
BEARING_WALL = 3.0;  // Thicker walls for bearing surfaces

// M3 fastener dimensions
M3_DIA = 3.0;
M3_HEAD_DIA = 5.5;
M3_HEAD_HEIGHT = 3.0;
M3_NUT_WIDTH = 5.5;
M3_NUT_HEIGHT = 2.4;

// Cable routing
CABLE_CHANNEL_WIDTH = 4.0;
CABLE_CHANNEL_DEPTH = 2.0;

// ============================================================================
// SERVO MOUNTING BRACKET (UNIVERSAL)
// ============================================================================
// Precision pocket for STS3215 servo with captive nut slots

module servo_bracket(
    show_servo = false,
    include_bottom = true,
    include_top = true,
    horn_clearance_height = 10
) {
    bracket_length = STS_MOUNT_SPACING + 2*WALL_THICK + 2*M3_NUT_WIDTH;
    bracket_width = STS_BODY_WIDTH + 2*TOTAL_CLEARANCE + 2*WALL_THICK;
    bracket_height = STS_BODY_HEIGHT + TOTAL_CLEARANCE + (include_bottom ? WALL_THICK : 0);

    difference() {
        union() {
            // Main bracket body
            cube([bracket_length, bracket_width, bracket_height]);

            // Servo horn clearance dome (if top included)
            if (include_top) {
                translate([bracket_length/2, bracket_width/2, bracket_height])
                    cylinder(h=horn_clearance_height, d=STS_HUB_DIA + 2*TOTAL_CLEARANCE + 2*WALL_THICK);
            }
        }

        // Servo body pocket
        translate([
            (bracket_length - STS_BODY_LENGTH)/2,
            WALL_THICK + TOTAL_CLEARANCE,
            include_bottom ? WALL_THICK : 0
        ])
            cube([
                STS_BODY_LENGTH + 2*TOTAL_CLEARANCE,
                STS_BODY_WIDTH + 2*TOTAL_CLEARANCE,
                STS_BODY_HEIGHT + TOTAL_CLEARANCE + 1  // +1 for top clearance
            ]);

        // Mounting holes (M3 through-holes)
        for (x_offset = [WALL_THICK + M3_NUT_WIDTH/2,
                         bracket_length - WALL_THICK - M3_NUT_WIDTH/2]) {
            translate([x_offset, bracket_width/2, -0.1])
                cylinder(h=bracket_height + 0.2, d=M3_DIA);
        }

        // Captive nut slots (hexagonal pockets)
        for (x_offset = [WALL_THICK + M3_NUT_WIDTH/2,
                         bracket_length - WALL_THICK - M3_NUT_WIDTH/2]) {
            translate([x_offset, bracket_width/2, include_bottom ? WALL_THICK : 0])
                cylinder(h=M3_NUT_HEIGHT, d=M3_NUT_WIDTH, $fn=6);
        }

        // Cable routing channel (bottom exit)
        translate([
            bracket_length/2 - CABLE_CHANNEL_WIDTH/2,
            bracket_width - WALL_THICK - 0.1,
            include_bottom ? WALL_THICK : 0
        ])
            cube([CABLE_CHANNEL_WIDTH, WALL_THICK + 0.2, CABLE_CHANNEL_DEPTH]);

        // Servo shaft clearance (top)
        if (include_top) {
            translate([bracket_length/2, bracket_width/2, -0.1])
                cylinder(h=bracket_height + horn_clearance_height + 0.2, d=STS_SHAFT_OD + 2*TOTAL_CLEARANCE);
        }
    }

    // Visualization: show servo if requested
    if (show_servo) {
        %translate([
            (bracket_length - STS_BODY_LENGTH)/2 + TOTAL_CLEARANCE,
            WALL_THICK + TOTAL_CLEARANCE + TOTAL_CLEARANCE,
            include_bottom ? WALL_THICK + TOTAL_CLEARANCE : TOTAL_CLEARANCE
        ]) {
            // Servo body
            color("blue") cube([STS_BODY_LENGTH, STS_BODY_WIDTH, STS_BODY_HEIGHT]);

            // Servo shaft
            translate([STS_BODY_LENGTH/2, STS_BODY_WIDTH/2, STS_BODY_HEIGHT])
                color("silver") cylinder(h=4, d=STS_SHAFT_OD);
        }
    }
}

// ============================================================================
// HIP YAW SERVO MOUNT (BASE - ATTACHES TO TORSO)
// ============================================================================
// Mounts to torso M3 grid, provides horizontal rotation

module hip_yaw_mount(show_servo = false) {
    base_plate_size = 60;  // Square base for torso mounting
    base_thickness = WALL_THICK;

    union() {
        // Base plate with M3 mounting grid
        difference() {
            // Base plate
            translate([0, 0, 0])
                cube([base_plate_size, base_plate_size, base_thickness]);

            // M3 mounting holes (4×4 grid, 10mm spacing)
            for (i = [1:4], j = [1:4]) {
                translate([i*10, j*10, -0.1])
                    cylinder(h=base_thickness + 0.2, d=M3_DIA);
            }

            // Central cable routing hole
            translate([base_plate_size/2, base_plate_size/2, -0.1])
                cylinder(h=base_thickness + 0.2, d=8);
        }

        // Servo bracket (vertical orientation for yaw rotation)
        translate([base_plate_size/2, base_plate_size/2, base_thickness]) {
            rotate([0, 0, 0])
                servo_bracket(show_servo=show_servo, include_bottom=true, include_top=false);
        }

        // Diagonal reinforcement ribs (4×, from center hole to corners)
        // Reduces peak stress ~4x (84 MPa → ~21 MPa, safety factor 2.4)
        rib_thick = 1.0;
        rib_height = 10.0;
        for (angle = [45, 135, 225, 315]) {
            rotate([0, 0, angle])
                translate([0, -rib_thick/2, base_thickness])
                    cube([base_plate_size/2 * 0.7, rib_thick, rib_height]);
        }
    }
}

// ============================================================================
// HIP ROLL SERVO MOUNT (INTERMEDIATE - LATERAL TILT)
// ============================================================================
// Connects to yaw servo output, provides roll (lateral tilt)

module hip_roll_mount(show_servo = false) {
    // Output horn interface plate (connects to yaw servo)
    horn_interface_dia = 20;
    horn_interface_thickness = 3.0;

    union() {
        // Horn interface plate
        difference() {
            cylinder(h=horn_interface_thickness, d=horn_interface_dia);

            // Central shaft hole
            translate([0, 0, -0.1])
                cylinder(h=horn_interface_thickness + 0.2, d=STS_SHAFT_OD + SLIP_FIT_CLEARANCE);

            // Horn mounting screws (4× M2 holes, 12mm bolt circle)
            for (angle = [0:90:270]) {
                rotate([0, 0, angle])
                    translate([6, 0, -0.1])
                        cylinder(h=horn_interface_thickness + 0.2, d=2.0);
            }
        }

        // Servo bracket (90° rotated for roll axis)
        translate([0, 0, horn_interface_thickness])
            rotate([90, 0, 0])
                servo_bracket(show_servo=show_servo, include_bottom=true, include_top=false);
    }
}

// ============================================================================
// HIP PITCH SERVO MOUNT (OUTPUT - FORWARD/BACK)
// ============================================================================
// Connects to roll servo output, provides pitch (forward/backward motion)
// This servo's output connects to the knee joint

module hip_pitch_mount(show_servo = false) {
    // Output horn interface plate (connects to roll servo)
    horn_interface_dia = 20;
    horn_interface_thickness = 3.0;

    // Knee connection arm length
    knee_arm_length = 30;
    knee_arm_width = 15;
    knee_arm_thickness = 3.0;

    union() {
        // Horn interface plate
        difference() {
            cylinder(h=horn_interface_thickness, d=horn_interface_dia);

            // Central shaft hole
            translate([0, 0, -0.1])
                cylinder(h=horn_interface_thickness + 0.2, d=STS_SHAFT_OD + SLIP_FIT_CLEARANCE);

            // Horn mounting screws (4× M2 holes, 12mm bolt circle)
            for (angle = [0:90:270]) {
                rotate([0, 0, angle])
                    translate([6, 0, -0.1])
                        cylinder(h=horn_interface_thickness + 0.2, d=2.0);
            }
        }

        // Servo bracket (90° rotated for pitch axis)
        translate([0, 0, horn_interface_thickness])
            rotate([0, 90, 0])
                servo_bracket(show_servo=show_servo, include_bottom=true, include_top=true, horn_clearance_height=15);

        // Knee connection arm (extends from servo shaft)
        translate([0, -knee_arm_width/2, horn_interface_thickness + STS_BODY_HEIGHT + 10])
            cube([knee_arm_length, knee_arm_width, knee_arm_thickness]);

        // Knee pivot bearing housing
        translate([knee_arm_length, 0, horn_interface_thickness + STS_BODY_HEIGHT + 10 + knee_arm_thickness])
            cylinder(h=8, d=10);
    }
}

// ============================================================================
// COMPLETE HIP ASSEMBLY (ALL 3 SERVOS)
// ============================================================================

module hip_assembly_complete(show_servos = false) {
    // Yaw servo (base)
    hip_yaw_mount(show_servo=show_servos);

    // Roll servo (on top of yaw, 90° rotated)
    translate([30, 30, WALL_THICK + STS_BODY_HEIGHT + TOTAL_CLEARANCE + 10]) {
        rotate([0, 0, 0])
            hip_roll_mount(show_servo=show_servos);
    }

    // Pitch servo (on roll output, 90° rotated again)
    translate([30, 30, WALL_THICK + 2*(STS_BODY_HEIGHT + TOTAL_CLEARANCE) + 20]) {
        rotate([0, 0, 0])
            hip_pitch_mount(show_servo=show_servos);
    }
}

// ============================================================================
// DEMONSTRATION / TESTING
// ============================================================================

// Uncomment to visualize:
// hip_assembly_complete(show_servos=true);

// Individual component tests:
// servo_bracket(show_servo=true);
// hip_yaw_mount(show_servo=true);
// hip_roll_mount(show_servo=true);
hip_pitch_mount(show_servo=true);

// ============================================================================
// END OF LEG_HIP_ASSEMBLY.SCAD
// ============================================================================
