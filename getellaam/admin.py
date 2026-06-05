from django.contrib import admin
from .models import CompanyProfile, Lead, Service, Portfolio, Testimonial, FAQ, JobOpening, JobApplication, Partner


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone', 'email', 'updated_at')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'subject', 'submitted_on', 'is_contacted')
    list_filter = ('is_contacted', 'submitted_on')
    search_fields = ('full_name', 'email', 'phone', 'subject')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client_name', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured', 'category')
    search_fields = ('title', 'client_name', 'category')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company_name', 'designation', 'rating', 'is_featured', 'order')
    list_filter = ('is_featured', 'rating')
    search_fields = ('client_name', 'company_name', 'designation')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('question',)

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'job_type', 'is_active', 'posted_on')
    list_filter = ('is_active', 'job_type', 'department')
    search_fields = ('title', 'department', 'location')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'job', 'applied_on')
    list_filter = ('job', 'applied_on')
    search_fields = ('full_name', 'email', 'phone')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)