from django.urls import path

from ticket import views

urlpatterns = [
    path('', views.MainView.as_view(), name="main"),
    path('add/', views.AddTicketView.as_view(), name="add_ticket"),
    path('ticket/<ticket_id>', views.TicketDetailView.as_view(), name="ticket_detail"),
    path('ticket/undertake/<ticket_id>', views.UndertakeTicketView.as_view(), name="undertake_ticket"),
    path('ticket/close/<ticket_id>', views.CloseTicketView.as_view(), name="close_ticket"),
    path('ticket/<ticket_id>/comment', views.AddCommentView.as_view(), name="add_comment"),
]