import math;

class Gauss:
	def __init__(self, mu, sigma):
		self.mu = mu;
		self.sigma = sigma;
	def value(self, x):
		k = 1./(self.sigma*math.sqrt(2.*math.pi));
		a = - (x - self.mu)*(x - self.mu)/(2.*self.sigma*self.sigma);
		return k*math.exp(a);
	def grad(self, x):
		k = (self.mu - x)/(self.sigma*self.sigma*self.sigma*math.sqrt(2*math.pi));
		a = - (x - self.mu)*(x - self.mu)/(2.*self.sigma*self.sigma);
		return k*math.exp(a);

class GaussND:
	def __init__(self, mss):
		self.mu = [];
		self.sigma = [];
		for ms in mss:
			self.mu.append(ms[0]);
			self.sigma.append(ms[1]);
	def value(self, x):
		k = 1.;
		for s in self.sigma:
			k = k*s;
		k = 1./(k*math.sqrt(math.pow(2*math.pi, len(self.sigma))));
		a = 0.0;
		for i in range(0, len(x)):
			a += (x[i] - self.mu[i])*(x[i] - self.mu[i])/(self.sigma[i]*self.sigma[i]);
		a = -a/2;
		return k*math.exp(a);
	def grad(self, n, x):
		return self.value(x)*2*(x[n] - self.mu[n])/(self.sigma[n]*self.sigma[n]);

def gauss(mu, sigma, x):
	return Gauss(mu, sigma).value(x);
def gradGauss(mu, sigma, x):
	return Gauss(mu, sigma).grad(x);

def gaussND(mss, x):
	return GaussND(mss).value(x);
def gradGaussND(mss, x):
	arr = [];
	for i in range(0, len(x)):
		arr.append(GaussND(mss).grad(i,x));
	return arr;
