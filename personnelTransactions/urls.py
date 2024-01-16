
from django.urls import path
from .views import *

urlpatterns = [
    path('create-user/', UserCreateAPIView.as_view(), name='create-user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('personnel-list/', UserList.as_view(), name='user-list'),
    path('unit-list/', UnitList.as_view(), name='unit-list'),
    path('user/<int:user_id>/', UserDetail.as_view(), name='user_detail'),
    path('personnel-id/<int:unit_id>/', UserIdList.as_view(), name='user_detail'),
    path('units/', UnitListCreateAPIView.as_view(), name='unit-list-create'),
    path('units/<int:pk>/', UnitDetailAPIView.as_view(), name='unit-detail'),
    path('subunits/<int:upper_unit_id>/', SubUnitsByUpperUnitAPIView.as_view(), name='subunits-by-upperunit'),

]