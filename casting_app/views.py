from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Application, Project, Role, Talent
from .serializers import (
    ApplicationSerializer,
    CompanySerializer,
    ProjectSerializer,
    RoleSerializer,
    TalentSerializer,
)


class TalentCreate(generics.CreateAPIView):
    """Create a talent."""

    serializer_class = TalentSerializer


class TalentRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """Get a talent and update it."""

    serializer_class = TalentSerializer
    queryset = Talent.objects.all()
    lookup_field = 'pk'


class CompanyCreate(generics.CreateAPIView):
    """Create a company."""

    serializer_class = CompanySerializer


class ProjectCreate(generics.CreateAPIView):
    """Create a project."""

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class RoleCreate(generics.CreateAPIView):
    """Create a role and assign it to a project."""

    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class ApplicationCreate(generics.CreateAPIView):
    """Apply for a role."""

    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()


class ApplicationList(APIView):
    """Show talents who applies for a certain role."""

    def get(self, request, role_id):
        """Override get method."""

        role = Role.objects.get(id=role_id)
        applicants = Application.objects.filter(role=role).values_list('talent__id', flat=True)
        talents = Talent.objects.filter(id__in=applicants)
        serializer = TalentSerializer(talents, many=True)

        return Response(serializer.data)
