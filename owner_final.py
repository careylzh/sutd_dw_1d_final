#the 2 lines below allow the use of the RPi screen with Kivy
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
#initialize list of orders as a list
class Orders:
    def __init__(self):
        self.list_of_orders = []
#when this function refresh_orders is called, read firebase for pending orders
    def refresh_orders(self):
        self.list_of_orders=db.child('chickenrice').child('pending').get().val()
        #remove placeholders and extra dictionary entries
        del self.list_of_orders['0']
        del self.list_of_orders['Placeholder']
order_list = Orders()

#custom button template
class newButton(Button):
    def __init__(self, **kwargs):
        Button.__init__(self, **kwargs)
        #new button has a mode that transits between verify, complete.
        self.mode = "verify"
        #verify payment shows as text on the button
        self.text = "Verify Payment"

class Page1(Screen):
    #make a container to add widgets to
    container = ObjectProperty(None)
    #add rows function: read the firebase for adding data into the container
    def add_rows(self):
        #clear everything
        self.container.clear_widgets()
        #read firebase for orders
        order_list.refresh_orders()
        #order list: for every element, create an entry
        for element in order_list.list_of_orders.items():
            #add id
            p = Label(id = element[0], text = str(element[0]), size_hint_y=None,height=100)
            self.container.add_widget(p)
            #add name
            q = Label(id = element[0], text = str(element[1]).replace('[', "").replace(']', "").replace("'", ""), text_size = (200, 100))
            self.container.add_widget(q)
            #add an instance of newButton 
            r = newButton(id = element[0], text = "Verify")
            #newButton bind to change of state
            r.bind(on_release = self.change_state)
            self.container.add_widget(r)
    def change_state(self, instance):
        #this is a button text changer
        #if the mode of the button is verify, change it to complete
        if instance.mode == "verify":
            instance.mode = "complete"
            instance.text = "Complete"
        #if the mode of the button is complete, then when its pressed again, remove the entry
        elif instance.mode == "complete":
            self.remove_entry(instance)


    def remove_entry(self, instance):
        #called everytime button is pressed. we used the on_release method in kivy language to call this function.
        #if the list is not empty, delete an element from list of orders
        #if the list is empty, then pressing the button will not delete anything (error prevention)
        if len(order_list.list_of_orders) != 0:
            del order_list.list_of_orders[instance.id]
            #for each element in the pending list on Firebase, read its values and keys
            for x in range(len(db.child('chickenrice').child('pending').child(instance.id).get().val())):
                #shift everything under pending to the collection tab
                a=db.child('chickenrice').child('pending').child(instance.id).get().val()[x]
               	db.child('chickenrice').child('collection').child(instance.id).child(x).set(a)
            db.child('chickenrice').child('pending').child(instance.id).remove()
            #and then read FB again and display the entries left
            self.add_rows()
#screen changer
    def change_screen(self):
        if self.manager.current == 'main':
            self.manager.current = 'second'

class Page2(Screen):
    def display_graph(self):
    	#read data from firebase
        self.data = db.child('chickenrice').child('end_of_day_sales').get().val()
        
        #data processing - data looks like Ordereddict((name, [list of food]), (name, [list of food]))
        #delete all placeholders from self.data
        del self.data['0']
        del self.data['Placeholder']
        g = []
#extract all items from self.data and plug into list g
        for key,val in self.data.items():
            for element in val:
                g.append(element)
#plot graph
#instantiate plot
        fig, ax = plt.subplots()
        bar_graph = FigureCanvas(fig)
#s is a list with only 1 of every item (no duplicates) used as the x axis of bar plot
        s = list(set(g))
        #counts of each element in s
        counts = []
        for i in range(len(s)):
            counts.append(g.count(s[i]))
        ax.bar(s, counts)
        #add the graph into box layout with id bargraph
        self.ids.bargraph.add_widget(bar_graph)
        
#instantiate screenmanager
class WindowManager(ScreenManager):
    pass
#save app 'owner.kv' into variable kv
kv = Builder.load_file('owner.kv')
class MyMainApp(App):
    #build app by returning kv
    def build(self):
        return kv
#run app
if __name__ == "__main__":
    MyMainApp().run()
