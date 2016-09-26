# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Students
 
def students_list(request):
	students = (
		{'id' : 1,
		'first_name': u'Ігор',
		'last_name': u'Кузь',
		'ticket': 1234,
		'image': 'img/1.png'},
		{'id' : 2,
		'first_name': u'Марко',
		'last_name': u'Зварич',
		'ticket': 1235,
		'image': 'img/2.png'},
		{'id' : 3,
		'first_name': u'Тарас',
		'last_name': u'Колодій',
		'ticket': 1236,
		'image': 'img/3.jpg'}
		)
	return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s </h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s </h1>' % sid)
