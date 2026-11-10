import math

from config import HEIGHT, WIDTH


class Brain:
    def think(self, detections, controller, aimbot):
        if not detections:
            controller.move(WIDTH / 2, HEIGHT / 2)
            return

        enemies = [d for d in detections if d.get("class") == "enemy"]
        if enemies:
            center = (WIDTH / 2, HEIGHT / 2)
            nearest = min(
                enemies,
                key=lambda d: math.hypot(d["center"][0] - center[0], d["center"][1] - center[1]),
            )
            aimbot.shoot({"center": nearest["center"], "velocity": (0, 0)}, controller)
            return

        gems = [d for d in detections if d.get("class") == "gem"]
        if gems:
            gem = min(
                gems,
                key=lambda d: math.hypot(d["center"][0] - (WIDTH / 2), d["center"][1] - (HEIGHT / 2)),
            )
            controller.move(*gem["center"])
            return

        controller.move(WIDTH / 2, HEIGHT / 2)
