from src.data_api import Task


class Job:
    def __init__(self, task: Task, number: int):
        self.duration = task.duration
        self.weight = task.weight
        self.due_date = task.due_date
        self.number = number
        self.stays = 0

    def __str__(self):
        output = f"Job no: {self.number}\tDuration: {self.duration}\tDue: {self.due_date}\tWeight: {self.weight}"
        return output

    def __repr__(self):
        return self.__str__()
