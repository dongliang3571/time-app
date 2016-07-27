from django.core.urlresolvers import reverse
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import TemporalUser


class TemporalUserCreateForm(ModelForm):
    class Meta:
        model = TemporalUser
        fields = ['first_name', 'last_name', 'email']

    # def __init__(self, *args, **kwargs):
    #     super(TemporalUserCreateForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'temp-user-create'
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = reverse('session-temporalusercreate')
    #     self.helper.add_input(Submit('submit', 'Create'))
