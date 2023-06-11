from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from TSMain.Libraries.Misc import CheckTaskCompleted
from TSMain.models import TaskAssign, TaskItem, TaskGoal


def Index(Response):
    if Response.user.is_authenticated:
        TaskListFK = TaskAssign.objects.filter(User=Response.user)

        if Response.method == "POST":
            if "NRemoveCompleted" in Response.POST:
                CheckTaskCompleted(Response)
            Break = False
            LIndex = int(0)
            AssignList = TaskAssign.objects.filter(User=Response.user)
            LIndex = int(0)

            while (LIndex < len(AssignList)) and not("NDelete_" + AssignList[LIndex].Task.Name in Response.POST):
                LIndex += 1
            if LIndex < len(AssignList):
                TaskItem.objects.get(Name=AssignList[LIndex].Task.Name, AssignedTo=Response.user.username).delete()
        TaskListDD = [(None, None, None)] * len(TaskListFK)

        for i in range(0, len(TaskListFK), 1):
            Task = TaskListFK[i].Task
            LGoalList = TaskGoal.objects.filter(TaskRef=Task)
            TaskListDD[i] = (Task.Name, Task.Desc, LGoalList)
        return render(Response, "Index.html", {"InUser": Response.user.first_name + " " + Response.user.last_name, "TaskList": TaskListDD})
    else:
        return render(Response, "Index.html", {"InUser": ""})

def CreateTask(Response):
    if Response.method == "POST":
        if "NSubmit" in Response.POST:
            LTaskName = Response.POST["NTaskName"]
            LTaskDesc = Response.POST["NTaskDesc"]
            LGoalTitle = Response.POST["NDefGoalTitle"]
            LGoalMaxID = Response.POST["NDefGoalMaxID"]

            if not TaskItem.objects.filter(Name=LTaskName, AssignedTo=Response.user.username).exists():
                NewTask = TaskItem.objects.create(Name=LTaskName, Desc=LTaskDesc, AssignedTo=Response.user.username)
                NewTask.save()
                NewAssign = TaskAssign.objects.create(User=Response.user, Task=NewTask)
                NewAssign.save()
                NewGoal = TaskGoal.objects.create(TaskRef=NewTask, Title=LGoalTitle, CStatusID=0, EStatusID=LGoalMaxID)
                NewGoal.save()
                return redirect("/")
            else:
                return render(Response, "CreateTask.html", {"CreationResult": "ATTENZIONE: Due task non possono avere lo stesso nome"})
        elif "NBack" in Response.POST:
            return redirect("/")
    else:
        return render(Response, "CreateTask.html")

def ModifyTask(Response, TaskName):
    LDict = dict()
    LTaskRef = TaskItem.objects.get(Name=TaskName)
    LDict["DefaultTaskName"] = TaskName
    LDict["DefaultTaskDesc"] = LTaskRef.Desc

    if Response.method == "POST":
        if "NSubmit" in Response.POST:
            LTaskName = Response.POST["NTaskName"]
            LTaskDesc = Response.POST["NTaskDesc"]
            LTaskSearch = TaskItem.objects.filter(Name=LTaskName)

            if not LTaskSearch.exists() or LTaskSearch.get(Name=LTaskName) == LTaskRef:
                LTaskRef.Name = LTaskName
                LTaskRef.Desc = LTaskDesc
                LTaskRef.save()
                return redirect("/")
            else:
                LDict["UpdateResult"] = "ATTENZIONE: Esiste già una task con questo nome"
                return render(Response, "ModifyTask.html", LDict)
        elif "NBack" in Response.POST:
            return redirect("/")
    else:
        return render(Response, "ModifyTask.html", LDict)

def UpdateTask(Response, TaskName):
    LTask = TaskItem.objects.get(Name=TaskName)
    LGoalList = TaskGoal.objects.filter(TaskRef=LTask)
    LGoalDisplay = list()

    for i in range(0, len(LGoalList), 1):
        LGoalDisplay.append((LGoalList[i].Title, LGoalList[i].CStatusID, LGoalList[i].EStatusID))
    if Response.method == "POST":
        if "NSubmit" in Response.POST:
            LIndex = int(0)
            LIndexCompList = list(tuple())

            while Response.POST.get("NGoalTitle" + str(LIndex + 1), "None") != "None":
                LGoalID = Response.POST["NGoalIndex" + str(LIndex + 1)]
                LGoalMaxID = Response.POST["NGoalMaxID" + str(LIndex + 1)]
                LIndexCompList.append((LGoalID, LGoalMaxID))

                if int(LGoalID) > int(LGoalMaxID):
                    LGoalDisplay.clear()

                    for i in range(0, len(LGoalList), 1):
                        LGoalDisplay.append((LGoalList[i].Title, LGoalList[i].CStatusID, LGoalList[i].EStatusID))
                    return render(Response, "UpdateTask.html", {"GoalList": LGoalDisplay,
                                                                "UpdateResult": "ATTENZIONE: Uno o più obiettivi hanno il valore di indice attuale più grande di quello massimo"})
                elif int(LGoalID) < 0:
                    LGoalDisplay.clear()

                    for i in range(0, len(LGoalList), 1):
                        LGoalDisplay.append((LGoalList[i].Title, LGoalList[i].CStatusID, LGoalList[i].EStatusID))
                    return render(Response, "UpdateTask.html", {"GoalList": LGoalDisplay,
                                                                "UpdateResult": "ATTENZIONE: Uno o più obiettivi hanno il valore di indice negativo"})
                LIndex += 1
            LIndex = 0

            while Response.POST.get("NGoalTitle" + str(LIndex + 1), "None") != "None":
                LGoalTitle = Response.POST["NGoalTitle" + str(LIndex + 1)]
                LGoalIndex = Response.POST["NGoalIndex" + str(LIndex + 1)]
                LGoalMaxID = Response.POST["NGoalMaxID" + str(LIndex + 1)]
                LGoalList[LIndex].Title = LGoalTitle
                LGoalList[LIndex].CStatusID = LGoalIndex
                LGoalList[LIndex].EStatusID = LGoalMaxID
                LGoalList[LIndex].save()
                LIndex += 1
            return redirect("/")
        elif "NAddGoal" in Response.POST:
            LGoalID = len(TaskGoal.objects.all())
            LGoalTitle = "None"
            LGoalIndex = 0
            LGoalMaxID = 1
            LGoalDisplay.append((LGoalTitle, LGoalIndex, LGoalMaxID))
            NewGoal = TaskGoal.objects.create(GoalID=LGoalID, TaskRef=LTask, Title=LGoalTitle, CStatusID=LGoalIndex, EStatusID=LGoalMaxID)
            NewGoal.save()
            return render(Response, "UpdateTask.html", {"GoalList": LGoalDisplay})
        elif "NBack" in Response.POST:
            return redirect("/")
        else:
            LTaskRef = TaskItem.objects.get(AssignedTo=Response.user)
            LIndex = 0
            LMaxID = len(TaskGoal.objects.filter(TaskRef=LTaskRef))
            LBreak = False

            while LIndex < LMaxID and not LBreak:
                if Response.POST.get("NRemoveGoal" + str(LIndex + 1), "None"):
                    LGoalList[LIndex].delete()

                    for Value in LGoalList:
                        Value.GoalID = Value.GoalID - 1
                    LBreak = True
                else:
                    LIndex += 1
                LGoalList = TaskGoal.objects.all()
                LGoalDisplay.clear()

                for i in range(0, len(LGoalList), 1):
                    LGoalDisplay.append((LGoalList[i].Title, LGoalList[i].CStatusID, LGoalList[i].EStatusID))
            return render(Response, "UpdateTask.html", {"GoalList": LGoalDisplay})
    else:
        return render(Response, "UpdateTask.html", {"GoalList": LGoalDisplay})

def SignIn(Response):
    if Response.method == "POST":
        if "NSubmit" in Response.POST:
            Username = Response.POST["NUsername"]
            Password = Response.POST["NPassword"]
            InUser = authenticate(username=Username, password=Password)

            if InUser is not None:
                login(Response, InUser)
                return redirect("/")
            else:
                return render(Response, "SignIn.html", {"SignInResult": "Il nome utente o la password inseriti non sono corretti"})
        elif "NBack" in Response.POST:
            return redirect("/")
    else:
        return render(Response, "SignIn.html")

def SignUp(Response):
    if Response.method == "POST":
        if "NSubmit" in Response.POST:
            FirstName = Response.POST["NFirstName"]
            LastName = Response.POST["NLastName"]
            Mail = Response.POST["NMail"]
            Username = Response.POST["NUsername"]
            Password1 = Response.POST["NPassword1"]
            Password2 = Response.POST["NPassword2"]

            if Password1 == "" or Password2 == "" or FirstName == "" or LastName == "" or Username == "":
                return render(Response, "SignUp.html", {"SignUpResult": "Alcuni campi obbligatori sono vuoti"})
            else:
                if Password1 == Password2:
                    NewUser = User.objects.create(username=Username, email=Mail, password=Password1)
                    NewUser.set_password(Password1)
                    NewUser.first_name = FirstName
                    NewUser.last_name = LastName
                    NewUser.save()
                    return redirect("/")
                else:
                    return render(Response, "SignUp.html", {"SignUpResult": "<span>WARNING: Passwords must match</span>"})
        elif "NBack" in Response.POST:
            return redirect("/")
    else:
        return render(Response, "SignUp.html")

def SignOut(Response):
    logout(Response)
    return redirect("Index")

def RemoveAccount(Response):
    User.objects.get(username=Response.user.username).delete()
    return redirect("/")

def ResetPassword(Response):
    if Response.method == "POST":
        if "NReset" in Response.POST:
            Username = Response.POST["NUsername"]
            Password1 = Response.POST["NPassword1"]
            Password2 = Response.POST["NPassword2"]

            if Password1 == Password2 and not(Password1 == "" or Password2 == ""):
                TargetUser = User.objects.get(username=Username)
                TargetUser.set_password(Password1)
                TargetUser.save()
                return redirect("/")
            elif Password1 == "" or Password2 == "":
                return render(Response, "ResetPassword.html", {"ResetResult": "Warning: password cannot be empty"})
            else:
                return render(Response, "ResetPassword.html", {"ResetResult": "Warning: passwords doesn't match"})
        elif "NBack" in Response.POST:
            return redirect("/SignIn")
    else:
        return render(Response, "ResetPassword.html")