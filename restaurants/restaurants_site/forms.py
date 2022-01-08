from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from restaurants_site.models import Restaurant

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

class AddRestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'country', 'city', 'street_address', 'google_maps_embed_link', 'image']
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'country': 'Kraj',
            'city': 'Miejscowość',
            'street_address': 'Adres',
            'google_maps_embed_link': 'Link do osadzenia z Google Maps',
            'image': 'Zdjęcie'
        }
    
    def __init__(self, *args, **kwargs):
        super(AddRestaurantForm, self).__init__(*args, **kwargs)
        self.fields['google_maps_embed_link'].required = False
