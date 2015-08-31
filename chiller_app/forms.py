# -*- coding: utf-8 -*-
from django import forms

class ImagesForm(forms.Form):
	image_file = forms.FileField()
