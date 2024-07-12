A simple platformer game in Python arcade library.

Arcade is a newer Python 2D game engine compared to its classic counterpart, pygame. While it may not have pygame's flexibility and compatibility with nearly every platform, it does offer many built-in features that make game development much easier and more entertaining. Additionally, it comes with better graphics and improved Sprite management.

The primary element of the arcade game engine is the arcade.Window class. This class is responsible for creating the game window and includes built-in functions for handling events, such as clicking, dragging, pressing a key on the keyboard, and updating the screen.

![arcade_window](https://github.com/user-attachments/assets/3e6cb3ca-ff78-466c-b6b6-2479010ea6db)

In order to create the game, we need to inherit our Game class from the arcade.Window class. By rewriting the __init__ function, we can define the initial setup for our game. Additionally, we will need to call super().__init__ to run the game window with its respective width, height, and title arguments. The arcade.Window class has two main functions: on_update and on_draw. In almost every arcade game, we are required to rewrite these two functions in our Game class. The arcade library comes with a specific refresh rate. Each time the window refreshes, it calls the on_update function. After refreshing, it calls the on_draw function to redraw the game window. The on_update function is used to create game object movements. For example, enemies in our platformer game move a few pixels every time the game window refreshes. Then, in the on_draw function, the game draws the new scene again.

Now that we have a good understanding of the core of the arcade library, let's revisit our code and create a simple platformer game. First, we'll define the constants for the game. These constants will include the assets files for the game such as player or enemy assets. We'll also set the scale for each character, the map, and the game window. Additionally, if we want to include sounds in our game (which we do), we can load the sounds using "arcade.load_sound("PATH_TO_SOUND_FILE")" at this stage.

As I mentioned earlier, the arcade library includes an excellent Sprite class. When you provide a sprite texture file, it automatically sets the hitbox and can recognize collisions between sprites. That's why, to create the characters in the game (player, enemies, etc.), we inherit them from the arcade.Sprite class.

![charater](https://github.com/user-attachments/assets/f53a9488-ad42-40b8-a9eb-61ff16b689b4)

We used a circular-shaped Sprite as the main chracter. In the code, we set the changes in sprite x and y coordinates to zero to initialize the object (I should note that the (x=0,y=0) coordination is the bottom-left of the window) . This is done because our character is not moving at this point. We will define the player character's movement later on when a key is pressed on the keyboard event. In the update method, the arcade.Sprite angle property is used to rotate the character if it is moving.

![Enemy](https://github.com/user-attachments/assets/c9790b1c-d402-4766-9215-63a46f36cf40)

Enemy class is slightly more complex as the enemy needs to move and change its sprite direction upon colliding with the platform or with each other. Therefore, we need to load the enemy's horizontally flipped texture.

![texture_pair](https://github.com/user-attachments/assets/f35bf301-57b8-4c5a-9c52-f3c7a50ca461)

I used the Tiled map editor to create the game map. It exports the map as a JSON file which is compatible with the arcade library. The map can be loaded and the platform elements can be understood as sprites. To learn more about tiles by visiting https://www.mapeditor.org/.

Now we created all the elements we needed in our platformer game. Next step we have to add our elements to each level setup and write our events. In this regard, for each level, we create an arcade.scene object and add the map, we created to the scene. Then, we make an instant of our player and every enemy we want in this level and add to the scene with the add_sprite() method. the arcade has a built-in physics engine that handles the physics of the sprite. In this game, we used the arcade.PhysicsEnginePlatformer and added the player sprite to the physics engine. The engine handles player collisions with the platform and the gravity. We also need to create two cameras included in the arcade library. One camera should be fixed on a character to move with it, while the other should constantly display stats on the screen. Then, we can use the camera move_to method to define the camera movement.

![camera](https://github.com/user-attachments/assets/7e8aaf0b-179d-4593-8c25-df64ca8590f5)

The game scene has been created and it is time to handle the events in the game. We need to rewrite every event method of the arcade.Window class that we want to interact with within the game.

![keypress](https://github.com/user-attachments/assets/d5200b48-116d-4bf5-9e68-6d401cf82110)

The on_key_press method is responsible for handling keyboard key presses, and the 'symbol' parameter returns the symbol of the pressed key. In this case, we are defining the actions for when the left, right, and up arrow keys are pressed. The left and right arrow keys are used to move the character left and right, while the up arrow key makes the character jump (the jump mechanism is built into the physics engine). We also handle the Enter key in menus to start the game. However, if, for example, the right arrow key is pressed, the character will move to the right indefinitely. Therefore, we need to handle key releases to stop the character's movement.

![keyrelease](https://github.com/user-attachments/assets/91b9ed12-4e82-4e4f-b997-08a738f2fb7c)

The on_update method of the class is quite long and is responsible for managing the game's movements, dynamics, and collisions. Within this method, enemy movement is first defined by adjusting their center_x coordinate based on their constant speed. Then, we handle player collisions with various sprites such as coins for collecting, teleporters, and enemies, which can cause the player to lose lives and restart the level. To detect these interactions, we use the arcade.check_for_collision_with_list method. Additionally, we utilize the camera movement method that we previously wrote to update the camera.

On the other hand, the on_draw method is quite simple. First, we clear the screen and put the player camera in use (self.camera.use()), and then simply draw the scene (self.scene.draw()). By switching to the constant camera (self.gui_camera.use()), we display the stats on the screen.

At last, we write the main function. Inside the function, we create an instance of the game and keep the game running using arcade.run().
