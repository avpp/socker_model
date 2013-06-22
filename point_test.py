import pygame as pg;
import copter;
import baseGameClasses as bg;
import worldModel as wm;
from ball import *;
from field import *;
from math import *;

class point(bg.movableObject):
	def __init__(self, x, y, vx, vy):
		movableObject.__init__(self, x, y);
		self.vx = vx;
		self.vy = vy;
		self.a_mod = 0;
		self.defColor = pg.Color(250, 250, 250);
		self.defSize = 5;
		self.name = 'point';
	def think(self):
		self.vx = 20;
		self.vy = 20*sin(self.x*0.1);

class worldModel(wm.worldModel):
	def __init__(self, sf):
		self.sf = sf;
		self.objects = [];
		self.ball = Ball();
		self.goals = [];
		self.field = Field(300, 200, self.ball, self.goals);
		self.myPoint = point(-130, -110, 0, 30);
		self.t1pl = [];
		self.t2pl = [];
		self.copter = copter.Copter(-100, 0, [self.myPoint]);
		self.fontObj = pg.font.Font(pg.font.get_default_font(), 15);
		self.fontObj = pg.font.Font(pg.font.get_default_font(), 15);
		self.objects.append(self.field);
		self.objects.append(self.ball);
		self.objects.append(self.myPoint);
		self.objects.append(self.copter);
		self.fontObj = pg.font.Font(pg.font.get_default_font(), 15);
