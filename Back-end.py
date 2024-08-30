import kivy
from kivy.app import App
from kivy.core.window import Window 
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty

class app_layout(Widget): # create grid layout of 1 grid layout 1 relative 1 grid and next is stack layout 
    # completion bar made up of 4 fuarters
    days = ObjectProperty(None)
    task = ObjectProperty(None)
    task_count = 0
    
    disabled_add = BooleanProperty(False)



    f1 = NumericProperty(0)
    f2 = NumericProperty(0)
    f3 = NumericProperty(0)
    f4 = NumericProperty(0)
    f5 = NumericProperty(0)

    

    def press_me(self): # trying for showing complition bar, if len of stage is 2 f(n) += 1 after pressing move right 
        print(self.days.text, self.task.text)
        """days_int = int(self.days.text)
         days_int += 5
        print(days_int) """
        if self.f1 and self.f2 and self.f3 and self.f4 and self.f5 == 1:
           self.f1 -= 1
           self.f2 -= 1
           self.f3 -= 1
           self.f4 -= 1
           self.f5 -= 1
        else:
           self.f1 += 1
           self.f2 += 1
           self.f3 += 1
           self.f4 += 1
           self.f5 += 1

    def add_task(self): # take input field text make widget with text and date
        
        table_layout = self.ids.table_id # the part where the labels will be

        task_str = str(self.task.text)
        x_pos = - 0.37 
        y_pos = 0.46 - 0.1 * self.task_count

        my_label = Label(text=task_str, pos_hint={'x': x_pos, 'y': y_pos})
        table_layout.add_widget(my_label)

        self.task_count = sum(1 for child in table_layout.children if isinstance(child, Label)) 
        
        print(f"Number of tasks: {self.task_count}")
        self.check_task_count()
        

    def check_task_count(self):
        if self.task_count >= 10:
            self.disabled_add = True
        else:
            self.disabled_add = False


    def delete_task(self): # if chosen delete
        pass

    def move_right(self): # add value to y
        pass

    def move_left(self): # subtract value from y
        pass

    def clear_table(self): # clear
        table_layout = self.ids.table_id
        table_layout.clear_widgets()
        self.task_count = 0
        self.check_task_count()

    def save_progress(self): # save
        pass

class Kanban(App):

    def build(self):
        Window.size = (1024, 768) 

        Window.resizable = False
        return app_layout()
    
if __name__ == "__main__":
    Kanban().run()