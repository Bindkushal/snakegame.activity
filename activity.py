from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugargame.canvas import PygameCanvas
import main  # your snake game logic

class SnakeActivity(activity.Activity):
    def __init__(self, handle):
        super(SnakeActivity, self).__init__(handle)
        self.max_participants = 1

        # Set up the Pygame canvas
        self._canvas = PygameCanvas(self)
        self.set_canvas(self._canvas)
        self._canvas.run_pygame(main.main)  # Start your game loop

        # Optional: Add a toolbar
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show_all()
