from django.contrib import admin
from django.urls import path
from core.views import (
    signup_view,
    login_view,
    logout_view,
    dashboard,
    mentor_dashboard,
    housewife_dashboard,
    create_job,
    mentor_jobs,
    jobs_list,
    job_detail,
    my_applications,
    view_applicants,
    upload_resume,
    notifications_view, 
)
# from rest_framework import routers
# from core.api_views import JobViewSet, ApplicationViewSet
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# router = routers.DefaultRouter()
# router.register(r'jobs', JobViewSet, basename='api-jobs')
# router.register(r'applications', ApplicationViewSet, basename='api-applications')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', logout_view, name="logout"),
    path('dashboard/', dashboard, name="dashboard"),

    # ROLE-BASED DASHBOARDS
    path('mentor/', mentor_dashboard, name="mentor_dashboard"),
    path('housewife/', housewife_dashboard, name="housewife_dashboard"),

    # JOBS (mentor)
    path('create-job/', create_job, name='create_job'),
    path('mentor-jobs/', mentor_jobs, name='mentor_jobs'),

    # JOBS - public / housewife
    path('jobs/', jobs_list, name='jobs_list'),
    path('jobs/<int:pk>/', job_detail, name='job_detail'),

    # Applications
    path('applications/', my_applications, name='my_applications'),

    # Mentor: applicants for specific job
    path('job/<int:job_id>/applicants/', view_applicants, name='view_applicants'),

    path('jobs/', jobs_list, name='jobs_list'),
    
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/', include(router.urls)),

    path('upload-resume/', upload_resume, name='upload_resume'),

    path('notifications/', notifications_view, name='notifications'),


]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )



