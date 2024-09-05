import kivy
from kivy.app import App
from kivy.core.window import Window 
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class app_layout(Widget): # create grid layout of 1 grid layout 1 relative 1 grid and next is stack layout 
    # completion bar made up of 4 fuarters
    days = ObjectProperty(None)
    task = ObjectProperty(None)
    task_count = 0
    finished = 0
    disabled_add = BooleanProperty(False)

    f1 = NumericProperty(0) # fifths of the progress bar
    f2 = NumericProperty(0)
    f3 = NumericProperty(0)
    f4 = NumericProperty(0)
    f5 = NumericProperty(0)

    def check_task_count(self):
        self.table_layout = self.ids.table_id # To avoid repeating it in every method
        if self.task_count >= 10:
            self.disabled_add = True
        else:
            self.disabled_add = False
    
    
    def add_task(self):  # take input field text, make widget with text and date
        table_layout = self.ids.table_id  # relative layout id

        task_str = str(self.task.text)
        x_pos = 0.005  # Horizontal position for the task
        y_pos = 0.9 - 0.1 * self.task_count  # Vertical position, spaced out per task

        if self.task.text != "":
            task_label = Label(text=task_str,
                            pos_hint={'x': x_pos, 'y': y_pos},
                            size_hint=(None, None), size=(200, 50))
            
            # Create the label_bgangle behind the label dilabel_bgly linked to this task
            with task_label.canvas.before:
                Color(1, 0, 0, 0.5, mode='rgba')  # Semi-transparent red background
                label_bg = Rectangle(pos=task_label.pos, size=task_label.size)

                # Bind the label_bg position and size to the task_label
                task_label.bind(pos=lambda instance, value: setattr(label_bg, 'pos', task_label.pos))
                task_label.bind(size=lambda instance, value: setattr(label_bg, 'size', task_label.size))

            table_layout.add_widget(task_label)

        self.task_count = sum(1 for child in table_layout.children if isinstance(child, Label))
        self.check_task_count()
        self.task.text = "" # Clear the input text for the next task
        

    def progress_bar(self):  # Track progress based on position
        finish_stage = 0.38  # position for when task is finished
        
        for child in self.table_layout.children:
            if isinstance(child, Label):
                curr_pos = child.pos_hint.get('x')
                if curr_pos >= finish_stage and not hasattr(child, 'is_finished'):
                    child.is_finished = True
                    self.finished += 1
                elif curr_pos < finish_stage and hasattr(child, 'is_finished'):
                    delattr(child, 'is_finished')
                    self.finished -= 1

        # Update progress bar
        self.f1 = 1 if self.finished >= 2 else 0
        self.f2 = 1 if self.finished >= 4 else 0
        self.f3 = 1 if self.finished >= 6 else 0
        self.f4 = 1 if self.finished >= 8 else 0
        self.f5 = 1 if self.finished >= 10 else 0


    def delete_task(self): # if chosen delete
        pass

    def move_right(self): # add value to x
        for child in self.table_layout.children:
            if isinstance(child, Label) and child.pos_hint['x'] < 0.755:
                child.pos_hint['x'] += 0.25
                Clock.schedule_once(lambda dt: self.table_layout.do_layout())
        self.progress_bar()
        
        # TODO to choose which labels gets moved
 

    def move_left(self): # subtract value from x
        for child in self.table_layout.children:
            if isinstance(child, Label) and child.pos_hint['x'] > 0.0050000000000000044:
                child.pos_hint['x'] -= 0.25
                Clock.schedule_once(lambda dt: self.table_layout.do_layout())
                print(child.pos_hint['x'])
        self.progress_bar()
        # TODO to choose which labels gets moved

    def clear_table(self): # clear
        self.table_layout.clear_widgets()
        self.task_count = 0
        self.finished = 0
        Clock.schedule_once(lambda dt: self.table_layout.do_layout())
        self.check_task_count()
        self.progress_bar()

    def save_progress(self): # save to database
        pass

class Kanban(App):

    def build(self):
        Window.size = (1024, 768) 
        return app_layout()
    
if __name__ == "__main__":
    Kanban().run()