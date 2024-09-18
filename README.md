# Kanban Table

- Full-stack Python App using Kivy for GUI and SQLAlchemy for database.
- The app is a Kanban table for software developers to create and manage up to ten tasks, with the ability to set deadlines. 
- Failure to complete tasks on time results in punishment points, which trigger progressively stricter punishments.

## Installation

````
pip install kivy
````

````
pip install sqlalchemy
````

````
pip install schedule
````

## Features

- Lets the user move/remove/edit task, that user chooses, text color will be white to indicate being chosen
- User can either remove one task or clear the whole table and start over
- Above the text inputs are counters for number of tasks, number of finished tasks and number of punishment points
- There is a progress bar that shows how is the user doing
    - It is a dynamic bar, which changes sizes as the tasks grow in number
- Allows the user to save the progress and task data into a in-memory database and afterwards load them back up
- In case of a red text, it indicates a late tasks, and there are 4 stages of punishments:
    1. A video pops up everyday and motivates the user to finish the tasks in case the user still has punishment points 
    2. Every 6 seconds a there will be a pop up, which will annoy and motivate the user
    3. A video pops up and tells the user that "Actions have consequences" and afterwards will bring pain to the users ears
    4. 4 Websites will be blocked, which are facebook, instagram, youtube, google and reddit