A simple platformer game in Python arcade library.

Arcade is a newer Python 2D game engine compared to its classic counterpart, pygame. While it may not have pygame's flexibility and compatibility with nearly every platform, it does offer many built-in features that make game development much easier and more entertaining. Additionally, it comes with better graphics and improved Sprite management.
The primary element of the arcade game engine is the arcade.Window class. This class is responsible for creating the game window and includes built-in functions for handling events, such as clicking, dragging, pressing a key on the keyboard, and updating the screen.

![arcade_window](https://github.com/user-attachments/assets/3e6cb3ca-ff78-466c-b6b6-2479010ea6db)

In order to create the game, we need to inherit our Game class from the arcade.Window class. By rewriting the __init__ function, we can define the initial setup for our game. Additionally, we will need to call super().__init__ to run the game window with its respective width, height, and title arguments. The arcade.Window class has two main functions: on_update and on_draw. In almost every arcade game, we are required to rewrite these two functions in our Game class. The arcade library comes with a specific refresh rate. Each time the window refreshes, it calls the on_update function. After refreshing, it calls the on_draw function to redraw the game window. The on_update function is used to create game object movements. For example, enemies in our platformer game move a few pixels every time the game window refreshes. Then, in the on_draw function, the game draws the new scene again.
Now that we have a good understanding of the core of the arcade library, let's revisit our code and create a simple platformer game. First, we'll define the constants for the game. These constants will include the assets files for the game such as player or enemy assets. We'll also set the scale for each character, the map, and the game window. Additionally, if we want to include sounds in our game (which we do), we can load the sounds using "arcade.load_sound("PATH_TO_SOUND_FILE")" at this stage.
As I mentioned earlier, the arcade library includes an excellent Sprite class. When you provide a sprite texture file, it automatically sets the hitbox and can recognize collisions between sprites. That's why, to create the characters in the game (player, enemies, etc.), we inherit them from the arcade.Sprite class.

![charater](https://github.com/user-attachments/assets/f53a9488-ad42-40b8-a9eb-61ff16b689b4)

We used a circular-shaped Sprite as the main chracter : ![parrot](https://github.com/user-attachments/assets/0a6119e8-b62b-4c0f-8bbe-7d81869f105b)
In the code, I set the changes in sprite x and y coordinates to zero to initialize the object (I should note that the (x=0,y=0) coordination is the bottom-left of the window) . This is done because our character is not moving at this point. We will define the player character's movement later on when a key is pressed on the keyboard event. In the update method, the arcade.Sprite angle property is used to rotate the character if it is moving.

![Enemy](https://github.com/user-attachments/assets/c9790b1c-d402-4766-9215-63a46f36cf40)

Enemy class is slightly more complex as the enemy needs to move and change its sprite direction upon colliding with the platform or with each other. Therefore, we need to load the enemy's horizontally flipped texture.

![texture_pair](https://github.com/user-attachments/assets/f35bf301-57b8-4c5a-9c52-f3c7a50ca461)


