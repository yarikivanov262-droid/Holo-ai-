import math

import pygame

from settings import HEIGHT, WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, 40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.target = pygame.math.Vector2(x, y)
        self.speed = 5.5
        self.shoot_cooldown = 0.0
        self.score = 0

    def update(self, dt, walls, bullets_group):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.target.x = mouse_x
        self.target.y = mouse_y

        direction = self.target - pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        if direction.length() > 1:
            direction = direction.normalize() * self.speed
            next_rect = self.rect.move(direction.x, direction.y)
            if not self._collides_with_walls(next_rect, walls):
                self.rect.x += direction.x
                self.rect.y += direction.y

        self.shoot_cooldown -= dt
        if pygame.mouse.get_pressed()[0] and self.shoot_cooldown <= 0:
            self.shoot_towards(mouse_x, mouse_y, bullets_group)
            self.shoot_cooldown = 0.18

    def _collides_with_walls(self, rect, walls):
        for wall in walls:
            if rect.colliderect(wall.rect):
                return True
        return False

    def shoot_towards(self, target_x, target_y, bullets_group):
        start_x = self.rect.centerx
        start_y = self.rect.centery
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.hypot(dx, dy)
        if distance == 0:
            dx, dy = 1, 0
            distance = 1
        vel_x = dx / distance
        vel_y = dy / distance
        bullets_group.add(Bullet(start_x, start_y, vel_x, vel_y, enemy=False))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.player = player
        self.speed = 1.4
        self.shoot_cooldown = 0.0

    def update(self, dt, walls, bullets_group):
        if self.player is None:
            return

        direction = pygame.math.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery,
        )
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
            next_rect = self.rect.move(direction.x, direction.y)
            if not self._collides_with_walls(next_rect, walls):
                self.rect.x += direction.x
                self.rect.y += direction.y

        self.shoot_cooldown -= dt
        dist = math.hypot(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery,
        )
        if dist < 250 and self.shoot_cooldown <= 0:
            self.shoot_at_player(bullets_group)
            self.shoot_cooldown = 1.0

    def _collides_with_walls(self, rect, walls):
        for wall in walls:
            if rect.colliderect(wall.rect):
                return True
        return False

    def shoot_at_player(self, bullets_group):
        start_x = self.rect.centerx
        start_y = self.rect.centery
        dx = self.player.rect.centerx - start_x
        dy = self.player.rect.centery - start_y
        distance = math.hypot(dx, dy)
        if distance == 0:
            dx, dy = 1, 0
            distance = 1
        vel_x = dx / distance
        vel_y = dy / distance
        bullets_group.add(Bullet(start_x, start_y, vel_x, vel_y, enemy=True))


class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 15
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 255), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, enemy=False):
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        color = (255, 255, 255) if not enemy else (255, 120, 120)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx * 8.0
        self.vy = vy * 8.0
        self.enemy = enemy

    def update(self, dt, walls):
        self.rect.x += self.vx * dt * 60
        self.rect.y += self.vy * dt * 60

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.kill()
                return

        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()
