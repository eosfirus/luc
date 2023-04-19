# Import pygame and random modules
import pygame
import random

# Initialize pygame
pygame.init()

# Define constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define constants for move speed, jump force and gravity
MOVE_SPEED = 5
JUMP_FORCE = 10
GRAVITY = 0.5

# Define constant for background color
BACKGROUND_COLOR = (135, 206, 235)

# Define constant for number of platforms to create
NUM_PLATFORMS = 10

# Create a screen object with the given width and height and fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Create a clock object to control the game loop
clock = pygame.time.Clock()


class Platform(pygame.sprite.Sprite):
    """A class to represent a platform sprite."""

    def __init__(self, color, width, height):
        """Initialize the platform with the given color, width and height."""
        super().__init__()
        # Create a surface with the given width and height
        self.image = pygame.Surface([width, height])
        # Fill the surface with the given color
        self.image.fill(color)
        # Get the rect of the surface
        self.rect = self.image.get_rect()
        # Set the initial x position to a random value between 0 and screen width minus width
        self.rect.x = random.randint(0, SCREEN_WIDTH - width)
        # Set the initial y position to a random value between 0 and screen height minus height
        self.rect.y = random.randint(0, SCREEN_HEIGHT - height)
        # Set the initial horizontal speed to zero
        self.vx = 0
        # Set the initial vertical speed to zero
        self.vy = 0

    def update(self):
        """Update the position of the platform."""
        # Add the horizontal speed to the x position
        self.rect.x += self.vx
        # Add the vertical speed to the y position
        self.rect.y += self.vy

        # If the platform goes beyond the left or right edge of the screen,
        # reverse its horizontal speed
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vx = -self.vx

        # If the platform goes beyond the top or bottom edge of the screen,
        # reverse its vertical speed
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.vy = -self.vy


class Player(pygame.sprite.Sprite):
    """A class to represent a player sprite."""

    def __init__(self, image):
        """Initialize the player with the given image."""
        super().__init__()
        # Load the image from a file
        self.image = pygame.image.load(image)
        # Get the rect of the image
        self.rect = self.image.get_rect()
        # Set the initial center position to (400, 300)
        self.rect.center = (400, 300)
        # Set the initial horizontal speed to move speed
        self.vx = MOVE_SPEED
        # Set the initial vertical speed to zero
        self.vy = 0
        # Set the initial jumping state to False
        self.jumping = False

    def collide_with_platforms(self):
        """Check for collisions between the player and the platforms."""
        # Use spritecollideany to get the first platform that collides with the player
        collision = pygame.sprite.spritecollideany(self, platforms)
        if collision:
            # If the player is moving down,
            if self.vy > 0:
                # Set the bottom of the player to the top of the platform
                self.rect.bottom = collision.rect.top
                # Set the vertical speed to zero
                self.vy = 0
                # Set the jumping state to False
                player.jumping = False


# Create a player object with the given image file
player = Player("player.png")

# Create a group to store all the platforms
platforms = pygame.sprite.Group()

# Create a ground platform and add it to the group
ground_platform = Platform((255, 255, 255), SCREEN_WIDTH, 20)
# Set the position of the ground platform at the bottom of the screen minus player height 
ground_platform.rect.y = SCREEN_HEIGHT - ground_platform.rect.height - player.rect.height 
platforms.add(ground_platform)

# Create a list of colors for the platforms 
colors = [
    (255, 0, 0),    # Red 
    (255, 165, 0),  # Orange 
    (255, 255, 0),  # Yellow 
    (0, 255, 0),    # Green 
    (0, 0, 255),    # Blue 
    (75, 0, 130),   # Indigo 
    (238, 130, 238),# Violet 
    (255, 192, 203),# Pink 
    (128, 128, 128),# Gray 
    (255, 255, 255) # White
]

# Use list comprehension to create NUM_PLATFORMS platforms with different colors,
# widths, heights and positions and add them to the group
platforms.add([
    Platform(
        random.choice(colors),          # Choose a random color from the list
        random.randint(100, 200),       # Choose a random width between 100 and 200 pixels
        20                              # Set a fixed height of 20 pixels
    ) for i in range(NUM_PLATFORMS)    # Repeat for NUM_PLATFORMS times
])

# Use a for loop to set the x and y positions of each platform in the group
for i, platform in enumerate(platforms):
    # Skip the ground platform as it already has a fixed position
    if i == 0:
        continue

    # Set the x position of the platform based on its index and width
    platform.rect.x = SCREEN_WIDTH // (NUM_PLATFORMS + 1) * (i + 1) - platform.rect.width // 2

    # Set the y position of the platform based on its index and height
    platform.rect.y = SCREEN_HEIGHT - ground_platform.rect.height - platform.rect.height * (i + 1)

# Create a boolean variable to control the game loop
running = True

# Create a variable to store the camera offset
camera_offset = 0

# Start the game loop
while running:
    # Set the frame rate to 60 FPS
    clock.tick(60)

    # Handle events in pygame
    for event in pygame.event.get():
        # If the user clicks on the close button,
        if event.type == pygame.QUIT:
            # Stop the game loop by setting running to False
            running = False

        # If a key is pressed down,
        if event.type == pygame.KEYDOWN:
            # If F11 or ESC is pressed,
            if event.key == pygame.K_F11 or event.key == pygame.K_ESCAPE:
                # Toggle fullscreen mode by calling toggle_fullscreen()
                pygame.display.toggle_fullscreen()

        # If the window is resized,
        if event.type == pygame.VIDEORESIZE:
            # Get the new width and height of the window
            new_width = event.w
            new_height = event.h
            # Resize the screen object with the new dimensions
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    # Get a dictionary of all pressed keys in pygame
    keys = pygame.key.get_pressed()

    # If left arrow key is pressed,
    if keys[pygame.K_LEFT]:
        # Set the horizontal speed of the player to negative move speed
        player.vx = -MOVE_SPEED

        # Decrease the camera offset by move speed
        camera_offset -= MOVE_SPEED
# If left arrow key is pressed,
    if keys[pygame.K_LEFT]:
        # Set the horizontal speed of the player to negative move speed
        player.vx = -MOVE_SPEED

        # Decrease the camera offset by move speed
        camera_offset -= MOVE_SPEED

        # Use a for loop to move all the platforms in the group to the right by move speed
        for platform in platforms:
            platform.rect.x += MOVE_SPEED

            # If the platform goes beyond the right edge of the screen,
            if platform.rect.left > SCREEN_WIDTH:
                # Remove it from the group
                platforms.remove(platform)

                # Create a new platform with a random color, width and height and add it to the group
                new_platform = Platform(
                    random.choice(colors),
                    random.randint(100, 200),
                    20
                )
                platforms.add(new_platform)

                # Set the x position of the new platform to the left edge of the screen minus its width
                new_platform.rect.x = -new_platform.rect.width

                # Set the y position of the new platform to a random value between ground platform height and screen height minus its height
                new_platform.rect.y = random.randint(ground_platform.rect.height, SCREEN_HEIGHT - new_platform.rect.height)

    # If right arrow key is pressed,
    elif keys[pygame.K_RIGHT]:
        # Set the horizontal speed of the player to positive move speed
        player.vx = MOVE_SPEED

        # Increase the camera offset by move speed
        camera_offset += MOVE_SPEED

        # Use a for loop to move all the platforms in the group to the left by move speed
        for platform in platforms:
            platform.rect.x -= MOVE_SPEED

            # If the platform goes beyond the left edge of the screen,
            if platform.rect.right < 0:
                # Remove it from the group
                platforms.remove(platform)

                # Create a new platform with a random color, width and height and add it to the group
                new_platform = Platform(
                    random.choice(colors),
                    random.randint(100, 200),
                    20
                )
                platforms.add(new_platform)

                # Set the x position of the new platform to the right edge of the screen plus its width
                new_platform.rect.x = SCREEN_WIDTH + new_platform.rect.width

                # Set the y position of the new platform to a random value between ground platform height and screen height minus its height
                new_platform.rect.y = random.randint(ground_platform.rect.height, SCREEN_HEIGHT - new_platform.rect.height)

    # Otherwise,
    else:
        # Set the horizontal speed of the player to zero
        player.vx = 0

    # If space key is pressed and the player is not jumping,
    if keys[pygame.K_SPACE] and not player.jumping:
        # Set the jumping state of the player to True
        player.jumping = True
        # Set the vertical speed of the player to negative jump force
        player.vy = -JUMP_FORCE

    # Add gravity to the vertical speed of the player
    player.vy += GRAVITY

    # Check for collisions between the player and the platforms
    player.collide_with_platforms()

    # If the player falls off from any platform,
    if player.rect.bottom > SCREEN_HEIGHT:
        # Reset the position and speed of the player 
        player.rect.center = (400, 300)
        player.vx = MOVE_SPEED
        player.vy = 0
        player.jumping = False

        # Reset the position and speed of all platforms in the group 
        for i, platform in enumerate(platforms):
            # Skip the ground platform as it already has a fixed position 
            if i == 0:
                continue

            # Set the x position of the platform based on its index and width 
            platform.rect.x = SCREEN_WIDTH // (NUM_PLATFORMS + 1) * (i + 1) - platform.rect.width // 2

            # Set the y position of the platform based on its index and height 
            platform.rect.y = SCREEN_HEIGHT - ground_platform.rect.height - platform.rect.height * (i + 1)

            # Set the horizontal and vertical speed of each platform to zero 
            platform.vx = 0 
            platform.vy = 0 

   # Fill the screen with the background color
    screen.fill(BACKGROUND_COLOR)

    # Update the platforms in the group
    platforms.update()

    # Create a new surface to draw the screen image on
    screen_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Fill the surface with the background color
    screen_image.fill(BACKGROUND_COLOR)

    # Use a for loop to blit the platforms on the screen image surface
    for platform in platforms:
        screen_image.blit(platform.image, (platform.rect.x, platform.rect.y))

    # Blit the player on the screen image surface
    screen_image.blit(player.image, (player.rect.x, player.rect.y))

    # Rotate and scale the screen image by a factor of 2
    screen_image = pygame.transform.rotozoom(screen_image, 0, 2)

    # Blit the screen image on the screen with an offset to center it and translate it by the camera offset times 2
    screen.blit(screen_image, (-SCREEN_WIDTH // 2 - camera_offset * 2, -SCREEN_HEIGHT // 2))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
