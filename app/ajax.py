from django.shortcuts import render, get_object_or_404, get_list_or_404, resolve_url
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http.response import *
from django.db.models import F
from app.models import *
from app.forms import *
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

def get_tags(request):
	json = {}
	tag_list = Tag.objects.all()
	tags = []
	for tag in tag_list:
		tags.append(tag.title)

	json['tags'] = tags
	return JsonResponse(json)

def get_authors(request):
	json = {}
	authors_list = Author.objects.all()
	authors = []
	for author in authors_list:
		authors.append(author.name)

	json['authors'] = authors
	return JsonResponse(json)