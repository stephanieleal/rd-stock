# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User as DjangoUser
from django.db import models
import datetime

class Company(models.Model):
	name = models.CharField(max_length=30, blank=False)
	logo = models.CharField(max_length=210, blank=False)
	nasdaq = models.CharField(max_length=10, blank=False)
	wikipedia = models.TextField(blank=False)
	stock = models.FloatField(null=True)
	def __str__(self):
		return self.name

	def getActualStock(self):
		try:
			return self.stocks.latest(field_name="date")
		except CompanyStockValue.DoesNotExist:
			return None

class CompanyStockValue(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="stocks")
	value = models.FloatField()
	date = models.DateTimeField(default=datetime.datetime.now())
	previous = models.OneToOneField('self', blank=True, null=True)
	def getIncrement(self):
		if self.previous:
			return self.value - self.previous.value
		return 0

	def getPercentIncrement(self):
		if self.previous:
			return (self.getIncrement() * 100) / self.previous.value
		return 0

	def tradeDecision(self):
		return -10

	def __str__(self):
		date_str = self.date.strftime('%d/%m/%Y %H:%M')
		return "%s - %.2f at %s" %(self.company.name, self.value, date_str)

class CompanyNews(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="news")
	date = models.DateTimeField(default=datetime.datetime.now())
	headline_link = models.TextField(blank=False)
	headline_text = models.TextField(blank=False)

class User(models.Model):
	companies = models.ManyToManyField(Company, related_name="users")
	django_user = models.OneToOneField(DjangoUser, related_name="site_user", on_delete=models.CASCADE)
	def __str__(self):
		return "%s %s" %(self.django_user.first_name, self.django_user.last_name)
