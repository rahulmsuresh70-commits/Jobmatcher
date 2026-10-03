from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone= models.IntegerField()
    location= models.CharField(max_length=100,null=True)
    linkedin=models.URLField(null=True)
    portfolio=models.URLField(null=True)
    headline=models.CharField(max_length=100,null=True)
    summary=models.TextField(null=True)
    password = models.CharField(max_length=100)
    rights=models.CharField(max_length=100,default='User')
    status=models.CharField(max_length=100,default='Pending',null=True)
    def __str__(self):
        return self.name

class Professional(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE,related_name='professional')
    jobTitle=models.CharField(max_length=100,null=True)
    experience=models.CharField(max_length=100,null=True)
    industry=models.CharField(max_length=100,null=True)
    preferred=models.CharField(max_length=100,null=True)
    salary_expectation_minimum=models.IntegerField(null=True)
    salary_expectation_maximum=models.IntegerField(null=True)
    currency=models.CharField(max_length=100,null=True)
    goals=models.TextField(null=True)
    date=models.DateField(auto_now_add=True,null=True)
    status = models.CharField(max_length=100, default='Pending', null=True)


class Experience(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE,related_name='experience')
    jobTitle=models.CharField(max_length=100,null=True)
    company=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=100,null=True)
    type=models.CharField(max_length=100,null=True)
    start_date=models.CharField(max_length=50,null=True)
    end_date=models.CharField(max_length=50,null=True)
    currently_working=models.BooleanField(default=False,null=True)
    skills=models.JSONField(null=True)
    status = models.CharField(max_length=100, default='Pending', null=True)

class Education(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE,related_name='education')
    degree=models.CharField(max_length=100,null=True)
    field=models.CharField(max_length=100,null=True)
    institution=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=100,null=True)
    start_year=models.IntegerField(null=True)
    end_year=models.CharField(max_length=100,null=True)
    currently_working = models.BooleanField(default=False, null=True)
    gpa=models.IntegerField(null=True)
    skills=models.JSONField(null=True)
    status = models.CharField(max_length=100, default='Pending', null=True)

class Skill(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE,related_name='skill')
    technical_skills=models.JSONField(null=True)
    soft_skills=models.JSONField(null=True)
    certifications=models.CharField(max_length=100,null=True)
    languages=models.JSONField(null=True)
    status = models.CharField(max_length=100, default='Pending', null=True)

class Preference(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE,related_name='preference')
    title = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=100,null=True)
    relocation=models.CharField(max_length=100,null=True)
    size = models.CharField(max_length=100,null=True)
    culture=models.CharField(max_length=100,null=True)
    non_negotiable=models.TextField(null=True)
    status = models.CharField(max_length=100, default='Pending', null=True)

class Files(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE,related_name='files')
    image=models.ImageField(upload_to='image/',null=True)
    resume=models.FileField(upload_to='resume/',null=True)
    portfolio=models.FileField(upload_to='portfolio/',null=True)
    status = models.CharField(max_length=100, default='Pending', null=True)

class Company(models.Model):
    company_name=models.CharField(max_length=100)
    company_email=models.EmailField()
    company_phone=models.IntegerField()
    website=models.URLField()
    logo=models.ImageField(upload_to='logo/',null=True)
    size=models.CharField(max_length=100)
    industry=models.CharField(max_length=100)
    description=models.TextField()
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    rights=models.CharField(max_length=100,default='New Company')
    date=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.company_name

class Job(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    description=models.TextField()
    location=models.CharField(max_length=100)
    salary_min=models.IntegerField()
    salary_max=models.IntegerField()
    currency=models.CharField(max_length=100)
    salary_period=models.CharField(max_length=100)
    skills=models.JSONField()
    qualifications=models.TextField()
    benefits=models.JSONField()
    openings=models.IntegerField()
    deadline=models.DateField()
    hiring_priority=models.CharField(max_length=100)
    requirements=models.JSONField()
    date=models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=100,default='Active')
    def __str__(self):
        return self.title

class Application(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE)
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    coverLetter=models.TextField()
    status=models.CharField(max_length=100,default='Pending', null=True)
    date=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.user.name