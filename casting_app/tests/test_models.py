from django.test import TestCase

from ..models import Company, Project, Role, Talent


class TalentTest(TestCase):
    """Test module for Talent model"""

    def setUp(self):
        self.talent_1 = Talent.objects.create(
            name='Mohamed Mousa', age=33, email='test@yahoo.com', gender='male', weight=88, height=170
        )
        self.talent_2 = Talent.objects.create(
            name='Ameer Anwar', age=40, email='test1@yahoo.com', gender='male', weight=88, height=175
        )

    def test_unicode(self):
        """Test __str__ function."""

        self.assertEqual(str(self.talent_1), self.talent_1.name)
        self.assertEqual(str(self.talent_2), self.talent_2.name)


class RoleTest(TestCase):
    """Test module for Talent model"""

    def setUp(self):
        self.company = Company.objects.create(name='seedstars', email='test@seed.com', description='test')
        self.project = Project.objects.create(
            company=self.company, name="Eagle eye", description="test description", location="Cairo"
        )
        self.role = Role.objects.create(
            name='officer',
            project=self.project,
            talent_age=33,
            talent_ethnicity='white',
            talent_gender='male',
            talent_weight=88,
            talent_height=170,
        )

    def test_unicode(self):
        """Test __str__ function."""

        self.assertEqual(str(self.role), f'{self.role.name} - {self.project.name}')
        self.assertEqual(str(self.project), self.project.name)
