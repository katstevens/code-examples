"""
A basic set of models that I use in the majority of my web apps, designed 
to be intuitive for non-technical users encountering them in the admin.
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_unicode
from django.utils.http import is_safe_url

class Page(models.Model):
	"Basic page model"
	slug = models.CharField(max_length=99, help_text="Displayed in URL - no spaces or punctuation please.")
	redirect_url = models.CharField(max_length=255,null=True,blank=True,help_text="")

	title = models.CharField(max_length=100,help_text="Main page title, maximum 100 characters.")
	content = models.TextField(max_length=4000,null=True,blank=True,help_text="Some HTML tags allowed.")
	
	meta_title = models.CharField(max_length=255)
	meta_description = models.CharField(max_length=500,null=True,blank=True)
	meta_keywords = models.CharField(max_length=500,null=True,blank=True)
		
	visible = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return smart_unicode(self.title)
	
	def validate_redirect(self):
		"Double check that the URL is either relative or present in ALLOWED_HOSTS"
		if self.redirect_url:
			if not is_safe_url(self.redirect_url):
				raise ValidationError("Please enter a safe and valid URL.")
		return True
