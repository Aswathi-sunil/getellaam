from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import CompanyProfile, Lead, Service, Portfolio, Testimonial, FAQ, JobOpening, JobApplication, Partner
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from urllib.parse import quote
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
def home(request):
    company = CompanyProfile.objects.first()
    featured_services = Service.objects.filter(is_featured=True)[:4]
    featured_projects = Portfolio.objects.filter(is_featured=True)[:10]
    featured_testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    faqs = FAQ.objects.filter(is_active=True)[:6]
    partners = Partner.objects.filter(is_active=True)

    return render(request, 'getellaam/index.html', {
        'company': company,
        'featured_services': featured_services,
        'featured_projects': featured_projects,
        'featured_testimonials': featured_testimonials,
        'faqs': faqs,
        'partners': partners,
    })


def about(request):
    company = CompanyProfile.objects.first()
    return render(request, 'getellaam/about.html', {
        'company': company
    })


def services(request):
    company = CompanyProfile.objects.first()
    all_services = Service.objects.all()
    return render(request, 'getellaam/services.html', {
        'company': company,
        'all_services': all_services
    })

def portfolio(request):
    company = CompanyProfile.objects.first()
    all_projects = Portfolio.objects.all()

    categories = []
    for project in all_projects:
        if project.category and project.category not in categories:
            categories.append(project.category)

    return render(request, 'getellaam/portfolio.html', {
        'company': company,
        'all_projects': all_projects,
        'categories': categories,
    })

def contact(request):
    company = CompanyProfile.objects.first()

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        # BLOCK SPAM: empty required fields
        if not full_name or not email or not phone or not message:
            messages.error(request, "Please fill all required fields.")
            return redirect('contact')

        # BLOCK SPAM: links / html tags
        spam_words = ['http://', 'https://', '<a href', '.ru', 'кухни', 'заказать']

        if any(word.lower() in message.lower() for word in spam_words) or any(word.lower() in subject.lower() for word in spam_words):
            return redirect('contact')

        recaptcha_response = request.POST.get('g-recaptcha-response')

        recaptcha_verify = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        )

        if not recaptcha_verify.json().get('success'):
            messages.error(request, "Please verify that you are not a robot.")
            return redirect('contact')

        # Save to DB
        Lead.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )

        # Send email to company
        email_subject = f"New Lead: {subject or 'Website Enquiry'}"
        email_message = f"""
New contact lead received.

Name: {full_name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}
"""

        send_mail(
            email_subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.COMPANY_LEAD_EMAIL],
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    return render(request, 'getellaam/contact.html', {
        'company': company,
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY

    })
def service_detail(request, slug):
    company = CompanyProfile.objects.first()
    service = get_object_or_404(Service, slug=slug)

    return render(request, 'getellaam/service_detail.html', {
        'company': company,
        'service': service
    })

def portfolio_detail(request, slug):
    company = CompanyProfile.objects.first()
    project = get_object_or_404(Portfolio, slug=slug)

    return render(request, 'getellaam/portfolio_detail.html', {
        'company': company,
        'project': project
    })

def careers(request):
    company = CompanyProfile.objects.first()
    jobs = JobOpening.objects.filter(is_active=True)

    if request.method == 'POST':
        job_id = request.POST.get('job')
        full_name = request.POST.get('full_name')
        applicant_email = request.POST.get('email')
        phone = request.POST.get('phone')
        resume = request.FILES.get('resume')
        message = request.POST.get('message')

        job = get_object_or_404(JobOpening, id=job_id)

        JobApplication.objects.create(
            job=job,
            full_name=full_name,
            email=applicant_email,
            phone=phone,
            resume=resume,
            message=message
        )

        mail = EmailMessage(
            subject=f"Job Application - {job.title} - {full_name}",
            body=f"""
New job application received.

Job Role: {job.title}
Name: {full_name}
Email: {applicant_email}
Phone: {phone}

Message:
{message}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.COMPANY_HR_EMAIL],
        )

        if resume:
            mail.attach(resume.name, resume.read(), resume.content_type)

        mail.send(fail_silently=False)

        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('careers')

    return render(request, 'getellaam/careers.html', {
        'company': company,
        'jobs': jobs
    })

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'getellaam/admin_login.html')


@login_required
def admin_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    leads_count = Lead.objects.count()
    applications_count = JobApplication.objects.count()
    jobs_count = JobOpening.objects.count()   # 👈 add this

    return render(request, 'dashboard/index.html', {
        'leads_count': leads_count,
        'applications_count': applications_count,
        'jobs_count': jobs_count,
    })

@login_required
def dashboard_leads(request):
    if not request.user.is_staff:
        return redirect('home')

    leads = Lead.objects.all()
    return render(request, 'dashboard/leads.html', {'leads': leads})


@login_required
def dashboard_jobs(request):
    if not request.user.is_staff:
        return redirect('home')

    jobs = JobApplication.objects.all()
    return render(request, 'dashboard/jobs.html', {'jobs': jobs})

@login_required
def dashboard_job_openings(request):
    if not request.user.is_staff:
        return redirect('home')

    jobs = JobOpening.objects.all()
    return render(request, 'dashboard/job_openings.html', {'jobs': jobs})


@login_required
def add_job_opening(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        JobOpening.objects.create(
            title=request.POST.get('title'),
            department=request.POST.get('department'),
            location=request.POST.get('location'),
            job_type=request.POST.get('job_type'),
            description=request.POST.get('description'),
            requirements=request.POST.get('requirements'),
            is_active=True if request.POST.get('is_active') == 'on' else False
        )
        messages.success(request, 'Job opening added successfully.')
        return redirect('dashboard_job_openings')

    return render(request, 'dashboard/job_form.html')


@login_required
def edit_job_opening(request, id):
    if not request.user.is_staff:
        return redirect('home')

    job = get_object_or_404(JobOpening, id=id)

    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.department = request.POST.get('department')
        job.location = request.POST.get('location')
        job.job_type = request.POST.get('job_type')
        job.description = request.POST.get('description')
        job.requirements = request.POST.get('requirements')
        job.is_active = True if request.POST.get('is_active') == 'on' else False
        job.save()

        messages.success(request, 'Job opening updated successfully.')
        return redirect('dashboard_job_openings')

    return render(request, 'dashboard/job_form.html', {'job': job})


@login_required
def delete_job_opening(request, id):
    if not request.user.is_staff:
        return redirect('home')

    job = get_object_or_404(JobOpening, id=id)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job opening deleted successfully.')
        return redirect('dashboard_job_openings')

    return render(request, 'dashboard/job_delete.html', {'job': job})