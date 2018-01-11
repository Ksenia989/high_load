from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:entity>/<int:entity_id>', views.getEntity, name='get_entity'),
    path('users/<int:entity_id>/visits', views.getPersonVisitList, name='get_visit_list_for_person'),
    path('locations/<int:entity_id>/avg', views.getLocationAverageMark, name='get_average_mark_for_location'),
    path('<int:entity_id>/new', views.createUser, name='new_user'),
]
