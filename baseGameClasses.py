import pygame as pg;

class drawableObject:
	defColor = pg.Color(0, 0, 0);
	defSize = 3;
	def draw(self, sf, xoff, yoff):
		if self.x == None:
			self.x = 0;
		if self.y == None:
			self.y = 0;
		pg.draw.circle(sf, self.defColor, (int(self.x+xoff), int(self.y+yoff)), self.defSize, 2);

class gameObject(drawableObject):
	x = .0;
	y = .0;
	width = .0;
	height = .0;
	def __init__(self, x = 0.0, y = 0.0, w = 0.0, h = 0.0):
		self.x = x;
		self.y = y;
		self.width = w;
		self.height = h;
	def get_center(self):
		return (self.x + self.width/2, self.y + self.width/2);
	def update(self):
		pass;
	def is_in(self, obj):
		return (obj.x <= self.x) and (self.x + self.width <= obj.x + obj.width) and (obj.y <= self.y) and (self.y + self.height <= obj.y + obj.height);

class movableObject(gameObject):
	vx = .0;
	vy = .0;
	ax = .0;
	ay = .0;
	a_mod = -0.47;
	t = None;
	def __init__(self, x = 0, y = 0):
		gameObject.__init__(self, x, y);
		self.t = pg.time.Clock();
		self.t.tick_busy_loop();
	def move(self):
		ms = self.t.tick_busy_loop();
		self.x = self.x + self.vx*ms*0.001;
		self.y = self.y + self.vy*ms*0.001;
		self.vx = self.vx + (self.vx*self.a_mod + self.ax)*ms*0.001;
		self.vy = self.vy + (self.vy*self.a_mod + self.ay)*ms*0.001;
	def think(self):
		pass
	def update(self):
		self.think();
		self.move();
