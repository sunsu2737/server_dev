from .models import Task
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render
from common.common import TodoView,SuccessResponse,SuccessResponseWithData,ErrorResponse,CommonResponse
# Create your views here.
import logging

logger=logging.getLogger('django')

class ToDo(TodoView):
    def post(self, request):

        name=request.data.get('name',"")
        end_date =request.data.get('end_date',None)
        if end_date:
            end_date = datetime.strptime(end_date,'%Y-%m-%d').date()
        task = Task.objects.create(user_id=self.user_id, name=name, end_date=end_date)

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

class TaskToggle(TodoView):
    def post(self,request):
        logger.info('Task Toggle Start!!')
        todo_id = request.data.get('todo_id','')
        logger.info('input data'+str(todo_id))
        task=Task.objects.get(id=todo_id)

        if task:
            task.done =False if task.done is True else True
            task.save()
        return Response()


class TaskDelete(TodoView):
    def post(self,request):
        logger.info('Task Delete Start!!')

        todo_id = request.data.get('todo_id','')
        logger.info('input data'+str(todo_id))

        task=Task.objects.get(id=todo_id)

        if task:
            task.delete()
        return Response()


class TaskCreate(TodoView):
    def post(self,request):
        logger.info('Task Create Start!!')


        name=request.data.get('name','')
        end_date = request.data.get('end_date',None)
        todo_id=request.data.get('todo_id','')

        logger.info('input data'+name,str(end_date)+str(todo_id)+str(self.user_id))

        if end_date:
            end_date = datetime.strptime(end_date,'%Y-%m-%d').date()
        task = Task.objects.create(id=todo_id,user_id=self.user_id, name=name, end_date=end_date)

        logger.info('Create'+str(task))
        return SuccessResponseWithData(dict(id=task.id))
class TaskSelect(TodoView):
    def post(self, request):
        logger.info('Task Create Start!!')
        page_number = request.data.get('page_number',5)



        logger.info('input data'+str(self.user_id)+str(page_number))
        tasks= Task.objects.filter(user_id=self.user_id)
        

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
                    user_id=self.user_id,
                    name=task.name,
                    start_date=task.start_date,
                    end_date=task.end_date,
                    state=task.state,
                    done=task.done,
                )
            )
        logger.info('Select'+str(task_list))
        if self.version=='1.1':
            return SuccessResponseWithData(dict(tasks=task_list, is_last_page=is_last_page))
        else:
            return Response(dict(tasks=task_list, is_last_page=is_last_page))