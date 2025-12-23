from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
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

    def test_album_is_featured_defaults_to_false(self):
        """Test that is_featured defaults to False"""
        album = Album.objects.create(title="Thrust", artist=self.artist, genre=self.genre)
        self.assertFalse(album.is_featured)
        self.assertIsNone(album.featured_at)

    def test_album_can_be_featured(self):
        """Test that an album can be marked as featured"""
        album = Album.objects.create(title="Headhunters", artist=self.artist, genre=self.genre, is_featured=True)
        self.assertTrue(album.is_featured)


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

    def test_home_page_shows_featured_albums_when_present(self):
        """Test that home page context includes featured albums"""
        artist = Artist.objects.create(name="Weather Report")
        genre = Genre.objects.create(name="Jazz Fusion")
        now = timezone.now()

        # Create 3 featured albums with different featured_at timestamps
        album1 = Album.objects.create(
            title="Heavy Weather", artist=artist, genre=genre, is_featured=True, featured_at=now - timedelta(days=2)
        )
        album2 = Album.objects.create(
            title="Black Market", artist=artist, genre=genre, is_featured=True, featured_at=now - timedelta(days=1)
        )
        album3 = Album.objects.create(
            title="Mysterious Traveller", artist=artist, genre=genre, is_featured=True, featured_at=now
        )

        # Create a non-featured album
        Album.objects.create(title="I Sing the Body Electric", artist=artist, genre=genre, is_featured=False)

        response = self.client.get(reverse("home"))

        # Check featured_albums is in context
        self.assertIn("featured_albums", response.context)

        # Check that only featured albums appear
        featured = list(response.context["featured_albums"])
        self.assertEqual(len(featured), 3)

        # Check ordering: most recently featured first (album3, album2, album1)
        self.assertEqual(featured[0].title, "Mysterious Traveller")
        self.assertEqual(featured[1].title, "Black Market")
        self.assertEqual(featured[2].title, "Heavy Weather")

    def test_home_page_limits_featured_albums_to_six(self):
        """Test that home page shows maximum 6 featured albums"""
        artist = Artist.objects.create(name="Pat Metheny")
        genre = Genre.objects.create(name="Contemporary Jazz")
        now = timezone.now()

        # Create 8 featured albums
        for i in range(8):
            Album.objects.create(
                title=f"Album {i}",
                artist=artist,
                genre=genre,
                is_featured=True,
                featured_at=now - timedelta(days=i),
            )

        response = self.client.get(reverse("home"))
        featured = response.context["featured_albums"]

        # Should only return 6
        self.assertEqual(len(featured), 6)

    def test_home_page_hides_featured_section_when_no_featured_albums(self):
        """Test that featured section is hidden when no albums are featured"""
        artist = Artist.objects.create(name="Joe Henderson")
        genre = Genre.objects.create(name="Post Bop")

        # Create non-featured album
        Album.objects.create(title="Page One", artist=artist, genre=genre, is_featured=False)

        response = self.client.get(reverse("home"))

        # featured_albums should be empty
        self.assertEqual(len(response.context["featured_albums"]), 0)


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
