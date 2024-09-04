from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Listing,Bid,Comment



def index(request):
    return render(request, "auctions/active.html", {"auctions": Listing.objects.filter(is_open=True)})

def closed_listings(request):
    return render(request, "auctions/closed.html", {"auctions": Listing.objects.filter(is_open=False)})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    


@login_required
def create(request):

    if request.method == "GET":
        categories = ["Books","Electronics","Fashion","Home","Music","Toys"]
        return render(request, "auctions/create.html",{"categories": categories }) 
    
    if request.method == "POST":

        new_listing = Listing(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            starting_price=request.POST.get('starting_price'),
            current_price = request.POST.get('starting_price'),
            url_image=request.POST.get('url_image'),
            category=request.POST.get('category') if request.POST.get('category') else None,
            owner=request.user,  
            is_open=True
            
        )
        new_listing.save()

        return  HttpResponseRedirect(reverse('index'))
    
def show_page(request, title):

    if request.method == "GET":

        listing = Listing.objects.get(title=title)

        if request.user.is_authenticated:

            
            if listing in request.user.watchlist.all():
                is_in_watchlist = True
            else:
                is_in_watchlist = False

            if request.user == listing.owner:
                is_owner = True 
            else:
                is_owner = False        

            if request.user == listing.current_winner:
                is_winner = True 
            else:
                is_winner = False      

        else:
            is_in_watchlist = False 
            is_owner = False   
            is_winner = False               

        return render(request, "auctions/page.html", {
            "auction": listing, 
            "is_in_watchlist": is_in_watchlist,
            "is_owner": is_owner,
            "is_winner": is_winner,
            "comments": Comment.objects.filter(listing=listing)
            })   

@login_required
def add_watch(request):
    if request.method == "POST":
        title = request.POST.get("title")
        listing = Listing.objects.get(title=title)
        
        user = request.user
        user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("page", kwargs={'title': title}))
    
@login_required    
def remove_watch(request):
    if request.method == "POST":
        title = request.POST.get("title")
        listing = Listing.objects.get(title=title)
        
        user = request.user
        user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("page", kwargs={'title': title}))    
    
@login_required
def view_watch(request):
    return render(request, "auctions/view_watch.html", {"auctions": request.user.watchlist.all() }) 


@login_required
def bid(request):
    if request.method == "POST":
        title = request.POST.get("title")
        listing = Listing.objects.get(title=title)
        
        new_bid = Bid(
            amount = float(request.POST.get("bid")),
            listing = listing,
            user = request.user
       
        )
        new_bid.save()

        if new_bid.amount > listing.current_price:
            listing.current_price = new_bid.amount
            listing.current_winner = request.user
            listing.save()

       
        return HttpResponseRedirect(reverse("page", kwargs={'title': title}))
    

@login_required
def close_auction(request):
    if request.method == "POST":
        title = request.POST.get("title")
        listing = Listing.objects.get(title=title)
        listing.is_open = False
        listing.save()

        return HttpResponseRedirect(reverse("page", kwargs={'title': title}))    
    

@login_required
def add_comment(request):
    if request.method == "POST":
        title = request.POST.get("title")
        listing = Listing.objects.get(title=title)
        
        new_comment = Comment(
            text = request.POST.get("comment"),
            listing = listing,
            user = request.user
       
        )
        new_comment.save()
        return HttpResponseRedirect(reverse("page", kwargs={'title': title}))    
    


def categories(request):
    if request.method == "GET":

        categories = ["Books","Electronics","Fashion","Home","Music","Toys"]
        return render(request, "auctions/categories.html",{"categories": categories })    
    

def category(request, title):

    if request.method == "GET": 
        return render(request, "auctions/category.html",{
            "category": title, 
            "auctions": Listing.objects.filter(category=title, is_open=True)
            })     