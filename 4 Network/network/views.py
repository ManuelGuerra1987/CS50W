from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Tweet
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def index(request):
    tweets = Tweet.objects.all().order_by('-timestamp')
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    tweets_page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        tweets_liked = request.user.liked_tweets.all()

    else:
        tweets_liked = []    


    return render(request, "network/index.html", {'tweets': tweets_page, 'tweets_liked': tweets_liked})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    



@login_required
def create(request):

    if request.method == "POST":

        new_post = Tweet(
            content=request.POST.get('content'),
            owner=request.user   
        )
        new_post.save()

        return  HttpResponseRedirect(reverse('index'))
    

def profile(request, name):

    if request.method == "GET":   
        user_profile = get_object_or_404(User, username=name)

        followers = user_profile.followers.all()
        following = user_profile.following.all()

        if request.user == user_profile:
            same_user = True
        else:
            same_user = False    

        if user_profile in request.user.following.all():
            is_following = True
        else:
            is_following = False

        return render(request, "network/profile.html",{
            "followers": followers, 
            "following": following, 
            "is_following": is_following, 
            "same_user": same_user, 
            "profile_owner": user_profile, 
            "tweets": Tweet.objects.filter(owner=user_profile).order_by('-timestamp')
            }) 
    

@login_required    
def follow(request):
    if request.method == "POST":
        user_follows_id = request.POST.get("user_follows")
        user_follows = get_object_or_404(User, id=int(user_follows_id))
        user_followed_id = request.POST.get("user_followed")
        user_followed = get_object_or_404(User, id=int(user_followed_id))

        user_follows.following.add(user_followed)
        
        return HttpResponseRedirect(reverse("profile", kwargs={'name': user_followed.username}))     
    

@login_required    
def unfollow(request):
    if request.method == "POST":
        user_unfollows_id = request.POST.get("user_unfollows")
        user_unfollows = get_object_or_404(User, id=int(user_unfollows_id))
        user_unfollowed_id = request.POST.get("user_unfollowed")
        user_unfollowed = get_object_or_404(User, id=int(user_unfollowed_id))

        user_unfollows.following.remove(user_unfollowed)
        
        return HttpResponseRedirect(reverse("profile", kwargs={'name': user_unfollowed.username}))      
    


@login_required    
def following(request):

    lista_following = request.user.following.all()
    lista_following_usernames = []

    for user_ in lista_following:
        lista_following_usernames.append(user_.username)

    lista_all_tweets = Tweet.objects.all().order_by('-timestamp')
    lista_tweets_following = [] 

    for tweet_ in lista_all_tweets:
        if tweet_.owner.username in lista_following_usernames:
            lista_tweets_following.append(tweet_)


   
    paginator = Paginator(lista_tweets_following, 10)
    page_number = request.GET.get('page')
    tweets_page = paginator.get_page(page_number)
  
    return render(request, "network/following.html", {"tweets": tweets_page})


@csrf_exempt
@login_required
def edit(request, tweet_id):


    if request.method == "PUT":

        tweet = Tweet.objects.get(pk=tweet_id)

        data = json.loads(request.body)
        if data.get("content") is not None:
            tweet.content = data["content"]

        tweet.save()
        content = tweet.content
        return JsonResponse({'content': content}, status=200)  
    

@csrf_exempt
@login_required
def like(request, tweet_id):


    if request.method == "PUT":

        tweet = Tweet.objects.get(pk=tweet_id)
        user = request.user

        if user in tweet.users_liked.all():
            tweet.users_liked.remove(user)
        else:
            tweet.users_liked.add(user)    

        tweet.save()

        likes_count = tweet.users_liked.count()
        return JsonResponse({'likes': likes_count}, status=200)  
    
  
