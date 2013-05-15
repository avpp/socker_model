import math;
from baseGameClasses import *;

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
