import sys;
import pygame as pg;
from pygame.locals import *;
from worldModel import *;

pg.init();
fpsClock = pg.time.Clock();

wnd = pg.display.set_mode((640, 480));
sf = pg.Surface((640, 480), SRCALPHA);
curPos = [0, 0];
isMouseDown = False;

wm = worldModel(sf);
while True:
	sf.fill(Color(128, 128, 128, 100));
	wm.iteration();
	wm.drawAll();
	for event in pg.event.get():
		if event.type == QUIT:
			pg.quit();
			sys.exit();
		elif event.type == MOUSEBUTTONUP:
			if event.button == 3:
				wm.kick_ball(event.pos[0] - curPos[0], event.pos[1] - curPos[1]);
		elif event.type == MOUSEMOTION:
			if event.buttons[0]:
				curPos = [curPos[0] + event.rel[0], curPos[1] + event.rel[1]];
	wnd.fill(Color(0,0,0));
	wnd.blit(sf, curPos);
	pg.display.update();
	fpsClock.tick_busy_loop(30);
