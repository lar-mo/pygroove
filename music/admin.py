from django.contrib import admin
from django.utils import timezone
from .models import Genre, RecordLabel, Artist, Album, Track, Cart, CartItem, Checkout


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(RecordLabel)
class RecordLabelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name", "website"]
    search_fields = ["name"]
    list_filter = ["name"]

    # Help text for Quick Facts field
    help_texts = {
        "quick_facts": """
            Enter Quick Facts as JSON. Example:
            {
              "Active Since": "1995",
              "Based In": "London, UK",
              "Album Count": "15",
              "Awards": "Multiple Grammy nominations",
              "Influences": "Jazz, Electronic"
            }
        """
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "quick_facts" in form.base_fields:
            form.base_fields["quick_facts"].help_text = self.help_texts["quick_facts"]
        return form


class TrackInline(admin.TabularInline):
    model = Track
    extra = 5  # Number of empty track forms to display
    fields = ["track_number", "title", "duration"]
    ordering = ["track_number"]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "artist", "genre", "release_date", "record_label", "number_of_discs", "is_featured"]
    search_fields = ["title", "artist__name"]
    list_filter = ["genre", "artist", "record_label", "release_date", "is_featured"]
    date_hierarchy = "release_date"
    inlines = [TrackInline]
    readonly_fields = ["featured_at"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "artist":
            kwargs["queryset"] = Artist.objects.order_by("name")
        elif db_field.name == "record_label":
            kwargs["queryset"] = RecordLabel.objects.order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Auto-update featured_at when is_featured is toggled"""
        if "is_featured" in form.changed_data:
            if obj.is_featured:
                # Album is being featured - set timestamp
                obj.featured_at = timezone.now()
            else:
                # Album is being unfeatured - clear timestamp
                obj.featured_at = None
        super().save_model(request, obj, form, change)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ["track_number", "title", "album"]
    search_fields = ["title", "album__title"]
    list_filter = ["album"]
    ordering = ["album", "track_number"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "cookie_id", "created_at"]
    search_fields = ["cookie_id"]
    date_hierarchy = "created_at"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "album", "quantity"]
    search_fields = ["album__title"]
    list_filter = ["cart"]


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ["cart", "name", "submitted_at"]
    search_fields = ["name", "mailing_address"]
    date_hierarchy = "submitted_at"
    readonly_fields = ["submitted_at"]
