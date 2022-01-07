from django import forms
from django.utils.safestring import mark_safe

class AddReviewForm(forms.Form):
    stars = (
        ('0', mark_safe('<span class="add_review__stars add_review__stars--full"></span><span class="add_review__stars add_review__stars--empty">★★★★★</span>')),
        ('1', mark_safe('<span class="add_review__stars add_review__stars--full">★</span><span class="add_review__stars add_review__stars--empty">★★★★</span>')),
        ('2', mark_safe('<span class="add_review__stars add_review__stars--full">★★</span><span class="add_review__stars add_review__stars--empty">★★★</span>')),
        ('3', mark_safe('<span class="add_review__stars add_review__stars--full">★★★</span><span class="add_review__stars add_review__stars--empty">★★</span>')),
        ('4', mark_safe('<span class="add_review__stars add_review__stars--full">★★★★</span><span class="add_review__stars add_review__stars--empty">★</span>')),
        ('5', mark_safe('<span class="add_review__stars add_review__stars--full">★★★★★</span><span class="add_review__stars add_review__stars--empty"></span>'))
    )

    title = forms.CharField(label='Tytuł', max_length=50)
    description = forms.CharField(label='Opis', widget=forms.Textarea())
    rate = forms.ChoiceField(label='Ocena', widget=forms.RadioSelect(), choices=stars)