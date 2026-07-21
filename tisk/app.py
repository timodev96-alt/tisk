#app.py
import argparse
import os
from . import TaskController

def main():
    tasks_file = os.path.join(os.path.expanduser('~'), 'tasks.txt')
    controller = TaskController.TaskController(tasks_file)

    parser = argparse.ArgumentParser(prog='tisk', description='Simple Task manager')
    subparsers = parser.add_subparsers()
    
    add_task = subparsers.add_parser('add', help='Add Task')
    add_task.add_argument('title', help='Title of the task', type=str)
    add_task.add_argument('-d', '--description', help='Short description of the task', type=str, default=None)
    add_task.add_argument('-s', '--start_date', help='Date to begin the task (YYYY-MM-DD)', type=str, default=None)
    add_task.add_argument('-e', '--end_date', help='Date to end the task (YYYY-MM-DD)', type=str, default=None)
    add_task.add_argument('-dn', '--done', help='Mark The Task as done', type=str, default=False)
    add_task.set_defaults(func = controller.add_task)

    list_tasks = subparsers.add_parser('list', help='List of unfinished tasks')
    list_tasks.add_argument('-a', '--all', help='List All tasks', action='store_true')
    list_tasks.set_defaults(func = controller.display)

    check_task = subparsers.add_parser('check', help='Mark a task as done')
    check_task.add_argument('-t', '--task', help='Number of task to mark done (default: last task)', type=int)
    check_task.set_defaults(func = controller.check_task)

    remove_task = subparsers.add_parser('remove', help='Remove a task')
    remove_task.add_argument('-t', '--task', help='Number of task to remove, (default: last task)',type=int)
    remove_task.set_defaults(func = controller.remove_task)

    reset = subparsers.add_parser('reset', help='Renove all tasks')
    reset.set_defaults(func = controller.reset)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
if __name__ == '__main__':
    main()