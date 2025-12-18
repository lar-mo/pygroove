from django.test import TestCase, Client
from django.urls import reverse
from music.models import Album, Artist, Genre, RecordLabel, Cart, CartItem


class ArtistModelTest(TestCase):
    """Test Artist model functionality"""

    def test_artist_slug_generation(self):
        """Test that artist slug is automatically generated from name"""
        artist = Artist.objects.create(name="Miles Davis")
        self.assertEqual(artist.slug, "miles-davis")

    def test_artist_slug_with_special_characters(self):
        """Test slug generation handles special characters"""
        artist = Artist.objects.create(name="D'Angelo & The Vanguard")
        self.assertEqual(artist.slug, "dangelo-the-vanguard")

    def test_artist_str_representation(self):
        """Test artist string representation"""
        artist = Artist.objects.create(name="John Coltrane")
        self.assertEqual(str(artist), "John Coltrane")


class AlbumModelTest(TestCase):
    """Test Album model functionality"""

    def setUp(self):
        """Set up test data"""
        self.artist = Artist.objects.create(name="Herbie Hancock")
        self.genre = Genre.objects.create(name="Jazz")
        self.label = RecordLabel.objects.create(name="Blue Note")

    def test_album_slug_generation(self):
        """Test that album slug is automatically generated from title"""
        album = Album.objects.create(title="Head Hunters", artist=self.artist, genre=self.genre)
        self.assertEqual(album.slug, "head-hunters")

    def test_album_str_representation(self):
        """Test album string representation includes title and artist"""
        album = Album.objects.create(title="Maiden Voyage", artist=self.artist, genre=self.genre)
        self.assertEqual(str(album), "Maiden Voyage (Herbie Hancock)")

    def test_album_genre_set_null_on_delete(self):
        """Test that deleting a genre doesn't delete albums"""
        album = Album.objects.create(title="Empyrean Isles", artist=self.artist, genre=self.genre)
        self.genre.delete()
        album.refresh_from_db()
        self.assertIsNone(album.genre)


class HomeViewTest(TestCase):
    """Test home page view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_home_page_loads(self):
        """Test that home page returns 200 OK"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_shows_recent_albums(self):
        """Test that home page context includes recent albums"""
        artist = Artist.objects.create(name="Chick Corea")
        genre = Genre.objects.create(name="Fusion")
        Album.objects.create(title="Return to Forever", artist=artist, genre=genre)

        response = self.client.get(reverse("home"))
        self.assertIn("recent_albums", response.context)


class CollectionViewTest(TestCase):
    """Test collection (albums list) view"""

    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.artist = Artist.objects.create(name="Wayne Shorter")
        self.genre = Genre.objects.create(name="Jazz")
        self.album = Album.objects.create(title="Speak No Evil", artist=self.artist, genre=self.genre)

    def test_collection_page_loads(self):
        """Test that collection page returns 200 OK"""
        response = self.client.get(reverse("albums"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "collection.html")

    def test_collection_filters_by_genre(self):
        """Test that collection can filter albums by genre"""
        response = self.client.get(reverse("albums"), {"genre": "Jazz"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.album, response.context["albums"])


class CartTest(TestCase):
    """Test cart functionality"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.artist = Artist.objects.create(name="Lee Morgan")
        self.genre = Genre.objects.create(name="Hard Bop")
        self.album = Album.objects.create(title="The Sidewinder", artist=self.artist, genre=self.genre)

    def test_add_to_cart_creates_cart(self):
        """Test that adding an item creates a cart"""
        response = self.client.get(reverse("add_to_cart", args=[self.album.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after adding
        self.assertTrue(Cart.objects.exists())

    def test_add_to_cart_creates_cart_item(self):
        """Test that adding an item creates a cart item"""
        self.client.get(reverse("add_to_cart", args=[self.album.id]))
        self.assertTrue(CartItem.objects.filter(album=self.album).exists())

    def test_cart_view_loads(self):
        """Test that cart view loads without errors"""
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart.html")
