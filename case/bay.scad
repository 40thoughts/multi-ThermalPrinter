//// VARS

w_th = 3;
wid = 103.5;
hei = 57;
dep = 50;
co_wid = 150;
co_hei = 87.5;
co_dep = 5;
fr_hei = 65.5;
fr_wid = 111.5;
fr_dep = 3;
h_v_spa = 43;
h_rad = 1;
bay_w = 147;
f_h_dis = 52;
s_dep = 57;
pad = 0.1;		// DON'T TOUCH THIS LINE
$fn = 50;
//$fn = 150;			// DON'T TOUCH THIS LINE
//wid = 170;		// Width
//hei = 75;			// Height
//len = 40;			// Length
//f_th = 5;			// Front thickness
//b_th = 5;			// Back thickness
//i_th = 2.5;		// Inward thickness
//l_rad = 2.5;		// Led radius
//v_led_sp = 40;	// Vertical space between leds
//l_e_sp = 7.5;	// space between led center and inner edge
//s_rad = 1.5;		// Screws radius
//s_h_dep = 3;		// Screw head depth
//s_h_rad = 3;		// Screw head radius
//s_dep = 10;		// Screw hole depth
//v_nb_led = 4 - 1;

difference() {
	union() {
//		translate([0, 0, (co_dep / 2)]) cube(size = [co_wid, co_hei, co_dep], center = true);
		translate([-((bay_w / 2) - ((bay_w - wid) / 4)), -(h_v_spa / 2), ((s_dep / 2) + co_dep)]) cube(size = [((bay_w - wid) / 2), w_th, s_dep], center = true);
		translate([-((bay_w / 2) - ((bay_w - wid) / 4)), (h_v_spa / 2), ((s_dep / 2) + co_dep)]) cube(size = [((bay_w - wid) / 2), w_th, s_dep], center = true);
//		translate([((bay_w / 2) - ((bay_w - wid) / 4)), (h_v_spa / 2), ((s_dep / 2) + co_dep)]) cube(size = [((bay_w - wid) / 2), w_th, s_dep], center = true);
//		translate([((bay_w / 2) - ((bay_w - wid) / 4)), -(h_v_spa / 2), ((s_dep / 2) + co_dep)]) cube(size = [((bay_w - wid) / 2), w_th, s_dep], center = true);
		translate([-((bay_w / 2) - ((bay_w - wid) / 4)), 0, ((s_dep / 2) + co_dep)]) cube(size = [w_th, (h_v_spa - w_th), s_dep], center = true);
//		translate([((bay_w / 2) - ((bay_w - wid) / 4)), 0, ((s_dep / 2) + co_dep)]) cube(size = [w_th, (h_v_spa - w_th), s_dep], center = true);
	}
	union() {
//		translate([0, 0, ((dep / 2) - pad)]) cube(size = [wid, hei, (dep + pad)], center = true);
		translate([0, 0, ((fr_dep / 2) - pad)]) cube(size = [fr_wid, fr_hei, (fr_dep + pad)], center = true);
		translate([-((bay_w - w_th) / 2), -(h_v_spa / 2), f_h_dis]) rotate([0, 90, 0]) cylinder(h = (w_th + (pad * 2)), r = h_rad, center = true);
		translate([-((bay_w - w_th) / 2), (h_v_spa / 2), f_h_dis]) rotate([0, 90, 0]) cylinder(h = (w_th + (pad * 2)), r = h_rad, center = true);
		translate([((bay_w - w_th) / 2), (h_v_spa / 2), f_h_dis]) rotate([0, 90, 0]) cylinder(h = (w_th + (pad * 2)), r = h_rad, center = true);
		translate([((bay_w - w_th) / 2), -(h_v_spa / 2), f_h_dis]) rotate([0, 90, 0]) cylinder(h = (w_th + (pad * 2)), r = h_rad, center = true);
	}
}





//// MODULES

//module case() {
//	union() {
//		intersection() {
//			union() {
//				translate([0, -((len + f_th) / 2), 0]) cube(size = [wid, f_th, hei], center = true);
//				translate([0, ((len + b_th) / 2), 0]) cube(size = [wid, b_th, hei], center = true);
//			}
//			scale([1.2,0.5,2]) sphere(r = 75);
//		}
//
//
//		difference() {
//			cube(size = [(70 + (l_e_sp * 2)), len, (v_led_sp + (l_e_sp * 2))], center = true);
//			cube(size = [(70 + (l_e_sp * 2) - (i_th * 2)), len + pad, (v_led_sp + (l_e_sp * 2) - (i_th * 2))], center = true);
//		}
//	}
//}
//
//module ledHole() {
//	union() {
//		translate([-35, -((len + f_th) / 2), -(v_led_sp / 2)]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		translate([-15, -((len + f_th) / 2), -(v_led_sp / 2)]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		translate([15, -((len + f_th) / 2), -(v_led_sp / 2)]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		translate([35, -((len + f_th) / 2), -(v_led_sp / 2)]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		
//		translate([-35, -((len + f_th) / 2), -((v_led_sp / 2) - ((v_led_sp / v_nb_led) * 1))]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		translate([-15, -((len + f_th) / 2), -((v_led_sp / 2) - ((v_led_sp / v_nb_led) * 1))]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		translate([15, -((len + f_th) / 2), -((v_led_sp / 2) - ((v_led_sp / v_nb_led) * 1))]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		translate([35, -((len + f_th) / 2), -((v_led_sp / 2) - ((v_led_sp / v_nb_led) * 1))]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		
//		translate([-15, -((len + f_th) / 2), -((v_led_sp / 2) - ((v_led_sp / v_nb_led) * 2))]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		translate([15, -((len + f_th) / 2), -((v_led_sp / 2) - ((v_led_sp / v_nb_led) * 2))]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		translate([35, -((len + f_th) / 2), -((v_led_sp / 2) - ((v_led_sp / v_nb_led) * 2))]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		
//		translate([-15, -((len + f_th) / 2), (v_led_sp / 2)]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//		translate([35, -((len + f_th) / 2), (v_led_sp / 2)]) rotate([90, 0, 0]) cylinder(h = (f_th + (pad * 2)), r = l_rad, center = true);
//	}
//}
//
//// Screw
//
//module screwa() {
//	rotate([-90, 0, 0]) {
//		cylinder(h = s_h_dep, r = s_h_rad);
//		translate([0, 0, (s_h_dep - pad)]) cylinder(h = (s_dep + pad), r = s_rad);
//	}
//}
//
//module screwb() {
//	rotate([90, 0, 0]) {
//		cylinder(h = s_h_dep, r = s_h_rad);
//		translate([0, 0, (s_h_dep - pad)]) cylinder(h = (s_dep + pad), r = s_rad);
//	}
//}


//// DESIGN

//difference() {
//	union() {
//		case();
//		translate([-((70 + (l_e_sp * 2)) / 2), 0, -((v_led_sp + (l_e_sp * 2)) / 2)]) rotate([90, 0, 0]) cylinder(h = len, r = (s_rad + i_th), center = true);
//		translate([-((70 + (l_e_sp * 2)) / 2), 0, ((v_led_sp + (l_e_sp * 2)) / 2)]) rotate([90, 0, 0]) cylinder(h = len, r = (s_rad + i_th), center = true);
//		translate([((70 + (l_e_sp * 2)) / 2), 0, -((v_led_sp + (l_e_sp * 2)) / 2)]) rotate([90, 0, 0]) cylinder(h = len, r = (s_rad + i_th), center = true);
//		translate([((70 + (l_e_sp * 2)) / 2), 0, ((v_led_sp + (l_e_sp * 2)) / 2)]) rotate([90, 0, 0]) cylinder(h = len, r = (s_rad + i_th), center = true);
//	}
//	union() {
//		ledHole();
//
//		translate([-((70 + (l_e_sp * 2)) / 2), -(((len + pad) / 2) + f_th), -((v_led_sp + (l_e_sp * 2)) / 2)]) screwa();
//		translate([-((70 + (l_e_sp * 2)) / 2), -(((len + pad) / 2) + f_th), ((v_led_sp + (l_e_sp * 2)) / 2)]) screwa();
//		translate([((70 + (l_e_sp * 2)) / 2), -(((len + pad) / 2) + f_th), -((v_led_sp + (l_e_sp * 2)) / 2)]) screwa();
//		translate([((70 + (l_e_sp * 2)) / 2), -(((len + pad) / 2) + f_th), ((v_led_sp + (l_e_sp * 2)) / 2)]) screwa();
//
//		translate([-((70 + (l_e_sp * 2)) / 2), (((len + pad) / 2) + b_th), -((v_led_sp + (l_e_sp * 2)) / 2)]) screwb();
//		translate([-((70 + (l_e_sp * 2)) / 2), (((len + pad) / 2) + b_th), ((v_led_sp + (l_e_sp * 2)) / 2)]) screwb();
//		translate([((70 + (l_e_sp * 2)) / 2), (((len + pad) / 2) + b_th), -((v_led_sp + (l_e_sp * 2)) / 2)]) screwb();
//		translate([((70 + (l_e_sp * 2)) / 2), (((len + pad) / 2) + b_th), ((v_led_sp + (l_e_sp * 2)) / 2)]) screwb();
//	}
//}