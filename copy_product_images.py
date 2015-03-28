"""
Admin helper function to copy across product images for different 
vintages of the same wine. The vast majority of wines[1] have the same
appearance every year, with the exception of the vintage number. As
wines can be sold before they are in bottle, images from older vintages
are commonplace for products on wine merchant websites.

The Wine model has two different fields for product image display:
- a FileField 'image_file'  (user uploads file in Admin)
- a URLField  'image_url'   (an external image or static file)

The URLField default is a static file, 'unknown_bottle.png'.

[1] Wines known to have different labels every year are handled in PROBLEM_WINE_CODES.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

DEFAULT_IMAGE = 'unknown_bottle.png'
PROBLEM_WINE_CODES = ["","X","1013544","1017757"]
DUTY_CHOICES = ["red","white","sparkling","fortified"]
VINTAGE_HELP_TEXT = _("Enter full year (e.g. '1982'), 'NV' or '0' for multi-vintage collections.")
DUTY_HELP_TEXT = _("For duty calculation purposes, i.e. sparkling is the same duty rate as Champagne.")

# example Model used by the function
class Wine(models.Model):
	"""
	Information associated a particular wine (price/format etc removed for this snippet).
	Related models (Producer, WineCategory etc) not shown for this snippet.
  	"""
	display_name = models.CharField()
	vintage = models.CharField(max_length=5,help_text=VINTAGE_HELP_TEXT)
	duty_type = models.CharField(max_length=20,choices=DUTY_CHOICES,null=True,blank=True,help_text=DUTY_HELP_TEXT)
	
	wine_code = models.CharField(max_length=50,default="X",help_text="Used for stock import matching.")	
	
	# Images
	image_url = models.CharField(max_length=100,default=DEFAULT_IMAGE)	
	image_file = models.ImageField(upload_to='images/bottles/', null=True,blank=True)
	
	def has_proper_image(self):
		if not self.image_file:
			if self.image_url == DEFAULT_IMAGE:
				return False
		return True

	def __unicode__(self):
		if self.vintage == '0':
	    	return self.display_name
		return "%s %s" % (self.vintage, self.display_name)


# Admin view to copy across files/urls to other matching wines
@staff_member_required
def copy_bottle_image_to_sister_wines(request, wine_id):
	"""
	Copy bottle image to other wines with this wine code
	Give sensible error messages to the user if unable to do so.
	"""	
	wine = get_object_or_404(Wine,pk=wine_id)
	updated, f, url = 0, False, False
	
	if wine.wine_code in PROBLEM_WINE_CODES:
		return HttpResponse("Images cannot be copied for this wine.")
	else:
		ws = Wine.objects.filter(wine_code=wine.wine_code).exclude(pk=wine.id)
	
	if ws:
	  # Look for file - this should take precedence over a static url
	  try:
	  	f = wine.bottle_image_file	
	  except:
		f = False
	
		if not f:
  			if wine.image_url == DEFAULT_IMAGE:
			  	return HttpResponse("This url cannot be copied to other wines.") 
			else:
				url = wine.image_url
	
	  	# Try file first
		if f:		
			  for w in ws:
				# Do not overwrite any existing images! So we can't use update() here.
				if not w.has_proper_image():
					w.image_file = f
					w.save()
					updated += 1
		  	return HttpResponse("%d wines updated with image file." % updated)
  		elif url:
			for w in ws:
			  	# As above, do not overwrite any existing images
				if not w.has_proper_image():
					w.image_url = url
					w.save()
					updated += 1
			return HttpResponse("%d wines updated with image url." % updated)
		else:
			return HttpResponse("No file or url available.")
	
	return HttpResponse("No wines to update.")
	
