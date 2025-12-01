from django import forms
from .models import Album, Artist, Genre, RecordLabel, Track, Checkout, CartItem

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['name', 'email', 'mailing_address', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'your@email.com'}),
            'mailing_address': forms.Textarea(attrs={'class': 'input', 'rows': 3, 'placeholder': 'Mailing Address'}),
            'message': forms.Textarea(attrs={'class': 'input', 'rows': 2, 'placeholder': 'Optional Message'}),
        }


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'input', 'min': 1}),
        }


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = [
            'title', 'artist', 'genre', 'release_date',
            'number_of_discs', 'record_label', 'cover_image', 'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'release_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
        }


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'bio', 'website', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'bio': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'input', 'placeholder': 'https://'}),
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
        }


class RecordLabelForm(forms.ModelForm):
    class Meta:
        model = RecordLabel
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
        }


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['album', 'title', 'track_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'track_number': forms.NumberInput(attrs={'class': 'input', 'min': 1}),
        }
