# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse

from .models import Company, User, CompanyNews
from .forms import UserRegistrationForm
from .utils import CompanyUtils

import json

@login_required
def company_details(request, company_id):
	company = get_object_or_404(Company, pk=company_id)
	CompanyUtils.updateShares(company)
	company_news = company.news.order_by("-date")[:5]
	user = request.user.site_user
	companies = Company.objects.exclude(pk__in=user.companies.all())
	name = 'images/{}.jpg'.format(company.name)
	return render(request, 'siteApp/company_details.html', {"company": company, "company_news": company_news, "user": request.user.site_user, "companies": companies, "name": name})

@login_required
def dashboard(request):
	user = request.user.site_user
	companies = Company.objects.exclude(pk__in=user.companies.all())
	return render(request, 'siteApp/dashboard.html', {"user": request.user.site_user, "companies": companies})

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			username = userObj['username']
			email =  userObj['email']
			first_name =  userObj['first_name']
			last_name =  userObj['last_name']
			password = userObj['password']
			if not (DjangoUser.objects.filter(username=username).exists() or DjangoUser.objects.filter(email=email).exists()):
				dj_user = DjangoUser.objects.create_user(username, email, password, first_name = first_name, last_name = last_name)
				User.objects.create(django_user=dj_user)
				user = authenticate(username = username, password = password)
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				raise forms.ValidationError('Email or username already registered')
	else:
		form = UserRegistrationForm()
	return render(request, 'registration/register.html', {'form' : form})

@csrf_exempt
def include_company(request):
	data = request.POST
	CompanyUtils.createCompany(data);
	return HttpResponse()

@csrf_exempt
def include_news(request):
	data = request.POST
	exists = CompanyNews.objects.filter(company=int(data["company"]), date=data["date"], headline_link=data["headline_link"], headline_text=data["headline_text"]).exists()
	if not exists:
		CompanyNews.objects.create(
			date=data["date"],
			headline_text=data["headline_text"],
			headline_link=data["headline_link"],
			company=Company.objects.get(pk=int(data["company"]))
		);
	return HttpResponse()

@csrf_exempt
def get_companies_codes(request):
	codes = {}
	for company in Company.objects.all():
		codes[company.id] = company.nasdaq
	return HttpResponse(json.dumps(codes))

@csrf_exempt
def get_companies_wikis(request):
	wikis = [
		"https://en.wikipedia.org/wiki/Cisco_Systems",
		"https://en.wikipedia.org/wiki/Apple_Inc.",
		"https://en.wikipedia.org/wiki/Qualcomm",
		"https://en.wikipedia.org/wiki/Nvidia",
		"https://en.wikipedia.org/wiki/Microsoft",
		"https://en.wikipedia.org/wiki/Intel",
		"https://en.wikipedia.org/wiki/21st_Century_Fox",
		"https://en.wikipedia.org/wiki/Comcast",
		"https://en.wikipedia.org/wiki/Micron_Technology",
		"https://en.wikipedia.org/wiki/Facebook",
		"https://en.wikipedia.org/wiki/Marvell_Technology_Group",
		"https://en.wikipedia.org/wiki/Ascena_Retail_Group",
		"https://en.wikipedia.org/wiki/Zynga",
		"https://en.wikipedia.org/wiki/Sirius_XM_Holdings",
		"https://en.wikipedia.org/wiki/Applied_Materials",
		"https://en.wikipedia.org/wiki/JD.com",
		"https://en.wikipedia.org/wiki/PayPal",
		"https://en.wikipedia.org/wiki/Nutanix",
		"https://en.wikipedia.org/wiki/Splunk",
		"https://en.wikipedia.org/wiki/Groupon",
	]
	return HttpResponse(json.dumps(wikis))

@login_required
def follow_company(request, company_id):
	exists = request.user.site_user.companies.filter(pk=company_id).exists()
	if not exists:
		company = Company.objects.get(pk=company_id)
		request.user.site_user.companies.add(company_id)
		request.user.site_user.save()
		CompanyUtils.getActualStock([company.nasdaq])
	return HttpResponseRedirect('/')

@login_required
def unfollow_company(request, company_id):
	request.user.site_user.companies.remove(company_id)
	request.user.site_user.save()
	return HttpResponseRedirect('/')
