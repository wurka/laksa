from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from core.models import Owner, Target, Instance
from datetime import date, datetime
import json
from django.contrib.auth import authenticate, login


# Create your views here.
def main(request):
	return HttpResponse("deleted")
	params = dict()
	# known_owners = Owner.objects.all()
	# known_targets = Target.objects.all().order_by("name")
	# all_instances = Instance.objects.all()

	# params["konwn_owners"] = known_owners
	# params["known_targets"] = known_targets
	# params["instances"] = all_instances

	# return render(request, 'core/laksa.html', params)


def test(request):
	return HttpResponse("deleted")
	# return render(request, 'core/test.html')


def new_target(request):
	if not request.user.is_authenticated:
		return HttpResponse(status=403)

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
	if not request.user.is_authenticated:
		return HttpResponse(status=403)
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


def for_login_only(func):
	def wraper(request):
		error = ""
		if not request.user.is_authenticated:
			if "login" in request.POST:
				if "password" in request.POST:
					user = authenticate(username=request.POST['login'], password=request.POST['password'])
					if user is not None:
						if user.is_active:
							login(request, user)
							return func(request)
						else:
							error = u"Этот аккаунт заблокирован"
					else:
						error = u"Похоже, логин/пароль не верен"
			return render(request, 'core/auth.html', {"error": error})
		return func(request)
	return wraper


@for_login_only
def view(request):
	return render(request, 'core/view.html')


@for_login_only
def analysis(request):
	return render(request, 'core/analysis.html')


def get_analysis_data(request):
	if not request.user.is_authenticated:
		return HttpResponse(status=403)

	must_be = ["fromYear", "fromMonth", "fromDay", "toYear", "toMonth", "toDay"]
	for must in must_be:
		if must not in request.GET:
			return HttpResponse("there is no parameter {}".format(must), status=500)

	try:
		fy = int(request.GET["fromYear"])
		fm = int(request.GET["fromMonth"])
		fd = int(request.GET["fromDay"])
		ty = int(request.GET["toYear"])
		tm = int(request.GET["toMonth"])
		td = int(request.GET["toDay"])
	except ValueError:
		return HttpResponse("wrong value", status=500)

	d_from = date(fy, fm, fd)
	d_to = date(ty, tm, td)
	result = Instance.objects.filter(when__gte=d_from, when__lte=d_to)\
		.values('target__name', 'target_id')\
		.annotate(sum=Sum('how_much'))\
		.order_by('target__name')[:1000]

	ans = [{
		'id': r['target_id'],
		'name': r['target__name'],
		'how_much': r['sum']
	} for r in result]

	ans = json.dumps(ans)
	return HttpResponse(ans)


def get_authors(request):
	if not request.user.is_authenticated:
		return HttpResponse(status=403)

	owners = Owner.objects.all().values('name', 'id')
	owners = json.dumps([{
		'id': x['id'],
		'name': x['name']
	} for x in owners])
	return HttpResponse(owners)


def get_targets(request):
	if not request.user.is_authenticated:
		return HttpResponse(status=403)

	targets = Target.objects.all().values("name", 'id').order_by("name")
	targets = json.dumps([{
		'id': x['id'],
		'name': x['name']
	} for x in targets])
	return HttpResponse(targets)


def new_record(request):
	if not request.user.is_authenticated:
		return HttpResponse(status=403)

	must_be = ["author", 'target', 'howmuch', 'year', 'month', 'day']
	for must in must_be:
		if must not in request.POST:
			return HttpResponse("there is no parameter {}".format(must), status=500)
	try:
		author_id = int(request.POST["author"])
		target_id = int(request.POST["target"])
		how_much = int(request.POST["howmuch"])
		year = int(request.POST["year"])
		month = int(request.POST["month"])
		day = int(request.POST["day"])
	except ValueError:
		return HttpResponse("not valid value of parameter", status=500)

	try:
		own = Owner.objects.get(id=author_id)
		tar = Target.objects.get(id=target_id)
		when = date(year, month, day)
	except Owner.DoesNotExist:
		return HttpResponse("invalid owner", status=500)
	except Target.DoesNotExist:
		return HttpResponse("invalid target", status=500)
	except TypeError:
		return HttpResponse("wrong date", status=500)

	has = Instance.objects.filter(
		owner=own, target=tar, when=when, how_much=how_much)[:1]
	if len(has) > 0:
		return HttpResponse(u"Запись уже есть в базе данных", status=500)

	record = Instance(owner=own, target=tar, when=when, how_much=how_much)
	tar.last_used = datetime.now()
	tar.save()
	record.save()
	return HttpResponse("OK")


def get_last_used_targets(request):
	lus = Target.objects.all().order_by("-last_used")[:4]
	lus = [{
		"id": x.id,
		"name": x.name
	} for x in lus]
	ans = json.dumps(lus)
	return HttpResponse(ans)
