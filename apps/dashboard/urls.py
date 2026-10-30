# apps/dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event/create/', views.create_manual_event, name='create_manual_event'),
    path('event/merge/', views.merge_events, name='merge_events'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/<int:pk>/update/', views.update_verification, name='update_verification'),
    path('event/<int:pk>/status-quick/', views.quick_status_change, name='quick_status_change'),
    path('api/event/<int:pk>/', views.get_event_json, name='get_event_json'),
    path('export/docx/', views.export_word_report, name='export_word'),
    path('export/wa/', views.export_wa_summary, name='export_wa'),
    path('export-center/', views.export_center, name='export_center'),
    path('cycle/lock/', views.lock_cycle, name='lock_cycle'),
    path('cycle/unlock/', views.unlock_cycle, name='unlock_cycle'),
    path('api/sync/', views.sync_now, name='sync_now'),
]
