import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.text.text_layout import layout_text
from kivy.properties import ObjectProperty
from libdw import pyrebase
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
url="https://dw4c3-f19ad.firebaseio.com/"
apikey="AIzaSyBNDJ2C8IvzTNJCJ0XUNbDFuyeIkqnz3gk"
config = {
    "apiKey": apikey,
    "databaseURL": url,
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

import copy
import numpy as np
import matplotlib.pyplot as plt

class Orders:
    def __init__(self):
        self.list_of_orders = []
    def refresh_orders(self):
        self.list_of_orders=db.child('chickenrice').child('pending').get().val()
        del self.list_of_orders['0']
        del self.list_of_orders['Placeholder']
orderlist = Orders()
class CompletedOrders:
    def __init__(self):
        self.complete_list = copy.deepcopy(orderlist.list_of_orders)

completedorderlist = CompletedOrders()

class newButton(Button):
    def __init__(self, **kwargs):
        Button.__init__(self, **kwargs)
        self.mode = "verify"
        self.text = "Verify Payment"

class Page1(Screen):
    container = ObjectProperty(None)

    def add_rows(self):
        self.container.clear_widgets()
        orderlist.refresh_orders()
        for element in orderlist.list_of_orders.items():
            print(element[0])
            p = Label(id = element[0], text = str(element[0]), size_hint_y=None,height=100)
            self.container.add_widget(p)
            q = Label(id = element[0], text = str(element[1]).replace('[', "").replace(']', "").replace("'", ""), text_size = (200, 100))
            self.container.add_widget(q)
            r = newButton(id = element[0], text = "Verify")
            r.bind(on_release = self.change_state)
            self.container.add_widget(r)
    def change_state(self, instance):
        if instance.mode == "verify":
            instance.mode = "complete"
            instance.text = "Complete"
        elif instance.mode == "complete":
            self.remove_entry(instance)


    def remove_entry(self, instance):
        if len(orderlist.list_of_orders) != 0:
            print('this is the id of the row',instance.id)
            del orderlist.list_of_orders[instance.id]
            for x in range(len(db.child('chickenrice').child('pending').child(instance.id).get().val())):
                a=db.child('chickenrice').child('pending').child(instance.id).get().val()[x]
               	db.child('chickenrice').child('collection').child(instance.id).child(x).set(a)
            db.child('chickenrice').child('pending').child(instance.id).remove()
            self.add_rows()
    def change_screen(self):
        if self.manager.current == 'main':
            self.manager.current = 'second'

class Page2(Screen):
    #read data from firebase
    def display_graph(self):
    	#read data from firebase
        self.data = db.child('chickenrice').child('end_of_day_sales').get().val()
        
        #data processing - data looks like Ordereddict((name, [list of food]), (name, [list of food]))
        del self.data['0']
        del self.data['Placeholder']
        g = []

        for key,val in self.data.items():
            for element in val:
                g.append(element)

        fig, ax = plt.subplots()
        bar_graph = FigureCanvas(fig)

        s = list(set(g))
        counts = []
        for i in range(len(s)):
            counts.append(g.count(s[i]))
        ax.bar(s, counts)
        self.ids.bargraph.add_widget(bar_graph)
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('owner.kv')
class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()



'''
class screen1(Screen):
    pass

class screen2(Screen):
    pass

class windowmanager(ScreenManager):
    pass
kv = Builder.load_file("owner.kv")
class ownerApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    ownerApp().run()
'''

