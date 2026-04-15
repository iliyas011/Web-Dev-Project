from django.urls import path
from . import views

urlpatterns = [

    path("auth/login/", views.login_view, name="login"),
    path("auth/register/", views.register_view, name="register"),
    path("auth/logout/", views.logout_view, name="logout"),
    path("auth/me/", views.me_view, name="me"),


    path("categories/", views.CategoryListView.as_view(), name="category-list"),


    path("listings/", views.ListingListCreateView.as_view(), name="listing-list-create"),
    path("listings/search/", views.listing_search, name="listing-search"),
    path("listings/my/", views.MyListingsView.as_view(), name="my-listings"),
    path("listings/<int:pk>/", views.ListingDetailView.as_view(), name="listing-detail"),
    path("listings/<int:pk>/sold/", views.mark_sold, name="mark-sold"),

    path("messages/", views.MessageView.as_view(), name="messages"),


    path("favorites/", views.FavoriteView.as_view(), name="favorites"),
]
