from django.urls import path
from category.views import CategoryList,CategoryDetail

urlpatterns = [
    path('categories',CategoryList.as_view()),
    path('categories/<uid>',CategoryDetail.as_view()),
]
