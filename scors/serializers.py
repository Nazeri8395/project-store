from rest_framework import serializers
from .models import Score

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ["product", "user", "score", "register_date"]
        read_only_fields = ["user", "register_date"]
