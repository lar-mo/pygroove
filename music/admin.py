from django.contrib import admin
from .models import Genre, RecordLabel, Artist, Album, Track, Cart, CartItem, Checkout


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(RecordLabel)
class RecordLabelAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'release_date', 'record_label', 'number_of_discs']
    search_fields = ['title', 'artist__name']
    list_filter = ['genre', 'artist', 'record_label', 'release_date']
    date_hierarchy = 'release_date'


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['track_number', 'title', 'album']
    search_fields = ['title', 'album__title']
    list_filter = ['album']
    ordering = ['album', 'track_number']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'cookie_id', 'created_at']
    search_fields = ['cookie_id']
    date_hierarchy = 'created_at'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'album', 'quantity']
    search_fields = ['album__title']
    list_filter = ['cart']


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['cart', 'name', 'submitted_at']
    search_fields = ['name', 'mailing_address']
    date_hierarchy = 'submitted_at'
    readonly_fields = ['submitted_at']
