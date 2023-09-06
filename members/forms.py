from django.forms import ModelForm
from .models import Member
from .models import Comment, Sentimen

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        # fields = ['firstname', 'lastname']
class MemberComment(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

class MemberSentimen(ModelForm):
    class Meta:
        model = Sentimen
        fields = '__all__'