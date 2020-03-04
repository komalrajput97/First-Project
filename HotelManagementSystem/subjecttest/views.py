# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
# from edxmako.shortcuts import render_to_response

from .models import Standard_Subject

# Create your views here.

class StandardList(ListView):
	"""
	This class contains all methods related to subject_test
	"""

	# template_name="subject_test/select_std.html"
	# model=Standard
	# context_object_name='standard_list'

	def get(self, request, **kwargs):
		"""
		Return all standards
		"""

		template_name="subjecttest/select_std.html"

		context={
			'standard_list':Standard_Subject.objects.all()
			}

		return render(request,template_name,context)

class SubjectTest(ListView):
	"""
	This class returns questions for the test
	"""

	def get(self,request,**kwargs):
		# import pdb;pdb.set_trace()
		# data=request.POST
		template_name="subjecttest/test.html"

		context={
			'standard_list':Standard_Subject.objects.all()
			}

		return render(request,template_name,context)
