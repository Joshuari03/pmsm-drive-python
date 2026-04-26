"""Simple PI controller."""


class PI:
	def __init__(self, kp, ki, u_min=None, u_max=None):
		self.kp = kp
		self.ki = ki
		self.u_min = u_min
		self.u_max = u_max
		self.integral = 0.0

	def step(self, error, dt):
		self.integral += error * dt
		u = self.kp * error + self.ki * self.integral

		if self.u_min is not None and u < self.u_min:
			u = self.u_min
		if self.u_max is not None and u > self.u_max:
			u = self.u_max

		return u
