from rest_framework.response import Response
from rest_framework.views import APIView

from viscosimeters.models import ViscosimeterType
from . import serializers

class ViscosimeterTypeListCreateApiView(APIView):
    def get(self, request):
        objects = ViscosimeterType.objects.all()
        return Response(serializers.note_to_json(obj) for obj in objects)

    def post(self, request):
        pass


