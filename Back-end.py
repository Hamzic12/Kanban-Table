import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.properties import StringProperty

class Grid(Widget): # create 4 grid layouts and one stack layout
    task = ObjectProperty(None)
    sign = ObjectProperty(None)
    b = 0
    variable = StringProperty("HELLO Variable")
    
    def pressed(self):
        position = self.task.pos
        text = self.task.text
        print(position)
        print(text)
        position[0] += 0
        position[1] += 50
        print(position)

        self.ids.grid_id.remove_widget(self.ids.label) # syntax for removing

        self.ids.grid_id.add_widget(Widget()) # syntax for adding
        
        self.add_widget(Label(text="Name: Jeff"))
        exampl = Label(text="Name: Jefssssssssssss")

        self.add_widget(exampl)
        exampl_pos = exampl.pos


        exampl_pos[0] += 200 + self.b
        exampl_pos[1] += 200 + self.b
        
        self.b += 50
        
        self.task.text = ""
        self.variable = "after click variable"

    def remove(self):
        #remove text from one label and change into another label
        pass

class Kanban(App):

    def build(self):
        return Grid()
    
if __name__ == "__main__":
    Kanban().run()