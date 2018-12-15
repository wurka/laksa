from django.shortcuts import render
from django.http import HttpResponse
from core.models import Owner, Target, Instance


# Create your views here.
def main(request):
	params = dict()
	known_owners = Owner.objects.all()
	known_targets = Target.objects.all()
	all_instances = Instance.objects.all()

	params["konwn_owners"] = known_owners
	params["known_targets"] = known_targets
	params["instances"] = all_instances

	return render(request, 'core/laksa.html', params)


def test(request):
	return render(request, 'core/test.html')
