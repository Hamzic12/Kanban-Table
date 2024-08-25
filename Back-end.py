import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

class Grid(GridLayout): # create 4 grid layouts and one stack layout
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.cols = 4 # stages
        self.rows = 10 # tasks
        self.add_widget(Label(text="New task"))
        self.add_widget(Widget())
        self.task = TextInput(multiline=False) 
        self.add_widget(self.task)



class Kanban(App):

    def build(self):
        return Grid()
    
if __name__ == "__main__":
    Kanban().run()