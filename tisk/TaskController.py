#TaskController.py
from . import Task 
import tabulate
import argparse
from datetime import date 

class TaskController():
    def __init__(self,file_name):
        self.file_name = file_name

    def add_task(self, args):
        if not args.start_date:
            now = date.today().isoformat()
            args.start_date = now
        task = Task.Task(args.title, args.description, args.start_date, args.end_date, args.done)
            
        with open(self.file_name, 'a') as file:
            file.write(str(task) + '\n')

    def list_tasks(self):
        unfinished_tasks = []
        with open(self.file_name, 'r') as file:
            for line in file:
                title, description, start_date, end_date, done = line.split(', ')
                end_date = None if end_date == 'None' else end_date
                done = False if done.strip('\n') == 'False' else True
                if done:
                    continue
                unfinished_tasks.append({
                    'title':title,
                    'description':description,
                    'start_date':start_date,
                    'end_date':end_date
                    })
        return unfinished_tasks
    
    def list_all_tasks(self):
        tasks = []
        with open(self.file_name, 'r') as file:
            for line in file:
                title, description, start_date, end_date, done = line.split(', ')
                end_date = None if end_date == 'None' else end_date
                done = False if done.strip('\n') == 'Fakse' else True
                tasks.append({
                    'title':title,
                    'description':description,
                    'start_date':start_date,
                    'end_date':end_date,
                    'done':done,
                    })
        return tasks
    
    def due_date(self, start, end):
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        date_delta = end_date-start_date
        return f'{date_delta.days} Days left.'
    
    def print_table(self, tasks):
        formatted_tasks = []
        for number, task in enumerate(tasks, 1):
            if task.get('start_date') and task.get('end_date'):
                calcuated_due = self.due_date(task['start_date'], task['end_date'])
            else:
                due_date = 'Open'
            formatted_tasks.append({
                'no.':number,
                'title': task.get('title'),
                'description': task.get('desciption'),
                'start_date': task.get('start_date'),
                'end_date':task.get('end_date'),
                'done':task.get('done', False),
                'due_date': calcuated_due
            })

        print(tabulate.tabulate(formatted_tasks, headers= 'keys'))

    def display(self, args):
        all_tasks = self.list_all_tasks()
        unchecked_tasks = self.list_tasks()
        if not all_tasks:
            print('There is no tasks! to add a task use add <task>')
            return
        if args.all:
            self.print_table(all_tasks)
        else: 
            if unchecked_tasks:
                self.print_table(unchecked_tasks)
            else:
                print('All tasks are Done!')

    def check_task(self, args):
        index = args.task
        tasks = self.list_all_tasks()
        if index <= 0 or index > len(tasks):
            print(f'Task number ({index}) does not exist!')
            return
        tasks[index-1]['done'] = True
        with open(self.file_name, 'w') as file:
            for task in tasks:
                self.add_task(argparse.Namespace(**task))
    
    def remove_task(self, args):
        tasks = self.list_all_tasks()
        if args.task:
            index = args.task
        else:
            index = len(tasks) -1

        if index <= 0 or index > len(tasks):
            print(f'Task Number ({index}) does not exist!')
            return
        
        tasks.pop(index-1)
        with open(self.file_name, 'w') as file:
            for task in tasks:
                self.add_task(argparse.Namespace(**task))

    def reset(self, args):
        with open(self.file_name, 'w') as file:
            file.write('')
            print('You have deleted all')