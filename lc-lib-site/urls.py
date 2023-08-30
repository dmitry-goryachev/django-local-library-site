"""
URL configuration for lc-lib-site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
]
# add URL maps to debug the requests and responses
urlpatterns += [path("debugger/", include("debug_toolbar.urls"))]
print(urlpatterns)

# add the catalog app urls
urlpatterns += [
    path("catalog/", include("catalog.urls")),
]   # TODO Почитать код функции include() для полного понимания того, как
    #  подтягивается новое адресное пространство для нашего приложения.

# add URL maps to redirect the base URL to our application
urlpatterns += [
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
] # TODO Вернуться к редирект вью уже непосредственно тогда, когда будем
  #  изучать редиректы. А пока что сейчас надо знать, что вместо строчек выше,
  #   можно было бы просто написать path('', include("catalog.urls"))

# Use static() to add URL mapping to serve static files during development (only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# TODO ВЕРНУТЬСЯ К ЭТОМУ КОГДА БУДУ У ШАБЛОНОВ. Путь статики надо выяснить, где они
# TODO выяснить, почему список urlpatterns будто бы в кучу все собрал
#  (хотя я то знаю, что тут все строки, ждя этого надо понять, как каждая функция или метод класса, или класс ВЫШЕ
#  все принимает, обрабатывает и возвращает)

# Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
