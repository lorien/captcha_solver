import os

from .browser import BrowserBackend


class CaptchaWindow(object):
    def __init__(self, path, solution):
        import pygtk
        import gtk

        pygtk.require('2.0')
        self.solution = solution
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.show()
        self.window.connect('destroy', self.destroy)
        self.box = gtk.HBox()
        self.image = gtk.Image()
        self.image.set_from_file(path)
        self.entry = gtk.Entry()
        self.entry.connect('activate', self.solve)
        self.button = gtk.Button('Go')
        self.button.connect('clicked', self.solve)

        self.window.add(self.box)
        self.box.pack_start(self.image)
        self.box.pack_start(self.entry)
        self.box.pack_start(self.button)
        self.box.show()
        self.image.show()
        self.button.show()
        self.entry.show()
        self.entry.grab_focus()

    def destroy(self, *args):
        import gtk

        gtk.main_quit()

    def solve(self, *args):
        import gtk

        solution = self.entry.get_text()
        if hasattr(solution, 'decode'):
            solution = solution.decode('utf8')
        self.solution.append(solution)
        self.window.hide()
        gtk.main_quit()

    def main(self):
        import gtk

        gtk.main()


class GuiBackend(BrowserBackend):
    def parse_check_solution_response(self, res):
        path = res['url'].replace('file://', '')
        solution = []
        window = CaptchaWindow(path, solution)
        window.main()
        os.unlink(path)
        return solution[0]
