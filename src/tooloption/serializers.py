# from typing_extensions import Required
from rest_framework import serializers
from .models import DomElement


class DomElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomElement
        exclude = ('UpdatedDate','created_at','slug','is_active','Entered_By',)
