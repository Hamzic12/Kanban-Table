import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

class app_layout(Widget): # create grid layout of 1 grid layout 1 relative 1 grid and next is stack layout 
    # completion bar made up of 4 quarters
    q1 = NumericProperty(0)
    q2 = NumericProperty(0)
    q3 = NumericProperty(0)
    q4 = NumericProperty(0)
    q5 = NumericProperty(0)

    variable = StringProperty("HELLO Variable")
    
    """  
    inspiration from experiments
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

        exampl_pos = exampl.pos #getting position


        exampl_pos[0] += 200 + self.b # changing position
        exampl_pos[1] += 200 + self.b
        
        self.b += 50
        
        self.task.text = "" # empty input field
        self.variable = "after click variable" # changing label text
        """

    def press_me(self): # trying for showing complition bar, if len of stage is 3 q(n) += 1 after pressing move right 
        if self.q1 and self.q2 and self.q3 and self.q4 and self.q5 == 1:
           self.q1 -= 1
           self.q2 -= 1
           self.q3 -= 1
           self.q4 -= 1
           self.q5 -= 1
        else:
           self.q1 += 1
           self.q2 += 1
           self.q3 += 1
           self.q4 += 1
           self.q5 += 1

    def move_right(self): # add value to y
        pass

    def move_left(self): # subtract value from y
        pass
    
    def add_task(self): # take input field text make widget with text and date
        pass

    def delete_task(self): # if chosen delete
        pass

    def clear_table(self): # clear
        pass

class Kanban(App):

    def build(self):
        return app_layout()
    
if __name__ == "__main__":
    Kanban().run()