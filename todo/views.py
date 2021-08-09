import rest_framework
from rest_framework.views import APIView
from .models import Task
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render
# Create your views here.


class ToDo(APIView):
    def post(self, request):
        user_id = request.data.get('user_id',"")
        name=request.data.get('name',"")
        end_date =request.data.get('end_date',None)
        if end_date:
            end_date = datetime.strptime(end_date,'%Y-%m-%d').date()
        task = Task.objects.create(user_id=user_id, name=name, end_date=end_date)

        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append(
                dict(
                    name=task.name,
                    start_date=task.start_date,
                    end_date=task.end_date,
                    state=task.state
                )
            )
        context=dict(task_list=task_list)
        return render(request,'todo/todo.html',context=context)
    def get(self,request):
        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append(
                dict(
                    name=task.name,
                    start_date=task.start_date,
                    end_date=task.end_date,
                    state=task.state
                )
            )
        context=dict(task_list=task_list)
        return render(request,'todo/todo.html',context=context)

class TaskToggle(APIView):
    def post(self,request):
        todo_id = request.data.get('todo_id','')

        task=Task.objects.get(id=todo_id)

        if task:
            task.done =False if task.done is True else True
            task.save()
        return Response()


class TaskDelete(APIView):
    def post(self,request):
        todo_id = request.data.get('todo_id','')

        task=Task.objects.get(id=todo_id)

        if task:
            task.delete()
        return Response()


class TaskCreate(APIView):
    def post(self,request):
        user_id = request.data.get('user_id','')
        name=request.data.get('name','')
        end_date = request.data.get('end_date',None)
        todo_id=request.data.get('todo_id','')

        if end_date:
            end_date = datetime.strptime(end_date,'%Y-%m-%d').date()
        task = Task.objects.create(id=todo_id,user_id=user_id, name=name, end_date=end_date)

        return Response(
            dict(
                msg='To-Do 생성 완료',
                todo_id=task.id,
                name=task.name, 
                start_date=task.start_date.strftime('%Y-%m-%d'),
                end_date=task.end_date
            )
        )
class TaskSelect(APIView):
    def post(self, request):
        user_id = request.data.get('user_id','')
        page_number = request.data.get('page_number','')



        tasks= Task.objects.filter(user_id=user_id)
        

        is_last_page=True
        if page_number is not None and page_number>=0:
            if tasks.count()<=10:
                pass
            elif tasks.count()<=(1+page_number)*10:
                tasks = tasks[page_number*10:]
            else:
                tasks = tasks[page_number*10:(page_number+1)*10]
                is_last_page=False
        
        task_list=[]


        for task in tasks:
            task_list.append(
                dict(
                    user_id=user_id,
                    name=task.name,
                    start_date=task.start_date,
                    end_date=task.end_date,
                    state=task.state,
                    done=task.done,
                )
            )
        return Response(dict(tasks=task_list, is_last_page=is_last_page))
