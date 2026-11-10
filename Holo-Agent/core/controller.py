import pyautogui

from config import ATTACK_BTN_X, ATTACK_BTN_Y

try:
    import adbutils
except ImportError:  # pragma: no cover
    adbutils = None


class Controller:
    def __init__(self, mode="pc", adb=None):
        self.mode = mode.lower()
        self.adb = adb
        if self.mode == "android" and adb is None and adbutils is not None:
            self.adb = adbutils.AdbClient()

    def move(self, x, y):
        if self.mode == "android" and self.adb is not None:
            self.adb.shell(f"input touchscreen tap {int(x)} {int(y)}")
            return
        pyautogui.moveTo(int(x), int(y), duration=0.05)

    def shoot_at(self, x, y):
        if self.mode == "android" and self.adb is not None:
            self.adb.shell(f"input swipe {ATTACK_BTN_X} {ATTACK_BTN_Y} {int(x)} {int(y)} 100")
            return
        pyautogui.click(x=int(x), y=int(y))

    def tap(self, x, y):
        if self.mode == "android" and self.adb is not None:
            self.adb.shell(f"input touchscreen tap {int(x)} {int(y)}")
            return
        pyautogui.click(x=int(x), y=int(y))
