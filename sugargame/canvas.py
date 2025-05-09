import os
from gi.repository import Gtk, GLib
from sugar3.activity.activity import PREVIEW_SIZE
import pygame
import sugargame.event as event

CANVAS = None

class PygameCanvas(Gtk.EventBox):
    def __init__(self, activity, main=None, modules=[pygame]):
        Gtk.EventBox.__init__(self)

        global CANVAS
        assert CANVAS is None, "Only one PygameCanvas can be created."
        CANVAS = self

        self.translator = event.Translator(activity, self)
        self._activity = activity
        self._main = main
        self._modules = modules

        self.set_can_focus(True)

        self._socket = Gtk.Socket()
        self._socket.connect('realize', self._realize_cb)
        self.add(self._socket)

        self.show_all()

    def _realize_cb(self, widget):
        os.environ['SDL_WINDOWID'] = str(widget.get_id())
        for module in self._modules:
            module.init()

        widget.props.window.set_cursor(None)

        r = self.get_allocation()
        self._screen = pygame.display.set_mode((r.width, r.height), pygame.RESIZABLE)

        self.translator.hook_pygame()

        if self._main:
            GLib.idle_add(self._main)

    def get_pygame_widget(self):
        return self._socket

    def get_preview(self):
        if not hasattr(self, '_screen'):
            return None

        _tmp_dir = os.path.join(self._activity.get_activity_root(), 'tmp')
        _file_path = os.path.join(_tmp_dir, 'preview.png')

        width = PREVIEW_SIZE[0]
        height = PREVIEW_SIZE[1]
        _surface = pygame.transform.scale(self._screen, (width, height))
        pygame.image.save(_surface, _file_path)

        with open(_file_path, 'rb') as f:
            preview = f.read()
        os.remove(_file_path)

        return preview
