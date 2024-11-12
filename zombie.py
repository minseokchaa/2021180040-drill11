import random
import math
import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 50
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.life = 2


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)

        if self.life == 0:
            game_world.remove_object(self)
            print ('zombie is dead again')
        pass


    def draw(self):
        if self.dir < 0:
            Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y*self.life+50, 100*self.life, 100*self.life)
        else:
            Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y*self.life+50, 100*self.life, 100*self.life)
        draw_rectangle(*self.get_bb())

        #draw_rectangle(self.x-1,self.y-1,self.x+1,self.y*self.life+50+1)

    def handle_event(self, event):
        pass

    def get_bb(self):
        # fill here
        if self.dir < 0:
            return self.x - 30*self.life, self.y, self.x + 30*self.life, self.y + 90*self.life      #4개의 값으로 구성된 하나의 패키지(튜플)을 넘겨줌
        else:
            return self.x - 30*self.life, self.y, self.x + 30*self.life, self.y + 90*self.life
        pass


    def handle_collision(self, group, other):
        # fill here
        if group == 'fired_ball:zombie':
            if self.life == 2:
                self.life = 2**(1/2)
                return

            if self.life == 2**(1/2):
                self.life = 0
        pass


