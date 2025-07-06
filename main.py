import arcade
import arcade.color

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Flappy Bird Clone"

MENU = 0
GAME = 1
GAME_OVER = 2

GRAVITY = 0.5
FLAP_STRENGTH = 10
BIRD_SCALE = 0.05
BIRD_START_X = 100
BIRD_START_Y = SCREEN_HEIGHT // 2

PIPE_COLOR = arcade.color.GREEN



class FlappyBird(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.bird_list = None
        self.bird = None
        self.pipe_list = None
        self.game_state = MENU
        self.score = 0

        self.hit_sound = arcade.load_sound("assets/sounds/hit.wav")
        


    def setup(self):
        self.bird_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()

        self.bird = arcade.Sprite("assets/images/bird.png", BIRD_SCALE)
        self.bird.center_x = BIRD_START_X
        self.bird.center_y = BIRD_START_Y
        self.bird.change_y = 0
        self.bird_list.append(self.bird)
        self.score = 0

        # Create top and bottom pipes with a visible gap
        pipe_width = 80
        pipe_gap_size = 180  # Make gap wide enough
        pipe_center = 300

        # Create pipe textures
        pipe_texture = arcade.make_soft_square_texture(80, PIPE_COLOR, outer_alpha=255)

        # Top pipe
        top_pipe_height = SCREEN_HEIGHT - (pipe_center + pipe_gap_size // 2)
        top_pipe = arcade.Sprite()
        top_pipe.texture = pipe_texture
        top_pipe.width = pipe_width
        top_pipe.height = top_pipe_height
        top_pipe.center_x = SCREEN_WIDTH + 100
        top_pipe.center_y = SCREEN_HEIGHT - top_pipe_height // 2
        self.pipe_list.append(top_pipe)

        # Bottom pipe
        bottom_pipe_height = pipe_center - pipe_gap_size // 2
        bottom_pipe = arcade.Sprite()
        bottom_pipe.texture = pipe_texture
        bottom_pipe.width = pipe_width
        bottom_pipe.height = bottom_pipe_height
        bottom_pipe.center_x = SCREEN_WIDTH + 100
        bottom_pipe.center_y = bottom_pipe_height // 2
        self.pipe_list.append(bottom_pipe)

        top_pipe.scored = False
        bottom_pipe.scored = False



    def on_draw(self):
        self.clear()
        
        if self.game_state == MENU:
            arcade.draw_text("Flappy Bird", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                            arcade.color.BLACK, 40, anchor_x="center")
            arcade.draw_text("Press SPACE to Start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                            arcade.color.BLACK, 20, anchor_x="center")
            

        elif self.game_state == GAME:
            self.bird_list.draw()
            self.pipe_list.draw()


             # 👉 Draw the score in the top-left corner
            arcade.draw_text(f"Score: {int(self.score)}", 10, SCREEN_HEIGHT - 30,
                         arcade.color.BLACK, 20)

        elif self.game_state == GAME_OVER:
            arcade.draw_text("Game Over!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                            arcade.color.RED, 40, anchor_x="center")
            arcade.draw_text("Press SPACE to Return to Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                            arcade.color.BLACK, 20, anchor_x="center")
            


    def on_update(self, delta_time):
        if self.game_state != GAME:
            return

        self.bird.change_y -= GRAVITY
        self.bird.center_y += self.bird.change_y

        for pipe in self.pipe_list:
            pipe.center_x -= 3

            if pipe.right < 0:
                pipe.center_x = SCREEN_WIDTH + 100
                pipe.scored = False

        # Collision detection
        if arcade.check_for_collision_with_list(self.bird, self.pipe_list) or self.bird.bottom <= 0:
            self.game_state = GAME_OVER
            arcade.play_sound(self.hit_sound)
        


        # Scoring logic
        for pipe in self.pipe_list:
            if not hasattr(pipe, "scored"):
                pipe.scored = False
            if not pipe.scored and pipe.center_x + pipe.width / 2 < self.bird.center_x:
                self.score += 0.5
                pipe.scored = True

        # Ground collision
        if self.bird.bottom <= 0:
            self.game_state = GAME_OVER



    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.game_state == MENU:
                self.setup()
                self.game_state = GAME
            elif self.game_state == GAME_OVER:
                self.game_state = MENU
            elif self.game_state == GAME:
                self.bird.change_y = FLAP_STRENGTH

    # def on_mouse_press(self, x, y, button, modififers):
    #     if self.current_state == MENU:
    #         self.current_state = GAME
    #         self.setup()

if __name__ == "__main__":
    window = FlappyBird()
    window.setup()
    arcade.run()

