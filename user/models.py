from django.db import models 
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 
import uuid

class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            name=name,
            email=self.normalize_email(email),
         
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):
        user = self.create_user(
            name=name,
            email=email,
            password=password,
     
            
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ('MEM', 'Member'),
        ('LIB', 'Librarian'),
        ('ADM', 'Admin'),
    ]
    
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50, blank=True)
    roll = models.PositiveIntegerField(default=0)
    department = models.CharField(max_length=100, blank=True, null=True)
    session = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    membership_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    user_type = models.CharField(
        max_length=3,
        choices=USER_TYPE_CHOICES,
        default='MEM',
    )
    image = models.ImageField(
        upload_to='user_image/',
        blank=True,
        null=True 
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]


    def __str__(self):
        return self.email
    
    def generate_unique_membership_number(self):
        """
        Generates a unique membership number.
        """
        while True:
            # Generate a new unique membership number
            membership_number = f'{uuid.uuid4().hex[:8].upper()}'
            if not User.objects.filter(membership_number=membership_number).exists():
                return membership_number
    def save(self, *args, **kwargs):
        if not self.membership_number:
            self.membership_number = self.generate_unique_membership_number()
        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
