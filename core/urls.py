
from django.urls import path
import core.views

urlpatterns = [
	path('', core.views.main),
	path('test/', core.views.test),
	path('x/', core.views.main),
	path("new-target/", core.views.new_target),
	path("load-file/", core.views.load_file)
]
