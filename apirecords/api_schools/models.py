from django.db import models
from django.core.exceptions import ValidationError

class SchoolManager(models.Manager):
    def create(self, name, maximum_capacity):
        if not isinstance(maximum_capacity, int):
            raise ValidationError("Maximum capacity must be an integer.")
        return super().create(name=name, maximum_capacity=maximum_capacity)

class School(models.Model):
    name = models.CharField(max_length=200, null=True)
    maximum_capacity = models.PositiveIntegerField(null=True)
    objects = SchoolManager()


class Student(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    school_id = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)

    def clean(self):
        super().clean()

        if self.school_id.students.count() >= self.school_id.maximum_capacity:
            raise ValidationError('School has reached maximum capacity.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)