#Task.py
class Task:
    def __init__(self,title,description=None,start_date=None,end_date=None,done=False):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.done = done

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'done': self.done,
        }

    @classmethod
    def from_dict(cls,data):
        return cls(
            data.get('title'),
            data.get('description'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('done', False),
        )

    def __str__(self):
        return f'{self.title}, {self.description}, {self.start_date}, {self.end_date}, {self.done}'
    