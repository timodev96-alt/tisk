import argparse

def main():
    parser = argparse.ArgumentParser(description='Simple Task manager')
    subparsers = parser.add_subparsers()
    add_task = subparsers.add_parser('add', help='Add Task')
    add_task.add_argument('title', help='Title of the task', type=str)
    add_task.add_argument('-d', '--description', help='Short description of the task', type=str, default=None)
    add_task.add_argument('-s', '--start_date', help='Date to begin the task', type=str, default=None)
    add_task.add_argument('-e', '--end_date', help='Date to end the task', type=str, default=None)
    add_task.add_argument('-dn', '--done', help='Check if the task is done', type=str, default=False)

    list_tasks = subparsers.add_parser('list', help='List of unfinished tasks')
    list_tasks.add_argument('-a', '--all', help='List All tasks', action='store_true')

    check_task = subparsers.add_parser('check', help='Check the given task')
    check_task.add_argument('-t', '--task', help='Number of task to mark done, if not specified, last task will be marked Done', type=int)

    remove_task = subparsers.add_parser('remove', help='Remove a task')
    remove_task.add_argument('-a', '--all', help='List All tasks', action='store_true')

    reset = subparsers.add_parser('reset', help='Renove all tasks')

    args = parser.parse_args()
    
if __name__ == '__main__':
    main()