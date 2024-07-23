from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Todo
from django.utils.dateparse import parse_date  # 문자열을 날짜 객체로 변환
from django.contrib.auth import get_user_model
import json
from django.views.decorators.csrf import csrf_exempt # post 테스트를 위한 import
class TodoView(View):
    #post test를 위한 임시 함수 실제 배포시 삭제해야함
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, todo_id=None, user_id=None):
        if todo_id:
            return self.get_todo_detail(request, todo_id)
        elif 'completion_percentage' in request.path:
            return self.get_completion_percentage(request, user_id)
        else:
            return self.get_todo_list(request)

    def get_todo_detail(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        return JsonResponse(
            {
                "id": todo.id,
                "user_id": todo.user_id.id,
                "task": todo.task,
                "is_done": todo.is_done,
                "date": todo.date,
            },
            status=200,
        )

    def get_todo_list(self, request):
        todos = Todo.objects.all()
        todo_list = [
            {
                "id": todo.id,
                "user_id": todo.user_id.id,
                "task": todo.task,
                "is_done": todo.is_done,
                "date": todo.date,
            }
            for todo in todos
        ]
        return JsonResponse({"todos": todo_list}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            user = get_object_or_404(
                get_user_model(), id=data["user_id"]
            )
            todo = Todo.objects.create(
                user_id=user,
                task=data["task"],
                is_done=data.get("is_done", False),
                date=parse_date(data["date"]),
            )
            return JsonResponse(
                {
                    "id": todo.id,
                    "user_id": todo.user_id.id,
                    "task": todo.task,
                    "is_done": todo.is_done,
                    "date": todo.date,
                },
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, todo_id):
        try:
            data = json.loads(request.body)
            todo = get_object_or_404(Todo, id=todo_id)
            todo.task = data.get("task", todo.task)
            todo.is_done = data.get("is_done", todo.is_done)
            todo.date = parse_date(data["date"]) if "date" in data else todo.date
            todo.save()
            return JsonResponse(
                {
                    "id": todo.id,
                    "user_id": todo.user_id.id,
                    "task": todo.task,
                    "is_done": todo.is_done,
                    "date": todo.date,
                },
                status=200,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, todo_id):
        try:
            todo = get_object_or_404(Todo, id=todo_id)
            todo.delete()
            return JsonResponse({"message": "Todo deleted"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get_completion_percentage(self, request, user_id=None):
        if user_id:
            todos = Todo.objects.filter(user_id=user_id)
        else:
            todos = Todo.objects.all()

        total_tasks = todos.count()
        completed_tasks = todos.filter(is_done=True).count()
        completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        return JsonResponse(
            {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_percentage": completion_percentage,
            },
            status=200,
        )

