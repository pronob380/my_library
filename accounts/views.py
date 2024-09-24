from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from user.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests 
from isodate import parse_duration







def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_view')
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login/login.html', {'error_message': error_message})
    else:
        return render(request, 'login/login.html')
    

def logout_view(request):
    logout(request)
    return redirect('login_view')






from django.contrib.auth.hashers import make_password
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name', '')
        roll = request.POST.get('roll', '0')
        department = request.POST.get('department', '')
        session = request.POST.get('session', '')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        
        # Handle image file
        image = request.FILES.get('image')
        
        # Handle password
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Basic validation
        if password != password_confirm:
            return render(request, 'login/registration.html', {
                'error': 'Passwords do not match'
            })
        
        if not email:
            return render(request, 'login/registration.html', {
                'error': 'Email is required'
            })
        
        if User.objects.filter(email=email).exists():
            return render(request, 'login/registration.html', {
                'error': 'Email is already taken'
            })
        
        user = User(
            email=email,
            name=name,
            roll=roll,
            department=department,
            session=session,
            phone_number=phone_number,
            address=address,
            user_type='MEM',  
            is_active=False,  
            is_admin=False,  
            image=image
        )
        
        user.password = make_password(password)
        user.save()
        
        messages.success(request, 'Your registration is done. Please wait for admin approval.')
        return redirect('login_view')  
    
    return render(request, 'login/registration.html')

def forgot_password_view(request):
    return render(request, 'login/forgotpassword.html')


















def youtube_search(request):
    videos =[]
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key': settings.YOUTUBE_API_KEY,
            'maxResults' : 12,
            'type' : 'video',

        }

        videos_ids=[]    
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        for result in results:
            videos_ids.append(result['id']['videoId'])

        video_params ={
            'key': settings.YOUTUBE_API_KEY,
            'part' : 'snippet, contentDetails',
            'id' : ','.join(videos_ids),
            'maxResults' : 12,
        }
        r = requests.get(video_url, params = video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'thumbnail': result['snippet']["thumbnails"]['high']['url'],
                'duration': int(parse_duration(result['contentDetails']["duration"]).total_seconds()//60),
            }

            videos.append(video_data)

    context = {
        'videos': videos
    }
         
    return render(request, 'youtube/youtube.html', context )



def search_wikipedia(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "utf8": 1,
            "srlimit": 12,  
        }
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get('query', {}).get('search', [])

    return render(request, 'wikipedia/wikipedia.html', {'results': results, 'query': query})