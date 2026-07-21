import Task
import tabulate
from datetime import date 

class TaskController():
    def __init__(self,file_name):
        self.file_name = file_name

    def add_task(self, args):
        if not args.start_date:
            now = date.today().isoformat()
            args.start_date = now
        task = Task(args.title, args.discription, args.start_date, args.end_date, args.done)
            
        with open(self.file_name, 'a') as file:
            file.write(str(task) + '\n')

    def list_tasks(self):
        unfinished_tasks = []
        with open(self.file_name, 'r') as file:
            for line in file:
                title, description, start_date, end_date, done = line.split(', ')
                end_date = None if end_date == 'None' else end_date
                done = False if done.strip('\n') == 'Fakse' else True
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
            if task['start_date'] and task['end_date']:
                self.due_date = self.due_date(task['start_date'], task['end_date'])
            else:
                due_date = 'Open'
                formatted_tasks.append({'no.':number, **task, 'due_date':due_date})
        print(tabulate(formatted_tasks, headers= 'keys'))