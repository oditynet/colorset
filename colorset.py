#!/usr/bin/env python3
import tkinter as tk
import subprocess
import re

class ScreenColorAdjuster:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Color Adjuster")
        
        self.red = tk.DoubleVar(value=1.0)
        self.green = tk.DoubleVar(value=1.0)
        self.blue = tk.DoubleVar(value=1.0)
        self.brightness = tk.DoubleVar(value=1.0)
        
        self.display, self.crtc = self.detect_display_and_crtc()
        
        self.create_widgets()

    def detect_display_and_crtc(self):
        """Определяем активный дисплей и CRTC"""
        try:
            output = subprocess.check_output(['xrandr', '--verbose']).decode()
            current_display = None
            for line in output.split('\n'):
                if ' connected' in line and ' primary ' in line:
                    current_display = line.split()[0]
                elif current_display and 'CRTC:' in line:
                    crtc = re.search(r'CRTC: (\d+)', line)
                    if crtc:
                        return current_display, crtc.group(1)
            return 'DP-1', '0'  # Fallback values
        except Exception as e:
            print(f"Error: {e}")
            return 'DP-1', '0'

    def update_color(self, *args):
        """Обновляем цвет с использованием CRTC"""
        gamma = (
            f"{self.red.get() * self.brightness.get():.2f}:"
            f"{self.green.get() * self.brightness.get():.2f}:"
            f"{self.blue.get() * self.brightness.get():.2f}"
        )
        try:
            subprocess.run([
                'xrandr',
                '--output', self.display,
                '--crtc', self.crtc,
                '--gamma', gamma
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"xrandr error: {e}")
    def reset_settings(self):
        """Сброс настроек к значениям по умолчанию"""
        self.red.set(1.0)
        self.green.set(1.0)
        self.blue.set(1.0)
        self.brightness.set(1.0)
        self.update_color()

    def save_settings(self):
        """Сохранение настроек в файл"""
        config = f"{self.red.get()}\n{self.green.get()}\n{self.blue.get()}\n{self.brightness.get()}"
        with open(os.path.expanduser('~/.screen_color_config'), 'w') as f:
            f.write(config)

    def load_settings(self):
        """Загрузка сохраненных настроек"""
        try:
            with open(os.path.expanduser('~/.screen_color_config'), 'r') as f:
                values = [float(line.strip()) for line in f.readlines()]
                self.red.set(values[0])
                self.green.set(values[1])
                self.blue.set(values[2])
                self.brightness.set(values[3])
                self.update_color()
        except FileNotFoundError:
            pass

    def create_widgets(self):
        """Создание элементов графического интерфейса"""
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()

        # Регуляторы цветов
        tk.Label(frame, text="Красный").grid(row=0, column=0)
        tk.Scale(frame, variable=self.red, from_=0.1, to=2.0, resolution=0.1,
                 orient=tk.HORIZONTAL, command=self.update_color).grid(row=0, column=1)

        tk.Label(frame, text="Зеленый").grid(row=1, column=0)
        tk.Scale(frame, variable=self.green, from_=0.1, to=2.0, resolution=0.1,
                 orient=tk.HORIZONTAL, command=self.update_color).grid(row=1, column=1)

        tk.Label(frame, text="Синий").grid(row=2, column=0)
        tk.Scale(frame, variable=self.blue, from_=0.1, to=2.0, resolution=0.1,
                 orient=tk.HORIZONTAL, command=self.update_color).grid(row=2, column=1)

        tk.Label(frame, text="Яркость").grid(row=3, column=0)
        tk.Scale(frame, variable=self.brightness, from_=0.1, to=1.0, resolution=0.1,
                 orient=tk.HORIZONTAL, command=self.update_color).grid(row=3, column=1)

        # Кнопки управления
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=4, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Сброс", command=self.reset_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Сохранить", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        tk.Button
    # Остальные методы остаются без изменений (reset_settings, save_settings и т.д.)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenColorAdjuster(root)
    root.mainloop()
