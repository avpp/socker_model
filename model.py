import pygame as pg;
import math;
import random;
from pprint import *;

class gameObject:
	x = .0;
	y = .0;
	width = .0;
	height = .0;
	def get_center(self):
		return (self.x + self.width/2, self.y + self.width/2);
	def update(self):
		self;
	def draw(self, sf, xoff, yoff):
		pg.draw.circle(sf, pg.Color(0, 0, 0), (x+xoff, y+yoff), 3, 2);
	def is_in(self, obj):
		return (obj.x <= self.x) and (self.x + self.width <= obj.x + obj.width) and (obj.y <= self.y) and (self.y + self.height <= obj.y + obj.height);

class movableObject(gameObject):
	vx = .0;
	vy = .0;
	ax = .0;
	ay = .0;
	a_mod = -0.7;
	t = None;
	def __init__(self):
		self.t = pg.time.Clock();
		self.t.tick_busy_loop();
	def move(self):
		ms = self.t.tick_busy_loop();
		self.x = self.x + self.vx*ms/1000;
		self.y = self.y + self.vy*ms/1000;
		self.vx = self.vx + (self.vx*self.a_mod + self.ax)*ms/1000;
		self.vy = self.vy + (self.vy*self.a_mod + self.ay)*ms/1000;
	def think(self):
		pass
	def update(self):
		self.think();
		self.move();
class Goal(gameObject):
	def __init__(self, x, y, width, height):
		self.x = x;
		self.y = y;
		self.width = width;
		self.height = height;
		self.goals = 0;
		self.fontObj = pg.font.Font(pg.font.get_default_font(), 15);
	def goal(self):
		self.goals += 1;
	def draw(self, sf, xoff, yoff):
		pg.draw.rect(sf, pg.Color(200, 200, 200), (self.x + xoff, self.y + yoff, self.width, self.height), 3);
		sf.blit(self.fontObj.render(str(self.goals), False, pg.Color(100,150, 200)), (self.x + 2 + xoff, self.y + self.height/2 - 7 + yoff));

class Field(gameObject):
	def __init__(self, width, height, ball = None, goals = []):
		self.width = width;
		self.height = height;
		self.x = - width/2;
		self.y = - height/2;
		self.goals = goals;
		self.ball = ball;
	def draw(self, sf, xoff, yoff):
		sf.fill(pg.Color(0,150,0), (xoff - self.width/2, yoff - self.height/2, self.width, self.height));
	def update(self):
		if self.ball == None:
			return;
		for g in self.goals:
			if self.ball.is_in(g):
				g.goal();
				self.ball.reset_position();
		if not self.ball.is_in(self):
			self.ball.stop_motion();
			nx=4*self.ball.x*self.ball.x - self.width*self.width;
			ny=4*self.ball.y*self.ball.y - self.height*self.height;
			if nx < 0:
				nx = -nx;
			if ny < 0:
				ny = -ny;
			if nx == 0:
				nx = ny + 1;
			if ny == 0:
				ny = nx + 1;
			if nx < ny:
				ny = self.ball.y;
				nx = self.width/2;
				if self.ball.x < 0:
					nx = -nx;
			else:
				nx = self.ball.x;
				ny = self.height/2;
				if self.ball.y < 0:
					ny = -ny;
			self.ball.reset_position(nx, ny);
class Ball(movableObject):
	def __init__(self, x = 0, y = 0, vx = 0, vy = 0):
		movableObject.__init__(self);
		self.x =  .0 + x;
		self.y =  .0 + y;
		self.vx = .0 + vx;
		self.vy = .0 + vy;
		self.time_last_kick = pg.time.Clock();
		self.time_last_kick.tick_busy_loop();
		self.tlk = 0;
#		self.ax = .0;
#		self.ay = .0;
#		self.a_mod = -0.5;#*math.sqrt(vx*vx + vy*vy);
#		self.t = pg.time.Clock();
#		self.t.tick_busy_loop();
	def draw(self, sf, xoff, yoff):
		pg.draw.circle(sf, pg.Color(255,255,255), (int(self.x + xoff), int(self.y + yoff)),5);
	def think(self):
		self.tlk += self.time_last_kick.tick_busy_loop();
#	def update(self):
#		ms = self.t.tick_busy_loop();
#		self.x = self.x + self.vx*ms/1000;
#		self.y = self.y + self.vy*ms/1000;
#		self.vx = self.vx + (self.vx*self.a_mod + self.ax)*ms/1000;
#		self.vy = self.vy + (self.vy*self.a_mod + self.ay)*ms/1000;
	def kick(self, dvx, dvy):
		k = (dvx**2 + dvy**2) / 100
		if k > 1:
			n = math.sqrt(1/k);
			dvx *= n;
			dvy *= n;
			
		self.vx = self.vx + dvx;
		self.vy = self.vy + dvy;
		self.tlk = 0;
		self.time_last_kick.tick_busy_loop();
	def set_const_accelerate(self, ax, ay):
		self.ax = ax;
		self.ay = ay;
	def stop_motion(self):
		self.vx = self.vy = self.ax = self.ay = .0;
	def reset_position(self, x = 0, y = 0):
		self.stop_motion();
		self.x = x;
		self.y = y;

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

class Player(movableObject):
	def __init__(self, field, x, y, role, teamNumber, color, name = ''):
		movableObject.__init__(self);
		self.field = field;
		self.m_x = x;
		self.m_y = y;
		self.x = x;
		self.y = y;
		self.vx = self.vy = self.ax = self.ay = 0;
		self.role = role;
		self.team = teamNumber;
		self.color = color;
		self.name = name;
		self.energy_max = 2000;
		self.energy_step = 5;
		self.energy = self.energy_max;
		self.a_mod = 0;
		self.marked = False;
	def think(self):
		self.a_mod = 1. - self.energy/self.energy_max;
		if self.energy <= self.energy_max - self.energy_step:
			self.energy += self.energy_step;
		if self.energy < 0:
			return;
		
		tlk = (1. * self.field.ball.tlk) / 1000;

		#want to ball
		dx = self.field.ball.x - self.x;
		dy = self.field.ball.y - self.y;
		d = math.sqrt(dx*dx + dy*dy);
		w1 = gradGaussND(((0,20), (0,20)), (dx, dy));
		w1d = gaussND(((0, 150), (0,150)), (dx, dy));
		w1dd = w1d / gaussND(((0, 150), (0, 150)), (0, 0));
		
#		wkb = 1;
#		if (self.field.goals[self.team].get_center()[0] - self.field.ball.x)**2 + (self.field.goals[self.team].get_center()[1] - self.field.ball.y)**2 < (self.field.goals[(self.team + 1)% 2].get_center()[0] - self.field.ball.x)**2 + (self.field.goals[(self.team + 1)% 2].get_center()[1] - self.field.ball.y)**2:
#			wkb += 1;

		wkb = (-0.2 + self.energy / self.energy_max)*2;
		
#		wkb = 1 - gauss(0, 100, self.field.ball.tlk);
#		wkbn = 1 +  10000000 * wkb / gauss(0, 100, 0);
		#want to start place
		dmx = self.m_x - self.x;
		dmy = self.m_y - self.y;
		w2 = gradGaussND(((0, 100), (0, 100)), (dmx, dmy));
		w2d = 1 - gaussND(((0, 150), (0, 150)), (dmx, dmy));
		w2dd = w2d / gaussND(((0, 150), (0, 150)), (0, 0));
		#want to attack
		og = self.field.goals[(self.team+1)%2];
		dogx = og.get_center()[0] - self.x;
		dogy = og.get_center()[1] - self.y;
		dogd = math.sqrt(dogx*dogx + dogy*dogy);
		wog  = gradGaussND(((self.x, 100), (self.y, 100)), (og.get_center()[0], og.get_center()[1]));
		wogd = 1 - gaussND(((self.x, 100), (self.y, 100)), (og.get_center()[0], og.get_center()[1]));
		wogdn = wogd / gaussND(((0, 100), (0, 100)), (0, 0));
		
		#change velocity
		self.vx  = w1[0]*w1dd*1000000*wkb;
		self.vy  = w1[1]*w1dd*1000000*wkb;
		self.vx += w2[0]*w2dd*1000;
		self.vy += w2[1]*w2dd*1000;

		self.vx += 2*dx*tlk/(d+1);
		self.vy += 2*dy*tlk/(d+1);
		
		self.vx += wog[0]*wogdn*1000;
		self.vy += wog[1]*wogdn*1000;
		
		self.vx = self.vx * (1 + random.gauss(0, 1)/10);
		self.vy = self.vy * (1 + random.gauss(0, 1)/10);

		#change accelerate
		self.ax  = w1[0]*w1dd;
		self.ay  = w1[1]*w1dd;
		self.ax += wog[0]*wogdn;
		self.ay += wog[1]*wogdn;
		

		de=self.energy*self.energy/(self.vx*self.vx + self.vy*self.vy);
#		if de < 1:
#			self.vx *= de;
#			self.vy *= de; 
		self.wx = self.vx;
		self.wy = self.vy;
		self.energy -= math.sqrt(self.vx*self.vx+self.vy*self.vy);

		#kick ball
		if self.energy > 7*self.energy_step and d < 10:
			k2 = 0.5 * gauss(0, 10, d)/gauss(0, 10, 0);
			c = self.field.goals[(self.team+1)%2].get_center();
			self.field.ball.kick(k2*(c[0]-self.x)*self.energy/self.energy_max*(1 + random.gauss(0, 2)), k2*(c[1]-self.y)*self.energy/self.energy_max*(1 + random.gauss(0, 2)));
			self.energy -= 3*self.energy_step;
	def draw(self, sf, xoff, yoff):
		pg.draw.circle(sf, self.color, (int(self.x) + xoff, int(self.y) + yoff), 5, 3);
		pg.draw.line(sf, self.color, (int(self.x) + xoff, int(self.y) + yoff), (int(self.x + self.wx) + xoff, int(self.y + self.wy) + yoff), 2);
		if self.marked:
			pg.draw.circle(sf, pg.Color(250, 250, 50), (int(self.x) + xoff, int(self.y) + yoff), 7, 2);
			sf.blit(pg.font.Font(pg.font.get_default_font(), 10).render(self.name, False, pg.Color(250, 250, 50)),(int(self.x) + xoff + 5, int(self.y) + yoff + 5));

	def mark(self):
		self.marked = not self.marked;
