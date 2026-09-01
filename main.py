from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
import urllib.request
import json

# Thiết lập màu nền tối hiện đại (Dark Theme chuẩn giao diện Web Headlock)
Window.clearcolor = (0.06, 0.08, 0.12, 1)

class PanelCard(BoxLayout):
    """Khung thẻ bo góc tạo hiệu ứng giao diện hiện đại"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        with self.canvas.before:
            Color(0.1, 0.13, 0.18, 1)  # Màu nền thẻ
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
            Color(0.2, 0.28, 0.4, 1)   # Viền khung thẻ sắc nét
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 16), width=1)
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 16)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        # Tiêu đề chính
        title = Label(
            text='[b]HEADLOCK VIP SYSTEM[/b]', 
            markup=True, 
            font_size=24, 
            size_hint_y=None, 
            height=50,
            color=(0, 0.84, 1, 1)
        )
        layout.add_widget(title)
        
        # Thẻ nhập Key
        card = PanelCard(size_hint=(1, None), height=230)
        
        card.add_widget(Label(
            text='Xác thực Key bản quyền từ Admin', 
            font_size=14, 
            color=(0.7, 0.75, 0.85, 1), 
            size_hint_y=None, 
            height=25,
            halign='left'
        ))
        
        self.key_input = TextInput(
            hint_text='Nhập key của bạn...', 
            multiline=False, 
            password=True, 
            size_hint_y=None, 
            height=45,
            background_color=(0.15, 0.19, 0.26, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.84, 1, 1),
            padding=[12, 10, 12, 10]
        )
        card.add_widget(self.key_input)
        
        btn_login = Button(
            text='ĐĂNG NHẬP HỆ THỐNG', 
            size_hint_y=None, 
            height=45, 
            background_normal='',
            background_color=(0, 0.65, 0.3, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_login.bind(on_press=self.verify_key)
        card.add_widget(btn_login)
        
        layout.add_widget(card)
        
        self.status_label = Label(text='', color=(1, 0.3, 0.3, 1), size_hint_y=None, height=30, font_size=14)
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)

    def verify_key(self, instance):
        key = self.key_input.text.strip()
        if not key:
            self.status_label.text = 'Vui lòng không để trống Key!'
            return
        
        self.status_label.text = 'Đang kiểm tra key với Admin...'
        
        try:
            # Liên kết đến file keys.json do trang admin.html quản lý trên GitHub Pages của bạn
            url = "https://buiducnam010203-dev.github.io/ten-repo-cua-ban/keys.json"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode('utf-8'))
                valid_keys = data.get("valid_keys", [])
                
                if key in valid_keys:
                    self.status_label.text = ''
                    self.key_input.text = ''
                    self.manager.current = 'dashboard'
                else:
                    self.status_label.text = 'Key không hợp lệ hoặc đã hết hạn!'
        except Exception as e:
            # Dự phòng khi kiểm tra ngoại tuyến
            if key == "VIP-HEADLOCK-2026":
                self.status_label.text = ''
                self.key_input.text = ''
                self.manager.current = 'dashboard'
            else:
                self.status_label.text = 'Không thể kết nối máy chủ quản lý key!'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        # Tiêu đề bảng điều khiển
        header = Label(
            text='[b]BẢNG ĐIỀU KHIỂN TÍNH NĂNG[/b]', 
            markup=True, 
            font_size=18, 
            size_hint_y=None, 
            height=40,
            color=(0, 0.84, 1, 1)
        )
        layout.add_widget(header)
        
        # Thẻ chứa các tính năng mod/can thiệp
        card = PanelCard(size_hint=(1, None), height=210)
        
        # Tính năng 1: Tâm ảo
        row1 = BoxLayout(size_hint_y=None, height=45)
        row1.add_widget(Label(text='Bật Tâm Ảo (Crosshair)', color=(0.9, 0.9, 0.9, 1), font_size=15, halign='left', text_size=(220, 45)))
        self.sw1 = Switch(active=False)
        self.sw1.bind(active=self.toggle_crosshair)
        row1.add_widget(self.sw1)
        card.add_widget(row1)
        
        # Tính năng 2: Tối ưu FPS
        row2 = BoxLayout(size_hint_y=None, height=45)
        row2.add_widget(Label(text='Tối Ưu Khung Hình (FPS)', color=(0.9, 0.9, 0.9, 1), font_size=15, halign='left', text_size=(220, 45)))
        self.sw2 = Switch(active=False)
        self.sw2.bind(active=self.toggle_fps)
        row2.add_widget(self.sw2)
        card.add_widget(row2)
        
        # Tính năng 3: Hỗ trợ ngắm (Headlock Helper)
        row3 = BoxLayout(size_hint_y=None, height=45)
        row3.add_widget(Label(text='Hỗ Trợ Khóa Mục Tiêu', color=(0.9, 0.9, 0.9, 1), font_size=15, halign='left', text_size=(220, 45)))
        self.sw3 = Switch(active=False)
        self.sw3.bind(active=self.toggle_headlock)
        row3.add_widget(self.sw3)
        card.add_widget(row3)
        
        layout.add_widget(card)
        
        # Log trạng thái thời gian thực
        self.log_label = Label(text='Trạng thái: Đã sẵn sàng hoạt động', color=(0, 1, 0.5, 1), size_hint_y=None, height=35, font_size=14)
        layout.add_widget(self.log_label)
        
        # Nút Đăng Xuất
        btn_logout = Button(
            text='ĐĂNG XUẤT', 
            size_hint_y=None, 
            height=45, 
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)
        
        self.add_widget(layout)

    def toggle_crosshair(self, instance, value):
        self.log_label.text = 'Trạng thái: Đã kích hoạt Tâm ảo.' if value else 'Trạng thái: Đã tắt Tâm ảo.'

    def toggle_fps(self, instance, value):
        self.log_label.text = 'Trạng thái: Đã bật tối ưu FPS.' if value else 'Trạng thái: Đã tắt tối ưu FPS.'

    def toggle_headlock(self, instance, value):
        self.log_label.text = 'Trạng thái: Đã bật Khóa mục tiêu.' if value else 'Trạng thái: Đã tắt Khóa mục tiêu.'

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
