from rest_framework import serializers
from projects.models import Project,Tag, Review
from users.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields='__all__'

class ProjectSerializer(serializers.ModelSerializer):
    #nested serializers
    owner=ProfileSerializer(many=False)
    tags=TagSerializer(many=True)
    # reviews set not in Project model
    # add reviews for project using methodfield
    reviews=serializers.SerializerMethodField()

    class Meta:
        model=Project
        fields='__all__'

    # method should start with get_ to use serializer method field
    def get_reviews(self,obj):
        reviews=obj.review_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return serializer.data