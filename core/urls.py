
from django.urls import path
import core.views

urlpatterns = [
	path('', core.views.main),
	path('test/', core.views.test),
	path('x/', core.views.main)
]
