from django.contrib import admin
from TSMain.models import *

class TaskItemAdmin(admin.ModelAdmin):
    model = TaskItem
    list_display = [
        "Name",
        "Desc",
        "AssignedTo"
    ]

class TaskAssignAdmin(admin.ModelAdmin):
    model = TaskAssign
    list_display = [
        "User",
        "Task"
    ]

class TaskGoalAdmin(admin.ModelAdmin):
    model = TaskGoal
    list_display = [
        "GoalID",
        "TaskRef",
        "Title",
        "CStatusID",
        "EStatusID"
    ]

admin.site.register(TaskItem, TaskItemAdmin)
admin.site.register(TaskAssign, TaskAssignAdmin)
admin.site.register(TaskGoal, TaskGoalAdmin)
