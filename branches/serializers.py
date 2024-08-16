from rest_framework import serializers
from .models import Branch, BranchImage


class BranchImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchImage
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    images = BranchImageSerializer(many=True, read_only=True, source='branchimage_set')

    class Meta:
        model = Branch
        fields = '__all__'


