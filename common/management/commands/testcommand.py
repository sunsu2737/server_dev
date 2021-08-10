from django.core.management.base import BaseCommand
from todo.models import Task
from datetime import datetime

class Command(BaseCommand):

    def handle(self,*args,**options):
        task_list = Task.objects.all()

        for task in task_list:
            if task.end_date < datetime.now.date():
                task.state = 3
                task.save()
                print(task.id,task.name,'만료되었습니다.',task.end_date)