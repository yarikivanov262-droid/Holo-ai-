import math

import pygame

from settings import BG_COLOR, FPS, HEIGHT, WIDTH
from entities import Enemy, Gem, Player, Wall


def build_level():
    walls = pygame.sprite.Group()
    gems = pygame.sprite.Group()

    border_thickness = 30
    wall_rects = [
        (0, 0, WIDTH, border_thickness),
        (0, 0, border_thickness, HEIGHT),
        (WIDTH - border_thickness, 0, border_thickness, HEIGHT),
        (0, HEIGHT - border_thickness, WIDTH, border_thickness),
        (500, 250, 120, 400),
        (1200, 250, 180, 200),
        (800, 600, 260, 120),
        (1400, 700, 220, 100),
        (300, 800, 200, 120),
    ]

    for x, y, w, h in wall_rects:
        walls.add(Wall(x, y, w, h))

    for i in range(10):
        angle = (2 * math.pi * i) / 10
        r = 170
        x = WIDTH / 2 + math.cos(angle) * r
        y = HEIGHT / 2 + math.sin(angle) * r
        gems.add(Gem(int(x), int(y)))

    player = Player(220, 220)
    enemies = pygame.sprite.Group(
        Enemy(1600, 200, player),
        Enemy(1500, 850, player),
        Enemy(900, 180, player),
    )

    return walls, gems, player, enemies


def main():
    pygame.init()
    pygame.display.set_caption("Holo Arena")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    walls, gems, player, enemies = build_level()
    bullets = pygame.sprite.Group()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        player.update(dt, None, walls, bullets)
        enemies.update(dt, walls, bullets)
        bullets.update(dt, walls)

        for bullet in list(bullets):
            if bullet.enemy:
                if player.rect.colliderect(bullet.rect):
                    bullet.kill()
            else:
                for enemy in enemies:
                    if enemy.rect.colliderect(bullet.rect):
                        bullet.kill()
                        enemy.kill()
                        break

        for gem in list(gems):
            if player.rect.colliderect(gem.rect):
                gem.kill()
                player.score += 1

        screen.fill(BG_COLOR)
        walls.draw(screen)
        gems.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)
        screen.blit(player.image, player.rect)

        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
