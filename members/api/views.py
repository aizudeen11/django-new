from rest_framework.decorators import api_view
from rest_framework.response import Response
from members.models import Member
from members.models import Comment
from .serializers import MemberSerializer
from .serializers import CommentSerializer
# user can only get data
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/members',
        'GET /api/comment'
    ]
    return Response(routes)
# @ is a decoretor django rest framework
@api_view(['GET'])
def getMembers(request):
    mymembers = Member.objects.all()
    # many mean serialize many object
    serializer = MemberSerializer(mymembers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getComment(request):
    comment = Comment.objects.all()
    # many mean serialize many object
    serializer = CommentSerializer(comment, many=True)
    return Response(serializer.data)