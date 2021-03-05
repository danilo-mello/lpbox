from django.forms import ModelForm
from .models import Lp


class LpModelForm(ModelForm):
    class Meta:
        model = Lp
        fields = ('artist', 'album_title', 'genre', 'year', 'lp_condition', 'cover_condition', 'cover_image', 'price',
                  'acquisition_date', 'country', 'user')

        def __init__(self, *args, **kwargs):
            super(Lp, self).__init__(*args, **kwargs)
            self.fields['cover_image'].required = False
