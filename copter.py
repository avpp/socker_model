from baseGameClasses import *;
from copterPlayer import *;

class Copter(movableObject):
	def __init__(self, x, y, plarr):
		movableObject.__init__(self, x, y);
		self.prp = [];
		for pl in plarr:
			self.prp.append(copterPlayer(pl));
	def think(self):
		for p in self.prp:
			p.KalmanFilter();
	def draw(self, sf, xoff, yoff):
		for p in self.prp:
			p.draw(sf, xoff, yoff);
		
