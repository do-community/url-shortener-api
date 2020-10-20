from rest_framework import routers
from shortener import views as myapp_views

router = routers.DefaultRouter()
router.register(r"users", myapp_views.UserViewset)
router.register(r"redirects", myapp_views.RedirectViewset)
