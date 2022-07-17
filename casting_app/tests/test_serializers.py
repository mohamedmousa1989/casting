from django.test import TestCase

from ..models import Application, Company, Project, Role, Talent
from ..serializers import TalentSerializer


class TalentSerializerTest(TestCase):
    def setUp(self):
        self.talent = Talent.objects.create(
            name='Mohamed Mousa',
            age=33,
            phone_number='01002145214',
            email='test@yahoo.com',
            gender='male',
            weight=88,
            height=170,
            ethnicity='white',
        )

        self.serializer = TalentSerializer(instance=self.talent)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(
            set(data.keys()), set(['name', 'age', 'phone_number', 'email', 'gender', 'weight', 'height', 'ethnicity'])
        )
        self.assertEqual(data['name'], self.talent.name)
        self.assertEqual(data['age'], self.talent.age)
        self.assertEqual(data['phone_number'], self.talent.phone_number)
        self.assertEqual(data['email'], self.talent.email)
        self.assertEqual(data['gender'], self.talent.gender)
        self.assertEqual(data['weight'], self.talent.weight)
        self.assertEqual(data['height'], self.talent.height)
        self.assertEqual(data['ethnicity'], self.talent.ethnicity)
