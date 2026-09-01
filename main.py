from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        self.title_label = Label(text='HEADLOCK VIP MANAGER', font_size=22, size_hint_y=None, height=50)
        self.key_input = TextInput(hint_text='Nhập Key bản quyền...', multiline=False, password=True, size_hint_y=None, height=50)
        
        btn_login = Button(text='Đăng Nhập', size_hint_y=None, height=50, background_color=(0, 0.7, 0.3, 1))
        btn_login.bind(on_press=self.verify_key)
        
        self.status_label = Label(text='', color=(1, 0, 0, 1), size_hint_y=None, height=30)
        
        layout.add_widget(self.title_label)
        layout.add_widget(self.key_input)
        layout.add_widget(btn_login)
        layout.add_widget(self.status_label)
        self.add_widget(layout)

    def verify_key(self, instance):
        key = self.key_input.text.strip()
        if not key:
            self.status_label.text = 'Vui lòng nhập key!'
            return
        
        # Khớp key với định dạng hoặc key mẫu của bạn (có thể đồng bộ với hệ thống admin.html)
        if key == "VIP-HEADLOCK-2026" or key.startswith("KEY-"):
            self.status_label.text = ''
            self.key_input.text = ''
            self.manager.current = 'dashboard'
        else:
            self.status_label.text = 'Key không hợp lệ hoặc đã hết hạn!'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        layout.add_widget(Label(text='BẢNG ĐIỀU KHIỂN VIP', font_size=22, size_hint_y=None, height=40))
        
        # Tính năng 1: Bật tâm ảo
        row1 = BoxLayout(size_hint_y=None, height=50)
        row1.add_widget(Label(text='Bật Tâm Ảo (Crosshair):'))
        self.sw1 = Switch(active=False)
        self.sw1.bind(active=self.toggle_crosshair)
        row1.add_widget(self.sw1)
        layout.add_widget(row1)
        
        # Tính năng 2: Tối ưu khung hình
        row2 = BoxLayout(size_hint_y=None, height=50)
        row2.add_widget(Label(text='Tối Ưu Khung Hình:'))
        self.sw2 = Switch(active=False)
        self.sw2.bind(active=self.toggle_fps)
        row2.add_widget(self.sw2)
        layout.add_widget(row2)
        
        self.log_label = Label(text='Trạng thái: Sẵn sàng hoạt động', color=(0, 1, 0, 1))
        layout.add_widget(self.log_label)
        
        btn_logout = Button(text='Đăng Xuất', size_hint_y=None, height=45, background_color=(0.8, 0.1, 0.1, 1))
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)
        
        self.add_widget(layout)

    def toggle_crosshair(self, instance, value):
        if value:
            self.log_label.text = 'Đã bật: Tâm ảo hiển thị.'
        else:
            self.log_label.text = 'Đã tắt: Tâm ảo.'

    def toggle_fps(self, instance, value):
        if value:
            self.log_label.text = 'Đã bật: Tối ưu hiệu năng game.'
        else:
            self.log_label.text = 'Đã tắt: Tối ưu hiệu năng game.'

    def logout(self, instance):
        self.manager.current = 'login'

class HeadlockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    HeadlockApp().run()
