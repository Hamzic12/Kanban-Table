import kivy
import datetime
from Punishments import *
from kivy.app import App
from kivy.core.window import Window 
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout



    
class App_layout(Widget): # create grid layout of 1 grid layout 1 relative 1 grid and next is stack layout 
    days = ObjectProperty(None)
    task = ObjectProperty(None)
    task_count = 0
    finished = 0
    disabled_add = BooleanProperty(False)
    bad_points = 0 # for every delayed task plus bad points every day => worse punishment

    f1 = NumericProperty(0) # fifths of the progress bar
    f2 = NumericProperty(0)
    f3 = NumericProperty(0)
    f4 = NumericProperty(0)
    f5 = NumericProperty(0)
    
    p = None
    punishments = Consequences()

    finish_stage = 0.7641 # position for when task is finished
    beginning_stage = 0.019

    def check_task_count(self):
        self.table_layout = self.ids.table_id # To avoid repeating it in every method
        if self.task_count >= 10:
            self.disabled_add = True
        else:
            self.disabled_add = False
    
    def on_touch_down(self, touch):
        table_layout = self.ids.table_id

        for child in table_layout.children:
            if isinstance(child, Label):
                x, y = table_layout.to_widget(*touch.pos)
                if child.collide_point(x, y):
                    if child.chosen is True:
                        child.chosen = False # If the label is already chosen, unselect it
                    else:
                        for other_child in table_layout.children:
                            if isinstance(other_child, Label):
                                other_child.chosen = False  # Deselects everyone else
                        child.chosen = True
                    return True  # Label was touched, consume the event

        return super().on_touch_down(touch)
    
    def add_task(self):  # take input field text, make widget with text and date
        table_layout = self.ids.table_id  # relative layout id

        task_str = str(self.task.text)
        
        if self.days.text != "": # fixed when clicking add and days input field is empty stops the app
            days_int = int(self.days.text)
            days_to_date = datetime.date.today() + datetime.timedelta(days=days_int)
        
        x_pos = 0.018  # Horizontal position for the task
        y_pos = 0.905 - 0.098 * self.task_count  # Vertical position, spaced out per task

        if self.task.text != "" and self.days.text != "":
            task_label = Label(text=f"{task_str}\n{days_to_date}", font_size = "15sp", color=(0,0,0,1),
                            pos_hint={'x': x_pos, 'y': y_pos},
                            size_hint=(None, None), size=(170, 50))
            
            task_label.due_date = days_to_date
            task_label.chosen = False
            task_label.is_finished = False

            # create background for label of tasks and before so the rectangle is under the text
            with task_label.canvas.before:
                Color(0,0,0,1, mode="rgba")
                highlight_task = Rectangle(pos=(task_label.pos[0] - 4, task_label.pos[1] - 4), size=(task_label.size[0] + 8, task_label.size[1] + 8))

                Color(1, 0, 0, 1, mode='rgba')  # rectangle for background of label
                label_bg = Rectangle(pos=task_label.pos, size=task_label.size)

                # Bind the rectangle for higlighting the task to task_label
                task_label.bind(pos=lambda instance, value: setattr(highlight_task, 'pos', (task_label.pos[0] - 4, task_label.pos[1] - 4)))
                task_label.bind(size=lambda instance, value: setattr(highlight_task, 'size', (task_label.size[0] + 8, task_label.size[1] + 8)))

                # Bind the label_bg position and size to the task_label
                task_label.bind(pos=lambda instance, value: setattr(label_bg, 'pos', task_label.pos))
                task_label.bind(size=lambda instance, value: setattr(label_bg, 'size', task_label.size))

            table_layout.add_widget(task_label)

        self.task.text = "" # Clears input field for tasks
        self.days.text = "" # Clears input field for days
        self.task_count = sum(1 for child in table_layout.children if isinstance(child, Label))
        self.check_task_count()

    def progress_bar(self):  # Track progress based on position
        
        for child in self.table_layout.children:
            if isinstance(child, Label):
                curr_pos = child.pos_hint.get('x')
                if curr_pos == self.finish_stage and child.is_finished is False:
                    child.is_finished = True
                    self.finished += 1
                elif curr_pos < self.finish_stage and child.is_finished is True:
                    child.is_finished = False
                    self.finished -= 1

        # Update progress bar
        self.f1 = 1 if self.finished >= 2 else 0
        self.f2 = 1 if self.finished >= 4 else 0
        self.f3 = 1 if self.finished >= 6 else 0
        self.f4 = 1 if self.finished >= 8 else 0
        self.f5 = 1 if self.finished >= 10 else 0


    def delete_task(self): # if chosen delete
        removed_child = None
        for child in self.table_layout.children:
            if isinstance(child, Label) and child.chosen is True:
                if child.is_finished is True: # if it was in the done stage
                    child.is_finished = False
                    self.finished -= 1
                
                removed_child = child 
                self.table_layout.remove_widget(child)
                self.task_count -= 1

        if removed_child.pos_hint['y'] is not None:
            for child in self.table_layout.children:
                if isinstance(child, Label) and removed_child.pos_hint['y'] > child.pos_hint['y']:
                    child.pos_hint['y'] += 0.1

            self.progress_bar()
        self.table_layout.do_layout()


    def move_right(self): # add value to x
        
        for child in self.table_layout.children:
            if isinstance(child, Label) and child.pos_hint['x'] < self.finish_stage and child.chosen is True:
                child.pos_hint['x'] += 0.2487
                self.table_layout.do_layout()
        self.progress_bar()

    def move_left(self): # subtract value from x
        for child in self.table_layout.children:
            if isinstance(child, Label) and child.pos_hint['x'] > self.beginning_stage and child.chosen is True:
                child.pos_hint['x'] -= 0.2487
                self.table_layout.do_layout()
        self.progress_bar()

    def clear_table(self): # clear
        for child in list(self.table_layout.children): # now it removes only labels, not the lines
            if isinstance(child, Label):
                self.table_layout.remove_widget(child)
        
        self.task_count = 0
        self.finished = 0

        self.check_task_count()
        self.progress_bar()

        self.table_layout.do_layout()

    def pop_up(self):
        self.p = P_edit()
        table_layout = self.ids.table_id
        for child in table_layout.children:
            if isinstance(child, Label) and child.chosen is True:
                popupWindow = Popup(title="Edit task", content = self.p, size_hint = (None, None), size=(400,400))
                popupWindow.open()

    def edit_task(self): # edit tasks
        if self.p is not None and self.p.changed_task is not None:
            ct = self.p.changed_task.text
            ct_str = str(ct)
        
        table_layout = self.ids.table_id
        for child in table_layout.children:
            if isinstance(child, Label) and child.chosen is True:
                child.text = ct_str
            
        self.table_layout.do_layout()
    
    def check_late_tasks(self, dt): # dt for amount of seconds since the call of this method
        table_layout = self.ids.table_id
        for child in table_layout.children:
            if hasattr(child, 'due_date'):
                if child.due_date < datetime.date.today(): # checks if today is later than date of task
                    self.bad_points += 1 # for every late task is a + for bad points for punishment
    
    def punishment_activator(self, dt):
        if self.bad_points >= 1:
            self.punishments.Motivator()
        if self.bad_points >= 3:
            self.punishments.Motivator()
        if self.bad_points  >= 6:
            self.punishments.Motivator()
        if self.bad_points >= 10:
            self.punishments.Motivator() 


    def every_24h(self): # right now 1 second to try it
        Clock.schedule_interval(self.check_late_tasks, 2) # checks every 24 hours (in seconds) if there is a late task
        Clock.schedule_interval(self.punishment_activator, 2)


class P_edit(GridLayout):
    changed_task = ObjectProperty(None)
    al = App_layout()

class Kanban(App):

    def build(self):
        Window.size = (1024, 768)
        layout = App_layout()
        layout.every_24h()
        return layout
    
if __name__ == "__main__":
    Kanban().run()