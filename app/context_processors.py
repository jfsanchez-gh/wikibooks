from django.core.urlresolvers import reverse

def main(request):
	ctx = {}
	ctx['app_name'] = 'Share!'

	ctx['menu'] = [
		{'title':'Home', 'url':reverse('index')},
		{'title':'About', 'url':reverse('about')},
		{'title':'Contact', 'url':reverse('contact')},
	]
	
	for item in ctx['menu']:
		if request.path == item['url']:
			item['active'] = True



	return ctx