from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.clock import Clock
import requests
import uuid
import threading

class CircularButton(Button):
    def __init__(self, **kwargs):
        super(CircularButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.15, 0.22, 0.35, 1)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)

class RoundedCard(BoxLayout):
    def __init__(self, **kwargs):
        super(RoundedCard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        with self.canvas.before:
            Color(0.074, 0.105, 0.180, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# شاشة البداية
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.02, 0.03, 0.05, 1)
            self.bg_rect = RoundedRectangle(size=(8000, 8000), pos=(-3000, -3000))
            
        layout.add_widget(Label(text="M-MA", font_size=70, bold=True, color=(0.01, 0.1, 0.18, 1), pos_hint={'center_x': 0.51, 'center_y': 0.53}))
        layout.add_widget(Label(text="M-MA", font_size=70, bold=True, color=(0.1, 0.2, 0.45, 1), pos_hint={'center_x': 0.505, 'center_y': 0.525}))
        layout.add_widget(Label(text="M-MA", font_size=70, bold=True, color=(0.15, 0.3, 0.85, 1), pos_hint={'center_x': 0.502, 'center_y': 0.52}))
        layout.add_widget(Label(text="M-MA", font_size=70, bold=True, color=(0.3, 0.85, 1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.515}))
        
        layout.add_widget(Label(text="Loading..", font_size=15, color=(0.6, 0.7, 0.8, 1), pos_hint={'center_x': 0.5, 'center_y': 0.38}))
        
        self.add_widget(layout)
        Clock.schedule_once(self.go_to_main, 2.5)

    def go_to_main(self, dt):
        self.manager.current = 'main_screen'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        self.session = requests.Session()
        self.headers = self.get_base_headers()
        self.phone = ""
        self.step = 1
        self.delete_event = None

        root = FloatLayout()
        with root.canvas.before:
            Color(0.043, 0.058, 0.098, 1)
            self.bg_rect = RoundedRectangle(size=(8000, 8000), pos=(-3000, -3000))

        # --- مساحة الشعار العلوي M-MA ---
        header_layout = FloatLayout(size_hint=(1, None), height=70, pos_hint={'top': 0.98})
        header_layout.add_widget(Label(text="M-MA", font_size=34, bold=True, color=(0.01, 0.1, 0.18, 1), pos_hint={'center_x': 0.505, 'center_y': 0.53}))
        header_layout.add_widget(Label(text="M-MA", font_size=34, bold=True, color=(0.15, 0.3, 0.85, 1), pos_hint={'center_x': 0.502, 'center_y': 0.515}))
        header_layout.add_widget(Label(text="M-MA", font_size=34, bold=True, color=(0.3, 0.85, 1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        root.add_widget(header_layout)

        # زر المطورين الدائري
        self.mma_btn = CircularButton(
            text="M-MA",
            size_hint=(None, None),
            size=(45, 45),
            pos_hint={'right': 0.98, 'top': 0.97},
            color=(1, 1, 1, 1),
            font_size=11
        )
        self.mma_btn.bind(on_press=self.show_mma_popup)
        root.add_widget(self.mma_btn)

        # المربع الرئيسي للادخال
        card = RoundedCard(size_hint=(0.96, 0.53), pos_hint={'center_x': 0.5, 'top': 0.88})

        self.title_label = Label(
            text="Twist-->1000",
            font_size=22,
            color=(0.219, 0.741, 0.972, 1),
            size_hint=(1, None),
            height=35
        )
        card.add_widget(self.title_label)

        self.instruction_label = Label(
            text="Enter phone number (011):",
            font_size=16,
            color=(0.803, 0.835, 0.878, 1),
            size_hint=(1, None),
            height=30
        )
        card.add_widget(self.instruction_label)

        self.input_field = TextInput(
            text='',
            multiline=False,
            readonly=True,
            font_size=24,
            halign='center',
            background_color=(0.058, 0.090, 0.164, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.219, 0.741, 0.972, 1),
            size_hint=(1, None),
            height=55
        )
        card.add_widget(self.input_field)

        self.action_btn = Button(
            text="Send Verification Code",
            font_size=18,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.02, 0.59, 0.41, 1),
            size_hint=(1, None),
            height=55
        )
        self.action_btn.bind(on_press=self.on_button_click)
        card.add_widget(self.action_btn)

        # تصميم التيرمنال مع محاذاة من اليسار تماماً
        terminal_container = BoxLayout(
            size_hint=(1, 1),
            padding=8
        )
        
        with terminal_container.canvas.before:
            Color(0.035, 0.050, 0.086, 1)
            self.term_bg = RoundedRectangle(size=terminal_container.size, pos=terminal_container.pos, radius=[10])
        terminal_container.bind(size=lambda i, v: setattr(self.term_bg, 'size', v), pos=lambda i, v: setattr(self.term_bg, 'pos', v))

        self.scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        
        self.status_label = Label(
            text="[color=55FF55][*] System ready, waiting for phone number...[/color]\n",
            markup=True,
            font_size=13,
            size_hint_y=None,
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(1, 1, 1, 1)
        )
        # ربط عرض التيرمنال لتوزيع النص من اليسار لليمين بشكل تلقائي
        self.scroll_view.bind(width=lambda i, w: setattr(self.status_label, 'text_size', (w - 20, None)))
        self.status_label.bind(texture_size=lambda i, s: setattr(i, 'height', s[1]))
        
        self.scroll_view.add_widget(self.status_label)
        terminal_container.add_widget(self.scroll_view)
        card.add_widget(terminal_container)

        root.add_widget(card)

        # لوحة مفاتيح الأرقام
        num_card = BoxLayout(
            orientation='vertical',
            size_hint=(0.96, 0.33),
            pos_hint={'center_x': 0.5, 'y': 0.01},
            padding=6,
            spacing=6
        )
        
        with num_card.canvas.before:
            Color(0.05, 0.07, 0.12, 1)
            self.numpad_bg = RoundedRectangle(size=num_card.size, pos=num_card.pos, radius=[20])
        num_card.bind(size=lambda i, v: setattr(self.numpad_bg, 'size', v), pos=lambda i, v: setattr(self.numpad_bg, 'pos', v))

        num_grid = GridLayout(cols=3, spacing=6, size_hint=(1, 1))
        buttons_text = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'X', '0', 'Enter']
        
        for b_text in buttons_text:
            b_color = (0.11, 0.16, 0.25, 1)
            if b_text == 'Enter':
                b_color = (0.02, 0.59, 0.41, 1)
            elif b_text == 'X':
                b_color = (0.8, 0.2, 0.2, 1)
                
            btn = Button(
                text=b_text,
                font_size=26,
                background_normal='',
                background_color=b_color,
                color=(1, 1, 1, 1)
            )
            
            if b_text == 'X':
                btn.bind(on_press=self.start_deleting)
                btn.bind(on_release=self.stop_deleting)
            else:
                btn.bind(on_press=self.on_numpad_press)
                
            num_grid.add_widget(btn)

        num_card.add_widget(num_grid)
        root.add_widget(num_card)
        self.add_widget(root)

    def start_deleting(self, instance):
        current_val = self.input_field.text
        if current_val:
            self.input_field.text = current_val[:-1]
        self.delete_event = Clock.schedule_interval(self.perform_continuous_delete, 0.12)

    def perform_continuous_delete(self, dt):
        current_val = self.input_field.text
        if current_val:
            self.input_field.text = current_val[:-1]
        else:
            self.stop_deleting(None)

    def stop_deleting(self, instance):
        if self.delete_event:
            self.delete_event.cancel()
            self.delete_event = None

    def on_numpad_press(self, instance):
        txt = instance.text
        current_val = self.input_field.text
        if txt == 'Enter':
            self.on_button_click(None)
        else:
            limit = 11 if self.step == 1 else 6
            if len(current_val) < limit:
                self.input_field.text = current_val + txt

    def show_mma_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        content.add_widget(Label(
            text="[Developers]\n\n• Mohamed Abdelrahman>MA\n• Mostafa Marzouk>M",
            font_size=18,
            halign='center',
            color=(1, 1, 1, 1)
        ))
        close_btn = Button(
            text="Close",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(close_btn)
        popup = Popup(title="M-MA Developers", content=content, size_hint=(0.8, 0.4), auto_dismiss=True)
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def log(self, message):
        if "❌" in message or "Error" in message or "Failed" in message or "Invalid" in message:
            colored_msg = f"[color=FF5555]{message}[/color]\n"
        else:
            colored_msg = f"[color=55FF55]{message}[/color]\n"
            
        def update_log(dt):
            self.status_label.text += colored_msg
            self.scroll_view.scroll_y = 0
            
        Clock.schedule_once(update_log)

    def generate_session_id(self):
        return str(uuid.uuid4())

    def get_base_headers(self):
        return {
            "user-agent": "Twist-Mobile/9999 (Android; 12; SM-A217F; music; ar-AE)",
            "app_version": "9999",
            "appversion": "9999",
            "channel": "mobileapp",
            "content-type": "application/json",
            "platform": "android",
            "accept": "application/json",
            "accept-language": "ar",
            "host": "api.twistmena.com",
            "device_id": "SP1A.210812.016",
            "tgdeviceid": "26284330",
            "sessionid": self.generate_session_id(),
            "accept-encoding": "gzip",
            "connection": "keep-alive"
        }

    def on_button_click(self, instance):
        text = self.input_field.text.strip()
        
        if self.step == 1:
            if len(text) != 11 or not text.startswith("01"):
                self.log("[❌] Error: Phone number must be 11 digits starting with 01!")
                return
            
            self.phone = "2" + text
            self.log(f"[*] Processing number: {text}")
            self.log("[⏳] Sending confirmation code to server...")
            threading.Thread(target=self.send_otp_thread, daemon=True).start()

        elif self.step == 2:
            if len(text) != 6:
                self.log("[❌] Error: Verification code must be 6 digits!")
                return
            code = text
            self.log("[⏳] Verifying code and executing tasks...")
            threading.Thread(target=self.verify_and_run_thread, args=(code,), daemon=True).start()

    def send_otp_thread(self):
        try:
            res = self.session.post(
                "https://api.twistmena.com/music/Dlogin/sendCode",
                headers=self.headers,
                json={"dial": self.phone},
                timeout=10
            )
            if res.status_code == 200:
                Clock.schedule_once(lambda dt: self.transition_to_step2())
            else:
                self.log(f"[❌] Failed to send code (Status: {res.status_code})")
        except Exception as e:
            self.log("[❌] Connection error or network failure")

    def transition_to_step2(self):
        self.log("[✔️] Verification code sent successfully!")
        self.instruction_label.text = "Enter the 6-digit verification code:"
        self.input_field.text = ""
        self.action_btn.text = "Verify & Run Tasks"
        self.action_btn.background_color = (0.145, 0.388, 0.921, 1)
        self.step = 2

    def verify_and_run_thread(self, code):
        try:
            verify_res = self.session.post(
                "https://api.twistmena.com/music/Dlogin/verify",
                headers=self.headers,
                json={"dial": self.phone, "verifyCode": code, "socialServiceName": "", "socialServiceToken": ""},
                timeout=10
            )
            
            if verify_res.status_code != 200:
                self.log("[❌] Invalid or expired code!")
                return

            data = verify_res.json()
            token = data.get('token') or data.get('authorization')
            if not token and verify_res.headers.get('authorization'):
                token = verify_res.headers.get('authorization').replace('Bearer ', '')

            if token:
                clean_token = str(token).replace('Bearer ', '')
                self.headers['authorization'] = 'Bearer ' + clean_token
                self.log("[🎉] Logged in successfully and token saved!")
            else:
                self.log("[⚠️] Warning: Connected, but token was not received.")
        except Exception as e:
            self.log("[❌] Error during execution")

class TwistUltimateApp(App):
    def build(self):
        self.title = "Twistmena Panel"
        
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MainScreen(name='main_screen'))
        
        return sm

if __name__ == '__main__':
    TwistUltimateApp().run()
