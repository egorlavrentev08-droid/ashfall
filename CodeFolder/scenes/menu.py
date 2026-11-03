import pygame
import os
import random
import math
from CodeFolder.config import *

class Particle:
    def __init__(self, ember=False):
        self.x = random.randint(0, BASE_WIDTH)
        self.y = random.randint(-50, BASE_HEIGHT)
        
        if ember:
            self.speed_y = random.uniform(-60, -30)
            self.speed_x = random.uniform(-10, 10)
            self.size = random.randint(1, 3)
            self.color = EMBER_COLOR
            self.life = random.uniform(1.0, 2.0)
        else:
            self.speed_y = random.uniform(10, 40)
            self.speed_x = random.uniform(-15, 15)
            self.size = random.randint(1, 2)
            self.color = ASH_COLOR
            self.life = 999

    def update(self, dt):
        self.y += self.speed_y * dt
        self.x += self.speed_x * dt
        self.life -= dt
        if self.y > BASE_HEIGHT + 10 or self.y < -10 or self.x < -10 or self.x > BASE_WIDTH + 10 or self.life <= 0:
            self.respawn()

    def respawn(self):
        if self.color == EMBER_COLOR:
            self.x = random.randint(0, BASE_WIDTH)
            self.y = BASE_HEIGHT + random.randint(0, 50)
            self.life = random.uniform(1.0, 2.0)
        else:
            self.x = random.randint(0, BASE_WIDTH)
            self.y = random.randint(-50, -10)

    def draw(self, surface):
        alpha = int(255 * (self.life / 0.5)) if self.life < 0.5 else 255
        particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, (*self.color, alpha), (self.size, self.size), self.size)
        surface.blit(particle_surf, (self.x, self.y))


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.time = 0 
        
        self.font_title = pygame.font.SysFont("impact", 100)
        self.font_btn = pygame.font.SysFont("consolas", 24, bold=True)
        self.font_main_btn = pygame.font.SysFont("impact", 40)
        
        # Загрузка фона
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        bg_path = os.path.join(base_dir, "AssetsFolder", "sprites", "bg_menu.png")
        
        try:
            self.bg_image = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (BASE_WIDTH, BASE_HEIGHT))
        except Exception as e:
            print(f"ОШИБКА ЗАГРУЗКИ ФОНА: {e}")
            self.bg_image = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
            self.bg_image.fill((20, 20, 20))

        self.overlay = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        self.overlay.set_alpha(50) 
        self.overlay.fill((0, 0, 0))

        # --- ПЕРСОНАЖ (3 кадра дыхания) ---
        self.hero_x = BASE_WIDTH // 2
        self.hero_y = BASE_HEIGHT - 260 
        
        self.hero_frames = []
        try:
            # Загружаем три кадра
            for i in range(1, 4):
                path = os.path.join(base_dir, "AssetsFolder", "sprites", f"hero{i}.png")
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (128, 192))
                self.hero_frames.append(img)
        except Exception as e:
            print(f"ОШИБКА ЗАГРУЗКИ КАДРОВ ГЕРОЯ: {e}")
            # Заглушка
            surf = pygame.Surface((128, 192), pygame.SRCALPHA)
            pygame.draw.rect(surf, (180, 40, 40), (24, 60, 80, 100), border_radius=6)
            self.hero_frames = [surf, surf.copy(), surf.copy()]

        # Переменные для анимации
        self.current_frame = 1 
        self.anim_timer = 0
        self.anim_speed = 0.4 

        # Частицы
        self.particles = []
        for _ in range(60):
            self.particles.append(Particle(ember=False))
        for _ in range(10):
            self.particles.append(Particle(ember=True))

        # --- КНОПКИ ---
        self.btn_play = {
            "text": "ВОЙТИ В ПУСТОШЬ", 
            "action": self.start_game, 
            "rect": pygame.Rect(BASE_WIDTH - 480, BASE_HEIGHT - 120, 440, 80),
            "hovered": False
        }

        icon_size = 50
        margin = 20
        self.top_buttons = [
            {"action": self.game.quit_game, "rect": pygame.Rect(margin, margin, icon_size, icon_size), "hovered": False, "icon": "exit"},
            {"action": self.dummy, "rect": pygame.Rect(margin * 2 + icon_size, margin, icon_size, icon_size), "hovered": False, "icon": "settings"},
            {"action": self.dummy, "rect": pygame.Rect(margin * 3 + icon_size * 2, margin, icon_size, icon_size), "hovered": False, "icon": "profile"}
        ]

    def start_game(self):
        from CodeFolder.scenes.class_select import ClassSelectScene
        self.game.change_scene(ClassSelectScene(self.game))

    def dummy(self):
        print("В разработке...")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.quit_game()
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_play["hovered"]:
                self.btn_play["action"]()
            for btn in self.top_buttons:
                if btn["hovered"]:
                    btn["action"]()

    def update(self, dt):
        self.time += dt 
        mouse_pos = pygame.mouse.get_pos()
        
        self.btn_play["hovered"] = self.btn_play["rect"].collidepoint(mouse_pos)
        for btn in self.top_buttons:
            btn["hovered"] = btn["rect"].collidepoint(mouse_pos)

        for p in self.particles:
            p.update(dt)

        # --- ЛОГИКА ДЫХАНИЯ ---
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            # Плавный цикл: вдох (0) -> стойка (1) -> выдох (2) -> стойка (1) -> вдох (0)
            if self.current_frame == 0:
                self.current_frame = 1
            elif self.current_frame == 1:
                # Здесь можно добавить рандом, чтобы он иногда просто стоял
                self.current_frame = 2
            elif self.current_frame == 2:
                self.current_frame = 1

    def draw_icon(self, surface, rect, icon_type, color):
        if icon_type == "exit":
            pygame.draw.line(surface, color, (rect.x+15, rect.y+15), (rect.x+35, rect.y+35), 3)
            pygame.draw.line(surface, color, (rect.x+35, rect.y+15), (rect.x+15, rect.y+35), 3)
        elif icon_type == "settings":
            pygame.draw.circle(surface, color, rect.center, 12, 3)
            pygame.draw.circle(surface, color, rect.center, 4)
            for i in range(8):
                angle = i * math.pi / 4
                x1 = rect.centerx + math.cos(angle) * 14
                y1 = rect.centery + math.sin(angle) * 14
                x2 = rect.centerx + math.cos(angle) * 20
                y2 = rect.centery + math.sin(angle) * 20
                pygame.draw.line(surface, color, (x1, y1), (x2, y2), 3)
        elif icon_type == "profile":
            pygame.draw.circle(surface, color, (rect.centerx, rect.y + 16), 8, 3)
            pygame.draw.arc(surface, color, (rect.x + 10, rect.y + 24, 30, 30), 0, math.pi, 3)

    def draw(self, surface):
        surface.blit(self.bg_image, (0, 0))
        surface.blit(self.overlay, (0, 0))

        # --- РИСУЕМ ПЕРСОНАЖА ---
        current_img = self.hero_frames[self.current_frame]
        hero_rect = current_img.get_rect(center=(self.hero_x, self.hero_y))
        
        # 1. Тень
        shadow_surf = pygame.Surface((100, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 120), (0, 0, 100, 30))
        surface.blit(shadow_surf, (hero_rect.centerx - 50, hero_rect.bottom - 15))

        # 2. Герой
        surface.blit(current_img, hero_rect)

        # Частицы
        for p in self.particles:
            p.draw(surface)

        # Логотип
        title_surf = self.font_title.render("ASHFALL", True, (200, 40, 30))
        title_shadow = self.font_title.render("ASHFALL", True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(BASE_WIDTH // 2, 100))
        surface.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        surface.blit(title_surf, title_rect)

        # --- ОТРИСОВКА ВЕРХНИХ КНОПОК ---
        for btn in self.top_buttons:
            bg_color = (60, 20, 20, 200) if btn["hovered"] else (10, 10, 10, 150)
            border_color = (255, 60, 40) if btn["hovered"] else (100, 100, 100)
            icon_color = (255, 255, 255) if btn["hovered"] else (180, 180, 180)

            btn_surf = pygame.Surface((btn["rect"].width, btn["rect"].height), pygame.SRCALPHA)
            btn_surf.fill(bg_color)
            surface.blit(btn_surf, btn["rect"].topleft)
            
            pygame.draw.rect(surface, border_color, btn["rect"], 2)
            self.draw_icon(surface, btn["rect"], btn["icon"], icon_color)

        # --- ОТРИСОВКА КНОПКИ "ВОЙТИ" ---
        bg_color = (120, 30, 20, 230) if self.btn_play["hovered"] else (20, 20, 20, 200)
        border_color = (255, 80, 60) if self.btn_play["hovered"] else (150, 150, 150)
        text_color = (255, 255, 255) if self.btn_play["hovered"] else (200, 200, 200)

        play_surf = pygame.Surface((self.btn_play["rect"].width, self.btn_play["rect"].height), pygame.SRCALPHA)
        play_surf.fill(bg_color)
        surface.blit(play_surf, self.btn_play["rect"].topleft)
        
        pygame.draw.rect(surface, border_color, self.btn_play["rect"], 3)
        
        text_surf = self.font_main_btn.render(self.btn_play["text"], True, text_color)
        text_rect = text_surf.get_rect(center=self.btn_play["rect"].center)
        surface.blit(text_surf, text_rect)