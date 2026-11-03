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
            # Заглушка, если картинок нет
            surf = pygame.Surface((128, 192), pygame.SRCALPHA)
            pygame.draw.rect(surf, (180, 40, 40), (24, 60, 80, 100), border_radius=6)
            # Добавляем 3 одинаковые заглушки, чтобы анимация не сломалась
            self.hero_frames = [surf, surf.copy(), surf.copy()]

        # Переменные для анимации дыхания
        self.current_frame = 1 # 0 - вдох, 1 - стойка, 2 - выдох
        self.anim_timer = 0
        self.anim_speed = 0.4 # Скорость смены кадров (в секундах)

        # Частицы
        self.particles = []
        for _ in range(60):
            self.particles.append(Particle(ember=False))
        for _ in range(10):
            self.particles.append(Particle(ember=True))

        # --- КНОПКИ ---
        # 1. Главная кнопка (Справа снизу)
        self.btn_play = {
            "text": "ВОЙТИ В ПУСТОШЬ", 
            "action": self.start_game, 
            "rect": pygame.Rect(BASE_WIDTH - 480, BASE_HEIGHT - 120, 440, 80),
            "hovered": False
        }

        # 2. Верхние кнопки (Слева сверху)
        icon_size = 50
        margin = 20
        self.top_buttons = [
            {"action": self.game.quit_game, "rect": pygame.Rect(margin, margin, icon_size, icon_size), "hovered": False, "icon": "exit"},
            {"action": self.dummy, "rect": pygame.Rect(margin * 2 + icon_size, margin, icon_size, icon_size), "hovered": False, "icon": "settings"},
            {"action": self.dummy, "rect": pygame.Rect(margin * 3 + icon_size * 2, margin, icon_size, icon_size), "hovered": False, "icon": "profile"}
        ]