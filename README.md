# Tisk
###### The coolest CLI task manager because I made it :D

## Installation
```
pip install tisk
```

## How to use
### Add a task
```
tisk add Do_Laundry -d "Only the red T-shirt" -e "tomorrow"
```
note: everyting in a task is optional exept the title!

### List tasks
`tisk` -->  Quick access to unfinished tasks
`tisk list`  --> List Unfinished tasks
`tisk list -a` --> List all tasks

### Mark a task as done
`tisk done 1` --> By task Number
`tisk done Laundry` --> By searching task title

## Edit a task
```
tisk edit 1 -t "New Title" -d "New description" -e "New End date"
```

### Remove a task
```
tisk remove 1
```

### Undo last action
```bash
tisk undo
```