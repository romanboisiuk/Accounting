# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from ..models.students import Student
from ..models.groups import Group

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.forms import ModelForm
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from ..util import paginate, get_current_group


class StudentForm(ModelForm):
	class Meta:
		model = Student
		fields = '__all__'

	def __init__(self, *args, **kwargs)	:
		super(StudentForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		#add form or edit form
		if kwargs['instance'] is None:
			add_form = True
		else:
			add_form = False

		# set form tag attributes
		if add_form:
			self.helper.form_action = reverse('students_add')
		else:
			self.helper.form_action = reverse('students_edit',
				kwargs={'pk': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		# add buttons
		if add_form:
			submit = Submit('add_button', u'Додати',
			 	css_class="btn btn-primary")
		else:
			submit = Submit('save_button', u'Зберегти',
				css_class="btn btn-primary")
		self.helper.layout[-1] = FormActions(
			submit, 
			Submit('cancel_button', u'Скасувати', 
				css_class="btn btn-link"),
			)	

class StudentAddView(CreateView):
		model = Student
		form_class = StudentForm
		template_name = 'students/students_form.html'

		def get_success_url(self):
			first_name = self.request.POST.get(u'first_name')
			last_name = self.request.POST.get(u'last_name')
			return u'%s?status_message=Студент %s %s успішно доданий' % (reverse('home'),
						self.request.POST.get('first_name'),
						self.request.POST.get('last_name'))

		def post(self, request, *args, **kwargs):
			# handle cancel button
			if request.POST.get('cancel_button'):
				return HttpResponseRedirect(reverse('home') + 
					u'?status_message=Додавання студента відмінено.')
			else:
				return super(StudentAddView, self).post(request, *args, **kwargs)	

class StudentUpdateView(UpdateView):
		model = Student
		form_class = StudentForm
		template_name = 'students/students_edit.html'

		def get_success_url(self):
			return u'%s?status_message=Студента успішно збережено!' % reverse('home')

		def post(self, request, *args, **kwargs):
			# handle cancel button
			if request.POST.get('cancel_button'):
				return HttpResponseRedirect(reverse('home') + 
					u'?status_message=Редагування студента відмінено.')
			else:
				return super(StudentUpdateView, self).post(request, *args, **kwargs)

class StudentDeleteView(DeleteView):
		model = Student
		template_name = 'students/students_confirm_delete.html'     

		def get_success_url(self):
			return u'%s?status_message=Студента успішно видалено!' % reverse('home')

def students_list(request):
	# check if we need to show only one group of students
	current_group = get_current_group(request)
	if current_group:
		students = Student.objects.filter(student_group=current_group)
	else:
		# otherwise show all students
		students = Student.objects.all()	

	# try to order students list
	order_by = request.GET.get('order_by', '')	
	if order_by in ('last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()

	# apply pagination, 3 students per page
	context = paginate(students, 3, request, {}, var_name='students')		
			
	return render(request, 'students/students_list.html', context)
'''
def students_add(request):
	# was form posted?
		if request.method == "POST":
		# was form add button clicked?
			if request.POST.get('add_button') is not None:
			
				# errors collection	
				errors = {}
				# validate student data will go here
				data = {'middle_name': request.POST.get('middle_name'),
				'notes': request.POST.get('notes')}

				# validate user input
				first_name = request.POST.get('first_name', '').strip()
				if not first_name:
					errors['first_name'] = u"Ім'я є обов'язковим"
				else:
				  data['first_name'] = first_name	

				last_name = request.POST.get('last_name', '').strip()
				if not last_name:
					errors['last_name'] = u"Прізвище є обов'язковим"
				else:
				  data['last_name'] = last_name	  

				birthday = request.POST.get('birthday', '').strip()
				if not birthday:
				  errors['birthday'] = u"Дата народження є обов'язковою"
				else:
					try:
						datetime.strptime(birthday, '%Y-%m-%d')
					except Exception:
						errors['birthday'] = u"Введіть коректний формат дати (напр. 1991-07-03)"
					else:	
						data['birthday'] = birthday

				ticket = request.POST.get('ticket', '').strip()	 	
				if not ticket:
					errors['ticket'] = u"Номер білета є обов'язковим"
				else:
					data['ticket'] = ticket

				student_group = request.POST.get('student_group', '').strip()	
				if not student_group:
					errors['student_group'] = u"Оберіть групу для студента"
				else:
					groups = Group.objects.filter(pk=student_group)
					if len(groups) != 1:
						errors['student_group'] = u"Оберіть коректну групу"
					else:
						data['student_group'] = groups[0]	

				photo = request.FILES.get('photo', '')
				if photo:
				  data['photo'] = photo	
        	
        # save students	
				if not errors:
					student = Student(**data)
					student.save()		
					
					# redirect to students list
					return HttpResponseRedirect(
						u'%s?status_message=Студента %s %s успішно додано! ' % (reverse('home'), student.first_name, student.last_name))

				else:	
						# render form with errors and previous user input
						return render(request, 'students/students_add.html', 
							{'groups': Group.objects.all().order_by('title'),
							 'errors': errors})
			elif request.POST.get('cancel_button') is not None:			
				# redirect to home page on cancel button
				return HttpResponseRedirect(
					u'%s?status_message=Додавання студента скасовано!' % reverse('home'))

		else:
				# initial form render
				return render(request, 'students/students_add.html', 
					{'groups': Group.objects.all().order_by('title')})
'''
