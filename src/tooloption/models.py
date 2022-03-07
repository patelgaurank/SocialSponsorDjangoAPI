from django.core.checks.messages import Error
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import date
from django_react.get_username import current_request
from django.utils.text import slugify
import random
import string
import secrets
today = date.today()

# Create your models here.

class DomElementManager(models.Manager):
    def get_queryset(self):
        return super(DomElementManager, self).get_queryset().filter(is_active=True)

def default_place_pics():
    return "place_pics/MF.svg"

# Generate random and unique Id for HTML Tags and Project
def GenerateClassForDOMTags():
    TagClass_length = 13
    while True:
        try:
            TagClass = secrets.token_urlsafe(TagClass_length)
            exist = DomElement.objects.filter(elementclass=TagClass)
            if exist:
                print('rerun')
            else:
                return TagClass
        except:
            print('rerun')

def GenerateIdForDOMTags():    
    while True:
        try:
            TagId = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            exist = DomElement.objects.filter(elementid=TagId)
            if exist:
                print('rerun')
            else:
                return TagId
        except:
            print('rerun')

class DomElement(models.Model):
    DomElement_Id = models.AutoField(primary_key=True)
    urlpath = models.CharField(
        'section Name', max_length=120, blank=True, null=True) 
    section = models.CharField(
        'section Name', max_length=120, blank=True, null=True)
    subsection = models.CharField(
        'sub-section Name', max_length=120, blank=True, null=True)

    arialabel = models.CharField(
        "Aria label", max_length=300, blank=True, null=True,default="None")
    ariahaspopup = models.CharField(
        "Aria has popup", max_length=300, blank=True, null=True,default="None")
    color = models.CharField(
        "Element color", max_length=300, blank=True, null=True,default="None")
    option = models.CharField(
        "Element option", max_length=300, blank=True, null=True,default="None")
    link = models.CharField(
        "Href link", max_length=300, blank=True, null=True, default='#')
    onclick = models.CharField(
        "On click send text variable", max_length=300, blank=True, null=True, default='None')
    description = models.CharField(
        "Element description", max_length=300, blank=True, null=True,default="None")
    comp = models.CharField(
        "Material UI Component name", max_length=300, blank=True, null=True,default="None")


    elementid = models.CharField(
        'Dom id', max_length=120, blank=True, null=True, default=GenerateIdForDOMTags)
    elementclass = models.CharField(
        'Dom class', max_length=120, blank=True, null=True, default=GenerateClassForDOMTags)

    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='Dom_Element_creator', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    DomElement = DomElementManager()

    class Meta:
        verbose_name_plural = 'Dom Element info'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.section} {self.subsection}'

    def save_model(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.DomElement_Id:
            self.slug = slugify(
                f'{self.section} {self.subsection}')
        else:
            self.slug = slugify(
                f'{self.DomElement_Id} {self.section} {self.subsection}')
        super(DomElement, self).save(*args, **kwargs)