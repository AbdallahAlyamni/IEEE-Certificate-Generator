from sys import path
import time
from logging import setLogRecordFactory
from kivy import app, clock
from kivy.core import window
from kivy.config import Config
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.core.image import Image as CoreImage, Texture
from io import BytesIO
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem
from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KImage
from theme import Theme
from kivy.cache import Cache
from kivy.properties import ObjectProperty
import pandas as pd
from datetime import datetime

from certs import Generate


class MainWindow(Screen):
    pass


class SingleWindow(Screen):
    pass


class MultibleWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class Content(Screen):
    pass

class MultiblePreview(Screen):
    pass


class MyMainApp(MDApp):
    icon = 'ieeesustsb.ico' 
    dialog = None
    cert_texture = Texture.create(size=(640, 480))
    cert_image = CoreImage('cert.jpg')
    name_list = [""]
    cert_type = ""
    cert_date = ""
    cert_txt = ""
    current_year = str(datetime.now().year)

    multi_cert_file_path = ""
    multi_cert_textures = []

    im = None
    ims = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # clock.max_iteration = 400
        self.screen = Builder.load_file("template.kv")

        # self.icon = 'assets/ieeesustsb.ico' 
        # Config.set('kivy','window_icon',self.icon)
        self.title='IEEE Certficate Generator'

        print(self.get_application_config())

        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

        types = ["OF VOLUNTEERING", "OF APPRECIATION",
                 "OF HONOR", "OF COMPLETION"]
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "certificate",
                "text": f"{types[i]}",
                "height": dp(56),
                "on_release": lambda x=f"{types[i]}": self.set_item(x),
            } for i in range(4)
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.single_window.ids.cert_type,
            items=menu_items,
            position="center",
            width_mult=5,
        )
        self.menu2 = MDDropdownMenu(
            caller=self.screen.ids.multible_window.ids.multi_cert_type,
            items=menu_items,
            position="center",
            width_mult=5,
        )
        self.menu.bind()
        self.menu2.bind()

    def set_item(self, text_item):
        self.screen.ids.single_window.ids.cert_type.text = 'CERTIFICATE '+text_item
        self.screen.ids.single_window.ids.cert_type.icon = 'certificate'
        self.screen.ids.multible_window.ids.multi_cert_type.text = 'CERTIFICATE '+text_item
        self.screen.ids.multible_window.ids.multi_cert_type.icon = 'certificate'
        self.menu.dismiss()
        self.menu2.dismiss()

    def build(self):
        self.icon = "sustico.png"
        self.theme_cls.colors = Theme.colors
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        return self.screen

    def getSource(self):
        return 'exported/test-certificate.png'

    def get_texture(self):
        im = Generate.startGeneration(
            "", self.name_list, "cert.jpg", self.cert_type, self.cert_date, self.cert_txt)
        bytes = BytesIO()
        im.save(bytes, format='png')
        bytes.seek(0)
        self.cert_image = CoreImage(BytesIO(bytes.read()), ext='png')
        return self.cert_image.texture

    def exportCertificate(self):
        name = self.screen.ids.single_window.ids.holder_name.text
        self.im.save("exported/"+ name +"-certificate.pdf")
        if not self.dialog:
            self.dialog = MDDialog(text="Certficate Exported Successfully")
        self.dialog.open()
    
    def exportCertificates(self):
        for i in range(len(self.name_list)):
            name =self.name_list[i]
            self.ims[i].save("exported/"+ name +"-certificate.pdf")

        if not self.dialog:
            self.dialog = MDDialog(text="Certficate Exported Successfully")
        self.dialog.open()

    def formatCertficateMainText(self,txt):
        lines = txt.strip().split('\n')
        temp = ""
        for i in lines:
            if len(i) > 61:
                print(len(i))
                i = i.strip()
                lb = i.rindex(' ',0,60)
                i = i[:lb].strip() + "\n" + i[lb:].strip()
                print(i)
            temp = temp + '\n' + i

        return temp

    def go_to_preview_screen(self):

        self.name_list = [self.screen.ids.single_window.ids.holder_name.text]
        self.cert_type = self.screen.ids.single_window.ids.cert_type.text
        self.cert_date = self.screen.ids.single_window.ids.date_field.text
        self.cert_txt = self.screen.ids.single_window.ids.cert_txt.text
        self.cert_txt = self.formatCertficateMainText(self.cert_txt)
        self.cert_txt_optional = self.screen.ids.single_window.ids.cert_txt_optional.text

        self.im = Generate.startGeneration("", self.name_list,
                                      "cert.jpg",
                                      self.cert_type[12:],
                                      self.cert_date,
                                      self.cert_txt, self.cert_txt_optional)[0]
        bytes = BytesIO()
        self.im.save(bytes, format='png')
        bytes.seek(0)
        self.cert_image = CoreImage(BytesIO(bytes.read()), ext='png')
        self.screen.ids.dia_content.ids.img3.texture = self.cert_image.texture
        self.screen.current = "preview"
    
    def go_to_preview_screen_from_multi(self):

        print(self.screen.ids.multible_window.ids.file_path.text)
        data = pd.read_excel(self.screen.ids.multible_window.ids.file_path.text)
        name_list = data['Name'].to_list()

        self.name_list = name_list
        self.cert_type = self.screen.ids.multible_window.ids.multi_cert_type.text
        self.cert_date = self.screen.ids.multible_window.ids.multi_date_field.text
        self.cert_txt = self.screen.ids.multible_window.ids.multi_cert_txt.text
        self.cert_txt = self.formatCertficateMainText(self.cert_txt)
        self.cert_txt_optional = self.screen.ids.multible_window.ids.multi_cert_txt_optional.text

        self.ims = Generate.startGeneration("", self.name_list,
                                      "cert.jpg",
                                      self.cert_type[12:],
                                      self.cert_date,
                                      self.cert_txt, self.cert_txt_optional)
        for i in self.ims:
            bytes = BytesIO()
            i.save(bytes, format='png')
            bytes.seek(0)
            temp_cert_image = CoreImage(BytesIO(bytes.read()), ext='png')
            image_preview = KImage(
                pos_hint= {"x": 0, 'y': 0},
                size_hint= (1, 1),
                texture= temp_cert_image.texture,
                allow_stretch= True
            )
            self.screen.ids.multible_preview_content.ids.carousel.add_widget(image_preview)
        self.screen.current = "multible_preview"

    def on_save(self, instance, value, date_range):
        print(value.strftime('%d %b %Y'))
        temp = value.strftime('%d %b %Y').upper()
        self.screen.ids.single_window.ids.date_field.set_text(
            self, temp[:temp.index(self.current_year)])
        self.screen.ids.multible_window.ids.multi_date_field.set_text(
            self, temp[:temp.index(self.current_year)])

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    
    ############## MDFile Manager Methods ######################
    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):

        self.exit_manager()
        toast(path)
        self.screen.ids.multible_window.ids.file_path.set_text(self,path)
    
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        print(keyboard,"\rkeycode:\r", keycode)
        print("\n", self.screen.current)
        if self.screen.current == 'multible_preview':
            if keycode == 79:
                self.screen.ids.multible_preview_content.ids.carousel.load_next(mode='next')
            if keycode == 80:
                self.screen.ids.multible_preview_content.ids.carousel.load_previous()

        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
    ########################################################################


LabelBase.register(
    name='Lexend', fn_regular='fonts/Lexend-VariableFont_wght.ttf')
LabelBase.register(name='Montserrat-SemiBold',
                   fn_regular='fonts/Montserrat-SemiBold.ttf')
LabelBase.register(name='Montserrat-Medium',
                   fn_regular='fonts/Montserrat-Medium.ttf')
if __name__ == "__main__":
    MyMainApp().run()
