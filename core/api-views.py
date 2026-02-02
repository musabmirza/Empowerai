from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Permission helper
class IsMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'mentor')

class IsHousewife(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'housewife')


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsMentor()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('-applied_at')
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        # list/retrieve: mentors can view applicants for their jobs; applicants can view their own
        if self.action in ['create']:
            return [IsAuthenticated(), IsHousewife()]
        if self.action in ['list']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # Expect job id in payload
        job_id = request.data.get('job')
        job = get_object_or_404(Job, pk=job_id)
        # prevent mentor applying
        if request.user.role != 'housewife':
            return Response({'detail':'Only housewives can apply.'}, status=status.HTTP_403_FORBIDDEN)
        # prevent duplicate
        if Application.objects.filter(job=job, applicant=request.user).exists():
            return Response({'detail':'Already applied.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(applicant=request.user, job=job)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Application.objects.none()
        if user.role == 'mentor':
            # mentor sees applications only for their jobs
            return Application.objects.filter(job__mentor=user).select_related('job','applicant')
        else:
            # housewife sees their own applications
            return Application.objects.filter(applicant=user).select_related('job')
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsMentor])
    def set_status(self, request, pk=None):
        app = self.get_object()
        # only mentor of the job can change status
        if app.job.mentor != request.user:
            return Response({'detail':'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        status_val = request.data.get('status')
        if status_val not in ['pending','shortlisted','rejected']:
            return Response({'detail':'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        app.status = status_val
        app.save()
        return Response({'detail':'Status updated', 'status': app.status})
