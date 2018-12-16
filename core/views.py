from django.shortcuts import render
from django.http import HttpResponse
from core.models import Owner, Target, Instance
from datetime import date


# Create your views here.
def main(request):
	params = dict()
	known_owners = Owner.objects.all()
	known_targets = Target.objects.all().order_by("name")
	all_instances = Instance.objects.all()

	params["konwn_owners"] = known_owners
	params["known_targets"] = known_targets
	params["instances"] = all_instances

	return render(request, 'core/laksa.html', params)


def test(request):
	return render(request, 'core/test.html')


def new_target(request):
	if "newTarget" not in request.POST:
		return HttpResponse("there is no newTarget parameter", status=500)

	val = request.POST["newTarget"]
	ntar = ". ".join([x.strip().capitalize() for x in val.split(".")])

	same = Target.objects.filter(name=ntar)

	if len(same) > 0:
		return HttpResponse("Такая запись уже есть в базе данных", status=500)

	Target.objects.create(name=ntar)
	return HttpResponse("OK")


def load_file(request):
	# all_targets = [x.name for x in Target.objects.all()]
	# all_owners = ["Маша", "Саша", "Саша и Маша"]
	Target.objects.all().delete()
	# Owner.objects.all().delete()
	Instance.objects.all().delete()

	if len(Owner.objects.all()) == 0:
		masha = Owner.objects.create(name="Маша")
		sasha = Owner.objects.create(name="Саша")
		both = Owner.objects.create(name="Саша и Маша")
	else:
		masha = Owner.objects.get(name="Маша")
		sasha = Owner.objects.get(name="Саша")
		both = Owner.objects.get(name="Саша и Маша")

	with open("C:\\traty.txt", encoding="UTF-8") as file:
		for i, line in enumerate(file.readlines()):
			if i == 0:
				continue
			els = line.split('\t')
			first = els[0].split('/')
			when = date(int(first[2]), int(first[0]), int(first[1]))
			howmuch = int(els[1])
			target = els[2]
			who = els[3].strip()

			owner = both
			if who == "Саша":
				owner = sasha
			elif who == "Маша":
				owner = masha

			try:
				target = Target.objects.get(name=target)
			except Target.DoesNotExist:
				target = Target.objects.create(name=target)

			Instance.objects.create(
				when=when,
				how_much=howmuch,
				target=target,
				owner=owner
			)

	return HttpResponse("OK")
