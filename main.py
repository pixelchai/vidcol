import os
import mpv

player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True)
player.play(os.path.expanduser("~/Downloads/Model.webm"))
player.wait_for_playback()
