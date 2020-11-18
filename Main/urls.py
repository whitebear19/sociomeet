
from django.contrib import admin
from django.conf.urls import url

from django.urls import path,include
from django.contrib.auth import views as auth_views
from account.views import LoginView, RegisterView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls',namespace='account')),
    path('', include('blog.urls',namespace='blog')),    
    path('', include('chat.urls',namespace='chat')),
    path('group/', include('groups.urls',namespace='groups')),
    path('page/', include('pages.urls',namespace='pages')),
    path('job/', include('jobs.urls',namespace='jobs')),
    path('', include('django.contrib.auth.urls')),  
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register')  
]

urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
