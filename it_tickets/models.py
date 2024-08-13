from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import random
import string



class Customer(models.Model):

    name = models.CharField(max_length=200, null=True)
    short_name = models.CharField(max_length=3, null=True)
    
    def __str__(self):

        return self.name

    


class Department(models.Model):

    name = models.CharField(max_length=200, null=True, unique=True)
    short_name = models.CharField(max_length=10, null=True, unique=True)
    description = models.TextField(max_length=500, null=True)

    def __str__(self):

        return self.name
    


class User(AbstractUser):

    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):

        return  self.username


class Workrole(models.Model):

    name = models.CharField(max_length=200, null=True, unique=True)
    description = models.TextField(max_length=500, null=True)

    def __str__(self):

        return self.name



class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    log_count = models.IntegerField(default=0)
    department = models.ForeignKey(Department,null=True ,on_delete=models.SET_NULL)
    workrole = models.ManyToManyField(Workrole, blank=True)
    avatar = models.ImageField(null=True,upload_to="images/user_images",default="images/default_user.jpg")
    bio = models.TextField(max_length=400, null=True)
    department_manager = models.BooleanField(default=False, blank=True)
    on_call_person = models.BooleanField(default=False, blank=True)
    

    def __str__(self):

        return f'{self.user.first_name}-{self.user.last_name}'
    
 
        
        



def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)





class Ticket(models.Model):
     
    class TicketPriority(models.TextChoices):
        INFO = "INFO", 'INFO'
        WARNING = "WARNING",'WARNING'
        CRITICAL = "CRITICAL",'CRITICAL'
        FATAL = "FATAL",'FATAL'

    class Resolution_Status(models.TextChoices):

        QUEUED ="QUEUED", 'QUEUED'
        INPROGRESS = "INPROGRESS" , 'INPROGRESS'
        RESOLVED = "RESOLVED" , 'RESOLVED'
        CLOSED = "CLOSED", 'CLOSED'


    ticket_id = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=150,blank=True, null=True)
    ticket_description = models.TextField(max_length=500, blank=True)
    dispacher_department = models.ForeignKey(Department, null=True ,on_delete=models.SET_NULL,related_name="dispacher_dep")
    dispacher_profile = models.ForeignKey(Profile, null=True ,on_delete=models.SET_NULL, related_name="dispacher_prof")
    resolver_department = models.ForeignKey(Department, null=True ,on_delete=models.SET_NULL, related_name="resolver_dep")
    resolver_profile = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL,related_name='resolver_prof')
    priority = models.CharField(max_length=20, choices=TicketPriority.choices, default=TicketPriority.INFO)
    status = models.CharField(max_length=20, choices=Resolution_Status.choices, default=Resolution_Status.QUEUED)
    customer = models.ForeignKey(Customer, null=True ,on_delete=models.SET_NULL,related_name="cust")
    resolution_status = models.TextField(max_length=500, null=True, blank=True)
    opened = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):

       return self.ticket_id 
    



class RandomTokenGenerator(object):
    def __init__(self, chars=None, random_generator=None):
        self.chars = string.digits
        self.random_generator = random_generator or random.SystemRandom()

    def make_token(self, n=20):
        return ''.join(self.random_generator.choice(self.chars) for _ in range(n))

token_generator = RandomTokenGenerator()
token = token_generator.make_token(10)


@receiver(pre_save, sender=Ticket)
def ticket_pre_save(sender, instance, *args, **kwargs):

    if not  instance.ticket_id:
        instance.ticket_id = f'IN-{token}'
 


