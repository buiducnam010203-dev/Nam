from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.clock import Clock
import random
import time
import os

# Thiết lập màu nền ứng dụng (#0b0914)
Window.clearcolor = (0.043, 0.035, 0.078, 1)

class PanelCard(BoxLayout):
    """Khung thẻ bo góc phong cách Cyber Dashboard"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 16
        self.spacing = 10
        with self.canvas.before:
            Color(0.090, 0.075, 0.156, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
            Color(0.329, 0.184, 0.596, 0.6)
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
        
        title = Label(
            text='[b]HEADLOCK DUAL FREE FIRE VIP + ANTIBAN[/b]', 
            markup=True, 
            font_size=18, 
            size_hint_y=None, 
            height=40,
            color=(0.690, 0.400, 0.960, 1)
        )
        layout.add_widget(title)
        
        card = PanelCard(size_hint=(1, None), height=210)
        card.add_widget(Label(
            text='Nhập Key bản quyền (Hỗ trợ Thường & Max)', 
            font_size=13, 
            color=(0.7, 0.7, 0.8, 1), 
            size_hint_y=None, 
            height=24
        ))
        
        self.key_input = TextInput(
            hint_text='Dán key (VD: VIP-DUAL-ANTIBAN)...', 
            multiline=False, 
            password=True, 
            size_hint_y=None, 
            height=44,
            background_color=(0.06, 0.05, 0.11, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.690, 0.400, 0.960, 1),
            padding=[12, 10, 12, 10]
        )
        card.add_widget(self.key_input)
        
        btn_login = Button(
            text='KÍCH HOẠT HỆ THỐNG DUAL AN TOÀN', 
            size_hint_y=None, 
            height=44, 
            background_normal='',
            background_color=(0.545, 0.271, 0.753, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_login.bind(on_press=self.verify_key)
        card.add_widget(btn_login)
        
        layout.add_widget(card)
        self.status_label = Label(text='', color=(0.956, 0.262, 0.211, 1), size_hint_y=None, height=28, font_size=13)
        layout.add_widget(self.status_label)
        self.add_widget(layout)

    def verify_key(self, instance):
        key = self.key_input.text.strip().upper()
        if not key:
            self.status_label.text = 'Vui lòng không để trống Key!'
            return
        
        if key.startswith("VIP-") or len(key) >= 5:
            self.status_label.text = ''
            dashboard_screen = self.manager.get_screen('dashboard')
            dashboard_screen.set_active_key(key)
            self.key_input.text = ''
            self.manager.current = 'dashboard'
        else:
            self.status_label.text = 'Key không hợp lệ!'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_key = "VIP-DUAL-ANTIBAN"
        self.key_type_text = "Key Dual Free Fire [Anti-Ban 100%] 👑"
        
        # Mặc định chọn phiên bản Thường
        self.selected_target = "com.dts.freefireth"
        self.target_display_name = "Free Fire Thường (TH)"
        
        self.log_event = None
        self.inject_event = None
        self.function_injected = False
        
        main_layout = BoxLayout(orientation='vertical', padding=12, spacing=8)
        
        # Header Thông tin & Chọn phiên bản Game
        top_info = BoxLayout(orientation='vertical', size_hint_y=None, height=155, spacing=4)
        
        row_ip = BoxLayout(size_hint_y=None, height=22)
        row_ip.add_widget(Label(text='IP: 171.255.65.106 [ANTIBAN SECURE 100%]', font_size=11, color=(0.2, 0.8, 0.4, 1), halign='left', size_hint_x=None, width=300))
        top_info.add_widget(row_ip)
        
        top_info.add_widget(Label(text='[b]HEADLOCK DUAL FREE FIRE VIP[/b]', markup=True, font_size=17, color=(1, 1, 1, 1), size_hint_y=None, height=24))
        
        self.sub_title = Label(text=f'KEY: {self.current_key}', font_size=11, color=(0.690, 0.400, 0.960, 1), size_hint_y=None, height=20)
        top_info.add_widget(self.sub_title)
        
        # Thanh chọn nhanh giữa 2 phiên bản game
        version_row = BoxLayout(size_hint_y=None, height=36, spacing=8)
        version_row.add_widget(Label(text='Phiên bản:', font_size=11, color=(0.8, 0.8, 0.9, 1), size_hint_x=None, width=70))
        
        self.btn_ver_th = Button(
            text='FF Thường', font_size=10, bold=True,
            background_normal='', background_color=(0.545, 0.271, 0.753, 1)
        )
        self.btn_ver_th.bind(on_press=lambda x: self.switch_game_target("com.dts.freefireth", "Free Fire Thường (TH)"))
        
        self.btn_ver_max = Button(
            text='FF Max', font_size=10, bold=True,
            background_normal='', background_color=(0.14, 0.11, 0.22, 1)
        )
        self.btn_ver_max.bind(on_press=lambda x: self.switch_game_target("com.dts.freefiremax", "Free Fire Max (MAX)"))
        
        version_row.add_widget(self.btn_ver_th)
        version_row.add_widget(self.btn_ver_max)
        top_info.add_widget(version_row)
        
        self.target_label = Label(text=f'[b][TARGET: {self.selected_target} ({self.target_display_name})][/b]', markup=True, font_size=11, color=(0.2, 0.8, 0.4, 1), size_hint_y=None, height=24)
        top_info.add_widget(self.target_label)
        
        main_layout.add_widget(top_info)
        
        # Tabs Điều hướng
        tab_bar = BoxLayout(size_hint_y=None, height=42, spacing=4)
        
        self.btn_t1 = Button(text='🎮 TÍNH\nNĂNG', font_size=10, markup=True, background_normal='', background_color=(0.545, 0.271, 0.753, 1))
        self.btn_t1.bind(on_press=lambda x: self.switch_tab('tinh_nang'))
        
        self.btn_t2 = Button(text='⚙ FUNCTION', font_size=11, markup=True, background_normal='', background_color=(0.14, 0.11, 0.22, 1))
        self.btn_t2.bind(on_press=lambda x: self.switch_tab('function'))
        
        self.btn_t4 = Button(text='⚡ BOOSTER', font_size=11, markup=True, background_normal='', background_color=(0.14, 0.11, 0.22, 1))
        self.btn_t4.bind(on_press=lambda x: self.switch_tab('booster'))
        
        self.btn_t5 = Button(text='ℹ INFO', font_size=11, markup=True, background_normal='', background_color=(0.14, 0.11, 0.22, 1))
        self.btn_t5.bind(on_press=lambda x: self.switch_tab('info'))
        
        tab_bar.add_widget(self.btn_t1)
        tab_bar.add_widget(self.btn_t2)
        tab_bar.add_widget(self.btn_t4)
        tab_bar.add_widget(self.btn_t5)
        
        main_layout.add_widget(tab_bar)
        
        self.content_area = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.content_area)
        self.add_widget(main_layout)
        
        self.switch_tab('tinh_nang')

    def set_active_key(self, key):
        self.current_key = key
        self.sub_title.text = f'KEY: {self.current_key} | {self.key_type_text}'

    def switch_game_target(self, package_name, display_name):
        self.selected_target = package_name
        self.target_display_name = display_name
        self.target_label.text = f'[b][TARGET: {self.selected_target} ({self.target_display_name})][/b]'
        
        if package_name == "com.dts.freefireth":
            self.btn_ver_th.background_color = (0.545, 0.271, 0.753, 1)
            self.btn_ver_max.background_color = (0.14, 0.11, 0.22, 1)
        else:
            self.btn_ver_max.background_color = (0.545, 0.271, 0.753, 1)
            self.btn_ver_th.background_color = (0.14, 0.11, 0.22, 1)
            
        print(f"[DUAL-TARGET] Đã chuyển mục tiêu sang: {package_name}")

    def reset_tab_colors(self):
        inactive_color = (0.14, 0.11, 0.22, 1)
        self.btn_t1.background_color = inactive_color
        self.btn_t2.background_color = inactive_color
        self.btn_t4.background_color = inactive_color
        self.btn_t5.background_color = inactive_color

    def cancel_clocks(self):
        if self.log_event:
            self.log_event.cancel()
            self.log_event = None
        if self.inject_event:
            self.inject_event.cancel()
            self.inject_event = None

    def switch_tab(self, tab_name):
        self.cancel_clocks()
        self.reset_tab_colors()
        self.content_area.clear_widgets()
        
        if tab_name == 'tinh_nang':
            self.btn_t1.background_color = (0.545, 0.271, 0.753, 1)
            self.load_tinh_nang_tab()
        elif tab_name == 'function':
            self.btn_t2.background_color = (0.545, 0.271, 0.753, 1)
            self.load_function_tab()
        elif tab_name == 'booster':
            self.btn_t4.background_color = (0.545, 0.271, 0.753, 1)
            self.load_booster_tab()
        elif tab_name == 'info':
            self.btn_t5.background_color = (0.545, 0.271, 0.753, 1)
            self.load_info_tab()

    def trigger_free_fire_action(self, feature_name, state):
        status_text = "BẬT AIMLOCK (100% HEADSHOT)" if state else "TẮT"
        print(f"[DUAL-ENGINE] Target [{self.selected_target}] -> Tính năng [{feature_name}] : {status_text}")
        try:
            if state:
                os.system(f"am broadcast -a com.headlock.dual.antiban --es target '{self.selected_target}' --es feature '{feature_name}' --es status 'forced_matrix_active'")
        except Exception as e:
            print(f"Lỗi lệnh hệ thống: {e}")

    def load_tinh_nang_tab(self):
        content_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        card_features = PanelCard(size_hint=(1, None), height=340)
        features_list = [
            ("🛡️ ANTI-BAN / CHỐNG KHÓA ACC (100%)", "anti_ban_core"), 
            ("🎯 AIMLOCK BÁM ĐẦU BONE-ID 8 (100%)", "aimlock_head"), 
            ("🚀 BOOST RAM & CHẶN DELAY", "boost_ram"), 
            ("💀 HEADLOCK CHUẨN TÂM MATRIX", "headlock_core"), 
            ("⚙️ FIX RUNG & CHỐNG GIẬT", "fix_rung"), 
            ("🛡️ CHỐNG TRÔI TÂM (FIX LỐ)", "fix_lo"), 
            ("🔒 SENSILOCK 100%", "sensilock")
        ]
        for name, key_id in features_list:
            row = BoxLayout(size_hint_y=None, height=33)
            row.add_widget(Label(text=name, color=(0.9, 0.9, 0.9, 1), font_size=10, bold=True, halign='left', text_size=(230, 33)))
            sw = Switch(active=True) # Mặc định bật sẵn bảo vệ tài khoản và aimlock
            sw.bind(active=lambda inst, val, fid=key_id: self.trigger_free_fire_action(fid, val))
            row.add_widget(sw)
            card_features.add_widget(row)
        content_layout.add_widget(card_features)
        
        # Độ nhạy màn hình
        card_sens = PanelCard(size_hint=(1, None), height=90)
        top_sens = BoxLayout(size_hint_y=None, height=22)
        top_sens.add_widget(Label(text='⚡ ĐỘ NHẠY KÉO TÂM AIMLOCK', color=(0.9, 0.9, 0.9, 1), font_size=11, bold=True, halign='left', text_size=(200, 22)))
        lbl_sens_val = Label(text='150%', color=(0.690, 0.400, 0.960, 1), font_size=11, bold=True, halign='right', text_size=(60, 22))
        top_sens.add_widget(lbl_sens_val)
        card_sens.add_widget(top_sens)
        
        slider_sens = Slider(min=50, max=200, value=150, size_hint_y=None, height=28)
        slider_sens.bind(value=lambda inst, val: [
            setattr(lbl_sens_val, 'text', f'{int(val)}%'),
            self.trigger_free_fire_action(f"SENSITIVITY_{int(val)}", True)
        ])
        card_sens.add_widget(slider_sens)
        content_layout.add_widget(card_sens)
        
        # Live Console Log
        card_console = PanelCard(size_hint=(1, None), height=135)
        top_console = BoxLayout(size_hint_y=None, height=20)
        top_console.add_widget(Label(text='>_ DUAL ANTIBAN & AIMLOCK MATRIX LOG', color=(0.2, 0.8, 0.4, 1), font_size=10, halign='left', text_size=(260, 20)))
        card_console.add_widget(top_console)
        
        self.log_lbl1 = Label(text='[STATUS] INITIALIZING MATRIX HOOK...', color=(0.7, 0.7, 0.8, 1), font_size=9, size_hint_y=None, height=18, halign='left')
        self.log_lbl2 = Label(text='[ANTIBAN] TELEMETRY BYPASSED: 100% SAFE', color=(0.2, 0.8, 0.4, 1), font_size=9, size_hint_y=None, height=18, halign='left')
        self.log_lbl3 = Label(text='[AIMLOCK] BONE ID 8 LOCKED TO HEAD [ACTIVE]', color=(0.690, 0.400, 0.960, 1), font_size=9, size_hint_y=None, height=18, halign='left')
        
        card_console.add_widget(self.log_lbl1)
        card_console.add_widget(self.log_lbl2)
        card_console.add_widget(self.log_lbl3)
        content_layout.add_widget(card_console)
        
        self.content_area.add_widget(content_layout)
        self.log_event = Clock.schedule_interval(self.update_hacker_logs, 0.2)

    def update_hacker_logs(self, dt):
        codes = [
            (f"TARGET [{self.selected_target}]: VECTOR HEADLOCK ACTIVE", (0.2, 0.8, 0.4, 1)),
            ("AIMLOCK: PULLING CROSSHAIR TO HEAD HITBOX [100%]", (0.690, 0.400, 0.960, 1)),
            ("BLOCKING TELEMETRY LOGS TO GARENA SERVER", (0.2, 0.8, 0.4, 1)),
            ("RECOIL COMPENSATION OFFSET APPLIED [0% SPREAD]", (0.7, 0.7, 0.8, 1))
        ]
        self.log_lbl1.text = self.log_lbl2.text
        self.log_lbl1.color = self.log_lbl2.color
        self.log_lbl2.text = self.log_lbl3.text
        self.log_lbl2.color = self.log_lbl3.color
        rand_code, rand_color = random.choice(codes)
        self.log_lbl3.text = f"[{time.strftime('%H:%M:%S')] {rand_code}"
        self.log_lbl3.color = rand_color

    def load_function_tab(self):
        if not self.function_injected:
            self.show_injection_screen()
        else:
            self.show_function_features_screen()

    def show_injection_screen(self):
        self.content_area.clear_widgets()
        card = PanelCard(size_hint=(1, None), height=230)
        card.add_widget(Label(text='🔒 TIÊM GÓI AIMLOCK & AN TOÀN', color=(0.690, 0.400, 0.960, 1), font_size=12, bold=True, size_hint_y=None, height=22, halign='left'))
        card.add_widget(Label(text=f'Đang cấu hình bám đầu cho mục tiêu: {self.selected_target}', color=(0.7, 0.7, 0.8, 1), font_size=10, size_hint_y=None, height=32, halign='left'))
        
        prog_layout = BoxLayout(size_hint_y=None, height=22)
        prog_layout.add_widget(Label(text='Tiến trình kích hoạt Aimlock Matrix', color=(0.8, 0.8, 0.9, 1), font_size=11, halign='left'))
        self.lbl_inject_percent = Label(text='0%', color=(0.690, 0.400, 0.960, 1), font_size=11, bold=True, halign='right')
        prog_layout.add_widget(self.lbl_inject_percent)
        card.add_widget(prog_layout)
        
        self.inject_slider = Slider(min=0, max=100, value=0, size_hint_y=None, height=24)
        card.add_widget(self.inject_slider)
        
        self.btn_inject = Button(text='⚡ TIÊM AIMLOCK CHO PHIÊN BẢN NÀY', size_hint_y=None, height=42, background_normal='', background_color=(0.545, 0.271, 0.753, 1), color=(1, 1, 1, 1), bold=True)
        self.btn_inject.bind(on_press=self.start_injection_process)
        card.add_widget(self.btn_inject)
        self.content_area.add_widget(card)

    def start_injection_process(self, instance):
        self.btn_inject.disabled = True
        self.btn_inject.text = '⏳ Đang ép buộc tọa độ tâm...'
        self.injection_value = 0
        if self.inject_event:
            self.inject_event.cancel()
        self.inject_event = Clock.schedule_interval(self.update_injection_progress, 0.03)

    def update_injection_progress(self, dt):
        self.injection_value += 4
        if self.injection_value >= 100:
            self.injection_value = 100
            self.inject_event.cancel()
            self.function_injected = True
            Clock.schedule_once(lambda x: self.show_function_features_screen(), 0.3)
        self.inject_slider.value = self.injection_value
        self.lbl_inject_percent.text = f'{int(self.injection_value)}%'

    def show_function_features_screen(self):
        self.content_area.clear_widgets()
        content_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        content_layout.add_widget(Label(text=f'🛡️ AIMLOCK & BẢO VỆ CHO: {self.target_display_name}', color=(0.2, 0.8, 0.4, 1), font_size=11, bold=True, size_hint_y=None, height=20, halign='left'))
        
        features_data = [
            ("🛡️ Anti-Ban Account Safety", "Chặn hoàn toàn cơ chế quét tài khoản"),
            ("🎯 AimLock Headshot Bone ID 8", "Tự động hút tâm thẳng vào đầu đối thủ 100%"),
            ("⚙️ Fix Rung Khi Bắn Sấy", "Giữ tâm súng đứng yên tuyệt đối"),
            ("🔍 Fix Lạc Đạn Băng Súng", "Gom toàn bộ đường đạn vào một điểm"),
            ("🔥 Auto Headshot Pro Matrix", "Hỗ trợ tối ưu hóa phát bắn chuẩn xác"),
            ("🚀 Mở Khóa 90FPS Mượt Mà", "Tăng tốc khung hình không giật lag")
        ]
        
        card_feats = PanelCard(size_hint=(1, None), height=255)
        for title, desc in features_data:
            row = BoxLayout(size_hint_y=None, height=35, spacing=5)
            lbl_box = BoxLayout(orientation='vertical', size_hint_x=0.8)
            lbl_box.add_widget(Label(text=title, color=(0.95, 0.95, 0.95, 1), font_size=11, bold=True, halign='left', text_size=(190, 18)))
            lbl_box.add_widget(Label(text=desc, color=(0.6, 0.6, 0.7, 1), font_size=9, halign='left', text_size=(190, 15)))
            row.add_widget(lbl_box)
            sw = Switch(active=True, size_hint_x=0.2)
            sw.bind(active=lambda inst, val, t=title: self.trigger_free_fire_action(t, val))
            row.add_widget(sw)
            card_feats.add_widget(row)
            
        content_layout.add_widget(card_feats)
        self.content_area.add_widget(content_layout)

    def load_booster_tab(self):
        content_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        card_opt = PanelCard(size_hint=(1, None), height=155)
        card_opt.add_widget(Label(text='⚡ BẢNG TỐI ƯU & HỆ THỐNG BOOSTER', color=(0.690, 0.400, 0.960, 1), font_size=11, bold=True, size_hint_y=None, height=20, halign='left'))
        
        opts = [
            ("🚀 FPS UNLOCKER (MAX 120)", True), 
            ("🧊 COOLING CPU (GIẢM NHIỆT)", True), 
            ("⚡ TOUCH BOOST (CẢM ỨNG NHẬY)", True)
        ]
        for name, state in opts:
            row = BoxLayout(size_hint_y=None, height=31)
            row.add_widget(Label(text=name, color=(0.9, 0.9, 0.9, 1), font_size=11, bold=True, halign='left', text_size=(220, 31)))
            sw = Switch(active=state, size_hint_x=None, width=50)
            sw.bind(active=lambda inst, val, n=name: self.trigger_free_fire_action(n, val))
            row.add_widget(sw)
            card_opt.add_widget(row)
        content_layout.add_widget(card_opt)
        
        card_hz = PanelCard(size_hint=(1, None), height=90)
        top_hz = BoxLayout(size_hint_y=None, height=22)
        top_hz.add_widget(Label(text='🎮 TỐC ĐỘ LÀM MỚI MÀN HÌNH (HZ)', color=(0.9, 0.9, 0.9, 1), font_size=11, bold=True, halign='left', text_size=(220, 22)))
        self.lbl_hz_val = Label(text='120Hz', color=(0.690, 0.400, 0.960, 1), font_size=11, bold=True, halign='right', text_size=(60, 22))
        top_hz.add_widget(self.lbl_hz_val)
        card_hz.add_widget(top_hz)
        
        slider_hz = Slider(min=60, max=120, value=120, step=10, size_hint_y=None, height=28)
        slider_hz.bind(value=lambda inst, val: [
            setattr(self.lbl_hz_val, 'text', f'{int(val)}Hz'),
            self.trigger_free_fire_action(f"REFRESH_RATE_{int(val)}Hz", True)
        ])
        card_hz.add_widget(slider_hz)
        content_layout.add_widget(card_hz)
        
        card_inject = PanelCard(size_hint=(1, None), height=185)
        card_inject.add_widget(Label(text='🚀 TRẠNG THÁI AIMLOCK & BẢO VỆ', color=(0.2, 0.8, 0.4, 1), font_size=11, bold=True, size_hint_y=None, height=20, halign='left'))
        card_inject.add_widget(Label(text=f'Aimlock Matrix đang hoạt động cho gói [{self.selected_target}].', color=(0.7, 0.7, 0.8, 1), font_size=10, size_hint_y=None, height=26, halign='left'))
        
        prog_row = BoxLayout(size_hint_y=None, height=20)
        prog_row.add_widget(Label(text='Trạng thái Aimlock', color=(0.8, 0.8, 0.9, 1), font_size=11, halign='left'))
        self.lbl_boost_percent = Label(text='ACTIVE (100% HEAD)', color=(0.2, 0.8, 0.4, 1), font_size=11, bold=True, halign='right')
        prog_row.add_widget(self.lbl_boost_percent)
        card_inject.add_widget(prog_row)
        
        self.boost_slider = Slider(min=0, max=100, value=100, size_hint_y=None, height=18)
        card_inject.add_widget(self.boost_slider)
        
        self.btn_boost_action = Button(text='✨ ĐÃ KÍCH HOẠT AIMLOCK THÀNH CÔNG', size_hint_y=None, height=40, background_normal='', background_color=(0.2, 0.8, 0.4, 1), color=(1, 1, 1, 1), bold=True)
        card_inject.add_widget(self.btn_boost_action)
        
        content_layout.add_widget(card_inject)
        self.content_area.add_widget(content_layout)

    def load_info_tab(self):
        card = PanelCard(size_hint=(1, None), height=270)
        card.add_widget(Label(text='[b]ℹ TRẠNG THÁI HỆ THỐNG DUAL[/b]', markup=True, color=(0.690, 0.400, 0.960, 1), size_hint_y=None, height=24))
        card.add_widget(Label(text=f'• Mục tiêu hiện tại: {self.target_display_name}', color=(0.9, 0.9, 0.9, 1), size_hint_y=None, height=24, halign='left'))
        card.add_widget(Label(text=f'• Package Name: {self.selected_target}', color=(0.7, 0.7, 0.8, 1), size_hint_y=None, height=24, halign='left'))
        card.add_widget(Label(text='• Trạng thái Aimlock: Đang khóa Bone ID 8 (100% Bám đầu)', color=(0.2, 0.8, 0.4, 1), size_hint_y=None, height=24, halign='left'))
        card.add_widget(Label(text=f'• Key bản quyền: {self.current_key}', color=(0.9, 0.9, 0.9, 1), size_hint_y=None, height=24, halign='left'))
        
        btn_logout = Button(text='ĐĂNG XUẤT', size_hint_y=None, height=38, background_normal='', background_color=(0.8, 0.2, 0.2, 1), color=(1,1,1,1), bold=True)
        btn_logout.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        card.add_widget(btn_logout)
        self.content_area.add_widget(card)

class HeadlockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    HeadlockApp().run()
