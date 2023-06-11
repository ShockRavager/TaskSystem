from django.db import models
from django.contrib.auth.models import User

class TaskItem(models.Model):
    Name = models.CharField(max_length=256)
    Desc = models.TextField(verbose_name="Description", max_length=1024)
    AssignedTo = models.CharField(verbose_name="Assignment", default="None", max_length=256)

    def __str__(self):
        return self.Name


class TaskGoal(models.Model):
    GoalID = models.IntegerField(default=0)
    TaskRef = models.ForeignKey(TaskItem, on_delete=models.CASCADE)
    Title = models.CharField(max_length=256)
    CStatusID = models.IntegerField(verbose_name="Current status ID", default=0)
    EStatusID = models.IntegerField(verbose_name="Max status ID", default=1)

    def __str__(self):
        return self.TaskRef.Name + ": " + self.Title

class TaskAssign(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Task = models.ForeignKey(TaskItem, on_delete=models.CASCADE)

    def __str__(self):
        return str("(" + self.User.first_name + " " + self.User.last_name + ", " + self.Task.Name + ")")
