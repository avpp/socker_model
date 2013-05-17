import pygame as pg;
#import model;
from field import *;
from goal import *;
from ball import *;
from player import *;
from copter import *;
import math;

class worldModel:
	def __init__(self, sf):
		self.sf = sf;
		self.objects = [];
		self.ball = Ball();
		self.goals = [];
		self.goals.append(Goal(-163, -30, 15, 60));
		self.goals.append(Goal(149, -30, 15, 60));
		self.field = Field(300, 200, self.ball, self.goals);
		self.t1pl = [];
		self.t2pl = [];
		for i in range(0, 10):
			x =  40 + ((i+1)%3)*40;
			y = (-0.5 + 0.125)*self.field.height + 0.25*self.field.height*(i/3) + 0.5*0.125*self.field.height*(i%3)*((i+1)%3 + (i+2)%3);
			self.t1pl.append(Player(self.field, -x, y, 0, 0, pg.Color(255, 0, 0), 't1p' + str(i)));
			self.t2pl.append(Player(self.field,  x, y, 0, 1, pg.Color(0, 0, 255), 't2p' + str(i)));
		aaa = [];
		aaa.extend(self.t1pl);
		aaa.extend(self.t2pl);
		self.copter = Copter(0, -150, aaa);

		self.objects.append(self.field);
		self.objects.append(self.ball);
		self.objects.extend(self.goals);
		self.objects.extend(self.t1pl);
		self.objects.extend(self.t2pl);
		self.objects.append(self.copter);
		self.fontObj = pg.font.Font(pg.font.get_default_font(), 15);
	def drawAll(self):
		for o in self.objects:
			o.draw(self.sf, self.sf.get_width()/2, self.sf.get_height()/2);
		self.r1 = [];
		for i in range(0, len(self.t1pl)):
			p = self.t1pl[i];
			cl = p.color;
			if p.marked:
				cl = pg.Color(250, 250, 50);
			self.r1.append(self.sf.blit(self.fontObj.render(p.name+' '+str(int(p.energy)), False, cl), (5, 30 + i*25)));
		self.r2 = [];
		for i in range(0, len(self.t2pl)):
			p = self.t2pl[i];
			cl = p.color;
			
			if p.marked:
				cl = pg.Color(250, 250, 50);
			self.r2.append(self.sf.blit(self.fontObj.render(p.name+' '+str(int(p.energy)), False, cl), (550, 30 + i*25)));
		self.sf.blit(self.fontObj.render('Ball v=' + str(math.sqrt(self.ball.vx*self.ball.vx + self.ball.vy*self.ball.vy)) + ' lk=' + str(self.ball.tlk),False, pg.Color(0, 150, 0, 128)), (250, 350));
	def update(self):
		self;
	def iteration(self):
		self.update();
		for o in self.objects:
			o.update();
	def kick_ball(self, x, y):
		dx = x - self.sf.get_width()/2 - self.ball.x;
		dy = y - self.sf.get_height()/2 - self.ball.y;
		self.ball.kick(dx, dy);
	def mousePress(self, x, y):
		if x >= 0 and y >=0 and x <= self.sf.get_size()[0] and y <= self.sf.get_size()[1]:
			for i in range(0, len(self.t1pl)):
				if (x >= self.r1[i].x and y >= self.r1[i].y and x <= self.r1[i].x + self.r1[i].width and y <= self.r1[i].y + self.r1[i].height) or ((self.t1pl[i].x + self.sf.get_width()/2 - x)**2 + (self.t1pl[i].y + self.sf.get_height()/2 - y)**2 < 25):
					self.t1pl[i].mark();
			for i in range(0, len(self.t2pl)):
				if (x >= self.r2[i].x and y >= self.r2[i].y and x <= self.r2[i].x + self.r2[i].width and y <= self.r2[i].y + self.r2[i].height) or ((self.t2pl[i].x + self.sf.get_width()/2 - x)**2 + (self.t2pl[i].y + self.sf.get_height()/2 - y)**2 < 25):
					self.t2pl[i].mark();
