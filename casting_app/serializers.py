from rest_framework import serializers

from .models import Application, Company, Project, Role, Talent


class TalentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talent
        fields = ['name', 'email', 'phone_number', 'age', 'gender', 'ethnicity', 'weight', 'height']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'email', 'description']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        """Making sure no duplicate projects are created."""

        if self.Meta.model.objects.filter(name__icontains=validated_data['name'].lower()).exists():
            raise serializers.ValidationError('A project with this name exists before')
        return super().create(validated_data)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data):
        """Making sure no duplicate roles are created within a project."""

        if self.Meta.model.objects.filter(
            name=validated_data['name'],
            project=validated_data['project'],
            talent_age=validated_data['talent_age'],
            talent_gender=validated_data['talent_gender'],
            talent_ethnicity=validated_data['talent_ethnicity'],
            talent_weight=validated_data['talent_weight'],
            talent_height=validated_data['talent_height'],
        ).exists():
            raise serializers.ValidationError('This role already exists in this project')
        return super().create(validated_data)


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['talent', 'role']

    def validate(self, data):
        """Stating some validations for application auto-rejection."""

        talent = data['talent']
        role = data['role']
        errors = []
        if talent.gender != role.talent_gender:
            errors.append('gender')
        if talent.ethnicity != role.talent_ethnicity:
            errors.append('ethnicity')
        if not role.talent_age - 5 <= talent.age <= role.talent_age + 5:
            errors.append('age')
        if not role.talent_weight - 5 <= talent.weight <= role.talent_weight + 5:
            errors.append('weight')
        if not role.talent_height - 5 <= talent.height <= role.talent_height + 5:
            errors.append('height')

        if errors:
            raise serializers.ValidationError(f'Application declined. Unsatisfied criteria of the role: {errors}')

        return super().validate(data)
