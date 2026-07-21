#TaskController.py
from . import Task 
import tabulate
import json
import os
from datetime import date 

class TaskController():
    def __init__(self,file_name):
        self.file_name = file_name
        if not os.path.exists(self.file_name):
            open(self.file_name, 'a').close()

    def _read_tasks(self):
        tasks = []
        with open(self.file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                tasks.append(json.loads(line))
        return tasks
    
    def _write_tasks(self, tasks):
        with open(self.file_name, 'w') as file:
            for task in tasks:
                file.write(json.dumps(task)+'\n')

    def add_task(self, args):
        start_date = args.start_date or date.today().isoformat()
        task = Task.Task(
            args.title,
            args.description,
            start_date,
            args.end_date,
            getattr(args, 'done', False)
        )
        with open(self.file_name, 'a') as file:
            file.write(json.dumps(task.to_dict())+ '\n')
        print(f'Added task: "{task.title}"')

    def list_all_tasks(self):
        return self._read_tasks()
    
    def list_tasks(self):
        return [t for t in self._read_tasks() if not t.get('done')]
    
    def due_date(self, start, end):
        if not start or not end:
            return 'Open'
        end_date = date.fromisoformat(end)
        delta = (end_date - date.today()).days
        if delta < 0:
            return f'Overdue by {abs(delta)}d'
        elif delta == 0:
            return 'Due today'
        return f'{delta}d left'
    
    def print_table(self, tasks):
        formatted_tasks = []
        for number, task in enumerate(tasks, 1):
            formatted_tasks.append({
                'no.':number,
                'title': task.get('title'),
                'description': task.get('description') or '',
                'start_date': task.get('start_date'),
                'end_date':task.get('end_date') or '-',
                'done':'Yes' if task.get('done') else 'No',
                'due_date': self.due_date(task.get('start_date'), task.get('end_date')),
            })

        print(tabulate.tabulate(formatted_tasks, headers= 'keys'))

    def display(self, args):
        all_tasks = self.list_all_tasks()
        if not all_tasks:
            print('There is no tasks yet! Use "tisk add <title> to add a task"')
            return
        if args.all:
            self.print_table(all_tasks)
        else:
            unfinished_tasks = self.list_tasks()
            if unfinished_tasks:
                self.print_table(unfinished_tasks)
            else:
                print('All tasks are Done!')

    def check_task(self, args):
        tasks = self.list_all_tasks
        if not tasks:
            print('There are no tasks to check.')
            return
        index = args.task if args.task else len(tasks)
        if index <= 0 or index > len(tasks):
            print(f'Task number ({index}) does not exist!')
            return
        tasks[index-1]['done'] = True
        self._write_tasks(tasks)
        print(f'Marked task {index} ("{tasks[index-1]["title"]}") as done.')
    
    def remove_task(self, args):
        tasks = self.list_all_tasks()
        if not tasks:
            print('There is no tasks to remove.')
            return
        index = args.task if args.task else len(tasks)
        if index <= 0 or index > len(tasks):
            print(f'Task Number ({index}) does not exist!')
            return
        removed = tasks.pop(index-1)
        self._write_tasks(tasks)
        print(f'Removed task {index} ("{"title"}").')

    def reset(self, args):
        confirm = input('Are you sure you want to delete ALL Tasks? [y/n]:')
        if confirm.strip().lower() != 'y':
            print('Cancelled.')
            return
        open(self.file_name, 'w').close()
        print('All tasks deleted.')