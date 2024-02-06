import json
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup


class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.create_buttons()

    def create_buttons(self):
        play_button = Button(text="Oyna", size_hint=(1, 1), size=(150, 50),font_size=90)
        play_button.bind(on_press=self.start_game)
        exit_button = Button(text="Çıkış", size_hint=(1, 1), size=(150, 50),font_size=90)
        exit_button.bind(on_press=self.quit_game)
        
        self.add_widget(Widget(size_hint_y=None, height=100))
        self.add_widget(Label(text="Adam", font_size=200))
        self.add_widget(Label(text="Asmaca", font_size=200))
        self.add_widget(Widget(size_hint_y=None, height=100))
        self.add_widget(play_button)
        self.add_widget(Widget(size_hint_y=None, height=100))
        self.add_widget(Label(text="Bu oyun paşasından şişkosuna", font_size=50))
        self.add_widget(Label(text="Doğum Günü Hediyesidir", font_size=50))
        self.add_widget(Widget(size_hint_y=None, height=100))
        self.add_widget(exit_button)
        self.add_widget(Widget(size_hint_y=None, height=100))

    def start_game(self, instance):
        hangman_app.root_window.remove_widget(self)
        hangman_app.root_window.add_widget(HangmanGame())

    def quit_game(self, instance):
        App.get_running_app().stop()

class SettingsPopup(Popup):
    def __init__(self, hangman_game, **kwargs):
        super(SettingsPopup, self).__init__(**kwargs)
        self.hangman_game = hangman_game
        self.title = "Ayarlar"
        self.size_hint = (1, None)
        self.size = (300, 200)  # Pop-up penceresinin boyutunu ayarlayın
        self.auto_dismiss = True  # Otomatik kapatmayı devre dışı bırak
        self.background_color = (1, 1, 1, 0.5)  # Arka planın transparan olmasını sağlar

        layout = BoxLayout(orientation="vertical")
        self.slider = Slider(min=10, max=100, value=self.hangman_game.font_size)
        self.slider.bind(value=self.update_font_size)
        layout.add_widget(self.slider)

        self.content = layout

    def update_font_size(self, instance, value):
        self.hangman_game.font_size = value
        self.hangman_game.hangman_display.font_size = value
        self.hangman_game.word_display.font_size = value
        self.hangman_game.feedback_display.font_size = value
        # Klavye düğmelerinin font boyutunu güncellemek istiyorsanız, buraya ekleyin
        for button in self.hangman_game.keyboard_buttons:
            button.font_size = value

class HangmanGame(BoxLayout):
    guessed_letters = ListProperty([])
    word_to_guess = ""
    keyboard_buttons = []
    font_size = 60
    hangman_ascii = [
    '''
      
           
           
           
             
           
      
    _|___ ''',
    '''
      _
      |     
      |      
      |      
      |        
      |      
      |
    _|___ ''',
    '''
      _______
      |/      |
      |      
      |      
      |        
      |      
      |
    _|___ ''',
    '''
      _______
      |/      |
      |      (_)
      |      
      |        
      |      
      |
    _|___ ''',
    '''
      _______
      |/      |
      |      (_)
      |        |
      |        
      |      
      |
    _|___ ''',
    '''
      _______
      |/      |
      |      (_)
      |      \|
      |        
      |      
      |
    _|___ ''',
    '''
      _______
      |/      |
      |      (_)
      |      \|/
      |        
      |      
      |
    _|___ ''',
    '''
      _______
      |/      |
      |      (_)
      |      \|/
      |        |
      |      
      |
    _|___ ''',
    '''
      _______
      |/      |
      |      (_)
      |      \|/
      |        |
      |      / 
      |
    _|___ ''',
    '''
      _______
      |/      |
      |      (_)
      |      \|/
      |        |
      |      / \\
      |
    _|___ ''',
    ]
    max_wrong_guesses = len(hangman_ascii) - 1
    wrong_guesses = 0

    def __init__(self, **kwargs):
        super(HangmanGame, self).__init__(**kwargs)
        self.load_words_from_json("kelimeler.json")
        self.orientation = "vertical"
        self.bottom_margin = Widget(size_hint_y=None, height=(self.font_size*8))
        self.start_new_game()
        self.update_font_size(60)

    def update_font_size(self, value):
        self.font_size = value
        self.hangman_display.font_size = value
        self.word_display.font_size = value
        self.feedback_display.font_size = value
        self.bottom_margin.height = value * 7
        # Klavye düğmelerinin font boyutunu güncellemek istiyorsanız, buraya ekleyin
        for button in self.keyboard_buttons:
            button.font_size = value

    def load_words_from_json(self, json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.words = data["words"]

    def choose_random_word(self):
        return random.choice(self.words)

    def display_word(self):
        displayed_word = ""
        for letter in self.word_to_guess:
            if letter in self.guessed_letters:
                displayed_word += letter + " "
            else:
                displayed_word += "_ "
        return displayed_word.strip()

    def create_hangman_display(self):
        self.hangman_display = Label(text=self.hangman_ascii[self.wrong_guesses], font_size=self.font_size)
        self.add_widget(self.hangman_display)

    def create_word_display(self):
        self.word_display = Label(text=self.display_word(), font_size=self.font_size)
        self.add_widget(self.word_display)

    def create_feedback_display(self):
        self.feedback_display = Label(text="", font_size=self.font_size)
        self.add_widget(self.feedback_display)

    def create_keyboard_buttons(self):
        layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10, pos_hint={"center_x": 0.5})
        restart_button = Button(text="Yeni Kelime", size_hint=(1, None), height=50, font_size = 30)
        restart_button.bind(on_press=self.start_new_game)
        layout.add_widget(restart_button)
        layout.add_widget(Widget(size_hint_y=None, height=30))

        rows = ["qwertyuıopğü", "asdfghjklşi", "zxcvbnmöç"]
        for row in rows:
            row_layout = BoxLayout(orientation="horizontal",spacing=10, size_hint=(1, None))
            for char in row:
                button = Button(text=char, size_hint=(1, 1), size=(50, 50), font_size = self.font_size)
                button.bind(on_press=self.guess_letter)
                row_layout.add_widget(button)
                self.keyboard_buttons.append(button)
            layout.add_widget(row_layout)
        layout.add_widget(Widget(size_hint_y=None, height=30))

        self.add_widget(layout)


    def guess_letter(self, instance):
        letter = instance.text.lower()  # Büyük harfi küçük harfe dönüştür
        if letter in self.guessed_letters:
            return
        self.guessed_letters.append(letter)
        instance.disabled = True
        if letter not in self.word_to_guess:
            self.wrong_guesses += 1
            self.feedback_display.text = "Hay aksi! Yanlış harf."
        else:
            self.feedback_display.text = "Harika! Doğru harf."
        self.update_hangman_display()
        self.update_word_display()
        self.check_game_over()

    def update_word_display(self):
        self.word_display.text = self.display_word()

    def update_hangman_display(self):
        if self.wrong_guesses >= len(self.hangman_ascii):
            hangman_index = len(self.hangman_ascii) - 1
        else:
            hangman_index = self.wrong_guesses
        self.hangman_display.text = self.hangman_ascii[hangman_index]


    def check_game_over(self):
        if self.wrong_guesses >= self.max_wrong_guesses:
            self.feedback_display.text = "Oyun bitti! Kelime: {}".format(self.word_to_guess)
            for button in self.keyboard_buttons:
                button.disabled = True
        elif set(self.word_to_guess) <= set(self.guessed_letters):
            self.feedback_display.text = "Tebrikler! Kelime: {}".format(self.word_to_guess)
            for button in self.keyboard_buttons:
                button.disabled = True

    def start_new_game(self, instance=None):
        self.clear_widgets()  # Oyunu tamamen sıfırdan başlatmak için mevcut widgetları temizle
        self.load_words_from_json("kelimeler.json")
        self.word_to_guess = self.choose_random_word()
        self.guessed_letters = []
        self.wrong_guesses = 0
        back_button = Button(text="<<", size_hint=(None, None), size=(150, 50))
        back_button.bind(on_press=self.exit_session)
        self.add_widget(back_button)
        self.add_widget(Widget(size_hint=(None, None), size=(150, 10)))
        settings_button = Button(text="Ayarlar", size_hint=(None, None), size=(150, 50))
        settings_button.bind(on_press=self.open_settings)
        self.add_widget(settings_button)
        self.create_hangman_display()
        self.create_feedback_display()
        self.create_word_display()
        self.add_widget(self.bottom_margin)
        self.create_keyboard_buttons()

    def exit_session(self, instance):
        hangman_app.root_window.remove_widget(self)
        hangman_app.root_window.add_widget(MainMenu())

    def open_settings(self, instance):
        settings_popup = SettingsPopup(self)
        settings_popup.open()

class HangmanApp(App):
    def build(self):
        self.root = MainMenu()
        return self.root

if __name__ == "__main__":
    hangman_app = HangmanApp()
    hangman_app.run()
