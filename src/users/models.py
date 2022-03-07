from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.conf import settings
from django.dispatch import receiver
from datetime import date
from phone_field import PhoneField
from django_react.get_username import current_request
from django.utils.text import slugify
today = date.today()

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, phone_number, password, **other_fields):

        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, phone_number, password, **other_fields)

    def create_user(self, email, user_name, phone_number, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=False)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    # first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'phone_number']

    def __str__(self):
        return f'{self.email} : {self.phone_number}'


class NewUserInfoManager(models.Manager):
    def get_queryset(self):
        return super(NewUserInfoManager, self).get_queryset().filter(is_active=True)

class ZoneInfoManager(models.Manager):
    def get_queryset(self):
        return super(ZoneInfoManager, self).get_queryset().filter(is_active=True)

class MandalInfoManager(models.Manager):
    def get_queryset(self):
        return super(MandalInfoManager, self).get_queryset().filter(is_active=True)

class SatsangCategoryInfoManager(models.Manager):
    def get_queryset(self):
        return super(SatsangCategoryInfoManager, self).get_queryset().filter(is_active=True)

class NewUserAddressManager(models.Manager):
    def get_queryset(self):
        return super(NewUserAddressManager, self).get_queryset().filter(is_active=True)

class ZoneSOLeaderInfoManager(models.Manager):
    def get_queryset(self):
        return super(ZoneSOLeaderInfoManager, self).get_queryset().filter(is_active=True)
# 
def default_place_pics():
    return "place_pics/MF.svg"

class ZoneInfo(models.Model):
    Zone_Id = models.AutoField(primary_key=True)
    Zone = models.CharField(
        'Zone Name', max_length=120, blank=True, null=True)
    Direction = models.CharField(
        'Zone Direction', max_length=120, blank=True, null=True)
    notes = models.CharField(
        "Notes relate to Zone", max_length=300, blank=True, null=True)        
    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='Zone_creator', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    zoneinfo = ZoneInfoManager()

    class Meta:
        verbose_name_plural = 'Zone info'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.Zone} {self.Direction}'

    def save_model(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.Zone_Id:
            self.slug = slugify(
                f'{self.Zone} {self.Direction}')
        else:
            self.slug = slugify(
                f'{self.Zone_Id} {self.Zone} {self.Direction}')
        super(ZoneInfo, self).save(*args, **kwargs)

class MandalInfo(models.Model):
    Mandal_Id = models.AutoField(primary_key=True)
    Mandal = models.CharField(
        'Mandal Name', max_length=120, blank=True, null=True)
    notes = models.CharField(
        "Notes relate to Mandal", max_length=300, blank=True, null=True)        
    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='Mandal_creator', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    MandalInfo = MandalInfoManager()

    class Meta:
        verbose_name_plural = 'Mandal info'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.Mandal}'

    def save_model(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.Mandal_Id:
            self.slug = slugify(
                f'{self.Mandal}')
        else:
            self.slug = slugify(
                f'{self.Mandal_Id} {self.Mandal}')
        super(MandalInfo, self).save(*args, **kwargs)

class SatsangCategoryInfo(models.Model):
    SatsangCategory_Id = models.AutoField(primary_key=True)
    SatsangCategory = models.CharField(
        'Satsang Category', max_length=120, blank=True, null=True)
    notes = models.CharField(
        "Notes relate to Satsang Category", max_length=300, blank=True, null=True)        
    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='Satsang_Category_creator', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    SatsangCategoryInfo = SatsangCategoryInfoManager()

    class Meta:
        verbose_name_plural = 'Satsang Category info'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.SatsangCategory}'

    def save_model(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.SatsangCategory_Id:
            self.slug = slugify(
                f'{self.SatsangCategory}')
        else:
            self.slug = slugify(
                f'{self.SatsangCategory_Id} {self.SatsangCategory}')
        super(SatsangCategoryInfo, self).save(*args, **kwargs)

class NewUserInfo(models.Model):
    YESNO_CHOICES = (
        ('Yes', 'Y'),
        ('No', 'N'),
    )    
    GENDER_CHOICES = (
        ('Male', 'M'),
        ('Female', 'F'),
        ('None', 'NA'),
    )
    VACCINATED_CHOICES = (
        ('Yes', 'Y'),
        ('No', 'N'),
        ('None', 'NA'),
    )        
    NewUserInfo_Id = models.AutoField(primary_key=True)
    IMS_Member_Id = models.IntegerField('IMS Id', blank=True, null=True)

    prefix = models.CharField(
        'First Name', max_length=120, blank=True, null=True)
    first_name = models.CharField(
        'First Name', max_length=120, blank=True, null=True)
    middle_name = models.CharField(
        'Middle Name', max_length=120, blank=True, null=True)
    last_name = models.CharField(
        'Last Name', max_length=120, blank=True, null=True)
    notes = models.CharField(
        "Notes relate to user", max_length=300, blank=True, null=True)
    Gender = models.CharField(
        'Gender', max_length=10, blank=True, null=True, choices=GENDER_CHOICES, default='N')
    spouse_IMSID = models.IntegerField("Spouse's IMS Id", blank=True, null=True)
    spouse_name = models.CharField(
        "Spouse's First Name", max_length=120, blank=True, null=True)
    father_IMSID = models.IntegerField("Father's IMS Id", blank=True, null=True)
    father_name = models.CharField(
        "Father's First Name", max_length=120, blank=True, null=True)
    mother_IMSID = models.IntegerField("Mother's IMS Id", blank=True, null=True)
    mother_name = models.CharField(
        "Mother's First Name", max_length=120, blank=True, null=True)
    Satsang_Category = models.ForeignKey(
        SatsangCategoryInfo, on_delete=models.DO_NOTHING, related_name='User_Satsang_Category', blank=True, null=True)
    Mandal = models.ForeignKey(
        MandalInfo, on_delete=models.DO_NOTHING, related_name='User_Mandal', blank=True, null=True)

    email = models.EmailField(_('email address'), max_length=120, blank=True, null=True)
    mobile_phone_number = PhoneField(blank=True, help_text='Contact mobile phone number')
    home_phone_number = PhoneField(blank=True, help_text='Contact home phone number')
    Zone_name = models.ForeignKey(
        ZoneInfo, on_delete=models.DO_NOTHING, related_name='Users_Zone', blank=True, null=True)
    comments = models.CharField(
        "Any Comments?", max_length=300, blank=True, null=True)
    vaccinated = models.CharField(
        'Are you vaccinated?', max_length=10, blank=True, null=True, choices=VACCINATED_CHOICES, default='NA')

    User_image = models.ImageField(
        default=default_place_pics, upload_to="place_pics/{tablename}/{field}".format(tablename="User Profile Image", field="Image"), null=True)
    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='User_Info_creator', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    newuserinfo = NewUserInfoManager()

    class Meta:
        verbose_name_plural = 'User info'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.IMS_Member_ID} - {self.last_name}, {self.first_name}'

    def save_model(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.NewUserInfo_Id:
            self.slug = slugify(
                f'{self.IMS_Member_ID} {self.last_name} {self.first_name}')
        else:
            self.slug = slugify(
                f'{self.IMS_Member_ID} {self.last_name} {self.first_name}')
        super(NewUserInfo, self).save(*args, **kwargs)    


class NewUserAddress(models.Model):
    NewUserAddress_Id = models.AutoField(primary_key=True)
    IMS_Member_Id = models.IntegerField('IMS Id', blank=True, null=True)

    Address1 = models.CharField('Address 1', default='NA',
                            blank=True, null=True, max_length=200)
    Address2 = models.CharField('Address 2', default='NA',
                            blank=True, null=True, max_length=200)
    ZipCode = models.DecimalField(
        'Zip Code', max_digits=20, decimal_places=0, blank=True, null=True)
    City = models.CharField('City', max_length=120, blank=True, null=True)
    State = models.CharField('State', max_length=120, blank=True, null=True)
    Country = models.CharField(
        'Country', max_length=120, blank=True, null=True)

    email = models.EmailField(_('email address'), max_length=120, blank=True, null=True)
    mobile_phone_number = PhoneField(blank=True, help_text='Contact mobile phone number')
    home_phone_number = PhoneField(blank=True, help_text='Contact home phone number')
    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='User_Address_creator', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    newuseraddress = NewUserAddressManager()

    class Meta:
        verbose_name_plural = 'User Address'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.NewUserAddress_Id} - {self.email}'

    def save_model(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.NewUserAddress_Id:
            self.slug = slugify(
                f'{self.email}')
        else:
            self.slug = slugify(
                f'{self.NewUserAddress_Id} {self.email}')
        super(NewUserAddress, self).save(*args, **kwargs)    


class ZoneSOLeaderInfo(models.Model):
    ZoneSOLeader_Id = models.AutoField(primary_key=True)
    Zone_SO_Leader_IMSId = models.IntegerField('Leader IMS Id', blank=True, null=True)
    Zone_SO_Leader = models.CharField(
        'Zone Leader First Name', max_length=120, blank=True, null=True)

    Zone_SO_Karyakar_IMSId = models.IntegerField('Karyakar IMS Id', blank=True, null=True)
    Zone_SO_Karyakar = models.CharField(
        'Zone Leader First Name', max_length=120, blank=True, null=True)

    notes = models.CharField(
        "Notes relate to user", max_length=300, blank=True, null=True)

    Zone = models.CharField(
        'Zone Name', max_length=120, blank=True, null=True)
    Direction = models.CharField(
        'Zone Direction', max_length=120, blank=True, null=True)

    comments = models.CharField(
        "Any Comments?", max_length=300, blank=True, null=True)

    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Entered_By = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='Zone_Leader_creator', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    zonesoleaderinfo = ZoneSOLeaderInfoManager()

    class Meta:
        verbose_name_plural = 'Zone SO Leader info'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Karyakar - {self.Zone_SO_Karyakar}, Leader - {self.Zone_SO_Leader}'

    def save_model(self, *args, **kwargs):
        self.Entered_By = current_request().user
        if not self.ZoneSOLeader_Id:
            self.slug = slugify(
                f'{self.Zone_SO_Leader} {self.Zone_SO_Karyakar}')
        else:
            self.slug = slugify(
                f'{self.ZoneSOLeader_Id} {self.Zone_SO_Leader} {self.Zone_SO_Karyakar}')
        super(ZoneSOLeaderInfo, self).save(*args, **kwargs)


class AuditEntry(models.Model):
    class Meta:
        get_latest_by = 'created_at'
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    email = models.CharField(max_length=256, null=True)
    counter = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.email, self.counter, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.email, self.counter, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(ip)
    # ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.filter(
        email=user.email).delete()
    AuditEntry.objects.create(action='user_logged_in',
                              ip=ip, email=user.email)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    # if request.data:
    #     email = request.data["email"]; phonenumber = request.data["phonenumber"]
    # elif request.query_params:
    #     email = request.query_params['email']; phonenumber = request.query_params['phonenumber']

    # if email:
    #     email = email
    # else:
    email = user.email

    AuditEntry.objects.filter(
        email=email).delete()
    AuditEntry.objects.filter(
        email__isnull=True).delete()
    AuditEntry.objects.create(action='user_logged_out',
                            ip=ip, email=email)


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    counter = 1
    logFailed = AuditEntry.objects.filter(
        action='user_login_failed', ip=ip)
# , created_at__year=today.year,
#         created_at__month=today.month,
#         created_at__day=today.day
    if logFailed:
        lastEntered = logFailed.latest()
        lastId = logFailed.values_list('id').order_by('-id')[0][0]
        for rw in logFailed:
            if rw.id == lastId:
                counter = rw.counter + 1
            rw.delete()
        if counter > 2:
            NewUser.objects.filter(
                email=credentials.get('email', None)
            ).update(is_active=False, is_staff=False)

    AuditEntry.objects.create(
        action='user_login_failed', ip=ip, email=credentials.get('email', None), counter=counter)
