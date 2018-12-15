from django.db import models


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
	target = models.ForeignKey(Target, on_delete=models.CASCADE)
	owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
