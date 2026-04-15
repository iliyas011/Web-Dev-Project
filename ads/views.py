from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.db.models import Q

from .models import Category, Listing, Message, Favorite
from .serializers import (
    LoginSerializer, RegisterSerializer, MessageCreateSerializer,
    ListingSearchSerializer, UserSerializer, CategorySerializer,
    ListingSerializer, MessageSerializer, FavoriteSerializer,
)




@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """Authenticate user and return auth token."""
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )
    if not user:
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "user": UserSerializer(user).data,
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """Register a new user account."""
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {"token": token.key, "user": UserSerializer(user).data},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Delete the user's auth token (logout)."""
    request.user.auth_token.delete()
    return Response({"detail": "Logged out successfully."})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Return the authenticated user's profile."""
    return Response(UserSerializer(request.user).data)




@api_view(["GET"])
@permission_classes([AllowAny])
def listing_search(request):
    """Full-text search + filter listings."""
    params = ListingSearchSerializer(data=request.query_params)
    if not params.is_valid():
        return Response(params.errors, status=status.HTTP_400_BAD_REQUEST)

    data = params.validated_data
    qs = Listing.active.all()

    if q := data.get("q"):
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if cat := data.get("category"):
        qs = qs.filter(category__slug=cat)
    if min_p := data.get("min_price"):
        qs = qs.filter(price__gte=min_p)
    if max_p := data.get("max_price"):
        qs = qs.filter(price__lte=max_p)
    if cond := data.get("condition"):
        qs = qs.filter(condition=cond)

    qs = qs.order_by(data.get("ordering", "-created_at"))
    serializer = ListingSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)



class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)




class ListingListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        listings = Listing.active.all()
        serializer = ListingSerializer(listings, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ListingSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListingDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Listing.objects.get(pk=pk, is_active=True)
        except Listing.DoesNotExist:
            return None

    def get(self, request, pk):
        listing = self.get_object(pk)
        if not listing:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        listing.views_count += 1
        listing.save(update_fields=["views_count"])
        serializer = ListingSerializer(listing, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        listing = self.get_object(pk)
        if not listing:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if listing.seller != request.user:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ListingSerializer(listing, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        listing = self.get_object(pk)
        if not listing:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if listing.seller != request.user:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        listing.is_active = False
        listing.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyListingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        listings = Listing.objects.filter(seller=request.user).order_by("-created_at")
        serializer = ListingSerializer(listings, many=True, context={"request": request})
        return Response(serializer.data)



class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """All messages where the user is sender or recipient."""
        messages = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).select_related("listing", "sender", "recipient")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            message = serializer.save()
            return Response(
                MessageSerializer(message).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class FavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favs = Favorite.objects.filter(user=request.user).select_related("listing")
        serializer = FavoriteSerializer(favs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        listing_id = request.data.get("listing_id")
        try:
            listing = Listing.objects.get(pk=listing_id, is_active=True)
        except Listing.DoesNotExist:
            return Response({"detail": "Listing not found."}, status=status.HTTP_404_NOT_FOUND)

        fav, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
        if not created:
            fav.delete()
            return Response({"detail": "Removed from favorites.", "favorited": False})
        return Response({"detail": "Added to favorites.", "favorited": True}, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def mark_sold(request, pk):
    """Mark a listing as sold."""
    try:
        listing = Listing.objects.get(pk=pk, seller=request.user)
    except Listing.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    listing.is_sold = True
    listing.save(update_fields=["is_sold"])
    return Response({"detail": "Listing marked as sold."})
