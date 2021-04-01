from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='app-home'),
    # path('', views.showresults),
    path('about/', views.about, name='app-about'),
    path('post/', views.post, name='app-post'),
    path('home/post', views.post, name='app-maphome'),
    path(r'^statistics/$', views.stats, name='app-stats'),
    path('population-chart/', views.stats, name='population-chart'),
    path('export_csv', views.export_csv, name="export-csv"),
    path(r'^admin/', admin.site.urls),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)