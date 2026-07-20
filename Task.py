class Task:
    def __init__(self,title,discription=None,start_date=None,end_date=None,done=False):
        self.title = title
        self.discription = discription
        self.start_date = start_date
        self.end_date = end_date
        self.done = done