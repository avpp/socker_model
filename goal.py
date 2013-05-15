import pygame as pg;
from baseGameClasses import *;

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
