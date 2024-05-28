from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,PermissionsMixin)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,full_name='null',phone_number=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),full_name=full_name,
                          phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user
  
    def create_superuser(self, email, password):
        user = self.create_user(email,password=password,full_name="SITE CREATOR",)
        user.is_admin = True
        user.staff=True
        user.is_super_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    full_name =models.CharField(verbose_name='full name', max_length=255)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    phone_number = models.CharField("phone_number", max_length=20,null=True,blank=True)
    is_super_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    staff=models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        if not self.is_super_admin:
            if perm =="Users.add_user" or perm=="Users.change_user" or perm=="Users.delete_user":
                return False
            else:
                return True
        else:
            return True

    # remember to set appropriate permissions.
    def has_module_perms(self, app_label):
        if not self.is_super_admin:
            if app_label =="knox" or app_label=="auth" :
                return False
            else:
                return True
        else:
            return True
    @property

    def is_staff(self):
        return self.staff


class Staff(models.Model):
    account = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="Account")
    verified = models.BooleanField(default=False)
    can_publish  = models.BooleanField(default=False)
    job_description = models.TextField("job description", max_length=150, null=True)

    def __str__(self):
        return self.account.full_name

    class Meta:
        managed = True
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'
        
        

