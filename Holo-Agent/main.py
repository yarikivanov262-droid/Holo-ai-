import time
from pathlib import Path

from config import BULLET_SPEED, MODEL_PATH
from core.aimbot import PredictiveAim
from core.controller import Controller
from core.vision import Vision
from logic.brain import Brain
from telegram_bot.bot import TgBot

ROOT = Path(__file__).resolve().parent
PAUSE_FLAG = ROOT / "pause.flag"


def main():
    vision = Vision(model_path=MODEL_PATH)
    controller = Controller(mode="pc")
    aimbot = PredictiveAim(bullet_speed=BULLET_SPEED)
    brain = Brain()

    bot = TgBot()
    bot.run()

    while True:
        if PAUSE_FLAG.exists():
            time.sleep(1)
            continue

        frame = vision.capture()
        detections = vision.detect(frame)
        brain.think(detections, controller, aimbot)
        time.sleep(0.03)


if __name__ == "__main__":
    main()
