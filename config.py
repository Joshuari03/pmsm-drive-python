"""Default configuration for PMSM dq simulation."""

MOTOR_PARAMS = {
	"Rs": 0.4,
	"Ld": 0.0012,
	"Lq": 0.0012,
	"psi_f": 0.06,
}

PI_D_PARAMS = {
	"kp": 10.0,
	"ki": 1200.0,
	"u_min": -200.0,
	"u_max": 200.0,
}

PI_Q_PARAMS = {
	"kp": 10.0,
	"ki": 1200.0,
	"u_min": -200.0,
	"u_max": 200.0,
}

MECH_PARAMS = {
	"J": 0.002,
	"pole_pairs": 4,
	"T_load": 0.2,
}

SIM_PARAMS = {
	"t_end": 3,
	"dt": 1e-4,
	"omega": 0.0,
	"v_dc": 200.0,
	"iq_ref": 8.0,
	"iq_ref_initial": 0.0,
	"iq_ref_final": 8.0,
	"t_step": 0.01,
}
