import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import random
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from data_txt import DATA

kivy.require('2.0.0')

class Card(Button):
    card_id = StringProperty(None)
    is_face_up = BooleanProperty(False)
    card_type = StringProperty("текст") # Тип карточки (текст, картинка, звук)
    front_value = StringProperty("") # Значение на лицевой стороне карточки
    back_color = (0.8, 0.8, 0.8, 1)
    front_color = (1, 1, 1, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = self.back_color # Серый фон
        self.color = (0, 0, 0, 1)  # Черный текст
        self.font_size = 24

    def on_release(self):
        self.flip_card()

    def flip_card(self):
        if not self.is_face_up:
            self.is_face_up = True
            self.background_color = self.front_color # Белый фон при открытии
            self.text = str(self.front_value) # Отображаем значение
            if self.card_type == "звуки":
                sound = SoundLoader.load(self.front_value)
                if sound:
                    sound.play()
            # Сообщаем MemoryGrid, что карточка открыта
            self.parent.card_selected(self)
        else:
            # Если карточка уже открыта, ничего не делаем
            pass

    def reset_card(self):
        self.is_face_up = False
        self.background_color = self.back_color
        self.text = ""

class MemoryGrid(GridLayout):
    first_card = None
    second_card = None

    def __init__(self, game_type="текст", **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.rows = 3
        self.spacing = 10
        self.padding = 10
        self.game_type = game_type
        self.card_values = self.choose_card_values() # Выбираем значения для карточек
        self.cards = [] # Список карточек

        self.init_grid()

    def choose_card_values(self):
        """Выбирает случайные пары значений из базы данных."""
        values = random.sample(DATA[self.game_type], self.cols * self.rows // 2)
        # Дублируем значения для создания пар
        values = values + values
        random.shuffle(values)
        return values

    def init_grid(self):
        """Создает сетку карточек с выбранными значениями."""
        for i in range(self.cols * self.rows):
            card_value = self.card_values[i]
            front_value = card_value[0] if self.game_type == "текст" else card_value # Отображаем первый элемент пары

            card = Card(card_id=str(i), card_type=self.game_type, front_value=str(front_value))
            self.cards.append(card)
            self.add_widget(card)

    def card_selected(self, card):
        """Обрабатывает выбор карточки."""
        if self.first_card is None:
            # Это первая открытая карточка
            self.first_card = card
        elif self.second_card is None:
            # Это вторая открытая карточка
            self.second_card = card
            # Проверяем совпадение
            if self.first_card.front_value == self.second_card.front_value:
                # Карточки совпадают, оставляем их открытыми
                self.first_card = None
                self.second_card = None
            else:
                # Карточки не совпадают, переворачиваем их обратно через некоторое время
                Clock.schedule_once(self.reset_cards, 1)  # Переворот через 1 секунду
    def reset_cards(self, dt):
        """Переворачивает карточки обратно."""
        self.first_card.reset_card()
        self.second_card.reset_card()
        self.first_card = None
        self.second_card = None

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title_label = Label(text="Memory Lane", font_size=32, halign='center', size_hint_y=None, height=60)
        layout.add_widget(title_label)

        text_button = Button(text="Текст", on_press=self.go_to_game, size_hint_y=None, height=50)
        text_button.game_type = "текст" # Передаем тип игры
        layout.add_widget(text_button)

        image_button = Button(text="Картинки", on_press=self.go_to_game, size_hint_y=None, height=50)
        image_button.game_type = "картинки"
        layout.add_widget(image_button)

        sound_button = Button(text="Звуки", on_press=self.go_to_game, size_hint_y=None, height=50)
        sound_button.game_type = "звуки"
        layout.add_widget(sound_button)

        self.add_widget(layout)

    def go_to_game(self, instance):
        """Переход к игровому экрану с выбранным типом игры."""
        game_type = instance.game_type
        game_screen = GameScreen(name='game', game_type=game_type)
        self.manager.add_widget(game_screen) # Добавляем экран в ScreenManager
        self.manager.current = 'game'  # Переключаемся на игровой экран

class GameScreen(Screen):
    def __init__(self, game_type="текст", **kwargs):
        super().__init__(**kwargs)
        self.game_type = game_type
        self.grid = MemoryGrid(game_type=self.game_type)
        self.add_widget(self.grid)

class ScreenManagement(ScreenManager):
    pass

class MemoryApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Белый фон
        sm = ScreenManagement()
        sm.add_widget(MenuScreen(name='menu')) # Добавляем экран меню
        sm.current = 'menu'
        return sm

if __name__ == '__main__':
    MemoryApp().run()
