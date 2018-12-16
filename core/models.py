from django.db import models
from datetime import date


# Create your models here.
class Target(models.Model):
	"""
	Цель траты
	"""
	name = models.TextField(default="")


class Owner(models.Model):
	"""
	имя того, кто тратит
	"""
	name = models.TextField(default="noname")


class Instance(models.Model):
	"""
	единица траты
	"""
	when = models.DateField(default=date(1970, 1, 1))
	how_much = models.IntegerField(default=0)
	target = models.ForeignKey(Target, on_delete=models.CASCADE)
	owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
