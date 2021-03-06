from baseGameClasses import *;
import numpy as np;
import pygame as pg;

# X - state.
# U - external motions
# P - uncirtainty (covariation) matrix.
# F - next state function
# H - measurement function
# R - measurement uncirtainty
# I - identity matrix

class copterPlayer(drawableObject):
#	F = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.double);
	U = np.array([[0, 0, 0, 0]], np.double).T;
	H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.double);
	R = np.array([[0.01, 0], [0, 0.01]], np.double);
	def __init__(self, realPlayer):
		self.pl = realPlayer;
		self.X = np.array([[self.pl.x, self.pl.y, 0, 0]], np.double).T;
		#self.X = np.array([[0, 0, 0, 0]], np.double).T;
		self.P = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 10, 0],[0, 0, 0, 10]], np.double);
		#self.P = np.array([[100, 0, 0, 0], [0, 100, 0, 0], [0, 0, 100, 0],[0, 0, 0, 100]], np.double);
		self.t = pg.time.Clock();
		self.t.tick_busy_loop();
	def prediction(self, u=None):
		if u == None:
			u = self.U;
		dt = float(self.t.tick_busy_loop())/1000;
		
		F = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]], np.double);
		self.X = np.dot(F, self.X)# + u;
		self.P = np.dot(np.dot(F, self.P), F.T);
		print self.pl.name, self.pl.x, self.pl.y,self.pl.vx,self.pl.vy;
		print self.X;
	def measurement(self, Z):
		y = Z - np.dot(self.H, self.X);
		S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R;
		K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S));
		self.X = self.X + np.dot(K, y);
		self.P = np.dot((np.identity(4) - np.dot(K, self.H)), self.P);
	def KalmanFilter(self):
		self.prediction();
		self.measurement(self.get_measurement());
#		self.prediction();
	def get_measurement(self):
		return np.array([[self.pl.x, self.pl.y]]).T;
	def draw (self, sf, xoff, yoff):
		pg.draw.circle(sf, pg.Color(0, 0, 0), (int(self.X[0]) + xoff, int(self.X[1]) + yoff), 2, 1);
		pg.draw.circle(sf, pg.Color(0, 0, 0), (int(self.X[0]) + xoff, int(self.X[1]) + yoff), int(self.P[0][0]*1000) + 1, 1);
		pg.draw.line(sf, pg.Color(0, 0, 0), (int(self.X[0]) + xoff, int(self.X[1]) + yoff), (int(self.X[0] + self.X[2]) + xoff, int(self.X[1] + self.X[3]) + yoff), 2);
