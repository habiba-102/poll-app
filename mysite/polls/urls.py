from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path("<int:pk>/", views.DetailView.as_view(), name = "detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name = "results"),
    path("<int:question_id>/vote/", views.vote, name = "vote"),
    path('signup/', views.signup_view, name = "signup"),
]
#Django extracts 5 from the URL.
#It calls the function views.results(request, question_id=5).