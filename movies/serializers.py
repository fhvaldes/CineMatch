from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    """

    class Meta:
        """
        Meta class to specify the model and fields to be used in the serializer.
        """
        model = Movie
        fields = "__all__"