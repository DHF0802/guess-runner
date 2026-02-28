#!/usr/bin/env python3
"""
简单横版酷跑游戏示例，使用 pygame 实现。

按空格跳跃，避开障碍，按 Esc 或关闭窗口退出。
需要先 `pip install pygame`。
"""

import sys
import random
import pygame

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
GROUND_HEIGHT = 40

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
        self.rect.x = 50
        self.vel_y = 0
        self.jump_strength = -15
        self.gravity = 0.8

    def update(self):
        self.vel_y += self.gravity
        self.rect.y += int(self.vel_y)
        # 限制落地
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.vel_y = 0

    def jump(self):
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.vel_y = self.jump_strength

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        width = random.randint(20, 40)
        height = random.randint(40, 80)
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
        self.rect.x = x
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("横版酷跑小游戏")
    clock = pygame.time.Clock()

    player = Player()
    all_sprites = pygame.sprite.Group(player)
    obstacles = pygame.sprite.Group()

    score = 0
    obstacle_timer = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    player.jump()

        # 生成障碍
        obstacle_timer += dt
        if obstacle_timer > 1500:  # 每1.5秒一障碍
            obstacle = Obstacle(SCREEN_WIDTH + 20)
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            obstacle_timer = 0

        all_sprites.update()

        # 碰撞检测
        if pygame.sprite.spritecollideany(player, obstacles):
            print(f"游戏结束，得分: {score}")
            running = False

        # 更新得分
        score += dt // 10

        # 绘制
        screen.fill((135, 206, 235))  # 天空蓝
        # 地面
        pygame.draw.rect(screen, (50, 205, 50), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        all_sprites.draw(screen)

        # 分数
        font = pygame.font.SysFont(None, 36)
        score_surf = font.render(f"得分: {score}", True, (0, 0, 0))
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
