import os
import mpv
from qtpy import QtWidgets
from ui.windows import MainWindow
from util import logger

if __name__ == '__main__':
    # player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True)
    # player.play(os.path.expanduser("~/Downloads/test.webm"))
    # player.wait_for_playback()
    logger.info("VidCol started")

    app = QtWidgets.QApplication([])
    main_window = MainWindow()

    main_window.show()
    app.exec_()
