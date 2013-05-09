import pygame as pg;
import model;
import math;

class worldModel:
	def __init__(self, sf):
		self.sf = sf;
		self.objects = [];
		self.ball = model.Ball();
		self.goals = [];
		self.goals.append(model.Goal(-163, -30, 15, 60));
		self.goals.append(model.Goal(149, -30, 15, 60));
		self.field = model.Field(300, 200, self.ball, self.goals);
		self.t1pl = [];
		self.t2pl = [];
		for i in range(1, 9):
			self.t1pl.append(model.Player(self.field, -((i%3)*30 + 40),  ((i%5)*30 - 50), 0, 0, pg.Color(255, 0, 0), 't1p' + str(i)));
			self.t2pl.append(model.Player(self.field,  ((i%3)*30 + 40), -((i%5)*30 - 50), 0, 1, pg.Color(0, 0, 255), 't2p' + str(i)));
		self.objects.append(self.field);
		self.objects.append(self.ball);
		self.objects.extend(self.goals);
		self.objects.extend(self.t1pl);
		self.objects.extend(self.t2pl);
		self.fontObj = pg.font.Font(pg.font.get_default_font(), 15);
	def drawAll(self):
		for o in self.objects:
			o.draw(self.sf, self.sf.get_width()/2, self.sf.get_height()/2);
		for i in range(0, len(self.t1pl)):
			p = self.t1pl[i];
			self.sf.blit(self.fontObj.render(p.name+' '+str(int(p.energy)), False, pg.Color(255, 0, 0, 128)), (5, 30 + i*25));
		for i in range(0, len(self.t2pl)):
			p = self.t2pl[i];
			self.sf.blit(self.fontObj.render(p.name+' '+str(int(p.energy)), False, pg.Color(0, 0, 255, 128)), (550, 30 + i*25));
		self.sf.blit(self.fontObj.render('Ball v=' + str(math.sqrt(self.ball.vx*self.ball.vx + self.ball.vy*self.ball.vy)),False, pg.Color(0, 150, 0, 128)), (250, 350));
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
