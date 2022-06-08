from django import forms

from kinematicviscosity.models import CommentsKinematicviscosity, ViscosityMJL


MODEL = ViscosityMJL
COMMENTMODEL = CommentsKinematicviscosity


class StrJournalUdateForm(forms.ModelForm):
    """форма для  обновления записи в журнале: поле модели fixation для отправки записи в ЖАЗ"""
    """стандартная"""
    fixation = forms.BooleanField(label='АЗ',  required=False)

    class Meta:
        model = MODEL
        fields = ['fixation']



class CommentCreationForm(forms.ModelForm):
    """форма для добавления комментариев к записи в журнале"""
    """стандартная"""
    name = forms.CharField(label='Комментировать', max_length=1000,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                               'placeholder': 'введите текст комментария'}))

    class Meta:
        model = COMMENTMODEL
        fields = ['name']







