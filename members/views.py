from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Member, Sentimen
from .models import Comment
from django.shortcuts import render, redirect
from .forms import MemberForm, MemberSentimen
from .forms import MemberComment
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
import requests as r
import datetime as dt
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def api(request):
    return render(request, 'api.html')

def test(request):
    
    if request.method == 'POST':
        user_input = request.POST['test']
        print(user_input)
        print(request.POST)
    
    return render(request, 'test.html')

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error(request, "user does not exist")
        user = authenticate(request, username= username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username or password does not exist")
    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            #  user who just registered will be log in
            return redirect('home')
        else:
            messages.error(request, 'An error happened during registration')
    context = {'form': form}
    return render(request, 'login_register.html', context)

def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))

def about(request):
    return render(request, 'about.html')

def details(request, id):
    mymember = Member.objects.get(id=id)
    if request.method == 'POST':
        mymember.delete()
        return redirect('members')
    template = loader.get_template('details.html')
    context = {'mymember': mymember,}
    return HttpResponse(template.render(context, request))

def portfolio(request):
    mymembers = Member.objects.all().values()
    context = {
        'mymembers': mymembers,
    }
    template = loader.get_template('main.html')
    return HttpResponse(template.render(context, request))

def home(request):
    try:
        api_key = 'd242f826443de65584d2d0a8ee695543'
        location = 'sungai besar'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'
        data = r.get(url).json()
        kelvin = data['main']['temp']
        celcius = kelvin - 273.15
        celcius0 = round(celcius,2)
        weather_discription = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        URL_icon = f'https://openweathermap.org/img/wn/{icon}@2x.png'
        country_code = data['sys']['country']
        location_name = data['name']
        sun_rise = dt.datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
        sun_set = dt.datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])
        date = dt.date.today().strftime("%d %b %Y")
        content1 = {
            'celcius' : celcius0,
            'weather_discription' : weather_discription,
            'country_code' : country_code,
            'location_name' : location_name, 
            'sun_rise' : sun_rise,
            'sun_set' : sun_set,
            'URL_icon' : URL_icon,
            'date': date
        }
    except:
        content1 = {
            'celcius' : 'NA',
            'weather_discription' : 'NA',
            'country_code' : 'NA',
            'location_name' : 'NA', 
            'sun_rise' : 'NA',
            'sun_set' : 'NA',
            'URL_icon' : 'NA',
            'date': 'NA'
        }
    try:
        token0 = 'xMHZezkhi6Bf4TrhixYtOZjvNcsycPxeGBm77lxd'
        url = f'https://api.nasa.gov/planetary/apod?api_key={token0}'
        data = r.get(url).json()
        title_nasa = data['title']
        url_nasa = data['url']
        date_nasa = data['date']
        info = data['explanation']
        content2 = {
            'title_nasa': title_nasa,
            'date_nasa' : date_nasa,
            'info_nasa' : info,
            'url_nasa' : url_nasa
        }
    except:
        content2 = {
            'title_nasa': 'NA',
            'date_nasa' : 'NA',
            'info_nasa' : 'NA',
            'url_nasa' : 'NA'
        }
    try:
        token = "zjNUF4abiX0eUwDn1Kl9GCKGNB50sWc4KcfJxHMO"
        url = f"https://api.marketaux.com/v1/news/all?symbols=TSLA,AMZN,MSFT&filter_entities=true&language=en&api_token={token}"
        data = r.get(url).json()
        title = data['data'][0]["title"]
        snippet = data['data'][0]["snippet"]
        snippet = ''.join(snippet.splitlines())
        url0 = data['data'][0]["url"]
        content3 = {
            'title' : title,
            'snippet' : snippet,
            'url0' : url0
        }
    except:
        content3 = {
            'title' : 'Sorry, unable to show daily economic news since this webpage already use all the api count for this month',
            'snippet' : 'Please try again later',
            'url0' : '/example'
        } 
    context = content1 | content2 | content3  

    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

def rate(request):
    form = MemberForm()
    
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('members')
    context = {'form' : form}
    return render(request, 'form.html', context)

def edit(request, id):
    if request.user.is_superuser:
        mymember = Member.objects.get(id=id)
        form = MemberForm(instance=mymember)
        if request.method == 'POST':
            form = MemberForm(request.POST, instance=mymember)
            if form.is_valid():
                form.save()
                return redirect('members')
        context = {'form' : form}
        return render(request, 'form.html', context)
    else:
        return render(request, 'admin access.html')

def delete(request, id):
    if request.user.is_superuser:
        member = Member.objects.get(id=id)
        if request.method == 'POST':
            member.delete()
            return redirect('members')
        context = {'obj': member}
        return render(request, 'delete.html', context)
    else:
        return render(request, 'admin access.html')
    
def analysis(request):
    return render(request, 'analysis main.html')

def project1(request):
    comment = Comment.objects.all().values()
    form = MemberComment()
    if request.method == 'POST':
        form = MemberComment(request.POST)
        if form.is_valid():
            form.save()
            return redirect('analysis1')
    context = {
        'comment' : comment,
        'form' : form       
    }
    return render(request, 'project 1.html', context)

def project2(request):
    mymembers = Member.objects.all().values()
    comment = Comment.objects.all().values()
    form = MemberComment()
    if request.method == 'POST':
        form = MemberComment(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('analysis2')
    context = {
        'comment' : comment,
        'form' : form,
        'mymembers' : mymembers,       
    }
    return render(request, 'project 2.html', context)

def project3(request):
    return render(request, 'project 3.html')

def project4(request):  
    sentimen = Sentimen.objects.all().values() 
    form = MemberSentimen()
    if request.method == 'POST':
        user_input = request.POST['comment']
        nlp = sia.polarity_scores(user_input)

        csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']
        comment = request.POST['comment']
        result1 = {
            'csrfmiddlewaretoken' : csrfmiddlewaretoken,
            'comment' : comment,
        }
        result2 = result1 | nlp
        form = MemberSentimen(result2)
        if form.is_valid():
            form.save()
            return redirect('analysis4')
    context = {
        'sentimen' : sentimen,
        'form' : form     
    }
    return  render(request, 'project 4.html', context)


