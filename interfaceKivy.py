from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty




class JanelaApp(Screen):
    
    pass
    
class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('GUI.kv')

sm = WindowManager()

screens= [JanelaApp(name='janela')]

for screen in screens:
    sm.add_widget(screen)
sm.current = 'janela'
    
class MyMainApp(App):
    def build(self):
        return sm
    def on_start(self):
        self.title = "ChatBot"
        self.geometry = (800, 600)
        return
    pass
        
if __name__ == "__main__":
    app = MyMainApp()
    app.run()