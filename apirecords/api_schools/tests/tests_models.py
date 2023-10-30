from django.db import IntegrityError
from apirecords.api_schools.models import School, Student
from django.test import TestCase
from django.core.exceptions import ValidationError


class SchoolModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        School.objects.create(name='IES Test Scenario', maximum_capacity=2)

    def test_first_name_label(self):
        school = School.objects.get(id=1)
        field_label = school._meta.get_field('name').name
        self.assertEqual(field_label, 'name')

    def test_first_name_label(self):
        school = School.objects.get(id=1)
        field_label = school._meta.get_field('maximum_capacity').name
        self.assertEqual(field_label, 'maximum_capacity')

    def test_school_name_max_length(self):
        school = School.objects.get(id=1)
        max_length = school._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_school_max_capacity(self):
        school = School.objects.get(id=1)
        maximum_capacity = school.maximum_capacity
        self.assertEqual(maximum_capacity, 2)

    def test_school_max_capacity_negative(self):
        with self.assertRaises(IntegrityError):
            School.objects.create(name='IES Test Scenario 3', maximum_capacity=-1)

    def test_school_max_capacity_not_int(self):
        with self.assertRaises(ValidationError):
            School.objects.create(name='IES Test Scenario 3', maximum_capacity=1.1)
            print(School.objects.get(id=2).maximum_capacity)

    def test_create_school_no_name(self):
        with self.assertRaises(TypeError):
            School.objects.create(maximum_capacity=1)
    def test_create_school_no_max_capacity(self):
        with self.assertRaises(TypeError):
            School.objects.create(name='IES Test Scenario 2')



class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        School.objects.create(name='IES Test Scenario', maximum_capacity=1)
        School.objects.create(name='IES Test Scenario', maximum_capacity=4)
        Student.objects.create(first_name='Fernando', last_name='Perez', school_id=School.objects.get(id=1))

    def test_first_name_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('first_name').name
        self.assertEqual(field_label, 'first_name')

    def test_last_name_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('last_name').name
        self.assertEqual(field_label, 'last_name')

    def test_student_first_name_max_length(self):
        student = Student.objects.get(id=1)
        max_length = student._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 200)

    def test_student_last_name_max_length(self):
        student = Student.objects.get(id=1)
        max_length = student._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 200)

    def test_create_student_above_capacity(self):
        with self.assertRaises(ValidationError):
            Student.objects.create(first_name='Fernando2', last_name='Perez2', school_id=School.objects.get(id=1))

    def test_create_student_no_first_name(self):
        with self.assertRaises(ValidationError):
            Student.objects.create(last_name='Perez3', school_id=School.objects.get(id=2))

    def test_create_student_no_last_name(self):
        with self.assertRaises(ValidationError):
            Student.objects.create(first_name='Fernando3', school_id=School.objects.get(id=2))

    def test_create_student_no_school_id(self):
        with self.assertRaises(School.DoesNotExist):
            Student.objects.create(first_name='Fernando3', last_name='Perez3')