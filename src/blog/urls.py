from rest_framework import routers
from .views import BlogPostViewSet

router = routers.DefaultRouter()
router.register('blog_posts', BlogPostViewSet, basename='blog_posts')

urlpatterns = router.urls