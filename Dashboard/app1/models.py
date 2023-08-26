from typing import Any
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError

   
def validate_file_size(value):
    max_size = 10240000000000000000000000000000000000000000000000000000000  # 5 MB in bytes
    print(value.size)
    if value.size > max_size:
        raise ValidationError(f"File size cannot exceed {max_size} bytes.")






class Signup_User(models.Model):
    uname = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    pass1 = models.CharField(max_length=50)
    pass2 = models.CharField(max_length=50)
    
    def __str__(self):
        return self.uname


class Dcs_moduls(models.Model):
    is_active = models.CharField(max_length=50)




class CSVFile(models.Model):
    file = models.FileField(upload_to='csv_files/',validators=[validate_file_size])
    uploaded_time = models.DateTimeField(default=datetime.now)  
    master_id=models.CharField(max_length=100,default='null')

    def __str__(self):
        return self.file.name
    
    def save(self, *args, **kwargs):
        if self.file:
            validate_file_size(self.file)
        super().save(*args, **kwargs)


class Dcs_ScrapingRequisition(models.Model):
    websitelink = models.URLField(default='null')
    PRIORITY_CHOICES = [('least', 'Least'),('medium', 'Medium'),('high', 'High'),]    
    priority_list = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    WEBSITE_CHOICES = [('Product', 'Product'),('Brand', 'Brand'),('Catagory', 'Catagory'),]    
    choose_website = models.CharField(max_length=50,choices=WEBSITE_CHOICES,default='Product',)
    file = models.FileField(upload_to='uploads/',validators=[validate_file_size])
    uploaded_time = models.DateTimeField(default=datetime.now)    
    reported = models.CharField(max_length=250)
    specific = models.CharField(max_length=250)
   
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.upload_time = datetime.now()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.reported
    
    def save(self, *args, **kwargs):
        if self.file:
            validate_file_size(self.file)
        super().save(*args, **kwargs)


class saveScapeUrl(models.Model):
    urlname = models.URLField()
    file = models.FileField(upload_to='uploads_Scrape/',validators=[validate_file_size])
    module=models.CharField(max_length=100,default='')
    uploaded_time = models.DateTimeField(default=datetime.now)
    uploaded_by = models.CharField(max_length=250)
    master_id=models.CharField(max_length=100,default='null')
    def save(self, *args, **kwargs):
        if self.file:
            validate_file_size(self.file)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.file.name

class WebsiteList(models.Model):
    website_list = models.URLField()
    upload_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.website_list



class Dcs_ActionsForms(models.Model):
    websitelink = models.ForeignKey(Dcs_ScrapingRequisition, on_delete=models.CASCADE,default='null')
    websites = models.CharField(max_length=200,default='null')  # You can adjust the max length as needed
    assign_to = models.CharField(max_length=100,default='null')
    assign_time = models.DateTimeField(default=datetime.now)
    provided_by = models.CharField(max_length=100,default='null')
    STATUS_CHOICES = [('In Progress', 'In Progress'), ('Done', 'Done'), ('On Hold', 'On Hold')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.assign_to
