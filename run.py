import sys
import os

# Получаем путь к папке, где лежит run.py (корень проекта Ashfall)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR) # Меняем рабочую директорию на корень проекта
sys.path.append(os.path.join(BASE_DIR, 'CodeFolder')) # Добавляем папку с кодом в пути

from main import Game

if __name__ == "__main__":
    game = Game()
    game.run()