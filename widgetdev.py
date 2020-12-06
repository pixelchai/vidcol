import os
from qtpy import QtWidgets
from ui import widgets
from ui import windows
from util import logger

if __name__ == '__main__':
    # player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True)
    # player.play(os.path.expanduser("~/Downloads/test.webm"))
    # player.wait_for_playback()
    logger.info("VidCol started")

    app = QtWidgets.QApplication([])
    window = windows.PasswordDialog()

    window.show()
    app.exec_()
