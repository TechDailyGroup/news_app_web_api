"""news_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("account.urls")),
    path('api/', include("main.urls")),
    path('picture_bed/', include("picture_bed.urls")),
    path('external_data_access/', include("external_data_access.urls")),
    path('mind_graph/', include("mind_graph.urls")),
    path('wechat_api/', include("wechat_api.urls")),
    path('user_actions/', include("user_actions.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
