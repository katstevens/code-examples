"""
Admin helper function to copy across images for different 
types of the same object.

The model has two different fields for image display:
- a FileField 'image_file'  (user uploads file in Admin)
- a URLField  'image_url'   (an external image or static file)

The URLField default is a static file, 'unknown_image.png'.
Let's assume that the form is going to handle URL validation.

"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

DEFAULT_IMAGE = 'unknown_image.png'
AMAZING_CHOICES = ['pugs','metal','biscuits','mt_everest','something_else']

# example Model used by the function
class BrilliantThing(models.Model):
	"An example model that will probably have a generic view and template"

	display_name = models.CharField()
	type = models.CharField(max_length=20,choices=AMAZING_CHOICES,null=True,blank=True)
		
	image_url = models.CharField(max_length=100,default=DEFAULT_IMAGE)	
	image_file = models.ImageField(upload_to='images/useruploaded/', null=True,blank=True)
	
	def has_proper_image(self):
		if not self.image_file:
			if self.image_url == DEFAULT_IMAGE:
				return False
		return True

	def __unicode__(self):
		return self.display_name


# Admin view to copy across files/urls 
@staff_member_required
def copy_image_to_sister_objects(request, thing_id):
	"""
	Copy image to other objects with this type
	Give sensible error messages to the user if unable to do so.
	"""	
	obj = get_object_or_404(BrilliantThing,pk=thing_id)
	updated, url = 0, False
	
	things = BrilliantThing.objects.filter(type=obj.type).exclude(pk=obj.id)
	
	if not things:
		return HttpResponse("Nothing to update.")		
	
	# Look for a file first - this should take precedence over a static url
	if obj.image_file:
		for t in things:
			# Do not overwrite any existing images. So we can't use update() here.
			if not t.has_proper_image():
				t.image_file = obj.image_file
				t.save()
				updated += 1
		return HttpResponse("%d objs updated with image file." % updated)
		
	elif obj.image_url == DEFAULT_IMAGE:
		return HttpResponse("This url cannot be copied to other objs.") 
	
	elif obj.image_url:
		for t in things:
			# As above, do not overwrite any existing images
			if not t.has_proper_image():
				t.image_url = url
				t.save()
				updated += 1
		return HttpResponse("%d objs updated with image url." % updated)
	
	else:
		return HttpResponse("No file or url available.")
