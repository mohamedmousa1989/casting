from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class Talent(models.Model):
    """A model representing a talent."""

    name = models.CharField(max_length=50)
    email = models.EmailField(db_index=True)
    phone_number = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=50)
    weight = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        """String representation of the talent."""

        return self.name


class Company(models.Model):
    """A model representing a company."""

    name = models.CharField(max_length=50)
    email = models.EmailField(db_index=True)
    description = models.TextField()

    def __str__(self):
        """String representation of the company."""

        return self.name


class Project(models.Model):
    """A model representing a project."""

    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=50)

    def get_roles(self):
        return Role.objects.filter(project=self).values_list('name', flat=True)

    def __str__(self):
        """String representation of the project."""

        return self.name


class Role(models.Model):
    """A model representing a role assigned to a project."""

    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    talent_age = models.IntegerField()
    talent_gender = models.CharField(max_length=50)
    talent_ethnicity = models.CharField(max_length=50)
    talent_weight = models.FloatField()
    talent_height = models.FloatField()

    def __str__(self):
        """String representation of the role."""

        return f'{self.name} - {self.project.name}'


class Application(models.Model):
    """A model representing an application for a role."""

    talent = models.ForeignKey(Talent, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    datetime_applied = models.DateTimeField(auto_now_add=True)
