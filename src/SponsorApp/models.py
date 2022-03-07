from django.db import models
from django.utils.timezone import get_current_timezone
from datetime import datetime
from datetime import date
from django.utils import timezone
from users.models import NewUser as CurrentUser
from django.utils.text import slugify
from django.conf import settings
from django_react.get_username import current_request

class pptbgManager(models.Manager):
    def get_queryset(self):
        return super(pptbgManager, self).get_queryset().filter(is_active=True)

class SponsorManager(models.Manager):
    def get_queryset(self):
        return super(SponsorManager, self).get_queryset().filter(is_active=True)

class purposeManager(models.Manager):
    def get_queryset(self):
        return super(purposeManager, self).get_queryset().filter(is_active=True)

def default_place_pics():
    return "place_pics/MF.svg"

class pptBackground(models.Model):
    pptbg_Id = models.AutoField(primary_key=True)
    currentTimeStamp = models.DateField(auto_now=True, blank=True, null=True)
    pptbg_description = models.CharField(
        'PPT Description', max_length=120, blank=True, null=True)
    pptbg_image = models.ImageField(
        default=default_place_pics, upload_to="place_pics/{tablename}/{field}".format(tablename="PPT Bacground", field="Image"), null=True)
    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='PPT_Background_creator', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    pptbackground = pptbgManager()

    class Meta:
        verbose_name_plural = 'Slides'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.pptbg_Id}, {self.pptbg_description}'

    def save_model(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.pptbg_Id:
            self.slug = slugify(
                f'{self.pptbg_description}-{self.pptbg_Id}')
        else:
            self.slug = slugify(
                f'{self.pptbg_Id}-{self.pptbg_description}')
        super(pptBackground, self).save(*args, **kwargs)


class purposeData(models.Model):
    # "purpose_Id", "Purpose", "Purpose_Code", "Purpose_Index", "DisplayOnPPT", "AnnounceAs"
    purpose_Id = models.AutoField(primary_key=True)
    currentTimeStamp = models.DateField(auto_now=True, blank=True, null=True)
    Purpose = models.CharField(
        'Purpose', max_length=120, blank=True, null=True)
    Purpose_Code = models.CharField(
        'Purpose Code', max_length=120, blank=True, null=True)
    Purpose_Index = models.IntegerField('Purpose Index', blank=True, null=True)
    DisplayOnPPT = models.CharField(
        'Purpose Title', max_length=120, blank=True, null=True)
    AnnounceAs = models.CharField(
        'Annoucer Note', max_length=120, blank=True, null=True)
    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='Purpose_creator', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    purposes = purposeManager()

    class Meta:
        verbose_name_plural = 'Purposes'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.purpose_Id}, {self.Purpose} {self.Purpose_Code}'

    def save(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.purpose_Id:
            self.slug = slugify(
                f'{self.Purpose}-{self.Purpose_Code}')
        else:
            self.slug = slugify(
                f'{self.purpose_Id}-{self.Purpose}-{self.Purpose_Code}')
        super(purposeData, self).save(*args, **kwargs)

class SponsorsData(models.Model):
    YESNO_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    sponsor_Id = models.AutoField(primary_key=True)
    first_name = models.CharField(
        'First Name', max_length=120, blank=True, null=True)
    middle_name = models.CharField(
        'Middle Name', max_length=120, blank=True, null=True)
    last_name = models.CharField(
        'Last Name', max_length=120, blank=True, null=True)
    Member_Id = models.DecimalField(
        'Member Id', default=0, max_digits=20, decimal_places=0, blank=True, null=True)
    ZipCode = models.DecimalField(
        'Zip Code', max_digits=20, decimal_places=0, blank=True, null=True)
    City = models.CharField('City', max_length=120, blank=True, null=True)
    State = models.CharField('State', max_length=120, blank=True, null=True)
    Country = models.CharField(
        'Country', max_length=120, blank=True, null=True)
    Purpose = models.CharField(
        'Purpose', max_length=120, blank=True, null=True)
    Purpose_Code = models.CharField(
        'Purpose Code', max_length=120, blank=True, null=True)
    Memo = models.CharField('Announcer Note(s)', default='NA',
                            blank=True, null=True, max_length=200)
    current_Time_Stamp = models.DateTimeField(auto_now_add=True)
    sponsorship_Date = models.DateField(
        'Sponsor Date', default=timezone.now, blank=True, null=True)
    Display_On_PPT = models.CharField(
        'PPT', max_length=3, blank=True, null=True, choices=YESNO_CHOICES, default='Y')
    Announce = models.CharField(
        'Announce', max_length=3, blank=True, null=True, choices=YESNO_CHOICES, default='Y')
    Name_to_annouce = models.CharField('Name(s) to annouce', default='NA',
                                       blank=True, null=True, max_length=200)
    amount_Received = models.CharField(
        'Amount Received', max_length=3, blank=True, null=True, choices=YESNO_CHOICES, default='Y')
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='Sponsor_creator', blank=True, null=True, default=CurrentUser)
    Updated_Date = models.DateTimeField('Updated Date', auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    sponsors = SponsorManager()

    class Meta:
        verbose_name_plural = 'Sponsors'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.sponsor_Id}, {self.first_name} {self.last_name}'
        # return self.title

    def save(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.slug:
            self.slug = slugify(self.first_name) + "-" + \
                slugify(self.last_name) + "-" + str(self.sponsor_Id)
            self.save()
        super(SponsorsData, self).save(*args, **kwargs)