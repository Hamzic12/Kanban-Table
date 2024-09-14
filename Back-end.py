import kivy, datetime, schedule, threading
from Punishments import *
from Database import *
from kivy.app import App
from kivy.core.window import Window 
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout



class P_edit(GridLayout):
    changed_task = ObjectProperty(None)
    def edit_task(self): # edit tasks
        ct = self.changed_task.text 
        ct_str = str(ct)
        app = App.get_running_app() # gets instance of running kivy app
        al = app.root # gets the root widget of the app
        al.get_edited_task(ct_str)
        self.changed_task.text = ""
    

class App_layout(Widget): # create grid layout of 1 grid layout 1 relative 1 grid and next is stack layout with grid layout above and beneath it
    days = ObjectProperty(None)
    task = ObjectProperty(None)
    task_count = NumericProperty(0)
    finished = NumericProperty(0)
    disabled_add = BooleanProperty(False)
    bad_points = NumericProperty(0) # for every delayed task plus bad points every day => worse punishment

    f1 = NumericProperty(0) # fifths of the progress bar
    f2 = NumericProperty(0)
    f3 = NumericProperty(0)
    f4 = NumericProperty(0)
    f5 = NumericProperty(0)
    rectangle_height = NumericProperty(10)  # Base height per task
    text_color = ListProperty((0,0,0,1))

    p = P_edit()
    punishments = Consequences()

    beginning_stage = 0.022 # starting position for task
    finish_stage = 0.7681 # position for when task is finished

    
    def create_tl(self):
         # To avoid repeating it in every method
        self.table_layout = self.ids.table_id


    def check_task_count(self):
        self.task_count = sum(1 for child in self.table_layout.children if isinstance(child, Label))
        
        if self.task_count >= 10:
            self.disabled_add = True
        else:
            self.disabled_add = False

    
    def on_touch_down(self, touch):

        for child in self.table_layout.children:
            if isinstance(child, Label):
                x, y = self.table_layout.to_widget(*touch.pos)
                if child.collide_point(x, y):
                    if child.chosen is True:
                        child.chosen = False # If the label is already chosen, unselect it
                        child.color = (0,0,0,1)
                    else:
                        for other_child in self.table_layout.children:
                            if isinstance(other_child, Label):
                                other_child.chosen = False  # Deselects everyone else
                                other_child.color = (0,0,0,1)
                        child.chosen = True
                        child.color = (1,1,1,1)
                    return True  # Label was touched, consume the event

        return super().on_touch_down(touch)
    
    
    def add_task(self):  # take input field text, make widget with text and date

        task_str = str(self.task.text)
        
        if self.days.text != "": # fixed when clicking add and days input field is empty stops the app
            days_int = int(self.days.text)
            days_to_date = datetime.date.today() + datetime.timedelta(days=days_int)
        
        x_pos = self.beginning_stage  # Horizontal position for the task
        y_pos = 0.905 - 0.098 * self.task_count  # Vertical position, spaced out per task

        if self.task.text != "" and self.days.text != "":
            task_label = Label(text=f"{task_str}\n{days_to_date}", font_size = "15sp",
                            pos_hint={'x': x_pos, 'y': y_pos},
                            size_hint=(None, None), size=(170, 50))
            
            task_label.due_date = days_to_date
            task_label.chosen = False
            task_label.is_finished = False
            task_label.color = self.text_color

            # create background for label of tasks and before so the rectangle is under the text
            with task_label.canvas.before:

                Color(0, 1, 0, 0.5, mode='rgba')  # rectangle for background of label
                label_bg = Rectangle(pos=task_label.pos, size=task_label.size)

                # Bind the label_bg position and size to the task_label
                task_label.bind(pos=lambda instance, value: setattr(label_bg, 'pos', task_label.pos))

            self.table_layout.add_widget(task_label)

        self.task.text = "" # Clears input field for tasks
        self.days.text = "" # Clears input field for days
        self.check_task_count()
        self.progress_bar()


    def progress_bar(self):
        # Reset the finished task count
        self.finished = 0  
        for child in self.table_layout.children:
            if isinstance(child, Label):
                if child.pos_hint['x'] == self.finish_stage:
                    if child.is_finished is False:  
                        child.is_finished = True
                    self.finished += 1  
                else:
                    if child.is_finished:  
                        child.is_finished = False
        
        self.check_task_count()
        if self.task_count > 0:
            progress_fraction = self.finished / self.task_count
            self.ids.progress_bar.size_hint_x = progress_fraction

            if self.finished == 0:
                self.ids.progress_bar.canvas.before.children[0].rgba = (0, 0, 0, 1)  # Black when no tasks are finished
            else:
                self.ids.progress_bar.canvas.before.children[0].rgba = (0, 1, 0, 1)  # Green when some tasks are finished
        else:
            # No tasks, set progress to zero and make the line black
            self.ids.progress_bar.size_hint_x = 0
            self.ids.progress_bar.canvas.before.children[0].rgba = (0, 0, 0, 1)  # Black when no tasks







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

        if removed_child is not None:
            for child in self.table_layout.children:
                if isinstance(child, Label) and removed_child.pos_hint['y'] > child.pos_hint['y']:
                    child.pos_hint['y'] += 0.1

            self.progress_bar()
            self.check_task_count()
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
        self.bad_points = 0

        self.check_task_count()
        self.progress_bar()

        self.table_layout.do_layout()


    def pop_up(self):
        self.p = P_edit()
        for child in self.table_layout.children:
            if isinstance(child, Label) and child.chosen is True:
                popupWindow = Popup(title="Edit task", content = self.p, size_hint = (None, None), size=(400,400))
                popupWindow.open()


    def get_edited_task(self, string): 
        for child in self.table_layout.children:
            if isinstance(child, Label) and child.chosen is True:
                child.text = f"{string}\n{child.due_date}"


        self.table_layout.do_layout()

    
    def check_late_tasks(self):
        late_tasks = False
        table_layout = self.ids.table_id
        for child in table_layout.children:
            if hasattr(child, 'due_date'): 
                if child.due_date < datetime.date.today(): # checks if today is later than date of task
                    self.bad_points += 1 # for every late task is a + for bad points for punishment
                    late_tasks = True
                else:
                    late_tasks = False
        if late_tasks is False:
            self.bad_points = 0


    def punishment_activator(self):
        if self.bad_points == 1:
            self.punishments.Motivator()
        if self.bad_points == 3:
            self.punishments.annoying_popup()
        if self.bad_points  == 6:
            self.punishments.annoying_sound()
        if self.bad_points == 10:
            self.punishments.block_websites() 


    def schedule_checker(self):
        while True:
            schedule.run_pending()
            time.sleep(59)


    def save_progress(self):
        self.check_task_count()
        if self.task_count != 0:
            session.query(User_Tasks).delete()
            for child in self.table_layout.children: 
                if isinstance(child, Label):
                    task = [
                            User_Tasks(t_text = child.text,
                                    t_position_x = child.pos_hint['x'],
                                    t_position_y = child.pos_hint['y'],
                                    t_date = child.due_date,
                                    t_chosen = child.chosen,
                                    bad_points = self.bad_points,
                                    t_finished = child.is_finished)
                            ]

                    session.add_all(task)
                
            session.commit()

            saved_tasks = session.query(User_Tasks).all()

            for task in saved_tasks: # shows all data from database
                print(f"Task: {task.t_text}, Position X: {task.t_position_x}, Position Y: {task.t_position_y}, "
                f"Date: {task.t_date}, Chosen: {task.t_chosen}, Bad Points: {task.bad_points}, Finished: {task.t_finished}")
            
            
    def load_progress(self):
        saved_tasks = session.query(User_Tasks).all()

        for child in list(self.table_layout.children):
            if isinstance(child, Label):
                self.table_layout.remove_widget(child)
        
        self.finished = 0
        
        for task in saved_tasks:
            task_label = Label(text=f"{task.t_text}", font_size = "15sp",
                            pos_hint={'x': task.t_position_x, 'y': task.t_position_y},
                            size_hint=(None, None), size=(170, 50))
            task_label.due_date = task.t_date
            task_label.chosen = task.t_chosen
            task_label.is_finished = task.t_finished
            task_label.color = (1,1,1,1) if task_label.chosen is True else (0,0,0,1)
            
            with task_label.canvas.before:
                Color(0, 1, 0, 0.5, mode='rgba')
                task_label.bg_color = Color(0, 1, 0, 0.5, mode='rgba')
                task_label.bg_rect = Rectangle(pos=task_label.pos, size=task_label.size)
                task_label.bind(pos=self.update_rect_pos_size, size=self.update_rect_pos_size)
            
            self.table_layout.add_widget(task_label)

            if task_label.is_finished:
                self.finished += 1
        
        self.progress_bar() 
        self.check_task_count()    
        self.check_late_tasks()      
        


    def update_rect_pos_size(self, instance, value): # Update the rectangle's position and size to match the label
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size


class Kanban(App):
    def build(self):
        Window.size = (1024, 768)
        layout = App_layout()
        layout.create_tl()
        schedule.every().day.at("00:00").do(layout.check_late_tasks)
        schedule.every().day.at("13:00").do(layout.punishment_activator)
        threading.Thread(target=layout.schedule_checker, daemon=True).start()
        return layout
    
if __name__ == "__main__":
    Kanban().run()