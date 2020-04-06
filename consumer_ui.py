#Kivy imports
from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.config import Config
import webbrowser
from kivy.uix.gridlayout import GridLayout

#Firebase imports
from libdw import pyrebase

#other imports
import random

#Setup Firebase
url = "https://dw4c3-f19ad.firebaseio.com/"
apikey = "AIzaSyBNDJ2C8IvzTNJCJ0XUNbDFuyeIkqnz3gk"

config = {
    "apiKey": apikey,
    "databaseURL": url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#Firebase codes
#this class fetches the firebase child with name 'Accounts' for user authentication
class Accounts:
    def __init__(self):
        self.accounts = db.child('Accounts').get()

    def update_accounts(self):
        self.accounts = db.child('Accounts').get()

#this allows user sessions just like other CMSes(content management system)
class UserInfo:
    def __init__(self, user=''):
        self.user = user
        self.curr_store = ''
        self.store_page = 'main_menu'

    def set_user(self, other):
        self.user = other
#the function below tracks which store the user is at for front-end screen display.
    def set_store(self, other):
        self.curr_store = other


curr_accounts = Accounts()
curr_user = UserInfo()

#Kivy codes
#set screen resolution in pixels
Config.set('graphics', 'width', '390')
Config.set('graphics', 'height', '600')

#this class consists of a method that calculates each item price and stores it in a local var. Firebase not involved.
class cart():
    def __init__(self):
        self.value = 0
        self.cart_lst = []
        self.cart_price = []

    def calculator(self, newVal):
        self.value += newVal
        return self.value

    def add_to_cart(self, order, price):
        self.cart_lst.append(order)
        self.cart_price.append(price)

cartInstance = cart()

class LoginPage(Screen):

    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.text_count_username = 0
        self.text_count_passw = 0
        self.text_color = (1, 1, 1, 0.5)

    def verify_credentials(self):
        #print(accounts.val()[self.ids['username'].text])
        try:
            print(curr_accounts.accounts.val()[self.ids['username'].text])
            if curr_accounts.accounts.val()[self.ids['username'].text] == self.ids["passw"].text:
                curr_user.set_user(self.ids['username'].text)
                self.manager.current = "main_menu"
            else:
                print('Invalid Password or Username')
                self.ids['invalid_account'].text = 'Invalid Username or Password'
        except KeyError:
            print('Invalid Password or Username')
            self.ids['invalid_account'].text = 'Invalid Username or Password'

    def clear_text_once_username(self):
        if self.text_count_username == 0:
            self.ids['username'].text = ""
            self.text_count_username += 1
            self.ids['username'].text_color = (1, 1, 1, 1)

    def clear_text_once_passw(self):
        if self.text_count_passw == 0:
            self.ids['passw'].text = ""
            self.ids['passw'].password = True
            self.text_count_passw += 1
            self.ids['passw'].text_color = (1, 1, 1, 1)

    def clear_text(self):
        self.ids['username'].text = ""
        self.ids['passw'].text = ""


class SignUpPage(Screen):
    def __init__(self, **kwargs):
        super(SignUpPage, self).__init__(**kwargs)
        self.text_count_username = 0
        self.text_count_passw = 0
        self.text_count_rtpassw = 0
        self.text_color = (1, 1, 1, 0.5)

    def create_account(self):
        if self.ids['new_password'].text == self.ids['retype_password'].text:
            db.child('Accounts').child(self.ids['new_username'].text).set(self.ids['retype_password'].text)
            self.ids['account_created'].text = 'ACCOUNT SUCCESSFULLY CREATED'
            curr_accounts.update_accounts()

    def clear_text_once_username(self):
        if self.text_count_username == 0:
            self.ids['new_username'].text = ""
            self.text_count_username += 1
            self.ids['new_username'].text_color = (1, 1, 1, 1)

    def clear_text_once_passw(self):
        if self.text_count_passw == 0:
            self.ids['new_password'].text = ""
            self.ids['new_password'].password = True
            self.text_count_passw += 1
            self.ids['new_password'].text_color = (1, 1, 1, 1)

    def clear_text_once_rtpassw(self):
        if self.text_count_rtpassw == 0:
            self.ids['retype_password'].text = ""
            self.ids['retype_password'].password = True
            self.text_count_rtpassw += 1
            self.ids['retype_password'].text_color = (1, 1, 1, 1)


class WindowManager(ScreenManager):
    pass


class PopupPage(GridLayout):

    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PopupPage, self).__init__(**kwargs)
        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.container.bind(minimum_height=self.container.setter('height'))
        self.add_text_inputs()

    def add_text_inputs(self):
        print(db.child('chickenrice').child('collection').child(curr_user.user).get().val())
        try:
            for x in range(len(db.child('chickenrice').child('collection').child(curr_user.user).get().val())):
                self.container.add_widget(Label(text="{}".format(db.child('chickenrice').child('collection')
                                                                 .child(curr_user.user).get().val()[x]),
                                                size_hint_y=None,
                                                color=(0, 0, 0, 0.7)))
        except TypeError:
            self.container.add_widget(Label(
                text="{}".format(''),
                size_hint_y=None,
                color=(0, 0, 0, 0.7)))
            self.container.add_widget(Label(
                text="{}".format('Your orders are being \nprocessed, it should only take \na few moments.'),
                size_hint_y=None,
                color=(0, 0, 0, 0.7)))
        try:
            if len(db.child('chickenrice').child('collection').child(curr_user.user).get().val()) >= 1:
                db.child('real_password').child(curr_user.user).set(random.randrange(100000, 999999, 1))
                print(db.child('real_password').child(curr_user.user).get().val())
                self.container.add_widget(Label(text='Password: {}'.format(db.child('real_password')
                                                                           .child(curr_user.user).get().val()),
                                                size_hint_y=None,
                                                color=(0, 0, 0, 0.7)))
                self.container.add_widget(
                    Label(text='{}'.format('\n\nYour orders are ready for \ncollection. Please use the \n'
                                           'password above to unlock \nyour box.'),
                          size_hint_y=None,
                          color=(0, 0, 0, 0.7)))
        except TypeError:
            print('Not ready')


class MainMenu(Screen):

    def switch_cr(self):
        self.manager.current = 'chicken_rice'
        curr_user.set_store('Chicken Rice')
        curr_user.store_page = 'chicken_rice'

    def switch_hs(self):
        self.manager.current = 'health_soup'
        curr_user.set_store('Health Soup')
        curr_user.store_page = 'health_soup'

    def show_popup(self):
        show_popup = PopupPage()
        popup_window = Popup(title='                       Your Orders',
                             title_size=38,
                             content=show_popup,
                             size_hint=(0.7, 1),
                             pos_hint={'center_x': 0.35, 'center_y': 0.5},
                             background='Green.png')
        popup_window.open()


class chickenRiceScreen(Screen):

    def on_press_rcr(self):
        cartInstance.calculator(3.5)
        cartInstance.add_to_cart('Roasted Chicken Rice', 'SGD 3.50')
        self.manager.current = 'cart_page'

    def on_press_scr(self):
        cartInstance.calculator(3)
        cartInstance.add_to_cart('Steamed Chicken Rice', 'SGD 3.00')
        self.manager.current = 'cart_page'

    def on_press_cwm(self):
        cartInstance.calculator(4)
        cartInstance.add_to_cart('Char Siew Wanton Mee', 'SGD 4.00')
        self.manager.current = 'cart_page'

    def on_press_csr(self):
        cartInstance.calculator(3.5)
        cartInstance.add_to_cart('Char Siew Rice', 'SGD 3.50')
        self.manager.current = 'cart_page'


class HealthSoupScreen(Screen):

    def on_press_ocs(self):
        cartInstance.calculator(4.5)
        cartInstance.add_to_cart('Old Cucumber Soup', 'SGD 4.50')
        self.manager.current = 'cart_page'

    def on_press_lrs(self):
        cartInstance.calculator(4.5)
        cartInstance.add_to_cart('Lotus Root Soup', 'SGD 4.50')
        self.manager.current = 'cart_page'

    def on_press_pts(self):
        cartInstance.calculator(4.5)
        cartInstance.add_to_cart('Pork Tripe Soup', 'SGD 4.50')
        self.manager.current = 'cart_page'

    def on_press_bkt(self):
        cartInstance.calculator(2.5)
        cartInstance.add_to_cart('Bak Kut Teh', 'SGD 2.50')
        self.manager.current = 'cart_page'

    def on_press_ts(self):
        cartInstance.calculator(4.5)
        cartInstance.add_to_cart('Tomato Soup', 'SGD 4.50')
        self.manager.current = 'cart_page'

    def on_press_wcs(self):
        cartInstance.calculator(4.5)
        cartInstance.add_to_cart('Watercress Soup', 'SGD 4.50')
        self.manager.current = 'cart_page'


class CartPage(Screen):
    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CartPage, self).__init__(**kwargs)
        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.container.bind(minimum_height=self.container.setter('height'))

    def add_text_inputs(self):
        print(cartInstance.cart_lst)
        self.ids['subtotal'].text = 'Subtotal: ' + str(cartInstance.value)
        for x in range(len(cartInstance.cart_lst)):
            self.container.add_widget(Label(text="{:<25}{:>25}".format(cartInstance.cart_lst[x], cartInstance.cart_price[x]),
                                            size_hint_y=None,
                                            height=100,
                                            color=(0, 0, 0, 0.7)))

    def clear_scroll(self):
        self.container.clear_widgets()

    def clear_orders(self):
        cartInstance.cart_lst = []
        cartInstance.cart_price = []
        cartInstance.value = 0
        curr_user.set_store('')
        self.add_text_inputs()

    def submit_orders(self):
        db.child('chickenrice').child('pending').child(curr_user.user).set(cartInstance.cart_lst)
        webbrowser.open('http://www.dbs.com.sg/personal/mobile/paylink/index.html?tranRef=n0eTGkTnvZ')

    def chosen_store(self):
        self.ids['store_name'].text = curr_user.curr_store

    def back_button(self):
        self.manager.current = curr_user.store_page

class OrdersPage(Screen):
    pass

kv = Builder.load_file("consumer.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()
