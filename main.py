import objc
from pyobjus import autoclass
from pyobjus.app_delegate import UIResponder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
import os

# Tích hợp WebKit Native để tải tệp index.html trực tiếp
WKWebView = autoclass('WKWebView')
WKWebViewConfiguration = autoclass('WKWebViewConfiguration')
UIViewController = autoclass('UIViewController')
UIView = autoclass('UIView')
NSURL = autoclass('NSURL')
NSURLRequest = autoclass('NSURLRequest')

class WebViewHolder(Widget):
    def __init__(self, **kwargs):
        super(ViewHolder, self).__init__(**kwargs)
        Clock.schedule_once(self.setup_webview, 1)

    def setup_webview(self, dt):
        # Thiết lập khung hiển thị trang HTML nhúng
        config = WKWebViewConfiguration.alloc().init()
        webview = WKWebView.alloc().initWithFrame_configuration_(
            ((0, 0), (self.width, self.height)), config
        )
        
        # Đường dẫn tới tệp HTML đóng gói trong ứng dụng
        html_path = os.path.join(os.path.dirname(__file__), 'index.html')
        ns_url = NSURL.fileURLWithPath_(str(html_path))
        request = NSURLRequest.requestWithURL_(ns_url)
        
        webview.loadRequest_(request)
        # Gắn vào cửa sổ chính của iOS
        app_window = autoclass('UIApplication').sharedApplication().keyWindow
        app_window.rootViewController().view().addSubview_(webview)

class HeadlockVIPApp(App):
    def build(self):
        return WebViewHolder()

if __name__ == '__main__':
    HeadlockVIPApp().run()
