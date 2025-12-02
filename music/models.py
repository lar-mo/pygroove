from django.db import models
from django.utils.text import slugify

class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class RecordLabel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(max_length=200, blank=True)
    image = models.ImageField(upload_to='artist_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Artist, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    release_date = models.DateField(blank=True, null=True)
    number_of_discs = models.PositiveSmallIntegerField(default=1)
    record_label = models.ForeignKey(RecordLabel, on_delete=models.SET_NULL, null=True)
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.artist.name})"


class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=100)
    track_number = models.PositiveSmallIntegerField()
    duration = models.CharField(max_length=10, blank=True, null=True, help_text="Track duration (e.g., 4:44)")

    class Meta:
        ordering = ['track_number']

    def __str__(self):
        return f"{self.track_number}. {self.title}"


class Cart(models.Model):
    cookie_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} ({self.cookie_id})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.album.title} x{self.quantity}"


class Checkout(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(default='noreply@example.com')
    mailing_address = models.TextField()
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout for Cart {self.cart.id} - {self.name}"
