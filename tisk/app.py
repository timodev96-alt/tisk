#app.py
import argparse
import os
import sys
from . import TaskController

def main():
    tasks_file = os.path.join(os.path.expanduser('~'), 'tasks.txt')
    controller = TaskController.TaskController(tasks_file)

    parser = argparse.ArgumentParser(prog='tisk', description='Simple Task manager')
    subparsers = parser.add_subparsers(dest='command')
    
    add_task = subparsers.add_parser('add', aliases=['a'], help='Add Task')
    add_task.add_argument('title', help='Title of the task', type=str)
    add_task.add_argument('-d', '--description', help='Short description', type=str, default=None)
    add_task.add_argument('-s', '--start_date', help='Start Date: (YYYY-MM-DD), "today", "3d", etc.', type=str, default=None)
    add_task.add_argument('-e', '--end_date', help='Due Date: (YYYY-MM-DD), "tomorrow", "in 2 weeks", etc.', type=str, default=None)
    add_task.add_argument('-dn', '--done', help='Mark The Task as done', action='store_true')
    add_task.set_defaults(func = controller.add_task)

    list_tasks = subparsers.add_parser('list', aliases=['ls','l'], help='List of unfinished tasks')
    list_tasks.add_argument('-a', '--all', help='List All tasks', action='store_true')
    list_tasks.set_defaults(func = controller.display)

    check_task = subparsers.add_parser('check', aliases=['c','done'], help='Mark a task as done')
    check_task.add_argument('selector', nargs='?', default=None, help='Task Number or a word from its title.')
    check_task.set_defaults(func = controller.check_task)

    remove_task = subparsers.add_parser('remove', aliases=['rm','del'], help='Remove a task')
    remove_task.add_argument('selector', nargs='?', default=None, help='Task Number or a word from its title.')
    remove_task.set_defaults(func = controller.remove_task)

    edit_task = subparsers.add_parser('edit', aliases=['e'], help='Edit an existing task')
    edit_task.add_argument('selector', help='Task number or a word from its title')
    edit_task.add_argument('-t', '--title', type=str, default=None)
    edit_task.add_argument('-d', '--description', type=str, default=None)
    edit_task.add_argument('-s', '--start_date', type=str, default=None)
    edit_task.add_argument('-e', '--end_date', type=str, default=None)
    edit_task.set_defaults(func=controller.edit_task)

    undo = subparsers.add_parser('undo', aliases=['u'], help='Undo the last change')
    undo.set_defaults(func=controller.undo)

    reset = subparsers.add_parser('reset',aliases=['clear'], help='Renove all tasks')
    reset.set_defaults(func = controller.reset)

    if len(sys.argv) == 1:
        controller.display(argparse.Namespace(all=False))
        return

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        
if __name__ == '__main__':
    main()