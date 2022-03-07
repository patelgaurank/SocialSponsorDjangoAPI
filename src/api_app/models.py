from django.db import models


def upload_place_pics(instance, filename):
    # return "place_pics/{user}/{filename}".format(user=instance.user, filename=filename)
    return "users/{filename}".format(filename=filename)


def default_place_pics():
    return "users/default_pic.jpg"


class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        default=default_place_pics, upload_to=upload_place_pics, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_at')

    def __str__(self):
        return self.name


class UserData(models.Model):

    class UserDataObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(UserActive='active')

    options = (
        ('active', 'Active'),
        ('not active', 'Not Active'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    UserId = models.CharField(max_length=100)
    UserPassword = models.CharField(max_length=20)
    # UserActive = models.CharField(
    #     max_length=10, choices=options, default='active'
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    # slug = models.SlugField(max_length=250, unique_for_date='created_at')
    objects = models.Manager()

    def __str__(self):
        return self.email

class url(models.Model):
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=300)
    url = models.CharField(max_length=300)    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name