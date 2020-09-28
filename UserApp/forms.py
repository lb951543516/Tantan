from django import forms

from UserApp.models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'birthday', 'location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    # 检查max和min的大小是否符合
    # clean_加上对应字段名字，只能处理后出现的字段，自己定义该字段的清理函数后，django不会再自动帮你清洗
    def clean_min_dating_age(self):
        # 跳过本层，用父类的clean方法
        cleaned_data = super().clean()

        # 如果最小距离大于最大距离是 抛出异常
        if cleaned_data['min_dating_age'] > cleaned_data['max_dating_age']:
            raise forms.ValidationError('最小年龄应该小于等于最大年龄')
        else:
            # 如果不返还，django里不会包含该字段
            return cleaned_data['min_dating_age']

    def clean_min_distance(self):
        cleaned_data = super().clean()

        if cleaned_data['min_distance'] > cleaned_data['max_distance']:
            raise forms.ValidationError('最小距离应该小于等于最大距离')
        else:
            return cleaned_data['min_distance']
