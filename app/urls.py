from src.api.admin import route as admin_route
from src.api.owner import route as owner_route
from src.api.guest import route as guest_route

urlpatterns = [
    *admin_route.routes,
    *owner_route.routes,
    *guest_route.routes,
]
