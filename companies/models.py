import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField

from contact_trace.unique_slug import generate_unique_slug


STATES = (
        (None, '---'),
        ('AK', 'Alaska'),
        ('AL', 'Alabama'),
        ('AR', 'Arkansas'),
        ('AZ', 'Arizona'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DC', 'District of Columbia'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('IA', 'Iowa'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('MA', 'Massachusetts'),
        ('MD', 'Maryland'),
        ('ME', 'Maine'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MO', 'Missouri'),
        ('MS', 'Mississippi'),
        ('MT', 'Montana'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('NE', 'Nebraska'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NV', 'Nevada'),
        ('NY', 'New York'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VA', 'Virginia'),
        ('VT', 'Vermont'),
        ('WA', 'Washington'),
        ('WI', 'Wisconsin'),
        ('WV', 'West Virginia'),
        ('WY', 'Wyoming')
    )


class Company(models.Model):

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    created = models.DateTimeField(
        default=timezone.now,
    )
    name = models.CharField(
        max_length=300,
        default=''
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
    )
    address1 = models.CharField(
        max_length=1024,
        null=True,
        blank=True
    )
    address2 = models.CharField(
        max_length=1024,
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=1024,
        null=True,
        blank=True
    )
    state = models.CharField(
        max_length=2,
        choices=STATES,
        null=True,
        blank=True
    )
    zip_code = models.CharField(
        max_length=5,
        null=True,
        blank=True
    )
    website = models.URLField(
        null=True,
        blank=True
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        region='US'
    )
    admins = models.ManyToManyField(
        'users.CustomUser',
        related_name='biz_admins',
        blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.name) != self.slug:
                self.slug = generate_unique_slug(Company, self.name)
        else:  # create
            self.slug = generate_unique_slug(Company, self.name)

        super(Company, self).save(*args, **kwargs)


class WaitList(models.Model):

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    submitted = models.DateTimeField(
        default=timezone.now,
    )
    email = models.EmailField()
