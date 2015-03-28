from django.conf.urls import patterns, include, url

urlpatterns = patterns('mybrilliantproject.pages.views',
	
	url(r'^$', 'home',  name='home'),
	# Alias to assist the terminally confused
	url(r'^xanadu/$', 'home',  name='xanadu'),
	
	# Database created pages - keep this last to ensure no non-slug urls are overwritten
	# Allow hyphens and underscores for happy slugifying
	url(r'^(?P<slug>[A-Za-z0-9_\-]+)/$', 'basic_page', name='page'),
	
)
