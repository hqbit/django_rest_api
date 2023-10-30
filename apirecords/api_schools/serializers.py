from apirecords.api_schools.models import School, Student
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'school_id']
        validators = []

class SchoolSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only = True)
    class Meta:
        model = School
        fields = ['name', 'maximum_capacity', 'students']