from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Todo
from django.utils.dateparse import parse_date #문자열을 날짜객체로
from django.contrib.auth import get_user_model 
import json

class TodoView(View):
    def get(self, request, todo_id=None):
        if todo_id:
            todo = get_object_or_404(Todo, id=todo_id)
            return JsonResponse({
                'id': todo.id,
                'user_id': todo.user_id.id,
                'task': todo.task,
                'is_done': todo.is_done,
                'date': todo.date
            }, status=200)
        else:
            todos = Todo.objects.all()
            todo_list = [{
                'id': todo.id,
                'user_id': todo.user_id.id,
                'task': todo.task,
                'is_done': todo.is_done,
                'date': todo.date
            } for todo in todos]
            return JsonResponse({'todos': todo_list}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            user = get_object_or_404(get_user_model(), id=data['user_id'])  # 커스텀 유저 모델을 참조
            todo = Todo.objects.create(
                user_id=user,
                task=data['task'],
                is_done=data.get('is_done', False),
                date=parse_date(data['date'])
            )
            return JsonResponse({
                'id': todo.id,
                'user_id': todo.user_id.id,
                'task': todo.task,
                'is_done': todo.is_done,
                'date': todo.date
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, todo_id):
        try:
            data = json.loads(request.body)
            todo = get_object_or_404(Todo, id=todo_id)
            todo.task = data.get('task', todo.task)
            todo.is_done = data.get('is_done', todo.is_done)
            todo.date = parse_date(data['date']) if 'date' in data else todo.date
            todo.save()
            return JsonResponse({
                'id': todo.id,
                'user_id': todo.user_id.id,
                'task': todo.task,
                'is_done': todo.is_done,
                'date': todo.date
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, todo_id):
        try:
            todo = get_object_or_404(Todo, id=todo_id)
            todo.delete()
            return JsonResponse({'message': 'Todo deleted'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
