from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

#Automatically generates auth-token for users saved in the system
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):
    """ Manager for users"""
    def create_user(self,email,password):
        """ creates a new user"""

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self,email,password):
        """ Creates a super user"""
        user = self.create_user(email,password)

        user.is_staff= True
        user.is_bank_clerk= True
        user.is_superuser = True
        user.save(using= self._db)

        return user


class User(AbstractBaseUser,PermissionsMixin):
    """ Database model for users"""
    email = models.EmailField(max_length=255, unique=True)
    is_bank_clerk = models.BooleanField(default=False)
    is_loan_provider = models.BooleanField(default=False)
    is_loan_taker = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def str(self):
        """ returns string representation of object"""
        return self.email

class LoanFund(models.Model):
    MaxAmount=models.IntegerField()
    MinAmount=models.IntegerField()
    InterestRate=models.IntegerField()
    Duration=models.IntegerField()

class Loan(models.Model):
    MaxAmount=models.IntegerField()
    MinAmount=models.IntegerField()
    InterestRate=models.IntegerField()
    Duration=models.IntegerField()


class LoanProvider(models.Model):
    Name=models.CharField(max_length=50)
    NationalId=models.CharField(max_length=50)
    MobileNumber=models.CharField(max_length=11)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class LoanTaker(models.Model):
    Name=models.CharField(max_length=50)
    NationalId=models.CharField(max_length=50)
    MobileNumber=models.CharField(max_length=11)
    IScore=models.BooleanField(default=False)  
    user=models.OneToOneField(User,on_delete=models.CASCADE) 

class LoanFundApplication(models.Model):
    Amount=models.IntegerField()
    LoanFund=models.ForeignKey(LoanFund,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,default='Applied')
    LoanProvider=models.ForeignKey(LoanProvider,on_delete=models.CASCADE)

class LoanApplication(models.Model):
    Amount=models.IntegerField()
    Loan=models.ForeignKey(Loan,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,default='Applied')
    LoanTaker=models.ForeignKey(LoanTaker,on_delete=models.CASCADE)    