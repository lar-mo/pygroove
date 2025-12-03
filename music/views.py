from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from .models import Album, Artist, Genre, Cart, CartItem
from .forms import CheckoutForm
import uuid

# -------------------------
# Core Views
# -------------------------

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get 6 most recently added albums
        context['recent_albums'] = Album.objects.select_related('artist', 'genre').order_by('-id')[:6]
        return context


class CollectionView(ListView):
    model = Album
    template_name = 'collection.html'
    context_object_name = 'albums'
    paginate_by = 20

    def get_queryset(self):
        queryset = Album.objects.select_related('artist', 'genre', 'record_label')
        genre = self.request.GET.get('genre')
        artist = self.request.GET.get('artist')
        label = self.request.GET.get('label')
        search = self.request.GET.get('q')
        sort = self.request.GET.get('sort', '-id')

        if genre:
            queryset = queryset.filter(genre__name__icontains=genre)
        if artist:
            queryset = queryset.filter(artist__name__icontains=artist)
        if label:
            queryset = queryset.filter(record_label__name__icontains=label)
        if search:
            queryset = queryset.filter(title__icontains=search)

        # Apply sorting
        if sort == 'artist':
            queryset = queryset.order_by('artist__name', 'title')
        elif sort == 'title':
            queryset = queryset.order_by('title')
        elif sort == '-release_date':
            queryset = queryset.order_by('-release_date', '-id')
        elif sort == 'release_date':
            queryset = queryset.order_by('release_date', 'id')
        elif sort == 'genre':
            queryset = queryset.order_by('genre__name', 'artist__name')
        else:  # Default: -id (Recently Added)
            queryset = queryset.order_by('-id')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all().order_by('name')
        return context


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'album_detail.html'
    context_object_name = 'album'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if this album is already in the cart
        cookie_id = self.request.COOKIES.get('cart_id')
        in_cart = False
        
        if cookie_id:
            try:
                cart = Cart.objects.get(cookie_id=cookie_id)
                in_cart = CartItem.objects.filter(cart=cart, album=self.object).exists()
            except Cart.DoesNotExist:
                pass
        
        context['in_cart'] = in_cart
        return context


class ArtistsListView(ListView):
    model = Artist
    template_name = 'artist_list.html'
    context_object_name = 'artists'
    paginate_by = 24

    def get_queryset(self):
        queryset = Artist.objects.annotate(
            album_count=models.Count('albums')
        ).filter(album_count__gt=0).order_by('name')
        
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'artist_detail.html'
    context_object_name = 'artist'


def cart_view(request):
    cookie_id = request.COOKIES.get('cart_id')
    cart = Cart.objects.filter(cookie_id=cookie_id).first()
    items = cart.items.select_related('album') if cart else []
    return render(request, 'cart.html', {'cart': cart, 'items': items})


class CheckoutView(FormView):
    template_name = 'checkout.html'
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cookie_id = self.request.COOKIES.get('cart_id')
        if cookie_id:
            context['cart'] = Cart.objects.filter(cookie_id=cookie_id).first()
        return context

    def form_valid(self, form):
        cookie_id = self.request.COOKIES.get('cart_id')
        cart = get_object_or_404(Cart, cookie_id=cookie_id)
        checkout = form.save(commit=False)
        checkout.cart = cart
        checkout.save()
        
        # Send email notifications
        self.send_checkout_emails(checkout, cart)
        
        # Clear the cookie so user gets a fresh cart next time
        # Keep the cart/checkout in database for history
        response = redirect('checkout_success')
        response.delete_cookie('cart_id')
        
        return response
    
    def send_checkout_emails(self, checkout, cart):
        """Send checkout notification to The Collector and copy to requestor"""
        
        # Build the email body
        items = cart.items.select_related('album__artist').all()
        
        email_body = f"""PyGroove Album Request
======================

From: {checkout.name}
Email: {checkout.email}

CHECKOUT REQUEST
================

Requested Albums:

"""
        for i, item in enumerate(items, 1):
            email_body += f"""Album #{i}:
  ID: {item.album.id}
  Artist: {item.album.artist.name}
  Album: {item.album.title}
  Year: {item.album.release_date.year if item.album.release_date else 'N/A'}
  Quantity: {item.quantity}

"""
        
        email_body += f"""
Shipping Address:
-----------------
{checkout.mailing_address}
"""
        
        if checkout.message:
            email_body += f"""
Additional Message:
-------------------
{checkout.message}
"""
        
        subject = "PyGroove :: Album Request"
        
        # Send to The Collector
        try:
            send_mail(
                subject=subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.COLLECTOR_EMAIL],
                fail_silently=False,
            )
            
            # Send copy to requestor
            requestor_subject = f"Copy: {subject}"
            requestor_body = f"This is a copy of your album request to PyGroove:\n\n{email_body}"
            
            send_mail(
                subject=requestor_subject,
                message=requestor_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[checkout.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't break the checkout flow
            print(f"Error sending email: {e}")


# -------------------------
# Cart Actions
# -------------------------

def get_cart(request):
    cookie_id = request.COOKIES.get('cart_id')
    
    if cookie_id:
        cart, created = Cart.objects.get_or_create(cookie_id=cookie_id)
    else:
        # Generate new unique cookie_id
        cookie_id = str(uuid.uuid4())
        cart = Cart.objects.create(cookie_id=cookie_id)
    
    return cart, cookie_id


def add_to_cart(request, album_id):
    cart, cookie_id = get_cart(request)
    album = get_object_or_404(Album, pk=album_id)

    item, created = CartItem.objects.get_or_create(cart=cart, album=album)
    if not created:
        item.quantity += 1
        item.save()

    response = redirect('cart')
    response.set_cookie('cart_id', cookie_id, max_age=30*24*60*60)  # 30 days
    return response


def remove_from_cart(request, item_id):
    cart, cookie_id = get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    return redirect('cart')


def update_cart_item(request, item_id):
    cart, cookie_id = get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)

    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        item.quantity = max(1, qty)
        item.save()
    return redirect('cart')


# -------------------------
# AJAX Endpoints
# -------------------------

def collection_ajax(request):
    genre = request.GET.get('genre')
    artist = request.GET.get('artist')
    label = request.GET.get('label')
    search = request.GET.get('q')
    sort = request.GET.get('sort', '-id')
    page = request.GET.get('page', 1)

    queryset = Album.objects.select_related('artist', 'genre', 'record_label')

    if genre:
        queryset = queryset.filter(genre__name__icontains=genre)
    if artist:
        queryset = queryset.filter(artist__name__icontains=artist)
    if label:
        queryset = queryset.filter(record_label__name__icontains=label)
    if search:
        queryset = queryset.filter(title__icontains=search)

    # Apply sorting
    if sort == 'artist':
        queryset = queryset.order_by('artist__name', 'title')
    elif sort == 'title':
        queryset = queryset.order_by('title')
    elif sort == '-release_date':
        queryset = queryset.order_by('-release_date', '-id')
    elif sort == 'release_date':
        queryset = queryset.order_by('release_date', 'id')
    elif sort == 'genre':
        queryset = queryset.order_by('genre__name', 'artist__name')
    else:  # Default: -id (Recently Added)
        queryset = queryset.order_by('-id')

    paginator = Paginator(queryset, 20)
    albums = paginator.get_page(page)

    # Return empty HTML if we're beyond the last page or no results
    if int(page) > paginator.num_pages or not albums:
        return JsonResponse({'html': ''})

    html = render_to_string('partials/album_cards.html', {'albums': albums}, request=request)
    return JsonResponse({'html': html})


def artists_ajax(request):
    search = request.GET.get('q')
    page = request.GET.get('page', 1)

    queryset = Artist.objects.annotate(
        album_count=models.Count('albums')
    ).filter(album_count__gt=0).order_by('name')
    
    if search:
        queryset = queryset.filter(name__icontains=search)

    paginator = Paginator(queryset, 24)
    artists = paginator.get_page(page)

    # Return empty HTML if we're beyond the last page or no results
    if int(page) > paginator.num_pages or not artists:
        return JsonResponse({'html': ''})

    html = render_to_string('partials/artist_cards.html', {'artists': artists}, request=request)
    return JsonResponse({'html': html})


def artist_albums_ajax(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    filter_type = request.GET.get('filter', 'all')

    albums = artist.albums.all()
    if filter_type == 'genre':
        albums = albums.order_by('genre__name')
    elif filter_type == 'label':
        albums = albums.order_by('record_label__name')

    html = render_to_string('partials/album_cards.html', {'albums': albums}, request=request)
    return JsonResponse({'html': html})


# -------------------------
# Redirect Views (No Slug)
# -------------------------

def album_detail_no_slug(request, pk):
    """Redirect old URLs without slugs to new slug-based URLs"""
    album = get_object_or_404(Album, pk=pk)
    return redirect('album_detail', pk=album.pk, slug=album.slug, permanent=True)


def artist_detail_no_slug(request, pk):
    """Redirect old URLs without slugs to new slug-based URLs"""
    artist = get_object_or_404(Artist, pk=pk)
    return redirect('artist_detail', pk=artist.pk, slug=artist.slug, permanent=True)
