from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ActiveListingManager(models.Manager):
    """Custom manager that returns only active (unsold) listings."""

    def get_queryset(self):
        return super().get_queryset().filter(is_sold=False, is_active=True)

    def by_category(self, category_slug):
        return self.get_queryset().filter(category__slug=category_slug)

    def recent(self, limit=10):
        return self.get_queryset().order_by("-created_at")[:limit]


class Listing(models.Model):
    CONDITION_CHOICES = [
        ("new", "New"),
        ("like_new", "Like New"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Poor"),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="listings"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="good"
    )
    location = models.CharField(max_length=200)
    image_url = models.URLField(blank=True)
    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveListingManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.seller.username}"


class Message(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Msg from {self.sender.username} about '{self.listing.title}'"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "listing")

    def __str__(self):
        return f"{self.user.username} ♥ {self.listing.title}"
