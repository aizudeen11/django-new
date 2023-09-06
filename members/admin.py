from django.contrib import admin
from .models import Member
from .models import Comment

class MemberAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "anonymous", "created")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "comment")
  
admin.site.register(Member, MemberAdmin)
admin.site.register(Comment, CommentAdmin)