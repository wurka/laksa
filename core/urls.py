
from django.urls import path
import core.views

urlpatterns = [
	#path('', core.views.main),
	path('', core.views.view),
	path('test/', core.views.test),
	path('x/', core.views.main),
	path("new-target/", core.views.new_target),
	path("load-file/", core.views.load_file),
	path("view", core.views.view),
	path("analysis", core.views.analysis),
	path("get-analysis-data", core.views.get_analysis_data),
	path("get-authors", core.views.get_authors),
	path("get-targets", core.views.get_targets),
	path("new-record", core.views.new_record),
	path("get-last-used-targets", core.views.get_last_used_targets),
]
