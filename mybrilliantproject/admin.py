from django.contrib import admin
from mybrilliantproject.models import Page

class PageAdmin(admin.ModelAdmin):
  "Split out the model fields into user-friendly sections."

	fieldsets = [
		('Slug', {'fields': ['slug','redirect_url']}),	   
		('Page Content', {'fields': ['title','content']}),	
		('Access', {'fields': ['visible','date_created']}),	
		('SEO Information', {'fields': ['meta_title','meta_keywords','meta_description']})
	]

	list_display = ['slug','title','visible','get_wordcount']	
	list_filter = ['visible']	
	search_fields = ['title','slug']
	readonly_fields = ['last_updated']

