from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Listing, Message, Favorite



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError({"username": "Username already taken."})
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email already registered."})
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class MessageCreateSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField()
    body = serializers.CharField(min_length=1, max_length=2000)

    def validate_listing_id(self, value):
        try:
            listing = Listing.objects.get(pk=value, is_active=True)
        except Listing.DoesNotExist:
            raise serializers.ValidationError("Listing not found or inactive.")
        self.context["listing"] = listing
        return value

    def create(self, validated_data):
        listing = self.context["listing"]
        sender = self.context["request"].user
        return Message.objects.create(
            listing=listing,
            sender=sender,
            recipient=listing.seller,
            body=validated_data["body"],
        )


class ListingSearchSerializer(serializers.Serializer):
    q = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    min_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, allow_null=True)
    max_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, allow_null=True)
    condition = serializers.CharField(required=False, allow_blank=True)
    ordering = serializers.ChoiceField(
        choices=["price", "-price", "-created_at", "created_at"],
        required=False,
        default="-created_at",
    )



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]
        read_only_fields = ["date_joined"]


class CategorySerializer(serializers.ModelSerializer):
    listing_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "icon", "listing_count"]

    def get_listing_count(self, obj):
        return obj.listings.filter(is_active=True, is_sold=False).count()


class ListingSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "price", "condition", "location",
            "image_url", "is_sold", "is_active", "views_count",
            "created_at", "updated_at",
            "seller", "category", "category_id", "is_favorited",
        ]
        read_only_fields = ["seller", "views_count", "created_at", "updated_at"]

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, listing=obj).exists()
        return False


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    listing_title = serializers.CharField(source="listing.title", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "listing", "listing_title",
            "sender", "recipient", "body", "is_read", "created_at",
        ]
        read_only_fields = ["sender", "recipient", "is_read", "created_at"]


class FavoriteSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "listing", "created_at"]
        read_only_fields = ["created_at"]
