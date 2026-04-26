"""PMSM electrical model in d-q coordinates."""


class PMSM:
	def __init__(self, Rs, Ld, Lq, psi_f):
		self.Rs = Rs
		self.Ld = Ld
		self.Lq = Lq
		self.psi_f = psi_f

		self.id = 0.0
		self.iq = 0.0

	def step(self, vd, vq, omega, dt):
		"""Advance the current state using forward Euler integration."""
		did_dt = (vd - self.Rs * self.id + omega * self.Lq * self.iq) / self.Ld
		diq_dt = (
			vq - self.Rs * self.iq - omega * (self.Ld * self.id + self.psi_f)
		) / self.Lq

		self.id += did_dt * dt
		self.iq += diq_dt * dt

		return self.id, self.iq

	def electromagnetic_torque(self, pole_pairs):
		"""Return electromagnetic torque for a PMSM in dq frame."""
		return 1.5 * pole_pairs * (
			self.psi_f * self.iq + (self.Ld - self.Lq) * self.id * self.iq
		)
