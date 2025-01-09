from django.urls import path
from .views import(
    home_view,
    register_view,
    logout_view,
    start_call_view,
    signaling_server_view
)
urlpatterns = [
    path('', home_view, name="home"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('startCall/<int:calleID>/', start_call_view, name="startCall"),
    path('signaling/', signaling_server_view, name="signalingServer")
]