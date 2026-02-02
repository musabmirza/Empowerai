from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'mentor', 'salary', 'created_at')
    search_fields = ('title', 'mentor__username', 'skills_required')
    list_filter = ('mentor', 'created_at')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_link', 'applicant', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('applicant__username', 'job__title', 'cover_letter')
    actions = ['mark_shortlisted', 'mark_rejected']

    def job_link(self, obj):
        # clickable link to job change page in admin (if you want)
        return f"{obj.job.title} (id:{obj.job_id})"
    job_link.short_description = 'Job'

    @admin.action(description='Mark selected applications as Shortlisted')
    def mark_shortlisted(self, request, queryset):
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f"{updated} application(s) marked as shortlisted.")

    @admin.action(description='Mark selected applications as Rejected')
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} application(s) marked as rejected.")
