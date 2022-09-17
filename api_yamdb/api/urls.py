from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    get_jwt_token,
    ReviewViewSet,
    registration,
    TitleViewSet,
    UserViewSet,
)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register("titles", TitleViewSet)
router_v1.register("categories", CategoryViewSet)
router_v1.register("genres", GenreViewSet)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)
router_v1.register("users", UserViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", registration, name="registration"),
    path("v1/auth/token/", get_jwt_token, name="token"),
]
