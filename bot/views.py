from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from aiogram import types
from loader import dp


class UpdadeBot(APIView):
    def post(self,request):
        json_string = request.body.decode('UTF-8')
        update = types.Update.as_json(json_string)
        dp.process_updates(update)
        return Response({'code':200})