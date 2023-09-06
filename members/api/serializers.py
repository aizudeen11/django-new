# turn python object to json
from rest_framework.serializers import ModelSerializer
from members.models import Member
from members.models import Comment

class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        # fields = ['firstname', 'lastname']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'comment']
