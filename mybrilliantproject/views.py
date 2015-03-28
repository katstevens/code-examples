from django.shortcuts import render, redirect, get_object_or_404

from mybrilliantproject.models import Page
from mybrilliantproject.globalfunctions import get_cookie_acceptance

def basic_page(request, slug=False):
	"Show Page model info in basic template"

	page = get_object_or_404(Page, slug=slug,visible=True)

	if page.redirect_url:
		return redirect(page.redirect_url)
	
	if slug == "recommendations":		# Handle custom templates for different pages
		template = "recs.html"
	else:
		template = "base.html"
		
	return render(request, template, {
			'page':page,
			'accept_cookies':get_cookie_acceptance(request),	# Display cookie message
		})
		
def home(request):
	"Named view for Home page for easy URL reference in templates"
	return basic_page(request, slug='home')
