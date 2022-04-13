from django.urls import path

from ticket import views

urlpatterns = [
    path('', views.MainView.as_view(), name="main"),
    path('add/', views.AddTicketView.as_view(), name="addticket"),
]