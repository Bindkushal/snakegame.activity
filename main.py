import random
import sugargame.canvas as canvas
from sugargame.activity import Activity

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS  # 25*25 = 625
WINDOW_HEIGHT = TILE_SIZE * ROWS  # 25*25 = 625

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SnakeGame(Activity):
    def __init__(self, handle):
        super(SnakeGame, self).__init__(handle)
        self._canvas = canvas.PygameCanvas(self, main=self.run_game)
        self.set_canvas(self._canvas)

        # initialize game variables
        self.snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
        self.food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
        self.velocityX = 0
        self.velocityY = 0
        self.snake_body = []  # list of snake body tiles
        self.game_over = False
        self.score = 0

        # Bind the arrow keys for direction changes
        self._canvas.bind("<KeyRelease>", self.change_direction)

    def change_direction(self, e):  # e = event
        if self.game_over:
            return  # edit this code to reset game variables to play again

        if e.keysym == "Up" and self.velocityY != 1:
            self.velocityX = 0
            self.velocityY = -1
        elif e.keysym == "Down" and self.velocityY != -1:
            self.velocityX = 0
            self.velocityY = 1
        elif e.keysym == "Left" and self.velocityX != 1:
            self.velocityX = -1
            self.velocityY = 0
        elif e.keysym == "Right" and self.velocityX != -1:
            self.velocityX = 1
            self.velocityY = 0

    def move(self):
        if self.game_over:
            return

        # Check for collisions with the boundaries
        if self.snake.x < 0 or self.snake.x >= WINDOW_WIDTH or self.snake.y < 0 or self.snake.y >= WINDOW_HEIGHT:
            self.game_over = True
            return

        # Check for collisions with itself
        for tile in self.snake_body:
            if self.snake.x == tile.x and self.snake.y == tile.y:
                self.game_over = True
                return

        # Collision with food
        if self.snake.x == self.food.x and self.snake.y == self.food.y:
            self.snake_body.append(Tile(self.food.x, self.food.y))
            self.food.x = random.randint(0, COLS - 1) * TILE_SIZE
            self.food.y = random.randint(0, ROWS - 1) * TILE_SIZE
            self.score += 1

        # Update snake body
        for i in range(len(self.snake_body) - 1, -1, -1):
            tile = self.snake_body[i]
            if i == 0:
                tile.x = self.snake.x
                tile.y = self.snake.y
            else:
                prev_tile = self.snake_body[i - 1]
                tile.x = prev_tile.x
                tile.y = prev_tile.y

        self.snake.x += self.velocityX * TILE_SIZE
        self.snake.y += self.velocityY * TILE_SIZE

    def draw(self):
        self.move()

        self._canvas.clear()

        # Draw food
        self._canvas.create_rectangle(self.food.x, self.food.y, self.food.x + TILE_SIZE, self.food.y + TILE_SIZE, fill='red')

        # Draw snake
        self._canvas.create_rectangle(self.snake.x, self.snake.y, self.snake.x + TILE_SIZE, self.snake.y + TILE_SIZE, fill='lime green')

        for tile in self.snake_body:
            self._canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='lime green')

        if self.game_over:
            self._canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20", text=f"Game Over: {self.score}", fill="white")
        else:
            self._canvas.create_text(30, 20, font="Arial 10", text=f"Score: {self.score}", fill="white")

        self._canvas.after(100, self.draw)  # call draw again every 100ms (1/10 of a second)

    def run_game(self):
        self.draw()

if __name__ == "__main__":
    from sugargame.activity import main
    main(SnakeGame)
