from django.db import models
from django.contrib.auth.models import ( PermissionsMixin, UserManager, AbstractBaseUser)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.apps import apps
from django.contrib.auth.hashers import make_password
import jwt
from django.conf import settings
from datetime import datetime, timedelta
# Create your models here.


class MyUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # if not username:
        #     raise ValueError("The given username must be set")
        
        if not email:
            raise ValueError("The given email must be set")
        
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        # username = GlobalUserModel.normalize_username(username)
        # username = username,
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # username
        return self._create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    # username = models.CharField(
    #     _("username"),
    #     max_length=150,
    #     unique=True,
    #     blank=True,
    #     help_text=_(
    #         "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    #     ),
    #     validators=[username_validator],
    #     error_messages={
    #         "unique": _("A user with that username already exists."),
    #     },
    # )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = MyUserManager()
    email_verified = models.BooleanField(
        _("email_verified"),
        default=False,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    phone_number = models.CharField(max_length=25, blank=True)
    location = models.CharField(max_length=300, blank=True)
    designation = models.CharField(max_length=110, blank=True)
    cv = models.FileField(upload_to="cv/", blank=True)

    #for the employers
    company_name = models.CharField(max_length=100, blank=True)
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['-created_at']

    @property
    def token(self):
        token = jwt.encode({'email': self.email, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, algorithm="HS256")

        return token
    
class JobPost(models.Model):
    employetype= (
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    jobtitle=models.CharField(max_length=100, null=True, blank=True)
    descriptions= models.CharField(max_length=250, null=True, blank=True)
    emptype= models.CharField(choices=employetype, max_length=100, null=True, blank=True)
    location=models.CharField(max_length=100, null=True, blank=True)
    worktype=models.CharField(max_length=20,choices=(('Onsite', 'Onsite'), ('Remote', 'Remote')), null=True, blank=True)
    responsibilities= models.CharField(max_length=500, null=True, blank=True)
    benifits=models.CharField(max_length=200, null=True, blank=True)
    minsalary= models.FloatField()
    maxsalary= models.FloatField()
    salarytype=models.CharField(max_length=20,choices=(('Monthly', 'Monthly'), ('Yearly', 'Yearly')), null=True, blank=True)
    postdate=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.email)

