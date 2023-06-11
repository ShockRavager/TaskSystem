from TSMain.models import TaskItem, TaskAssign, TaskGoal

def CheckTaskCompleted(Response):
    LAssignList = TaskAssign.objects.filter(User=Response.user)

    for TaskValue in LAssignList:
        LGoalList = TaskGoal.objects.filter(TaskRef=TaskValue.Task)
        LIndex = int(0)

        for GoalValue in LGoalList:
            if GoalValue.EStatusID == GoalValue.CStatusID:
                LIndex += 1
        if LIndex == len(LGoalList):
            TaskItem.objects.get(Name=TaskValue.Task.Name).delete()