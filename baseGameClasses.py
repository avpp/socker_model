import pygame as pg;

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
