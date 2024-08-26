import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label

class Grid(Widget): # create 4 grid layouts and one stack layout
    task = ObjectProperty(None)
    sign = ObjectProperty(None)
    b = 0
    """ 
        def pressed(self):
        position = self.task.pos
        text = self.task.text
        print(position)
        print(text)
        position[0] += 1
        position[1] += 5
        print(position)
        self.remove_widget(self.sign)
        self.add_widget(Label(text="Name: Jeff"))
        exampl = Label(text="Name: Jefssssssssssss")

        self.add_widget(exampl)
        exampl_pos = exampl.pos


        exampl_pos[0] += 200 + self.b
        exampl_pos[1] += 200 + self.b
        
        self.b += 50
        
        self.task.text = ""
    """
    
    def remove(self):
        #remove text from one label and change into another label
        pass

class Kanban(App):

    def build(self):
        return Grid()
    
if __name__ == "__main__":
    Kanban().run()