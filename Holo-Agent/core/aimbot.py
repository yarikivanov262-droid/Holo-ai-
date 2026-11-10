import math

from config import BULLET_SPEED


class PredictiveAim:
    def __init__(self, bullet_speed=BULLET_SPEED):
        self.bullet_speed = bullet_speed

    def calculate_lead(self, target_center, target_velocity, player_pos=(960, 540)):
        px, py = player_pos
        tx, ty = target_center
        vx, vy = target_velocity

        dx = tx - px
        dy = ty - py
        distance = math.hypot(dx, dy)
        if distance <= 0:
            return (tx, ty)

        flight_time = distance / self.bullet_speed
        return (tx + vx * flight_time, ty + vy * flight_time)

    def shoot(self, target, controller):
        if not target:
            return

        center = target.get("center", (960, 540))
        velocity = target.get("velocity", (0, 0))
        predicted = self.calculate_lead(center, velocity)
        controller.shoot_at(*predicted)
