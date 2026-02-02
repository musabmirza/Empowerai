from rest_framework import serializers
from .models import Job, Application
from django.conf import settings

class JobSerializer(serializers.ModelSerializer):
    mentor_username = serializers.ReadOnlyField(source='mentor.username')

    class Meta:
        model = Job
        fields = ['id','title','description','skills_required','salary','created_at','mentor','mentor_username']
        read_only_fields = ['mentor','mentor_username','created_at']

class ApplicationSerializer(serializers.ModelSerializer):
    applicant_username = serializers.ReadOnlyField(source='applicant.username')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = Application
        fields = ['id','job','job_title','applicant','applicant_username','cover_letter','status','applied_at']
        read_only_fields = ['applicant','applicant_username','status','applied_at','job_title']
