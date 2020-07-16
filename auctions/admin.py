from django.contrib import admin
from .models import Categories, Listings, User, Comments, Bids

admin.site.register(Categories),
admin.site.register(Listings),
admin.site.register(User),
admin.site.register(Comments),
admin.site.register(Bids),