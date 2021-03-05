from django.db import models
from djmoney.models.fields import MoneyField
from stdimage import StdImageField
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django_countries.fields import CountryField


def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


class Base(models.Model):
    created = models.DateField('Created', auto_now_add=True)
    motified = models.DateField('Modified', auto_now=True)
    active = models.BooleanField('Active?', default=True)

    class Meta:
        abstract = True


class Lp(Base):
    LP_CONDITION = (
        ('SE', 'Sealed'),
        ('M', 'Mint'),
        ('NM', 'Near Mint'),
        ('VG+', 'Very Good Plus'),
        ('VG', 'Very Good'),
        ('G', 'Good'),
        ('F', 'Fair'),
        ('P', 'Poor')
    )

    COVER_CONDITION = (
        ('SE', 'Sealed'),
        ('M', 'Mint'),
        ('NM', 'Near Mint'),
        ('VG+', 'Very Good Plus'),
        ('VG', 'Very Good'),
        ('G', 'Good'),
        ('F', 'Fair'),
        ('P', 'Poor')
    )

    artist = models.CharField('Artist', max_length=100)
    album_title = models.CharField('Album', max_length=100)
    genre = models.CharField('Genre', max_length=100)
    year = models.IntegerField('Year of Release', validators=[MinValueValidator(0),
                                                              MaxValueValidator(int(date.today().year))])
    lp_condition = models.CharField('LP Condition', max_length=14, choices=LP_CONDITION)
    cover_condition = models.CharField('Cover Condition', max_length=14, choices=COVER_CONDITION)
    # cover_image = StdImageField(_('Cover'), upload_to=get_file_path, default="./static/img/logo1.png")
    cover_image = StdImageField(_('Cover'), upload_to=get_file_path, default="./static/img/logo1.png",
                                variations={'thumb': {'width': 480, 'height': 480, 'crop': True}})
    price = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11)
    acquisition_date = models.DateTimeField(null=True, blank=True)
    country = CountryField(default='US')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Lp'
        verbose_name_plural = 'Lps'

    def __str__(self):
        return self.album_title


