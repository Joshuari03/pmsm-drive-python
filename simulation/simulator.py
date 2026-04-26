"""Time-domain simulation loop for PMSM + FOC current control."""

from dataclasses import dataclass
import math


@dataclass
class SimulationResult:
	time: list
	id_values: list
	iq_values: list
	iq_ref_values: list
	vd_values: list
	vq_values: list
	vd_req_values: list
	vq_req_values: list
	omega_values: list
	te_values: list
	tl_values: list
	is_voltage_saturated: list


def _saturate_voltage_vector(vd, vq, v_limit):
	if v_limit is None:
		return vd, vq, False
	if v_limit <= 0.0:
		return 0.0, 0.0, True

	v_sq = vd * vd + vq * vq
	v_lim_sq = v_limit * v_limit
	if v_sq <= v_lim_sq:
		return vd, vq, False

	scale = v_limit / math.sqrt(v_sq)
	return vd * scale, vq * scale, True


def run_simulation(
	motor,
	controller,
	t_end,
	dt,
	omega,
	iq_ref_profile,
	voltage_limit=None,
	mech_params=None,
	tl_profile=None,
):
	steps = int(t_end / dt)
	omega_k = float(omega)

	result = SimulationResult(
		time=[],
		id_values=[],
		iq_values=[],
		iq_ref_values=[],
		vd_values=[],
		vq_values=[],
		vd_req_values=[],
		vq_req_values=[],
		omega_values=[],
		te_values=[],
		tl_values=[],
		is_voltage_saturated=[],
	)

	if mech_params is not None:
		J = float(mech_params["J"])
		pole_pairs = int(mech_params["pole_pairs"])
		default_tl = float(mech_params.get("T_load", 0.0))
	else:
		J = None
		pole_pairs = None
		default_tl = 0.0

	for k in range(steps):
		t = k * dt
		iq_ref = iq_ref_profile(t) if callable(iq_ref_profile) else float(iq_ref_profile)

		vd_req, vq_req = controller.step(
			id_meas=motor.id,
			iq_meas=motor.iq,
			iq_ref=iq_ref,
			dt=dt,
			id_ref=0.0,
		)
		vd, vq, is_sat = _saturate_voltage_vector(vd_req, vq_req, voltage_limit)
		id_val, iq_val = motor.step(vd=vd, vq=vq, omega=omega_k, dt=dt)

		if pole_pairs is not None:
			te = motor.electromagnetic_torque(pole_pairs)
			tl = tl_profile(t) if callable(tl_profile) else default_tl
			domega_dt = (te - tl) / J
			omega_k += domega_dt * dt
		else:
			te = 0.0
			tl = 0.0

		result.time.append(t)
		result.id_values.append(id_val)
		result.iq_values.append(iq_val)
		result.iq_ref_values.append(iq_ref)
		result.vd_values.append(vd)
		result.vq_values.append(vq)
		result.vd_req_values.append(vd_req)
		result.vq_req_values.append(vq_req)
		result.omega_values.append(omega_k)
		result.te_values.append(te)
		result.tl_values.append(tl)
		result.is_voltage_saturated.append(is_sat)

	return result
