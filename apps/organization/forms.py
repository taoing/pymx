# -*- coding: utf-8 -*-

import re
from django import forms

from operation.models import UserAsk

class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ('name', 'mobile', 'course_name')

    def clean_mobile(self):
        data = self.cleaned_data.get('mobile')
        re_mobile = re.compile(r'^1[358]\d{9}$|^147\d{8}$|^176\d{8}$')
        if re_mobile.match(data):
            return data
        else:
            raise forms.ValidationError('手机号非法', code='invalid mobile')