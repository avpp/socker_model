import pygame as pg;
import math;
import random;
from myGauss import *;
from baseGameClasses import *;

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
