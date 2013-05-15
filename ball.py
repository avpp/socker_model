import pygame as pg;
import math;
from baseGameClasses import *;

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
