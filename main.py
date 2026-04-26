"""Entry point for PMSM dq simulation with electrical and mechanical dynamics."""

import math

import matplotlib

from config import MECH_PARAMS, MOTOR_PARAMS, PI_D_PARAMS, PI_Q_PARAMS, SIM_PARAMS
from control.foc import FOCController
from control.pi import PI
from models.pmsm import PMSM
from simulation.simulator import run_simulation


def constant_iq_ref(value):
	def _profile(_t):
		return value

	return _profile


def step_iq_ref(t_step, initial, final):
	def _profile(t):
		if t < t_step:
			return initial
		return final

	return _profile


def main():
	motor = PMSM(**MOTOR_PARAMS)
	pi_d = PI(**PI_D_PARAMS)
	pi_q = PI(**PI_Q_PARAMS)
	controller = FOCController(pi_d=pi_d, pi_q=pi_q)

	if all(k in SIM_PARAMS for k in ("t_step", "iq_ref_initial", "iq_ref_final")):
		iq_ref_profile = step_iq_ref(
			SIM_PARAMS["t_step"],
			SIM_PARAMS["iq_ref_initial"],
			SIM_PARAMS["iq_ref_final"],
		)
	else:
		iq_ref_profile = constant_iq_ref(SIM_PARAMS.get("iq_ref", 0.0))

	result = run_simulation(
		motor=motor,
		controller=controller,
		t_end=SIM_PARAMS["t_end"],
		dt=SIM_PARAMS["dt"],
		omega=SIM_PARAMS["omega"],
		iq_ref_profile=iq_ref_profile,
		voltage_limit=SIM_PARAMS.get("v_dc"),
		mech_params=MECH_PARAMS,
	)

	print(f"samples: {len(result.time)}")
	print(f"id_final: {result.id_values[-1]:.4f} A")
	print(f"iq_final: {result.iq_values[-1]:.4f} A")
	print(f"iq_ref_final: {result.iq_ref_values[-1]:.4f} A")
	print(f"vd_final: {result.vd_values[-1]:.4f} V")
	print(f"vq_final: {result.vq_values[-1]:.4f} V")
	print(f"omega_final: {result.omega_values[-1]:.4f} rad/s")
	print(f"te_final: {result.te_values[-1]:.4f} N m")

	v_dc = float(SIM_PARAMS.get("v_dc", 200.0))
	v_dc_sq = v_dc * v_dc
	vd_req_values = getattr(result, "vd_req_values", result.vd_values)
	vq_req_values = getattr(result, "vq_req_values", result.vq_values)
	v_req_sq_values = [
		vd * vd + vq * vq for vd, vq in zip(vd_req_values, vq_req_values)
	]
	max_v_req = math.sqrt(max(v_req_sq_values)) if v_req_sq_values else 0.0
	sat_indices = [idx for idx, v_sq in enumerate(v_req_sq_values) if v_sq > v_dc_sq]
	sat_count = len(sat_indices)

	print("inverter_check:")
	print(f"  v_dc = {v_dc:.3f} V")
	print(f"  max_v_req = {max_v_req:.3f} V")
	print(f"  saturation_samples = {sat_count}/{len(result.time)}")
	if sat_count > 0:
		first_idx = sat_indices[0]
		print(f"  first_saturation_time = {result.time[first_idx]:.6f} s")
		print(f"  first_saturation_omega = {result.omega_values[first_idx]:.3f} rad/s")
	else:
		print("  no saturation detected")

	#try:
	import matplotlib
	matplotlib.use("QtAgg")
	import matplotlib.pyplot as plt

	fig, (ax_i, ax_w) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

	ax_i.plot(result.time, result.iq_values, label="iq")
	ax_i.plot(result.time, result.iq_ref_values, "--", label="iq_ref")
	ax_i.set_ylabel("Current [A]")
	ax_i.grid(True)
	ax_i.legend()

	ax_w.plot(result.time, result.omega_values, label="omega", color="tab:orange")
	ax_w.set_xlabel("Time [s]")
	ax_w.set_ylabel("Speed [rad/s]")
	ax_w.grid(True)
	ax_w.legend()

	fig.tight_layout()
	plt.show()
	#except ImportError:
		# Keep simulation runnable even if plotting dependency is not installed.
		#pass


if __name__ == "__main__":
	main()
