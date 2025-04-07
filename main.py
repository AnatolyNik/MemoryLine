# Memory Line

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.core.window import Window

kivy.require('2.0.0')

class MemoryButton(Button):
    card_id = StringProperty(None)

    def on_release(self):
        # Обработка нажатия на карточку
        pass

class MemoryGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MemoryGrid, self).__init__(**kwargs)
        self.cols = 4 # Количество столбцов
        self.rows = 4 # Количество строк
        self.spacing = 10
        self.padding = 10

        # Создание карточек (пример)
        for i in range(16):
            btn = MemoryButton(text=str(i), card_id=str(i))
            self.add_widget(btn)

class MemoryApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1) # Белый фон
        return MemoryGrid()

if __name__ == '__main__':
    MemoryApp().run()
