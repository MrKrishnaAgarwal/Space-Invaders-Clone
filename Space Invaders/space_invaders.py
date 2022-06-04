from ursina import *
from time import sleep
import sys
from random import randint

app = Ursina(title = 'Space Invaders', fullscreen = True, vsync = False, paused = True)
main_music = Audio('music.wav', loop = True)

player_texture = load_texture('spaceship.png')
background_texture = load_texture('background.png')
logo_texture = load_texture('logo.png')
start_button_texture = load_texture('start_button.png')
exit_button_texture = load_texture('exit_button.png')
alien_texture = load_texture('alien.png')
alien_two_texture = load_texture('alien_two.png')
alien_three_texture = load_texture('alien_three.png')

dx = dy = 0.007
start = False
bullets = []
invaders = []
invaders_two = []
invaders_three = []
spawn = True
end = False
score = 0

class Player(Entity):

	def __init__(self):
		super().__init__(
			model = 'cube',
			texture = player_texture,
			scale = (.6,.5,.01),
			position = (0,-3,0),
			collider = 'box')


	def update(self):

		global dx
		global dy

		if held_keys['d']:
			self.x += 10 * time.dt
		if held_keys['a']:
			self.x -= 10 * time.dt

class Bullet(Entity):
	def __init__(self):
		super().__init__(
			model = 'cube',
			position = (player.x, player.y + .4),
			scale = (.04,.2,0),
			color = color.rgb(0,255,10),
			collider = 'box')



class Invader(Entity):
	def __init__(self):
		super().__init__(
			model = 'cube',
			position = (randint(-4,4),9),
			scale = (1,1,0),
			texture = alien_texture,
			collider = 'box'
			)


	def input(self, key):
		if key == 'space':
			self.y -= 1


class Invader_two(Entity):
	def __init__(self):
		super().__init__(
			model = 'cube',
			position = (randint(-4,4),15),
			scale = (1,1,0),
			collider = 'box',
			texture = alien_two_texture
			)
		self.life = 2

	def update(self):

		self.y -= 2 * time.dt

class Invader_three(Entity):
	def __init__(self):
		super().__init__(
			model = 'cube',
			position = (randint(-3,3),6),
			scale = (1,1,0),
			collider = 'box',
			texture = alien_three_texture
			)
		self.life = 4


	def update(self):

		self.y -= .5 * time.dt


def input(key):

	global start
	global spawn

	if key == 'space':
		bullet = Bullet()
		bullets.append(bullet)
		if start == False:
			start = True
		if randint(1,3) == 1:
			invader = Invader()
			invaders.append(invader)
		if spawn:
			invader_two = Invader_two()
			invaders_two.append(invader_two)
			spawn = False
		elif spawn == False:
			spawn = True
		if score == 150 or score == 300 or score == 350 or score == 450 or score == 550:
			invader_three = Invader_three()
			invaders_three.append(invader_three)

def update():

	global logo
	global start
	global end
	global score

	if start:
		if logo.y < 2:
			logo.y += dy
		else:
			start_button.visible = True
			exit_button.visible = True

	for bullet in bullets:
		bullet.y += 6 * time.dt

	hit_info_start = start_button.intersects()
	if hit_info_start.hit:
		Audio('hit.wav')
		bullet.disable()
		logo.disable()
		start_button.x = -60
		start_button.disable()
		exit_button.x = -60
		exit_button.disable()

	hit_info_exit = exit_button.intersects()
	if hit_info_exit.hit:
		Audio('hit.wav')
		sys.exit()

	if player.x > 4:
		player.x = 4
	if player.x < -4:
		player.x = -4 

	for bullet in bullets:
		hit_info_bullet = bullet.intersects()
		if hit_info_bullet:
			Audio('hit.wav')
			bullet.x = 10
			if hit_info_bullet.entity in invaders:
				bullet.x = 30
				hit_info_bullet.entity.x = 40
				hit_info_bullet.entity.disable()
				bullet.disable()
				score += 5
			if hit_info_bullet.entity in invaders_two:
				hit_info_bullet.entity.life -= 1
				bullet.disable()
				if hit_info_bullet.entity.life == 0:
					hit_info_bullet.entity.x = 40
					hit_info_bullet.entity.disable()
					score += 10

			if hit_info_bullet.entity in invaders_three:
				hit_info_bullet.entity.life -= 1
				bullet.disable()
				if hit_info_bullet.entity.life == 0:
					hit_info_bullet.entity.x = 40
					hit_info_bullet.entity.disable()
					score += 50

	score_text.text = 'Score: {} '.format(score)
				

	hit_info_player = player.intersects()
	if hit_info_player:
		main_music.stop()
		if end == False:
			Audio('explosion.wav')
			Audio('game_over.wav')
			player.x = 99
			player.disable()
			Text(text = 'GAME OVER', color = color.red, position = (-.3,.2), scale = (4,4))
			end = True




player = Player()

background = Entity(model = 'quad', scale = 10, texture = background_texture)
aspect_ratio = Entity(model = 'quad', color = color.black, scale = (3, 60), position = (5.8, 0))
aspect_ratio_two = Entity(model = 'quad', color = color.black, scale = (3, 60), position = (-5.8, 0))
logo = Entity(model = 'cube', texture = logo_texture, scale = (6,6,0), position = (0,0), ignore_paused = True)
start_button = Entity(model = 'cube', scale = (1,1,0), position = (-2,-1), collider = 'box', visible = False, texture = start_button_texture, ignore_paused = True)
exit_button = Entity(model = 'cube', scale = (1,1,0), position = (2,-1), collider = 'box', visible = False, texture = exit_button_texture, ignore_paused = True)
score_text = Text(text = 'Score: ', scale = (1,1), background = True, position = (.4,.45))


app.run()