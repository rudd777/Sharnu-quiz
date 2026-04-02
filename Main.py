from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.animation import Animation
from kivy.clock import Clock
from random import sample, shuffle, choice

flags_ordered = [
("Congo","cg"),
("Bhutan","bt"),
("Afghanistan","af"),
("France","fr"),
("Japan","jp")
]

all_countries = [
"Burkina Faso","Eswatini","Kyrgyzstan","Tajikistan","Turkmenistan",
"Uzbekistan","Djibouti","Lesotho","Comoros","Cape Verde",
"Equatorial Guinea","Guinea-Bissau","Sao Tome and Principe",
"Timor-Leste","Vanuatu","Solomon Islands","Micronesia",
"Palau","Kiribati","Nauru","Tuvalu",
"Montenegro","Moldova","Andorra","Liechtenstein",
"San Marino","Monaco","Malta","Cyprus",
"Suriname","Guyana","Belize",
"Benin","Togo","Gabon","Niger",
"Chad","Central African Republic","Eritrea",
"Bhutan","Afghanistan","Congo","France","Japan"
]

button_colors = [
(0.9,0.3,0.3,1),
(0.3,0.9,0.3,1),
(0.3,0.3,0.9,1),
(0.9,0.9,0.3,1),
(0.9,0.3,0.9,1)
]

class FlagGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.setup_game()

    def setup_game(self):
        self.score = 0
        self.rounds_played = 0
        self.max_rounds = len(flags_ordered)
        self.time_left = 10
        self.remaining_flags = flags_ordered.copy()

        self.clear_widgets()
        self.canvas.before.clear()

        with self.canvas.before:
            Color(0.95,0.95,1,1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        self.score_label = Label(text=f"Score: {self.score}", font_size=30, size_hint=(1,0.1))
        self.timer_label = Label(text=f"Waktu: {self.time_left}", font_size=25, size_hint=(1,0.1))
        self.add_widget(self.score_label)
        self.add_widget(self.timer_label)

        self.flag_image = Image(size_hint=(1,0.5))
        self.flag_image.allow_stretch = True
        self.flag_image.keep_ratio = True
        self.add_widget(self.flag_image)

        self.btn_layout = BoxLayout(size_hint=(1,0.3), spacing=10, padding=10)
        self.add_widget(self.btn_layout)

        self.generate_round()
        Clock.schedule_interval(self.update_timer, 1)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def generate_round(self):
        if self.rounds_played >= self.max_rounds:
            self.show_congratulations()
            return

        self.btn_layout.clear_widgets()
        self.country, code = self.remaining_flags.pop(0)

        self.flag_image.source = f"https://flagcdn.com/w320/{code}.png"

        wrong = [c for c in all_countries if c != self.country]
        options = [self.country] + sample(wrong, 3)
        shuffle(options)

        for c in options:
            btn = Button(text=c, background_color=choice(button_colors))
            btn.bind(on_press=self.check_answer)
            self.btn_layout.add_widget(btn)

            btn.y += 100
            anim = Animation(y=btn.y - 100, duration=0.5, t='out_bounce')
            anim.start(btn)

        self.time_left = 10

    def check_answer(self, instance):
        if instance.text == self.country:
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
            self.show_effect(instance, correct=True)
        else:
            self.show_effect(instance, correct=False)
            self.shake_button(instance)

        self.rounds_played += 1
        self.generate_round()

    def update_timer(self, dt):
        if self.rounds_played >= self.max_rounds:
            return False

        self.time_left -= 1
        self.timer_label.text = f"Waktu: {self.time_left}"

        if self.time_left <= 0:
            self.rounds_played += 1
            self.generate_round()

    def show_effect(self, widget, correct):
        color = [0,1,0,0.8] if correct else [1,0,0,0.8]
        effect = Widget()
        with effect.canvas:
            Color(*color)
            Ellipse(pos=(widget.x-30, widget.y-30), size=(widget.width+60, widget.height+60))

        self.add_widget(effect)
        anim = Animation(opacity=0, duration=0.7)
        anim.bind(on_complete=lambda *x: self.remove_widget(effect))
        anim.start(effect)

    def shake_button(self, button):
        anim = Animation(x=button.x-5, duration=0.05) + Animation(x=button.x+5, duration=0.05)
        anim += Animation(x=button.x, duration=0.05)
        anim.start(button)

    def show_congratulations(self):
        self.btn_layout.clear_widgets()
        self.flag_image.source = ""
        self.timer_label.text = ""

        if self.score == self.max_rounds:
            msg = "Keren juga lu tod!"
        else:
            msg = "Yahahah Bego!"

        final_label = Label(text=msg, font_size=40, color=(0,0,0,1), bold=True)
        self.add_widget(final_label)

        btn_reset = Button(text="Main Lagi")
        btn_reset.bind(on_press=lambda x: self.setup_game())
        self.add_widget(btn_reset)

class FlagGameApp(App):
    def build(self):
        return FlagGame()

if __name__ == "__main__":
    FlagGameApp().run()
