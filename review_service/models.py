from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class PersonManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    objects = PersonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, review_cycle=None):
        try:
            if isinstance(review_cycle, ReviewCycle) and \
                    self.pk is review_cycle.creator_id:
                return True
            return False
        except:
            return False


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class ReviewCycle(models.Model):
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='+')
    reviewees = models.ManyToManyField(Person, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
