"""Field oriented control current loop in d-q frame."""

from control.pi import PI


class FOCController:
	def __init__(self, pi_d: PI, pi_q: PI):
		self.pi_d = pi_d
		self.pi_q = pi_q

	def step(self, id_meas, iq_meas, iq_ref, dt, id_ref=0.0):
		err_d = id_ref - id_meas
		err_q = iq_ref - iq_meas

		vd = self.pi_d.step(err_d, dt)
		vq = self.pi_q.step(err_q, dt)
		return vd, vq
