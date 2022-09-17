from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles:
    """
    The class defines user roles.
    """

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_ROLES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class User(AbstractUser):
    """
    The model creates instances of users.
    """

    username = models.CharField(
        "username",
        db_index=True,
        max_length=150,
        unique=True
    )
    email = models.EmailField("email", db_index=True, unique=True)
    first_name = models.CharField(
        "First name",
        max_length=150,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        "Last name",
        max_length=150,
        null=True,
        blank=True
    )
    bio = models.TextField("Biography", null=True, blank=True)
    role = models.CharField(
        "Role",
        choices=UserRoles.USER_ROLES,
        max_length=50,
        default=UserRoles.USER
    )
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["id"]
        constraints = (
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            ),
            models.UniqueConstraint(
                fields=[
                    "email",
                ],
                name="email",
            ),
            models.UniqueConstraint(
                fields=[
                    "username",
                ],
                name="username",
            ),
        )

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        """
        The method adds the moderator property to the user instance
        (with the role field == moderator).
        """
        return self.role == UserRoles.MODERATOR

    @property
    def is_admin(self):
        """
        The method adds the admin property to the user instance
        (with the role field == admin).
        """
        return self.role == UserRoles.ADMIN or self.is_superuser

    @property
    def is_user(self):
        """
        The method adds the user property to the user instance
        (with the role field == user).
        """
        return self.role == UserRoles.USER
