#TaskController.py
from . import Task 
from .dateparse import parse_date
import json
import os
from datetime import date 

from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

console = Console()

class TaskController():
    def __init__(self,file_name):
        self.file_name = file_name
        self.backup_file = file_name +'.bak'
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

    def _backup(self):
        with open(self.backup_file, 'w') as dst:
            for task in self._read_tasks():
                dst.write(json.dumps(task) + '\n')

    def undo(self, args):
        if not os.path.exists(self.backup_file):
            console.print('[yellow]Nothing to undo.[/yellow]')
            return
        os.replace(self.backup_file, self.file_name)
        console.print('[green]Undid the last change :D[/green]')

    def resolve_selector(self, tasks, selector, default_last=True):
        if selector is None or selector == '':
            if default_last and tasks:
                return len(tasks)
            raise ValueError('No task specified')

        selector = str(selector).strip()
        if selector.isdigit():
            return int(selector)
        
        matches = [i for i, t in enumerate(tasks, 1) if selector.lower() in (t.get('title') or '').lower()]
        if len(matches) == 1:
            return matches[0]
        if len(matches)>1:
            titles = ', '.join(f'"{tasks[i - 1]["title"]}"' for i in matches)
            raise ValueError(f'"{selector}" Matches multiple tasks: {titles}. Use the task number insted.')
        raise ValueError(f'No task found matching "{selector}".')

    def add_task(self, args):
        start_date = parse_date(args.start_date) or date.today().isoformat()
        end_date = parse_date(args.end_date)
        task = Task.Task(
            args.title,
            args.description,
            start_date,
            end_date,
            getattr(args, 'done', False)
        )
        self._backup()
        with open(self.file_name, 'a') as file:
            file.write(json.dumps(task.to_dict())+ '\n')
        console.print(f'[green]Added task:[/green]"{task.title}"')

    def list_all_tasks(self):
        return self._read_tasks()
    
    def list_tasks(self):
        return [t for t in self._read_tasks() if not t.get('done')]
    
    def _due_display(self, start, end, done):
        if done:
            return 'done', 'dim'
        if not end:
            return 'Open', ''
        end_date = date.fromisoformat(end)
        delta= (end_date-date.today()).days
        if delta<0:
            return f'overdue {abs(delta)}d', 'bold red'
        if delta==0:
            return f'due today', 'bold yellow'
        if delta <=2:
            return f'{delta}d left', 'yellow'
        return f'{delta}d left', 'green'
    
    def print_table(self, tasks):
        table = Table(show_header=True, header_style='bold')
        table.add_column('#', justify='right')
        table.add_column('Title')
        table.add_column('Description')
        table.add_column('Start')
        table.add_column('End')
        table.add_column('Due')
        table.add_column('Done', justify='center')

        for i, task in enumerate(tasks,1):
            due_text , style = self._due_display(task.get('start_date'), task.get('end_date'), task.get('done'))
            title = task.get('title') or ''
            if task.get('done'):
                title = f'[strike]{title}[/strike]'
            table.add_row(
                str(i),
                title,
                task.get('description') or '-',
                task.get('start_date') or '-',
                task.get('end_date') or '-',
                f'[{style}]{due_text}[/{style}]' if style else due_text,
                '*' if task.get('done') else '',
            )
        console.print(table)

    def display(self, args):
        all_tasks = self.list_all_tasks()
        if not all_tasks:
            console.print('There is no tasks yet! Try: [bold]tisk add "My first task"[/bold] ,[bold]Use "tisk -h" for help![/bold]')
            return
        show_all = getattr(args, 'all', False)
        if show_all:
            self.print_table(all_tasks)
        else:
            unfinished = self.list_tasks()
            if unfinished:
                self.print_table(unfinished)
            else:
                console.print('[green]All tasks are done![/green] Run "tisk list -a" to see everything')

    def check_task(self, args):
        tasks = self.list_all_tasks()
        if not tasks:
            console.print('[yellow]There are no tasks to check.[/yellow]')
            return
        try:
            index = self.resolve_selector(tasks, args.selector, default_last=True)
            if index <= 0 or index > len(tasks):
                raise ValueError(f'Task number ({index}) does not exist!')
        except ValueError as e:
            console.print(f'[red]{e}[/red]')
            return
        self._backup()
        tasks[index-1]['done'] = True
        self._write_tasks(tasks)
        title = tasks[index - 1]['title']
        console.print(f'"{title}": [green]Marked Done[/green]')
    
    def remove_task(self, args):
        tasks = self.list_all_tasks()
        if not tasks:
            console.print('[yellow]There is no tasks to remove.[/yellow]')
            return
        try:
            index = self.resolve_selector(tasks, args.selector, default_last=True)
            if index <=0 or index > len(tasks):
                raise ValueError(f'Task number ({index}) does not exist')
        except ValueError as e:
            console.print(f'[red]{e}[/red]')
            return
        self._backup()
        removed = tasks.pop(index-1)
        self._write_tasks(tasks)
        console.print(f'[red]Removed[/red]:"{removed["title"]}"')

    def edit_task(self, args):
        tasks = self.list_all_tasks()
        if not tasks:
            console.print('[yellow]There is no tasks to edit.[/yellow]')
            return
        try:
            index = self.resolve_selector(tasks, args.selector, default_last=True)
            if index <=0 or index > len(tasks):
                raise ValueError(f'Task number ({index}) does not exist')
        except ValueError as e:
            console.print(f'[red]{e}[/red]')
            return
        
        task = tasks[index-1]
        if args.title:
            task['title'] = args.title
        if args.description:
            task['description'] = args.description
        if args.start_date:
            task['start_date'] = parse_date(args.start_date)
        if args.end_date:
            task['end_date'] = parse_date(args.end_date)
        self._backup()
        self._write_tasks(tasks)
        console.print(f'[green]Updated:[/green] "{task["title"]}"')

    def reset(self, args):
        if not Confirm.ask('Delete [bold red]ALL[/bold red] tasks?', default=False):
            console.print('Cancelled.')
            return
        self._backup()
        open(self.file_name, 'w').close()
        console.print('[green]All tasks Deleted.[/green] (Run "tisk undo" to bring them back.)')