import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Flappy Bird Clone"

class FlappyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome to Flappy Bird!", 200, 300, arcade.color.BLACK, 24)

if __name__ == "__main__":
    window = FlappyGame()
    arcade.run()
