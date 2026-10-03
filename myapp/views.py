from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from datetime import date

from django.core.mail import send_mail
from django.conf import settings
import random


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        reg=Register.objects.create(name=name,email=email,phone=phone,password=password)
        Professional(user=reg).save()
        Experience(user=reg).save()
        Education(user=reg).save()
        Skill(user=reg).save()
        Preference(user=reg).save()
        Files(user=reg).save()
        reg.save()
        return redirect('/login/')
    return render(request, 'register.html')

def company_register(request):
    if request.method == 'POST':
        company_name=request.POST.get('company_name')
        company_email=request.POST.get('company_email')
        company_phone=request.POST.get('company_phone')
        website=request.POST.get('website')
        size=request.POST.get('size')
        logo=request.FILES.get('logo')
        industry=request.POST.get('industry')
        description=request.POST.get('description')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        com=Company(company_name=company_name,company_email=company_email,company_phone=company_phone,website=website,size=size,logo=logo,
                    industry=industry,description=description,fname=fname,lname=lname,email=email,password=password)
        com.save()
        return redirect('/login/')
    return render(request, 'company-register.html')

def login(request):
    msg=''
    if request.method == 'POST':
        email=request.POST.get('email')
        password = request.POST.get('password')
        log=Register.objects.filter(email=email,password=password)
        com=Company.objects.filter(email=email,password=password)
        if log:
            for i in log:
                if i.rights=='User':
                    request.session['uid']=i.id
                    return redirect('/user/')
                elif i.rights=='Admin':
                    return redirect('/adminp/')
        elif com:
            for i in com:
                if i.rights=='Company':
                    request.session['cid']=i.id
                    return redirect('/company/')
                elif i.rights=='New Company':
                    msg='Your application is in progress!'
                elif i.rights=='Rejected':
                    msg='Your application is rejected!'
                elif i.rights=='Blocked':
                    msg='Your has been blocked!'
        else:
            msg='Invalid Credentials!'
    return render(request, 'login.html',{'msg':msg})

def user(request):
    return render(request, 'user/user.html')

def admin(request):
    return render(request, 'admin/admin.html')

def company(request):
    return render(request, 'company/company.html')

def new_companies(request):
    companies=Company.objects.filter(rights='New Company')
    return render(request, 'admin/new-companies.html',{'companies':companies})

def manage_company(request,id,status):
    Company.objects.filter(id=id).update(rights=status)
    try:
        if status =='Company':
            status='Approved'
        com=Company.objects.get(id=id)
        email=com.company_email
        subject = 'JobMatcher - Company Verification'
        message = f'Hi,your application has been!{status}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
    except:
        pass
    return redirect(request.META['HTTP_REFERER'])

def companies(request):
    companies=Company.objects.exclude(rights__in=['New Company','Rejected'])
    return render(request, 'admin/companies.html',{'companies':companies})

def add_job(request):
    cid=request.session.get('cid')
    company=Company.objects.get(id=cid)
    if request.method == 'POST':
        title=request.POST.get('title')
        department=request.POST.get('department')
        type=request.POST.get('type')
        experience=request.POST.get('experience')
        description=request.POST.get('description')
        location=request.POST.get('location')
        salary_min=request.POST.get('salary_min')
        salary_max=request.POST.get('salary_max')
        currency=request.POST.get('currency')
        salary_period=request.POST.get('salary_period')
        skills=request.POST.getlist('skills')
        qualifications=request.POST.get('qualifications')
        benefits=request.POST.getlist('benefits')
        openings=request.POST.get('openings')
        deadline=request.POST.get('deadline')
        hiring_priority=request.POST.get('hiring_priority')
        requirements=request.POST.getlist('appRequirements')
        job=Job(company=company,title=title,department=department,type=type,experience=experience,description=description,
                location=location,salary_min=salary_min,salary_max=salary_max,currency=currency,salary_period=salary_period,
                skills=skills,qualifications=qualifications,benefits=benefits,openings=openings,deadline=deadline,hiring_priority=hiring_priority,
                requirements=requirements)
        job.save()
        return redirect('/add-job/')
    return render(request, 'company/add-job.html')

def jobs(request):
    cid=request.session.get('cid')
    company=Company.objects.get(id=cid)
    jobs=Job.objects.filter(company=company)
    return render(request, 'company/jobs.html',{'jobs':jobs})

def edit_job(request,id):
    job=Job.objects.get(id=id)
    if request.method == 'POST':
        title=request.POST.get('title')
        department=request.POST.get('department')
        type=request.POST.get('type')
        experience=request.POST.get('experience')
        description=request.POST.get('description')
        location=request.POST.get('location')
        salary_min=request.POST.get('salary_min')
        salary_max=request.POST.get('salary_max')
        currency=request.POST.get('currency')
        salary_period=request.POST.get('salary_period')
        skills=request.POST.getlist('skills')
        qualifications=request.POST.get('qualifications')
        benefits=request.POST.getlist('benefits')
        openings=request.POST.get('openings')
        deadline=request.POST.get('deadline')
        hiring_priority=request.POST.get('hiring_priority')
        requirements=request.POST.getlist('appRequirements')
        Job.objects.filter(id=id).update(title=title,department=department,type=type,experience=experience,description=description,
                location=location,salary_min=salary_min,salary_max=salary_max,currency=currency,salary_period=salary_period,
                skills=skills,qualifications=qualifications,benefits=benefits,openings=openings,deadline=deadline,hiring_priority=hiring_priority,
                requirements=requirements)
        return redirect(request.META['HTTP_REFERER'])
    return render(request, 'company/edit-job.html',{'job':job})

def delete_job(request,id):
    Job.objects.filter(id=id).delete()
    return redirect(request.META['HTTP_REFERER'])

def profile(request):
    uid=request.session.get('uid')
    reg=Register.objects.get(id=uid)
    professional=Professional.objects.get(user=reg)
    experience=Experience.objects.filter(user=reg).first()
    experiences=Experience.objects.filter(user=reg)
    education=Education.objects.filter(user=reg).first()
    educations=Education.objects.filter(user=reg)
    skill=Skill.objects.get(user=reg)
    preference=Preference.objects.get(user=reg)
    file=Files.objects.get(user=reg)
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        location=request.POST.get('location')
        linkedin=request.POST.get('linkedin')
        portfolio=request.POST.get('portfolio')
        headline=request.POST.get('headline')
        summary=request.POST.get('summary')
        reg.name=name
        reg.email=email
        reg.phone=phone
        reg.location=location
        reg.linkedin=linkedin
        reg.portfolio=portfolio
        reg.headline=headline
        reg.summary=summary
        reg.status='Completed'
        reg.save()
        return redirect('/profile/')
    return render(request, 'user/profile.html',{'reg':reg,'professional':professional,'experience':experience,'education':education,'skill':skill,'preference':preference,'file':file,'experiences':experiences,'educations':educations})

def professional_details(request):
    uid = request.session.get('uid')
    reg = Register.objects.get(id=uid)
    professional = Professional.objects.get(user=reg)
    if request.method == 'POST':
        jobTitle=request.POST.get('jobTitle')
        experience=request.POST.get('experience')
        industry=request.POST.get('industry')
        preferred=request.POST.get('employmentType')
        salary_expectation_minimum=request.POST.get('salary_expectation_minimum')
        salary_maximum_maximum=request.POST.get('salary_expectation_maximum')
        currency=request.POST.get('currency')
        goals=request.POST.get('goals')
        professional.jobTitle=jobTitle
        professional.experience=experience
        professional.industry=industry
        professional.preferred=preferred
        professional.salary_expectation_minimum=salary_expectation_minimum
        professional.salary_maximum_maximum=salary_maximum_maximum
        professional.currency=currency
        professional.goals=goals
        professional.status='Completed'
        professional.save()
    return redirect('/profile/')

def experience_details(request):
    uid = request.session.get('uid')
    reg=Register.objects.get(id=uid)
    if request.method == 'POST':
        jobTitle=request.POST.get('jobTitle')
        company=request.POST.get('company')
        location=request.POST.get('location')
        type=request.POST.get('type')
        start_date=request.POST.get('start_date')
        currently_worked=request.POST.get('currently_worked')
        end_date=request.POST.get('end_date')
        skills=request.POST.getlist('expSkillsContainer')
        if currently_worked:
            currently_worked=True
        else:
            currently_worked=False
        exp=Experience(user=reg,jobTitle=jobTitle,company=company,location=location,type=type,start_date=start_date,end_date=end_date,currently_working=currently_worked,skills=skills)
        exp.save()
    return redirect('/profile/')

def experience_continue(request):
    uid = request.session.get('uid')
    reg=Register.objects.get(id=uid)
    experience=Experience.objects.filter(user=reg).first()
    if request.method == 'POST':
        experience.status='Completed'
        experience.save()
    return redirect('/profile/')

def education_details(request):
    uid = request.session.get('uid')
    reg=Register.objects.get(id=uid)
    if request.method == 'POST':
        degree=request.POST.get('degree')
        field=request.POST.get('field')
        institution=request.POST.get('institution')
        location=request.POST.get('location')
        start_year=request.POST.get('start_year')
        end_year=request.POST.get('end_year')
        currently_working=request.POST.get('currently_working')
        gpa=request.POST.get('gpa')
        skills=request.POST.getlist('eduSkillsContainer')
        education=Education(user=reg,degree=degree,field=field,institution=institution,location=location,start_year=start_year,end_year=end_year,currently_working=currently_working,gpa=gpa,skills=skills)
        education.save()
    return redirect('/profile/')

def education_continue(request):
    uid = request.session.get('uid')
    reg=Register.objects.get(id=uid)
    education=Education.objects.filter(user=reg).first()
    if request.method == 'POST':
        education.status='Completed'
        education.save()
    return redirect('/profile/')

def skills_details(request):
    uid = request.session.get('uid')
    reg=Register.objects.get(id=uid)
    skill=Skill.objects.get(user=reg)
    if request.method == 'POST':
        technical_skills=request.POST.getlist('technicalSkillsContainer')
        soft_skills=request.POST.getlist('softSkillsContainer')
        certifications=request.POST.get('certifications')
        languages=request.POST.getlist('languagesContainer')
        skill.technical_skills=technical_skills
        skill.soft_skills=soft_skills
        skill.certifications=certifications
        skill.languages=languages
        skill.status='Completed'
        skill.save()
    return redirect('/profile/')

def preference_details(request):
    uid = request.session.get('uid')
    reg=Register.objects.get(id=uid)
    preference=Preference.objects.get(user=reg)
    if request.method == 'POST':
        title=request.POST.get('title')
        location=request.POST.get('location')
        relocate=request.POST.get('relocate')
        size=request.POST.get('companySize')
        culture=request.POST.get('culture')
        non_negotiable=request.POST.get('non_negotiable')
        preference.title=title
        preference.location=location
        preference.relocate=relocate
        preference.size=size
        preference.culture=culture
        preference.non_negotiable=non_negotiable
        preference.status='Completed'
        preference.save()
    return redirect('/profile/')

def file_details(request):
    uid = request.session.get('uid')
    reg=Register.objects.get(id=uid)
    file=Files.objects.get(user=reg)
    if request.method == 'POST':
        image=request.FILES.get('image')
        resume=request.FILES.get('resume')
        portfolio=request.FILES.get('portfolio')
        if image:
            file.image=image
        if resume:
            file.resume=resume
        if portfolio:
            file.portfolio=portfolio
        file.status='Completed'
        file.save()
    return redirect('/profile/')

def job_lists(request):
    uid=request.session.get('uid')
    user = Register.objects.get(id=uid)
    skill = Skill.objects.filter(user=user).first()
    jobs = Job.objects.filter(status='Active')
    print(skill)
    if skill and skill.technical_skills:
        skill_queries = Q()
        for s in skill.technical_skills:
            skill_queries |= Q(skills__icontains=s)
        jobs = jobs.filter(skill_queries)
    else:
        jobs=[]

    return render(request, 'user/job-lists.html', {'jobs': jobs})

def job_details(request,id):
    job=Job.objects.get(id=id)
    uid = request.session.get('uid')
    reg = Register.objects.get(id=uid)
    apps=Application.objects.filter(user=reg,job=job)
    msg=False
    today=date.today()
    exp=job.deadline<today
    if request.method == 'POST':
        coverLetter = request.POST.get('coverLetter')
        app = Application(user=reg, job=job, coverLetter=coverLetter)
        app.save()
        msg=True
    return render(request,'user/job-details.html',{'job':job,'reg':reg,'msg':msg,'apps':apps,'exp':exp})

def applications(request):
    uid=request.session.get('uid')
    reg=Register.objects.get(id=uid)
    apps=Application.objects.filter(user=reg)
    return render(request,'user/applications.html',{'apps':apps})

def manage_applications(request):
    cid=request.session.get('cid')
    com=Company.objects.get(id=cid)
    apps=Application.objects.filter(job__company=com)
    return render(request,'company/manage-applications.html',{'apps':apps})

def update_status(request,id,status):
    Application.objects.filter(id=id).update(status=status)
    return redirect(request.META['HTTP_REFERER'])

def email(request):
    msg=False
    if request.method=="POST":
        email=request.POST.get('email')
        reg=Register.objects.filter(email=email)
        sell=Company.objects.filter(email=email)
        if reg or sell:
            request.session['email']=email
            rid=str(random.randint(0000,9999))
            request.session['otp']=rid
            subject = 'JobMatcher - Password Reset OTP'
            message = f'Hi,this is one time password to change your password!{rid}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('/otp/')
        else:
            msg=True
    return render(request, 'email.html',{'msg':msg})

def otp(request):
    msg=False
    if request.method=="POST":
        otp=request.POST.get('otp')
        rid=request.session['otp']
        if otp==rid:
            return redirect('/password/')
        else:
            msg=True
    return render(request, 'otp.html',{'msg':msg})

def password(request):
    msg=False
    if request.method=="POST":
        password=request.POST.get('np')
        cpassword=request.POST.get('cp')
        if password==cpassword:
            email=request.session['email']
            reg = Register.objects.filter(email=email)
            sell = Company.objects.filter(email=email)
            if reg:
                reg.password=password
            elif sell:
                sell.password=password
            return redirect('/login/')
        else:
            msg=True
    return render(request, 'password.html',{'msg':msg})

def company_profile(request):
    cid=request.session.get('cid')
    company=Company.objects.get(id=cid)
    if request.method=="POST":
        company.company_name=request.POST.get('company_name')
        company.company_email=request.POST.get('company_email')
        company.company_phone=request.POST.get('company_phone')
        company.website=request.POST.get('website')
        logo=request.FILES.get('logo')
        if logo:
            company.logo=logo
        company.size=request.POST.get('size')
        company.industry=request.POST.get('industry')
        company.description=request.POST.get('description')
        company.fname=request.POST.get('fname')
        company.lname=request.POST.get('lname')
        company.email=request.POST.get('email')
        password=request.POST.get('password')
        if password:
            company.password=password
        company.save()
        return redirect(request.META['HTTP_REFERER'])
    return render(request,'company/company-profile.html',{'company':company})

def users(request):
    users=Register.objects.exclude(rights='Admin')
    return render(request,'admin/users.html',{'users':users})

def manage_user(request,id,status):
    Register.objects.filter(id=id).update(rights=status)
    return redirect(request.META['HTTP_REFERER'])