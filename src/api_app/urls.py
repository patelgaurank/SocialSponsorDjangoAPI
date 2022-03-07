from . import views
from users import views as uv
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

app_name = 'apiview'
router = DefaultRouter(trailing_slash=False)
# router.include_format_suffixes = False

# router.register('user/data', views.UserData, basename='users-detail')
# router.register('finduser/detail', uv.FindUserActiveOrNot,
#                 basename='find-user-detail')
router.register('url', views.BackendAppOverView, basename='url')


urlpatterns = router.urls
