from rest_framework import viewsets, status
from django.db.models import Q
from apirecords.api_schools.models import School, Student
from apirecords.api_schools.serializers import SchoolSerializer, StudentSerializer
from rest_framework.response import Response


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        # Get the school ID from the request data
        school_id = request.data.get('school_id')
        try:
            school = School.objects.get(pk=school_id)
        except School.DoesNotExist:
            return Response({'message': 'School not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Checking if school is full
        if school.students.count() >= school.maximum_capacity:
            return Response({'message': 'School is full'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = Student.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
        else:
            queryset = Student.objects.all()
        return queryset
    

class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows schools to be viewed
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = School.objects.filter(Q(name__icontains=search_query))
        else:
            queryset = School.objects.all()
        return queryset
    

