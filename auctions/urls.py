from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("page/<int:id>", views.listingpage, name="listingpage"),
    path("addwatchlist/<int:id>",views.addwatchlist,name="addwatchlist"),
    path("removewatchlist/<int:id>",views.removewatchlist,name="removewatchlist"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("close/<int:id>",views.closeauction,name="closeauction"),
    path("addcomment/<int:id>",views.addcomment,name="addcomment"),
    path("addbid/<int:id>",views.addbid,name="addbid"),
    path("categories",views.categories,name="categories"),
    path("category/<int:id>",views.category,name="category"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
