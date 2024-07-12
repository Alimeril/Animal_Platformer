import arcade
import arcade.color
import arcade.csscolor
import time
import random

# Adjusting the size of the game window:
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
# Title of the game:
GAME_TITLE = 'Platformer'
# Maps scales
TILE_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
GRAVITY = 1

# Character files and scales and movement speeds
PARROT = 'Assets/Characters/parrot.png'
PANDA = 'Assets/Characters/panda.png'
P_SCALE = 0.2
CHARACTER_SPEED = 6
CHARACTER_BOOSTED_SPEED = 8
ANGLE_SPEED = 4
JUMP_SPEED = 20

# Enemy files,scale and movement speeds
#----------- Half Razor
ENEMY0_SCALE = 0.5
ENEMY0A = 'Assets/Enemies/0a.png'
ENEMY0B = 'Assets/Enemies/0b.png'
ENEMY0_SPEED = 3
#----------- Full Razor
ENEMY00_SCALE = 1
ENEMY00A = 'Assets/Enemies/00a.png'
ENEMY00B = 'Assets/Enemies/00b.png'
ENEMY00_SPEED = 3
#----------- Blue Alien
ENEMY1_SCALE = 1
ENEMY1A = 'Assets/Enemies/1a.png'
ENEMY1B = 'Assets/Enemies/1b.png'
ENEMY1C = 'Assets/Enemies/1c.png'
ENEMY1_SPEED = 2
# ----------- Bee
ENEMY2_SCALE = 0.5
ENEMY2A = 'Assets/Enemies/2a.png'
ENEMY2B = 'Assets/Enemies/2b.png'
ENEMY2_SPEED = 5
#----------- Frog
ENEMY3_SCALE = 1
ENEMY3A = 'Assets/Enemies/3a.png'
ENEMY3B = 'Assets/Enemies/3b.png'
ENEMY3C = 'Assets/Enemies/3c.png'
ENEMY3_SPEED = 2
#----------- Slime
ENEMY4_SCALE = 1
ENEMY4A = 'Assets/Enemies/4a.png'
ENEMY4B = 'Assets/Enemies/4b.png'
ENEMY4C = 'Assets/Enemies/4c.png'
ENEMY4_SPEED = 1
# ----------- Worm
ENEMY5_SCALE = 0.7
ENEMY5A = 'Assets/Enemies/5a.png'
ENEMY5B = 'Assets/Enemies/5b.png'
ENEMY5_SPEED = 1
#----------- Red Alien
ENEMY6_SCALE = 1
ENEMY6A = 'Assets/Enemies/6a.png'
ENEMY6B = 'Assets/Enemies/6b.png'
ENEMY6C = 'Assets/Enemies/6c.png'
ENEMY6_SPEED = 2
#----------- Spider
ENEMY7_SCALE = 1
ENEMY7A = 'Assets/Enemies/7a.png'
ENEMY7B = 'Assets/Enemies/7b.png'
ENEMY7C = 'Assets/Enemies/7c.png'
ENEMY7_SPEED = 1

# Items sprite path
HEART = 'Assets/Other/Heart.png'

# Number of frames to update animation
UPDATE_PER_FRAME = 7

# Loading Sounds
COIN_SOUND = arcade.load_sound('Sounds/coin.wav')
JUMP_SOUND = arcade.load_sound('Sounds/jump.wav')
PRIZE_SOUND = arcade.load_sound('Sounds/prize.wav')
KILL_SOUND = arcade.load_sound('Sounds/kill.wav')
LOST_SOUND = arcade.load_sound('Sounds/lost.wav')

MENU = arcade.load_sound('Sounds/Menu.wav')
ENDGAME = arcade.load_sound('Sounds/EndGame.wav')
GAMEOVER = arcade.load_sound('Sounds/GameOver.wav')
LEVEL1_SOUND = arcade.load_sound('Sounds/Level1.wav')
LEVEL2_SOUND = arcade.load_sound('Sounds/Level2.wav')
LEVEL3_SOUND = arcade.load_sound('Sounds/Level3.wav')
LEVEL4_SOUND = arcade.load_sound('Sounds/Level4.wav')
LEVEL5_SOUND = arcade.load_sound('Sounds/Level5.wav')
LEVEL6_SOUND = arcade.load_sound('Sounds/Level6.wav')


class Character(arcade.Sprite):
    # A character class that builds the sprite and update its animation
    def __init__(self,file,scale):
        super().__init__(file,scale)
        self.change_x = 0
        self.change_y = 0

    def update(self):
        # Creating character rotating animation on movement
        if self.change_x > 0 :
            self.angle -= ANGLE_SPEED
        elif self.change_x < 0 :
            self.angle += ANGLE_SPEED

def load_texture_pair(filename):
    # Load a texture pair, with the second being a mirror image.
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class Enemy(arcade.Sprite):
    # An enemy class that builds enemy sprites and update their animations
    def __init__(self,scale,speed, *files):
        super().__init__(files[0],scale)

        self.can_be_killed = True

        # Creating a list of animation texture files
        self.texture_list = []
        for file in files:
            self.texture_list.append(load_texture_pair(file))
        self.texture_index = 0

        # Initiating enemy facing direction (left: -1, right: 1), speed and frame counter
        self.direction = -1
        self.change_x = speed * self.direction
        self.frame_counter = 0 
    
    def update(self, *collision_lists: arcade.SpriteList):
        # Moving enemy
        self.center_x += self.change_x

        # if enemy collide with anything, changes its movement direction
        for cl in collision_lists:
            if len(self.collides_with_list(cl)) > 0:
                self.direction *= -1
                self.change_x *= -1
            self.texture = self.texture_list[self.texture_index][0] if self.direction == -1 else self.texture_list[self.texture_index][1]

        # Creating movement animation
        # Choosing animation textures every (UPDATE_PER_FRAME) frame
        self.frame_counter += 1
        if self.frame_counter > UPDATE_PER_FRAME:
            self.frame_counter = 0
            self.texture_index += 1
            if self.texture_index > len(self.texture_list)-1:
                self.texture_index = 0
        

class Game(arcade.Window):

    # Making the game window and its initial setup:
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,GAME_TITLE)
        arcade.set_background_color(arcade.csscolor.DARK_BLUE)

        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        self.score = 0
        self.score_saved = 0

        # Determines the state of the game (menu, game, game_over, game_won)
        self.game_state = 'menu'

        self.media = arcade.play_sound(MENU)

        # Character lives (max 3) and heart sprite
        self.character_lives = 3
        self.heart = arcade.Sprite(HEART, 0.3)

        # Special tokens pointers and time counters
        self.double_coins = False
        self.double_coins_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        # Showing the prize of special tile
        self.special_phrase = ''

        self.level = 1
        self.level_text = ''

        self.tile_map = None

        self.end_of_map = None

        self.scene = None

        self.physics_engine = None

        self.enemies = None
        self.dead_enemies = arcade.SpriteList()

    def reset(self):
        self.score = 0
        self.score_saved = 0

        # Determines the state of the game (menu, game, game_over, game_won)
        # self.game_state = 'menu'
        self.game_state = 'menu'

        arcade.sound.stop_sound(self.media)
        self.media = arcade.play_sound(MENU)

        # Character lives (max 3) and heart sprite
        self.character_lives = 3
        self.heart = arcade.Sprite(HEART, 0.3)

        # Special tokens pointers and time counters
        self.double_coins = False
        self.double_coins_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        # Showing the prize of special tile
        self.special_phrase = ''

        self.level = 1
        self.level_text = ''

    def level1_setup(self):
        # Setup for Level 1
        self.level_text = 'LEVEL 1'

        arcade.sound.stop_sound(self.media)
        self.media = arcade.sound.play_sound(LEVEL1_SOUND)

        self.score = self.score_saved

        # Special tokens pointers and time counters
        self.double_coins = False
        self.double_coins_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        # Showing the prize of special tile
        self.special_phrase = ''

        # Adding map file and its options
        map_name = 'Maps/lvl1.json'

        layer_options = {
            "Platform": {
                "use_spatial_hash": True,
            },
            "Specials": {
                "use_spatial_hash": True,
            },
            "Coins": {
                "use_spatial_hash": True,
            },
            "House": {
                "use_spatial_hash": True,
            },
            "Door": {
                "use_spatial_hash": True,
            },
        }

        # Loading map file
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Creating the level's scene from map json file
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        
        # Creating player sprite
        self.player = Character(PARROT, P_SCALE)
        self.player.center_x = 50
        self.player.center_y = 150
        
        # Creating Enemies
        self.enemies = arcade.SpriteList()
        self.dead_enemies.clear()

        # Half Razors
        self.enemy01 = Enemy(ENEMY0_SCALE, ENEMY0_SPEED, ENEMY0A, ENEMY0B)
        self.enemy01.center_x = 1500
        self.enemy01.center_y = 162
        self.enemy01.can_be_killed = False
        self.enemies.append(self.enemy01)
        self.enemy02 = Enemy(ENEMY0_SCALE, ENEMY0_SPEED, ENEMY0A, ENEMY0B)
        self.enemy02.center_x = 2100
        self.enemy02.center_y = 162
        self.enemy02.can_be_killed = False
        self.enemies.append(self.enemy02)
        self.enemy03 = Enemy(ENEMY0_SCALE, ENEMY0_SPEED + 1, ENEMY0A, ENEMY0B)
        self.enemy03.center_x = 2400
        self.enemy03.center_y = 162
        self.enemy03.can_be_killed = False
        self.enemies.append(self.enemy03)

        # Blue Alien
        self.enemy1 = Enemy(ENEMY1_SCALE, ENEMY1_SPEED, ENEMY1A, ENEMY1B, ENEMY1C)
        self.enemy1.center_x = 1000
        self.enemy1.center_y = 175
        self.enemies.append(self.enemy1)

        # Bee
        self.enemy2 = Enemy(ENEMY2_SCALE, ENEMY2_SPEED, ENEMY2A, ENEMY2B)
        self.enemy2.center_x = 2000
        self.enemy2.center_y = 220
        self.enemies.append(self.enemy2)

        self.scene.add_sprite("Player", self.player)
        for enemy in self.enemies:
            self.scene.add_sprite("Enemy", enemy)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant = GRAVITY, walls = self.scene['Platform']
        )

    def level2_setup(self):
        # Setup for Level 2
        self.level_text = 'LEVEL 2'

        arcade.sound.stop_sound(self.media)
        self.media = arcade.sound.play_sound(LEVEL2_SOUND)

        self.score = self.score_saved

        # Special tokens pointers and time counters
        self.double_coins = False
        self.double_coins_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        # Showing the prize of special tile
        self.special_phrase = ''

        # Adding map file and its options
        map_name = 'Maps/lvl2.json'

        layer_options = {
            "Platform": {
                "use_spatial_hash": True,
            },
            "Specials": {
                "use_spatial_hash": True,
            },
            "Coins": {
                "use_spatial_hash": True,
            },
            "House": {
                "use_spatial_hash": True,
            },
            "Door": {
                "use_spatial_hash": True,
            },
        }

        # Loading map file
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Creating the level's scene from map json file
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        
        # Creating player sprite
        self.player = Character(PARROT, P_SCALE)
        self.player.center_x = 50
        self.player.center_y = 150
        
        # Creating Enemies
        self.enemies = arcade.SpriteList()
        self.dead_enemies.clear()

        # Red Alien
        self.enemy6 = Enemy(ENEMY6_SCALE, ENEMY6_SPEED, ENEMY6A, ENEMY6B, ENEMY6C)
        self.enemy6.center_x = 700
        self.enemy6.center_y = 175
        self.enemies.append(self.enemy6)

        # Fixed Full Razor
        self.enemy001 = Enemy(ENEMY00_SCALE, 0, ENEMY00A, ENEMY00B)
        self.enemy001.center_x = 1185
        self.enemy001.center_y = 500
        self.enemy001.can_be_killed = False
        self.enemies.append(self.enemy001)

        # Worms
        self.enemy51 = Enemy(ENEMY5_SCALE, ENEMY5_SPEED, ENEMY5A, ENEMY5B)
        self.enemy51.center_x = 900
        self.enemy51.center_y = 140
        self.enemies.append(self.enemy51)

        self.enemy52 = Enemy(ENEMY5_SCALE, ENEMY5_SPEED, ENEMY5A, ENEMY5B)
        self.enemy52.center_x = 1100
        self.enemy52.center_y = 140
        self.enemies.append(self.enemy52)

        self.enemy53 = Enemy(ENEMY5_SCALE, ENEMY5_SPEED, ENEMY5A, ENEMY5B)
        self.enemy53.center_x = 1300
        self.enemy53.center_y = 140
        self.enemies.append(self.enemy53)

        self.enemy54 = Enemy(ENEMY5_SCALE, ENEMY5_SPEED, ENEMY5A, ENEMY5B)
        self.enemy54.center_x = 1500
        self.enemy54.center_y = 140
        self.enemies.append(self.enemy54)

        # Half Razor
        self.enemy01.center_x = 2100
        self.enemy01.center_y = 162
        self.enemy01.can_be_killed = False
        self.enemies.append(self.enemy01)
        self.enemy01 = Enemy(ENEMY0_SCALE, ENEMY0_SPEED, ENEMY0A, ENEMY0B)

        # Slimes
        self.enemy41 = Enemy(ENEMY4_SCALE, ENEMY4_SPEED, ENEMY4A, ENEMY4B, ENEMY4C)
        self.enemy41.center_x = 1900
        self.enemy41.center_y = 145
        self.enemies.append(self.enemy41)

        self.enemy42 = Enemy(ENEMY4_SCALE, ENEMY4_SPEED, ENEMY4A, ENEMY4B, ENEMY4C)
        self.enemy42.center_x = 3000
        self.enemy42.center_y = 145
        self.enemies.append(self.enemy42)

        # Moving Full Razor
        self.enemy002 = Enemy(ENEMY00_SCALE, ENEMY00_SPEED, ENEMY00A, ENEMY00B)
        self.enemy002.center_x = 3700
        self.enemy002.center_y = 500
        self.enemy002.can_be_killed = False
        self.enemies.append(self.enemy002)

        self.scene.add_sprite("Player", self.player)
        for enemy in self.enemies:
            self.scene.add_sprite("Enemy", enemy)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant = GRAVITY, walls = self.scene['Platform']
        )        

    def level3_setup(self):
        # Setup for Level 3

        self.level_text = 'LEVEL 3'

        arcade.sound.stop_sound(self.media)
        self.media = arcade.sound.play_sound(LEVEL3_SOUND)

        self.score = self.score_saved

        # Special tokens pointers and time counters
        self.double_coins = False
        self.double_coins_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        # Showing the prize of special tile
        self.special_phrase = ''

        # Adding map file and its options
        map_name = 'Maps/lvl3.json'

        layer_options = {
            "Platform": {
                "use_spatial_hash": True,
            },
            "Specials": {
                "use_spatial_hash": True,
            },
            "Coins": {
                "use_spatial_hash": True,
            },
            "House": {
                "use_spatial_hash": True,
            },
            "Door": {
                "use_spatial_hash": True,
            },
            "Water": {
                "use_spatial_hash": True,
            },
        }

        # Loading map file
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Creating the level's scene from map json file
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        
        # Creating player sprite
        self.player = Character(PARROT, P_SCALE)
        self.player.center_x = 50
        self.player.center_y = 150
        
        # Creating Enemies
        self.enemies = arcade.SpriteList()
        self.dead_enemies.clear()

        # Frog
        self.enemy31 = Enemy(ENEMY3_SCALE, ENEMY3_SPEED, ENEMY3A, ENEMY3B)
        self.enemy31.center_x = 500
        self.enemy31.center_y = 155
        self.enemies.append(self.enemy31)

        # Bee
        self.enemy2 = Enemy(ENEMY2_SCALE, ENEMY2_SPEED, ENEMY2A, ENEMY2B)
        self.enemy2.center_x = 800
        self.enemy2.center_y = 230
        self.enemies.append(self.enemy2)

        # Slime
        self.enemy4 = Enemy(ENEMY4_SCALE, ENEMY4_SPEED, ENEMY4A, ENEMY4B, ENEMY4C)
        self.enemy4.center_x = 1100
        self.enemy4.center_y = 273
        self.enemies.append(self.enemy4)

        # Worms
        self.enemy5 = Enemy(ENEMY5_SCALE, ENEMY5_SPEED, ENEMY5A, ENEMY5B)
        self.enemy5.center_x = 2050
        self.enemy5.center_y = 330
        self.enemies.append(self.enemy5)

        self.scene.add_sprite("Player", self.player)
        for enemy in self.enemies:
            self.scene.add_sprite("Enemy", enemy)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant = GRAVITY, walls = self.scene['Platform']
        )

    def level4_setup(self):
        # Setup for Level 4

        self.level_text = 'LEVEL 4'

        arcade.sound.stop_sound(self.media)
        self.media = arcade.sound.play_sound(LEVEL4_SOUND)

        self.score = self.score_saved

        # Special tokens pointers and time counters
        self.double_coins = False
        self.double_coins_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        # Showing the prize of special tile
        self.special_phrase = ''

        # Adding map file and its options
        map_name = 'Maps/lvl4.json'

        layer_options = {
            "Platform": {
                "use_spatial_hash": True,
            },
            "Specials": {
                "use_spatial_hash": True,
            },
            "Coins": {
                "use_spatial_hash": True,
            },
            "House": {
                "use_spatial_hash": True,
            },
            "Door": {
                "use_spatial_hash": True,
            },
            "Water": {
                "use_spatial_hash": True,
            },
        }

        # Loading map file
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Creating the level's scene from map json file
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        
        # Creating player sprite
        self.player = Character(PARROT, P_SCALE)
        self.player.center_x = 50
        self.player.center_y = 150
        
        # Creating Enemies
        self.enemies = arcade.SpriteList()
        self.dead_enemies.clear()

        # Worms
        self.enemy51 = Enemy(ENEMY5_SCALE, ENEMY5_SPEED, ENEMY5A, ENEMY5B)
        self.enemy51.center_x = 925
        self.enemy51.center_y = 393
        self.enemies.append(self.enemy51)

        # Bee
        self.enemy2 = Enemy(ENEMY2_SCALE, ENEMY2_SPEED, ENEMY2A, ENEMY2B)
        self.enemy2.center_x = 1000
        self.enemy2.center_y = 310
        self.enemies.append(self.enemy2)

        self.scene.add_sprite("Player", self.player)
        for enemy in self.enemies:
            self.scene.add_sprite("Enemy", enemy)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant = GRAVITY, walls = self.scene['Platform']
        )

    def level5_setup(self):
        # Setup for Level 5

        self.level_text = 'LEVEL 5'

        arcade.sound.stop_sound(self.media)
        self.media = arcade.sound.play_sound(LEVEL5_SOUND)

        self.score = self.score_saved

        # Special tokens pointers and time counters
        self.double_coins = False
        self.double_coins_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        # Showing the prize of special tile
        self.special_phrase = ''

        # Adding map file and its options
        map_name = 'Maps/lvl5.json'

        layer_options = {
            "Platform": {
                "use_spatial_hash": True,
            },
            "Specials": {
                "use_spatial_hash": True,
            },
            "Coins": {
                "use_spatial_hash": True,
            },
            "House": {
                "use_spatial_hash": True,
            },
            "Door": {
                "use_spatial_hash": True,
            },
            "Water": {
                "use_spatial_hash": True,
            },
        }

        # Loading map file
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Creating the level's scene from map json file
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        
        # Creating player sprite
        self.player = Character(PARROT, P_SCALE)
        self.player.center_x = 50
        self.player.center_y = 150

        # Creating Enemies
        self.enemies = arcade.SpriteList()
        self.dead_enemies.clear()

        # Frog
        self.enemy3 = Enemy(ENEMY3_SCALE, ENEMY3_SPEED, ENEMY3A, ENEMY3B)
        self.enemy3.center_x = 500
        self.enemy3.center_y = 155
        self.enemies.append(self.enemy3)

        # Spiders
        self.enemy71 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy71.center_x = 1300
        self.enemy71.center_y = 155
        self.enemies.append(self.enemy71)

        self.enemy72 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy72.center_x = 1600
        self.enemy72.center_y = 155
        self.enemies.append(self.enemy72)

        self.enemy73 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy73.center_x = 1700
        self.enemy73.center_y = 155
        self.enemies.append(self.enemy73)

        self.enemy74 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy74.center_x = 1900
        self.enemy74.center_y = 155
        self.enemies.append(self.enemy74)

        self.enemy75 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy75.center_x = 2000
        self.enemy75.center_y = 155
        self.enemies.append(self.enemy75)

        self.enemy76 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy76.center_x = 2250
        self.enemy76.center_y = 155
        self.enemies.append(self.enemy76)

        self.enemy77 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy77.center_x = 2350
        self.enemy77.center_y = 155
        self.enemies.append(self.enemy77)

        self.enemy78 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy78.center_x = 2550
        self.enemy78.center_y = 155
        self.enemies.append(self.enemy78)

        self.enemy79 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy79.center_x = 2650
        self.enemy79.center_y = 155
        self.enemies.append(self.enemy79)

        self.enemy710 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy710.center_x = 2900
        self.enemy710.center_y = 155
        self.enemies.append(self.enemy710)

        self.enemy711 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy711.center_x = 3100
        self.enemy711.center_y = 155
        self.enemies.append(self.enemy711)

        self.enemy712 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy712.center_x = 3400
        self.enemy712.center_y = 155
        self.enemies.append(self.enemy712)

        self.scene.add_sprite("Player", self.player)
        for enemy in self.enemies:
            self.scene.add_sprite("Enemy", enemy)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant = GRAVITY, walls = self.scene['Platform']
        )
        
    def level6_setup(self):
        # Setup for Level 6

        self.level_text = 'LEVEL 6'

        arcade.sound.stop_sound(self.media)
        self.media = arcade.sound.play_sound(LEVEL6_SOUND)

        self.score = self.score_saved

        # Special tokens pointers and time counters
        self.double_coins = False
        self.double_coins_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        # Showing the prize of special tile
        self.special_phrase = ''

        # Adding map file and its options
        map_name = 'Maps/lvl6.json'

        layer_options = {
            "Platform": {
                "use_spatial_hash": True,
            },
            "Specials": {
                "use_spatial_hash": True,
            },
            "Coins": {
                "use_spatial_hash": True,
            },
            "House": {
                "use_spatial_hash": True,
            },
            "Door": {
                "use_spatial_hash": True,
            },
            "Water": {
                "use_spatial_hash": True,
            },
        }

        # Loading map file
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Creating the level's scene from map json file
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        
        # Creating player sprite
        self.player = Character(PARROT, P_SCALE)
        self.player.center_x = 50
        self.player.center_y = 150
        
        # Creating Enemies
        self.enemies = arcade.SpriteList()
        self.dead_enemies.clear()

        # Half Razors
        self.enemy01 = Enemy(ENEMY0_SCALE, ENEMY0_SPEED, ENEMY0A, ENEMY0B)
        self.enemy01.center_x = 310
        self.enemy01.center_y = 162
        self.enemy01.can_be_killed = False
        self.enemies.append(self.enemy01)

        self.enemy02 = Enemy(ENEMY0_SCALE, ENEMY0_SPEED, ENEMY0A, ENEMY0B)
        self.enemy02.center_x = 380
        self.enemy02.center_y = 162
        self.enemy02.can_be_killed = False
        self.enemies.append(self.enemy02)

        self.enemy03 = Enemy(ENEMY0_SCALE, ENEMY0_SPEED, ENEMY0A, ENEMY0B)
        self.enemy03.center_x = 450
        self.enemy03.center_y = 162
        self.enemy03.can_be_killed = False
        self.enemies.append(self.enemy03)

        # Spiders
        self.enemy71 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy71.center_x = 1150
        self.enemy71.center_y = 346
        self.enemies.append(self.enemy71)

        self.enemy72 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy72.center_x = 2050
        self.enemy72.center_y = 475
        self.enemies.append(self.enemy72)

        self.enemy73 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy73.center_x = 2400
        self.enemy73.center_y = 155
        self.enemies.append(self.enemy73)

        self.enemy74 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy74.center_x = 2600
        self.enemy74.center_y = 155
        self.enemies.append(self.enemy74)

        self.enemy75 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy75.center_x = 2800
        self.enemy75.center_y = 155
        self.enemies.append(self.enemy75)

        self.enemy76 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy76.center_x = 2900
        self.enemy76.center_y = 155
        self.enemies.append(self.enemy76)

        self.enemy77 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy77.center_x = 3100
        self.enemy77.center_y = 155
        self.enemies.append(self.enemy77)

        self.enemy78 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy78.center_x = 3200
        self.enemy78.center_y = 155
        self.enemies.append(self.enemy78)

        self.enemy79 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy79.center_x = 3400
        self.enemy79.center_y = 155
        self.enemies.append(self.enemy79)

        self.enemy710 = Enemy(ENEMY7_SCALE, ENEMY7_SPEED, ENEMY7A, ENEMY7B, ENEMY7C)
        self.enemy710.center_x = 3500
        self.enemy710.center_y = 155
        self.enemies.append(self.enemy710)

        self.scene.add_sprite("Player", self.player)
        for enemy in self.enemies:
            self.scene.add_sprite("Enemy", enemy)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant = GRAVITY, walls = self.scene['Platform']
        )

    # Levels setup based on self.level
    def setup(self):
        match self.level:
            case 1:
                self.level1_setup()
            case 2:
                self.level2_setup()
            case 3:
                self.level3_setup()
            case 4:
                self.level4_setup()
            case 5:
                self.level5_setup()
            case 6:
                self.level6_setup()

    # Keyboard inputs for player movement
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            if self.physics_engine.can_jump():
                arcade.play_sound(JUMP_SOUND)
                self.player.change_y = JUMP_SPEED
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.change_x = CHARACTER_SPEED if not self.speed_boost else CHARACTER_BOOSTED_SPEED
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.change_x = -1 * CHARACTER_SPEED if not self.speed_boost else -1 * CHARACTER_BOOSTED_SPEED
        elif symbol == arcade.key.ENTER:
            if self.game_state == 'game_over' or self.game_state == 'game_won':
                self.reset()
            elif self.game_state == 'menu':
                self.game_state = 'game'
                self.setup()
    
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.change_x = 0
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.change_x = 0
    
    def camera_movement(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 3)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        # Don't let camera travel past the end of map
        if screen_center_x > self.end_of_map - (self.camera.viewport_width):
            screen_center_x = self.end_of_map - (self.camera.viewport_width)

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time: float):

        if self.game_state == 'game':
            # Updating player animation
            self.player.update()

            # Updating enemy movements
            for enemy in self.enemies:
                enemy.update(self.scene["Platform"],self.scene["Invisibles"],self.enemies)

            # activating player movement and physics
            self.physics_engine.update()
            
            # Checking player collecting coins
            coin_hit_list = arcade.check_for_collision_with_list(
            self.player, self.scene["Coins"]
            )
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                arcade.play_sound(COIN_SOUND)
                self.score = self.score + 1 if not self.double_coins else self.score + 2
            
            # Managing Special Blocks:
            specials_hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene["Specials"]
            )
            for special in specials_hit_list:
                arcade.play_sound(PRIZE_SOUND)
                special.remove_from_sprite_lists()
                n = random.randrange(1,5)
                match n:
                    case 1:
                        self.special_phrase = 'FREE COIN'
                        self.score += 1
                    case 2:
                        self.special_phrase = 'FREE HEART'
                        if self.character_lives < 3:
                            self.character_lives += 1
                    case 3:
                        self.special_phrase = 'DOUBLE COINS'
                        self.double_coins = True
                        self.double_coins_time = 0
                    case 4:
                        self.special_phrase = 'SPEED BOOST'
                        self.speed_boost = True
                        self.speed_boost_time = 0
            if self.double_coins:
                self.double_coins_time += 1
                if self.double_coins_time > 500:
                    self.double_coins = False
                    self.double_coins_time = 0
                    self.special_phrase = ''
            if self.speed_boost:
                self.speed_boost_time += 1
                if self.speed_boost_time > 400:
                    self.speed_boost = False
                    self.speed_boost_time = 0
                    self.special_phrase = ''

            # Collision with enemies
            enemy_hit_list = arcade.check_for_collision_with_list (
                self.player, self.enemies
            )
            for enemy in enemy_hit_list:
                if enemy.can_be_killed and self.player.collides_with_point((enemy.center_x,enemy.top)):
                    arcade.play_sound(KILL_SOUND)
                    self.score += 1
                    enemy.remove_from_sprite_lists()
                    self.dead_enemies.append(enemy)
                else:
                    arcade.play_sound(LOST_SOUND)
                    time.sleep(2)
                    self.character_lives -= 1
                    self.score = self.score_saved
                    if self.character_lives <= 0:
                        arcade.sound.stop_sound(self.media)
                        self.media = arcade.play_sound(GAMEOVER)
                        self.game_state = 'game_over'
                        self.character_lives = 3
                    else:
                        self.setup()
            
            # Character Teleportation
            if len(self.scene['Teleporter']) > 1:
                if self.scene['Teleporter'][1].collides_with_point((self.player.center_x,self.player.center_y)):
                    self.player.center_x = self.scene['Teleporter'][0].center_x + 50
                    self.player.center_y = self.scene['Teleporter'][0].center_y
                elif self.scene['Teleporter'][0].collides_with_point((self.player.center_x,self.player.center_y)):
                    self.player.center_x = self.scene['Teleporter'][1].center_x - 50
                    self.player.center_y = self.scene['Teleporter'][1].center_y
                
            # Dropping out
            if self.player.top < 0:
                arcade.play_sound(LOST_SOUND)
                time.sleep(2)
                self.character_lives -= 1
                self.score = self.score_saved
                if self.character_lives <= 0:
                    arcade.sound.stop_sound(self.media)
                    self.media = arcade.play_sound(GAMEOVER)
                    self.game_state = 'game_over'
                    self.character_lives = 3
                else:
                    self.setup()

            # Finishing level
            Finish = arcade.check_for_collision_with_list(self.player, self.scene['Door'])
            if len(Finish) > 0:
                self.score_saved = self.score
                if self.level < 6:
                    self.level += 1
                    self.setup()
                elif self.level == 6:
                    arcade.sound.stop_sound(self.media)
                    self.media = arcade.play_sound(ENDGAME)
                    self.game_state = 'game_won'

            # Updating camera movement
            self.camera_movement()

    def on_draw(self):
        # Rendering the screen:
        self.clear()

        match self.game_state:
            case 'menu':
                arcade.draw_text(
                    'ANIMAL ADVENTURES',
                    SCREEN_WIDTH/2-250, SCREEN_HEIGHT/2 + 150,
                    arcade.color.PINK_PEARL , 50,
                    width = 500, align = 'center',
                    bold = True,
                )
                arcade.draw_text(
                    'PRESS ENTER TO START THE GAME',
                    SCREEN_WIDTH/2-500, SCREEN_HEIGHT/2 - 100,
                    arcade.color.WHITE , 20,
                    width = 1000, align = 'center',
                    bold = True,
                )
            case 'game':

                # Using player camera and drawing the scene
                self.camera.use()
                self.scene.draw()

                # Dead enemies animation
                for enemy in self.dead_enemies:
                    if enemy.top > 0:
                        enemy.center_y -= 8
                        enemy.draw()
                    else:
                        self.dead_enemies.remove(enemy)

                # Activating the constant GUI camera:
                self.gui_camera.use()

                score_text = f"Score: {self.score}"
                arcade.draw_text(
                    score_text,
                    10,
                    SCREEN_HEIGHT-30,
                    arcade.csscolor.WHITE,
                    18,
                )
                arcade.draw_text(
                    self.level_text,
                    SCREEN_WIDTH/2-150, SCREEN_HEIGHT-30,
                    arcade.csscolor.WHITE, 18,
                    width = 300, align = 'center',
                    bold = True,
                )
                arcade.draw_line(0, SCREEN_HEIGHT-45,SCREEN_WIDTH,SCREEN_HEIGHT-45,arcade.csscolor.WHITE,line_width=2)

                # Drawing character lives (hearts) on GUI camera:
                for n in range(self.character_lives):
                    self.heart.center_y = SCREEN_HEIGHT - 20
                    self.heart.center_x = SCREEN_WIDTH - (n + 1) * 30
                    self.heart.draw()
                # Writing Special Effects:
                arcade.draw_text(
                    self.special_phrase,
                    SCREEN_WIDTH/2-150, SCREEN_HEIGHT-75,
                    arcade.color.AFRICAN_VIOLET, 18,
                    width = 300, align = 'center',
                    bold = True,
                )
            case 'game_won':
                arcade.draw_text(
                    'CONGRATULATIONS \n GAME FINISHED',
                    SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2 + 100,
                    arcade.color.WHITE , 30,
                    width = 300, align = 'center',
                    bold = True,
                )
                score_text = f"SCORE: {self.score_saved}"
                arcade.draw_text(
                    score_text,
                    SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2 - 60,
                    arcade.color.WHITE , 25,
                    width = 300, align = 'center',
                    bold = True,
                )
            case 'game_over':
                arcade.draw_text(
                    'GAME OVER',
                    SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2 + 10,
                    arcade.color.WHITE , 30,
                    width = 300, align = 'center',
                    bold = True,
                )
                score_text = f"SCORE: {self.score_saved}"
                arcade.draw_text(
                    score_text,
                    SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2 - 60,
                    arcade.color.WHITE , 25,
                    width = 300, align = 'center',
                    bold = True,
                )

def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()