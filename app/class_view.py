from django.shortcuts import render
from django.views.generic import View
from django.http.response import *

class HelloView(View):
	def get(self, request):
		return render(request,'app/form.html',{})

	def post(self, request):
		q = request.POST.get('q', None)
		return HttpResponse('POST: q=%s' %q)