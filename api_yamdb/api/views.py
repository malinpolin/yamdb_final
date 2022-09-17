from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter

from .mixins import ListCreateDestroyViewSet

from .permissions import (
    IsAdmin,
    IsAdminModeratorAuthorOrReadOnly,
    IsAdminOrReadOnly
)

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    RegisterDataSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitlesSerializer,
    TokenSerializer,
    UserSerializer
)
from accounts.models import User

from reviews.models import Category, Genre, Review, Title


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def registration(request):
    """
    View function handles user registration. Actions: POST.
    """
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            username=serializer.validated_data.get("username"),
            email=serializer.validated_data.get("email"),
        )
    except Exception:
        return Response(
            {"data": serializer.data,
             "message": "Could not create or get an object with such data"},
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="YaMDb registration",
        from_email=None,
        message=f"Your confirmation code: {confirmation_code}",
        recipient_list=[user.email],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """
    View function handles providing JWT Token. Actions: POST.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data["username"])
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet handles User endpoints. Actions: List, Create,
    Retrieve, PartialUpdate, Destroy.
    """

    queryset = User.objects.all().order_by("id")
    lookup_field = "username"
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
    )
    def users_own_profile(self, request):
        """
        The action method to process additional "me" endpoints.
        Methods: GET and PATCH.
        """
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    ViewSet handles Category endpoints. Actions: List, Create, Destroy.
    """

    lookup_field = "slug"
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenreViewSet(ListCreateDestroyViewSet):
    """
    ViewSet handles Genre endpoints. Actions: List, Create, Destroy.
    """

    lookup_field = "slug"
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet handles Title endpoints. Actions: List, Create,
    Retrieve, PartialUpdate, Destroy.
    """

    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category__slug", "genre__slug", "name", "year")
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in (
            "POST",
            "PATCH",
        ):
            return TitleSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet handles Review endpoints. Actions: List, Create,
    Retrieve, PartialUpdate, Destroy.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        """
        The method request a list of objects, one object,
        deletes one object. Actions: List, Retrieve, Destroy.
        """
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.select_related("title", "author").all()

    def perform_create(self, serializer):
        """
        The method saves the review object in a POST request.
        """
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        author = self.request.user
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet handles comment endpoints. Actions: List, Create,
    Retrieve, PartialUpdate, Destroy.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        """
        The method request a list of objects, one object,
        deletes one object. Actions: List, Retrieve, Destroy.
        """
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.select_related("review", "author").all()

    def perform_create(self, serializer):
        """
        The method saves the comment object in a POST request.
        """
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(review=review, author=self.request.user)
