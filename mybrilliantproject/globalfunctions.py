"""
General functions for use throughout the project.
"""

def cookie_check(request, keyname):
	"Returns value of cookie if present, False otherwise"
	if request.COOKIES.has_key(keyname):
		return request.COOKIES[keyname]
	return False
	
def get_cookie_acceptance(request):
	"""
	If the user is logged in then their acceptance of the T&C includes cookies.
	Otherwise check for 'accept-cookies' cookie set in session
	Used in views.basic_page to determine whether to display cookie message in template.
	"""
	if request.user.is_authenticated():
		return True
	else:
		return cookie_check(request, 'accept_cookies')		

