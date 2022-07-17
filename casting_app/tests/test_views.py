import json

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from ..models import Application, Company, Project, Role, Talent
from ..serializers import TalentSerializer

# initialize the APIClient app
client = Client()


class CreateNewTalentTest(TestCase):
    """Test module for inserting a new talent."""

    def setUp(self):
        self.valid_payload = {
            'name': 'Mohamed Mousa',
            'age': 33,
            'email': 'test@yahoo.com',
            'phone_number': '010021445221',
            'gender': 'male',
            'ethnicity': 'white',
            'weight': 88,
            'height': 178,
        }
        self.invalid_payload = {
            'name': '',
            'age': 'fourty',
            'email': 'test@yahoo.com',
            'phone_number': '010021445221',
            'gender': 'male',
            'ethnicity': 'white',
            'weight': 88,
            'height': 178,
        }

    def test_create_valid_talent(self):
        response = client.post(
            reverse('talent_create'), data=json.dumps(self.valid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Talent.objects.count(), 1)
        self.assertEqual(Talent.objects.first().name, 'Mohamed Mousa')
        self.assertEqual(Talent.objects.first().age, 33)
        self.assertEqual(Talent.objects.first().email, 'test@yahoo.com')
        self.assertEqual(Talent.objects.first().phone_number, '010021445221')
        self.assertEqual(Talent.objects.first().gender, 'male')
        self.assertEqual(Talent.objects.first().ethnicity, 'white')
        self.assertEqual(Talent.objects.first().weight, 88)
        self.assertEqual(Talent.objects.first().height, 178)

    def test_create_invalid_talent(self):
        response = client.post(
            reverse('talent_create'), data=json.dumps(self.invalid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Talent.objects.count(), 0)


class GetSingleTalentTest(TestCase):
    """Test module for GET single talent API."""

    def setUp(self):
        self.talent_1 = Talent.objects.create(
            name='Mohamed Mousa', age=33, email='test@yahoo.com', gender='male', weight=88, height=170
        )

    def test_get_valid_single_talent(self):
        response = client.get(reverse('talent_get_update', kwargs={'pk': self.talent_1.pk}))
        serializer = TalentSerializer(self.talent_1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_talent(self):
        response = client.get(reverse('talent_get_update', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleTalentTest(TestCase):
    """Test module for updating an existing talent record."""

    def setUp(self):
        self.talent_1 = Talent.objects.create(
            name='Mohamed Mousa', age=33, email='test@yahoo.com', gender='male', weight=88, height=170
        )
        self.valid_payload = {
            'name': 'Mohamed Mousa',
            'age': 38,
            'email': 'test@yahoo.com',
            'phone_number': '010021445221',
            'gender': 'male',
            'ethnicity': 'white',
            'weight': 82,
            'height': 178,
        }
        self.invalid_payload = {
            'name': 'Mohamed Mousa',
            'age': 33,
            'email': '',
            'phone_number': '010021445221',
            'gender': '',
            'ethnicity': 'white',
            'weight': 82,
            'height': 178,
        }

    def test_valid_update_talent(self):
        response = client.put(
            reverse('talent_get_update', kwargs={'pk': self.talent_1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.talent_1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.talent_1.age, 38)

    def test_invalid_update_talent(self):
        response = client.put(
            reverse('talent_get_update', kwargs={'pk': self.talent_1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNewCompanyTest(TestCase):
    """Test module for inserting a new company."""

    def setUp(self):
        self.valid_payload = {'name': 'Seedstars', 'email': 'test@yahoo.com', 'description': 'test'}
        self.invalid_payload = {'name': '', 'email': 'test@yahoo.com', 'description': ''}

    def test_create_valid_company(self):
        response = client.post(
            reverse('company_create'), data=json.dumps(self.valid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.first().name, 'Seedstars')
        self.assertEqual(Company.objects.first().description, 'test')
        self.assertEqual(Company.objects.first().email, 'test@yahoo.com')

    def test_create_invalid_company(self):
        response = client.post(
            reverse('company_create'), data=json.dumps(self.invalid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(), 0)


class CreateNewProjectTest(TestCase):
    """Test module for inserting a new project."""

    def setUp(self):
        self.company = Company.objects.create(name='seedstars', email='test@seed.com', description='test')
        self.valid_payload = {
            'company': str(self.company.pk),
            'name': 'Eagle eye',
            'location': 'Cairo',
            'description': 'test',
        }
        self.invalid_payload = {'name': '', 'location': 'Minia', 'description': ''}

    def test_create_valid_project(self):
        response = client.post(
            reverse('project_create'), data=json.dumps(self.valid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().name, 'Eagle eye')
        self.assertEqual(Project.objects.first().description, 'test')
        self.assertEqual(Project.objects.first().location, 'Cairo')

    def test_create_invalid_project(self):
        response = client.post(
            reverse('project_create'), data=json.dumps(self.invalid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Project.objects.count(), 0)


class CreateNewRoleTest(TestCase):
    """Test module for inserting a new role."""

    def setUp(self):
        self.company = Company.objects.create(name='seedstars', email='test@seed.com', description='test')
        self.project = Project.objects.create(
            company=self.company, name="Eagle eye", description="test description", location="Cairo"
        )
        self.valid_payload = {
            'name': 'pilot',
            'project': str(self.project.pk),
            'talent_age': 25,
            'talent_weight': 75,
            'talent_height': 180,
            'talent_gender': 'male',
            'talent_ethnicity': 'white',
        }
        self.invalid_payload = {
            'talent_age': 'fourty',
            'talent_weight': 75,
            'talent_height': 'white',
            'talent_gender': 'male',
            'talent_ethnicity': 'white',
        }

    def test_create_valid_role(self):
        response = client.post(
            reverse('role_create'), data=json.dumps(self.valid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 1)
        self.assertEqual(Role.objects.first().name, 'pilot')
        self.assertEqual(Role.objects.first().project.pk, 1)
        self.assertEqual(Role.objects.first().talent_age, 25)
        self.assertEqual(Role.objects.first().talent_weight, 75)
        self.assertEqual(Role.objects.first().talent_height, 180)
        self.assertEqual(Role.objects.first().talent_gender, 'male')
        self.assertEqual(Role.objects.first().talent_ethnicity, 'white')

    def test_create_invalid_role(self):
        response = client.post(
            reverse('role_create'), data=json.dumps(self.invalid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Role.objects.count(), 0)


class ApplicationCreateTest(TestCase):
    """Test creating an application to a certain role."""

    def setUp(self):
        self.company = Company.objects.create(name='seedstars', email='test@seed.com', description='test')
        self.project = Project.objects.create(
            company=self.company, name="Eagle eye", description="test description", location="Cairo"
        )
        self.talent = Talent.objects.create(
            name='Mohamed Mousa',
            age=33,
            email='test@yahoo.com',
            gender='male',
            weight=88,
            height=170,
            ethnicity='white',
        )
        self.role = Role.objects.create(
            name='pilot',
            project=self.project,
            talent_age=35,
            talent_gender='male',
            talent_ethnicity='white',
            talent_weight=85,
            talent_height=172,
        )
        self.valid_payload = {
            'talent': str(self.talent.pk),
            'role': str(self.role.pk),
        }
        self.invalid_payload = {
            'talent': '22',
            'role': '50',
        }

    def test_create_valid_role(self):
        response = client.post(
            reverse('application_create'), data=json.dumps(self.valid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.first().talent.name, 'Mohamed Mousa')
        self.assertEqual(Application.objects.first().role.name, 'pilot')

    def test_create_invalid_role(self):
        response = client.post(
            reverse('application_create'), data=json.dumps(self.invalid_payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(), 0)


class ApplicationListTest(TestCase):
    """Test listing applications for a certain role."""

    def setUp(self):
        self.company = Company.objects.create(name='seedstars', email='test@seed.com', description='test')
        self.project = Project.objects.create(
            company=self.company, name="Eagle eye", description="test description", location="Cairo"
        )
        self.role = Role.objects.create(
            name='pilot',
            project=self.project,
            talent_age=35,
            talent_gender='male',
            talent_ethnicity='white',
            talent_weight=85,
            talent_height=172,
        )
        self.talent_1 = Talent.objects.create(
            name='Mohamed Mousa', age=33, email='test@yahoo.com', gender='male', weight=88, height=170
        )
        self.talent_2 = Talent.objects.create(
            name='Mohamed Ahmed', age=35, email='test1@yahoo.com', gender='male', weight=84, height=175
        )
        self.talent_3 = Talent.objects.create(
            name='Kamal Ezz', age=38, email='test2@yahoo.com', gender='male', weight=86, height=173
        )
        self.application_1 = Application.objects.create(talent=self.talent_1, role=self.role)
        self.application_2 = Application.objects.create(talent=self.talent_2, role=self.role)
        self.application_3 = Application.objects.create(talent=self.talent_3, role=self.role)

    def test_list_applicants_for_a_role(self):
        response = client.get(
            reverse('application_list', kwargs={'role_id': self.role.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
