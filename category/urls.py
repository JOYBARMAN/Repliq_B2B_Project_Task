from django.urls import path
from category.views import CategoryList,CategoryDetail

urlpatterns = [
    path('all/',CategoryList.as_view()),
    path('detail/<uid>/',CategoryDetail.as_view()),
]
