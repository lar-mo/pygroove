from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('albums/', views.CollectionView.as_view(), name='albums'),
    path('artists/', views.ArtistsListView.as_view(), name='artists_list'),
    
    # Redirect old collection URL to albums
    path('collection/', views.collection_redirect, name='collection'),
    
    # Slug-based URLs
    path('album/<int:pk>/<slug:slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('artist/<int:pk>/<slug:slug>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    
    # Fallback URLs without slugs (for old links)
    path('album/<int:pk>/', views.album_detail_no_slug, name='album_detail_no_slug'),
    path('artist/<int:pk>/', views.artist_detail_no_slug, name='artist_detail_no_slug'),
    
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success/', views.HomeView.as_view(template_name="checkout_success.html"), name='checkout_success'),

    # Cart actions
    path('cart/add/<int:album_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),

    # AJAX endpoints
    path('albums/ajax/', views.collection_ajax, name='albums_ajax'),
    path('artists/ajax/', views.artists_ajax, name='artists_ajax'),
    path('artist/<int:pk>/albums/', views.artist_albums_ajax, name='artist_albums_ajax'),
]
