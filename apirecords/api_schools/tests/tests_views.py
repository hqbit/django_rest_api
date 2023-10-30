from django.test import TestCase
from apirecords.api_schools.models import Student, School


class SchoolViewSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_schools = 10
        for school_id in range(number_of_schools):
            School.objects.create(
                name = f'IES test {school_id}',
                maximum_capacity = 5
            )

    def test_view_url_at_desired_location(self):
        # List schools
        response = self.client.get('/api/school/')
        self.assertEqual(response.status_code, 200)

        # Check each school exists at desired location
        number_of_schools = 10
        for school_id in range(1, number_of_schools+1):
            response = self.client.get(f'/api/school/{school_id}/')
            self.assertEqual(response.status_code, 200)
       
        # Check each school does NOT exist at desired location
        response = self.client.get(f'/api/school/11/')
        self.assertEqual(response.status_code, 404)

    def test_delete_school(self):
        response = self.client.delete('/api/school/10/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/school/10/')
        self.assertEqual(response.status_code, 404)

    def test_retrieve_school(self):
        response = self.client.get('/api/school/', {'search':1})
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"name":"IES test 1","maximum_capacity":5, "students":[]}])



class StudentViewSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        school_test = School.objects.create(
                name = f'IES test x',
                maximum_capacity = 10
            )
        
        number_of_students = 10
        for i in range(number_of_students):
            Student.objects.create(
                first_name = f'Alberto{i}',
        	    last_name = f'Fernandez{i}',
                school_id = school_test
            )

    def test_view_url_at_desired_location(self):
        # List students
        response = self.client.get('/api/student/')
        self.assertEqual(response.status_code, 200)

        # Check each student exists at desired location
        number_of_students = 10
        for student_number in range(1, number_of_students+1):
            response = self.client.get(f'/api/student/{student_number}/')
            self.assertEqual(response.status_code, 200)
        
        # Check each student does NOT exist at desired location
        response = self.client.get('/api/student/11/')
        self.assertEqual(response.status_code, 404)

    def test_delete_student(self):
        response = self.client.delete('/api/student/10/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/student/10/')
        self.assertEqual(response.status_code, 404)

    def test_retrieve_student(self):
        response = self.client.get('/api/student/', {'search':1})
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"first_name":"Alberto1","last_name":"Fernandez1","school_id":1}])
