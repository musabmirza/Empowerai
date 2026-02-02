from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from PyPDF2 import PdfReader

from .forms import SignupForm, JobForm
from .models import Job, Application, Notification
from .skill_extractor import extract_skills_from_text
from .utils import calculate_match_score


# ================= AUTH =================

def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            if user.role == 'mentor':
                return redirect('mentor_dashboard')
            elif user.role == 'housewife':
                return redirect('housewife_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # fallback dashboard
    if request.user.role == 'mentor':
        return redirect('mentor_dashboard')
    elif request.user.role == 'housewife':
        return redirect('housewife_dashboard')
    return redirect('login')


# ================= DASHBOARDS =================

@login_required
def mentor_dashboard(request):
    return render(request, 'mentor_dashboard.html')


@login_required
def housewife_dashboard(request):
    return render(request, 'housewife_dashboard.html')


# ================= JOBS =================

@login_required
def create_job(request):
    if request.user.role != 'mentor':
        return redirect('dashboard')

    form = JobForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        job = form.save(commit=False)
        job.mentor = request.user
        job.save()
        messages.success(request, "Job created successfully!")
        return redirect('mentor_jobs')

    return render(request, 'create_job.html', {'form': form})


@login_required
def mentor_jobs(request):
    jobs = Job.objects.filter(mentor=request.user)
    return render(request, 'mentor_jobs.html', {'jobs': jobs})


@login_required
def jobs_list(request):
    jobs = Job.objects.all()
    job_data = []

    for job in jobs:
        score = 0
        if request.user.role == 'housewife' and request.user.skills:
            score = calculate_match_score(
                request.user.skills,
                f"{job.title} {job.skills_required} {job.description}"
            )
        job_data.append({
            'job': job,
            'match_score': score
        })

    if request.user.role == 'housewife':
        job_data.sort(key=lambda x: x['match_score'], reverse=True)

    return render(request, 'jobs_list.html', {'job_data': job_data})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    has_applied = Application.objects.filter(
        job=job,
        applicant=request.user
    ).exists()

    if request.method == 'POST':
        if request.user.role != 'housewife':
            return redirect('jobs_list')

        if not request.user.resume:
            messages.warning(request, "Please upload resume before applying.")
            return redirect('housewife_dashboard')

        if has_applied:
            return redirect('my_applications')

        Application.objects.create(
            job=job,
            applicant=request.user,
            cover_letter=request.POST.get('cover_letter', '')
        )

        Notification.objects.create(
            user=job.mentor,
            message=f"{request.user.username} applied for your job: {job.title}"
        )

        messages.success(request, "Application submitted successfully!")
        return redirect('my_applications')

    return render(request, 'job_detail.html', {
        'job': job,
        'has_applied': has_applied
    })



# ================= APPLICATIONS =================

@login_required
def my_applications(request):
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job').order_by('-applied_at')

    return render(request, 'my_applications.html', {
        'applications': applications
    })

@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if request.user != job.mentor:
        messages.error(request, "Not authorized")
        return redirect('mentor_dashboard')

    if request.method == 'POST':
        app = get_object_or_404(
            Application,
            pk=request.POST.get('app_id'),
            job=job
        )
        action = request.POST.get('action')

        if action == 'shortlist':
            app.status = 'shortlisted'
            app.save()

            Notification.objects.create(
                user=app.applicant,
                message=f"Your application for '{job.title}' was shortlisted"
            )

        elif action == 'reject':
            app.status = 'rejected'
            app.save()

            Notification.objects.create(
                user=app.applicant,
                message=f"Your application for '{job.title}' was rejected"
            )

        return redirect('view_applicants', job_id=job_id)

    applicants = job.applications.select_related('applicant').order_by('-applied_at')
    return render(request, 'view_applicants.html', {
        'job': job,
        'applicants': applicants
    })


# ================= RESUME =================

@login_required
def upload_resume(request):
    if request.method == 'POST':
        file = request.FILES.get('resume')

        if not file or not file.name.lower().endswith('.pdf'):
            messages.error(request, "Only PDF files allowed.")
            return redirect('housewife_dashboard')

        if file.size > 2 * 1024 * 1024:
            messages.error(request, "Resume must be under 2MB.")
            return redirect('housewife_dashboard')

        user = request.user
        user.resume = file

        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        user.skills = extract_skills_from_text(text)
        user.save()

        messages.success(request, "Resume uploaded & skills extracted!")
        return redirect('housewife_dashboard')


# ================= NOTIFICATIONS =================

@login_required
def notifications_view(request):
    notifications = request.user.notifications.all().order_by('-created_at')

    unread = notifications.filter(is_read=False)
    unread.update(is_read=True)

    return render(request, 'notifications.html', {
        'notifications': notifications
    })

