import re

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import User, UserRoles

from reviews.models import Category, Comment, Genre, Review, Title


class RegisterDataSerializer(serializers.ModelSerializer):
    """
    Serializes data during self-registration of users.
    """

    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r"^[\w.@+-]",
    )
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        fields = ("username", "email")
        model = User

    def validate_username(self, value):
        """
        Validates the user name in order to exclude the name "me".
        """
        if value.lower() in settings.RESERVED_NAMES:
            raise serializers.ValidationError(f"Username {value} is not valid")
        return value


class TokenSerializer(serializers.Serializer):
    """
    Serializes data during the request to receive the token.
    """

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes data during the users requests.
    Handles actions: List, Create, Retrieve, PartialUpdate, Destroy.
    """

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    first_name = serializers.CharField(allow_blank=True, default="")
    last_name = serializers.CharField(allow_blank=True, default="")
    bio = serializers.CharField(allow_blank=True, default="")
    role = serializers.ChoiceField(
        choices=UserRoles.USER_ROLES,
        default=UserRoles.USER
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User

    def validate_username(self, value):
        """
        Validates the user name for valid characters.
        """
        pattern = re.compile(r"^[\w.@+-]+$")
        if not pattern.match(value):
            raise serializers.ValidationError(
                "Error. Letters, digits and @/./+/-/_ only."
            )
        return value

    def validate_role(self, value):
        """
        Validates the role field.
        """
        if self.context.get('view').__dict__.get(
                'action_map').get('patch') == 'users_own_profile':
            if self.context.get('view').request.user.is_user:
                return UserRoles.USER
            if self.context.get('view').request.user.is_moderator:
                return UserRoles.MODERATOR
            if self.context.get('view').request.user.is_admin:
                return UserRoles.ADMIN
        return value


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes data during the category requests.
    Handles actions: List, Create, Destroy.
    """

    class Meta:
        exclude = ("id",)
        model = Category
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializes data during the genre requests.
    Handles actions: List, Create, Destroy.
    """

    class Meta:
        exclude = ("id",)
        model = Genre
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class TitleSerializer(serializers.ModelSerializer):
    """
    Serializes data during the title requests.
    Handles actions: List, Create, Retrieve, PartialUpdate, Destroy.
    """

    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ("id", "name", "year", "rating",
                  "description", "genre", "category")
        model = Title
        read_only_fields = ("id", "rating")

    def validate_year(self, value):
        """
        Validates the year of the title.
        """
        year = timezone.now().year
        if not (settings.ZERO_YEAR < value <= year):
            raise serializers.ValidationError(
                f"The year should be in the range between 0 and {year}."
            )
        return value


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:

        fields = ("id", "name", "year", "rating",
                  "description", "genre", "category")
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializes data during the review requests.
    Handles actions: List, Create, Retrieve, PartialUpdate, Destroy.
    """

    author = serializers.StringRelatedField()

    class Meta:

        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("id", "author", "pub_date")

    def validate_score(self, value):
        if value > settings.TEN_RAITING or value < settings.ZERO_RATING:
            raise serializers.ValidationError(
                "The score should be in the range between 0 and 10."
            )
        return value

    def validate(self, data):
        request = self.context.get("request")
        if request.method == "POST":
            title_id = self.context.get("view").kwargs.get("title_id")
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(
                    title=title, author=request.user).exists():
                raise serializers.ValidationError(
                    "Have you already left a review for this title."
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializes data during the comments requests.
    Handles actions: List, Create, Retrieve, PartialUpdate, Destroy.
    """

    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("id", "author", "pub_date")
