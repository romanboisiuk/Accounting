# -*- coding: utf-8 -*-
from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView, CreateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models.groups import  Group
from ..util import paginate, get_current_group

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False

        # set form tag attributes
        if add_form:
            self.helper.form_action = reverse('groups_add')
        else:
            self.helper.form_action = reverse('groups_edit',
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
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        )

class GroupAddView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'

    def get_success_url(self):
        title = self.request.POST.get(u'title')
        return u'%s?status_message=Групу %s успішно додано!' % (reverse('home'), 
            self.request.POST.get('title'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
            u'%s?status_message=Додавання групи скасовано' % reverse('home'))
        else:
            return super(GroupAddView, self).post(request, *args, **kwargs) 

class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form_edit.html'

    def get_success_url(self):
        return u'%s?status_message=Групу успішно збережено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
            u'%s?status_message=Редагування групи скасовано' % reverse('home'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs) 
    
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Групу успішно видалено!' % reverse('home')


def groups_list(request):
    current_group = get_current_group(request)
    if current_group:
        groups = Group.objects.filter(id=current_group.id)
    else:    
        groups = Group.objects.all()

    # try to order group list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    context = paginate(groups, 3, request, {}, var_name='groups')  

    return render(request, 'students/groups_list.html', context)