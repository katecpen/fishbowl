from condition.models import condition
from condition.serializers import conditionSerializer
from rest_framework import generics


# Create your views here.
class conditionListCreate(generics.ListCreateAPIView):
    queryset = condition.objects.all()
    serializer_class = conditionSerializer