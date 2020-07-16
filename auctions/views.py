from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max


from .models import User, Categories, Listings, Comments, Bids

# load the index page
def index(request):
    # get all the active listings. 
    all = Listings.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        "all":all
    })


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
        #load all the available listing categories
        categories = Categories.objects.all()
        # renders the html for creating a new listing, and passes the categories
        return render(request, "auctions/create.html",{
            "categories":categories
        })

    username = request.user.username
    title = request.POST["title"]
    description = request.POST["description"]
    startbid = request.POST["startbid"]
    image = request.FILES["image"]
    category = request.POST["category"]

    # creating and saving the new listing
    listing = Listings(title=title, description=description, 
    picture=image, lister=username,category=Categories.objects.get(category=category))
    listing.save()

    # creating and saving a new bid for the listing
    bid = Bids(user=request.user, bid=startbid, product=listing)
    bid.save()

    return HttpResponseRedirect(reverse("index"))


# loading up the page of a listing after clicking on it
def listingpage(request,id):
    user = User.objects.filter(username=request.user.username)
    listing = Listings.objects.get(pk=id)

    #checks to see if the listing is no longer active, loads the html for a closed listing
    if listing.active == False:
        winningBid = Bids.objects.filter(product=listing).latest("bid") 
        winner = winningBid.user
        return render(request,"auctions/closed.html",{
            "winner":winner,
            "listing":listing
        })

    # if the user is logged on, gets the user's watchlist and passes it to the page
    elif user:
        user = user[0]
        watchlist = user.watchlist
        latestbid = listing.bids.latest("bid")
        latestbid = latestbid.bid
        minimum_bid = latestbid + (latestbid * 0.05)
        comments = listing.comments.all()
        return render(request, "auctions/listingpage.html",{
            "listing":listing,
            "latestbid":latestbid,
            "minimum":minimum_bid,
            "comments":comments
            })

    latestbid = listing.bids.latest("bid")
    latestbid = latestbid.bid
    comments = listing.comments.all()
    return render(request, "auctions/listingpage.html",{
        "listing":listing,
        "latestbid":latestbid,
        "comments":comments
    })


# adding a listing to the user's watchlist
@login_required
def addwatchlist(request,id):
    listing = Listings.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("watchlist"))

# remove a listing from the user's watchlist
@login_required
def removewatchlist(request,id):
    listing = Listings.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse("watchlist"))

# close an active auction by updating the listing.active column to False
@login_required
def closeauction(request,id):
    listing = Listings.objects.get(pk=id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("index"))

# create a new comment for a listing by a user
@login_required
def addcomment(request,id):
    comment = request.POST["comment"]
    listing = Listings.objects.get(pk=id)
    Comments.objects.create(text=comment,user=request.user.username,product=listing)
    return HttpResponseRedirect(reverse("listingpage",args=(listing.id,)))

# create a new bid by a user for a listing
@login_required
def addbid(request,id):
    listing = Listings.objects.get(pk=id)
    bid = request.POST["bid"]
    Bids.objects.create(user=request.user.username,bid=bid,product=listing)
    return HttpResponseRedirect(reverse("listingpage",args=(listing.id,)))

@login_required
def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    watchlist = user.watchlist.all()
    return render(request,"auctions/watchlist.html",{
        "watchlist":watchlist
    })

def categories(request):
    categories = Categories.objects.all()
    return render(request,"auctions/categories.html",{
        "categories":categories
    })

def category(request,id):
    category = Categories.objects.get(pk=id)
    listings = Listings.objects.filter(category=category)
    return render(request,"auctions/category.html",{
        "listings":listings
    })
