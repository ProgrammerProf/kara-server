from src.api.admin import route as admin_route

urlpatterns = [
    *admin_route.routes,
]
