from urllib import request
import csv
import pandas as pd
import re
from django.db.models import Count
from itertools import zip_longest
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import *
from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import render, redirect
import logging
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import FileResponse
import os
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.db import connection

def run_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
# Create your views here.


@login_required(login_url='login')
# ****************************************************** SignUp Page ******************************************************************
def BasePage(request):
    print('..........................basepage')
    return render(request, 'base.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        print(uname, email, pass1, pass2)

        try:
            if pass1 != pass2:
                messages.error(
                    request, "Your password and confirm password are not the same!")
                return redirect('signup')
            else:
                # Validate the email address
                try:
                    validate_email(email)
                except ValidationError:
                    messages.error(request, "Invalid email address!")
                    return redirect('signup')

                if User.objects.filter(email=email).exists():
                    messages.error(
                        request, "Email already exists! Please try a different email.")
                    return redirect('signup')
                else:
                    # Create a new user with the provided credentials
                    my_user = User.objects.create_user(uname, email, pass1)
                    my_user.is_staff = False
                    my_user.is_superuser = False
                    my_user.save()
                    messages.success(
                        request, "You have successfully signed up. Please log in using your credentials.")
                    return redirect('login')
        except:
            return redirect('login')

    return render(request, "signup.html")


# ****************************************************** LoginPage ******************************************************************
def LoginPage(request):
    print('...............................Loginpage')
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            # messages.success(request, "Login successful!")
            request.session['name'] = username
            # Add this line for the success message
            return redirect('home')
        else:
            messages.error(
                request, "Username or Password is incorrect!!!  Please try currect user name or password")
            return redirect('login')
    # If the user is already authenticated, redirect them to the 'home' page.
    print('..............')
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'login.html')


def LogoutPage(request):
    print('....................Logoutpage')
    # Delete the 'name' key if it exists, otherwise do nothing
    request.session.pop('name', None)
    logout(request)
    return redirect('login')


# ****************************************************** ShowForm ******************************************************************
@login_required(login_url='login')
def ShowForm(request):
    print('...............................showform')
    if request.method == 'POST':
        website = request.POST.get('website')
        csv_file = request.FILES.get('filename')
        priority = request.POST.get('priority')
        choose_website = str(request.POST.getlist('choose_website')).replace("'",'').replace("[",'').replace(']','')
        choose_website_list = request.POST.getlist('choose_website')
        choose_website = ','.join(choose_website_list)
        Reported = request.POST.get('Reported')
        Specific = request.POST.get('Specific')
        print('csv_file...', csv_file)

        # Store choose_website value in a session variable
        request.session['choose_website'] = choose_website

        form_data = Dcs_ScrapingRequisition(
            websitelink=website,
            priority_list=priority,
            # Make sure 'choose_website' is assigned a valid value
            choose_website=choose_website,
            file=csv_file,
            reported=Reported,
            specific=Specific
        )
        form_data.save()
        print("submited data...", form_data)

        # messages.success(
        #     request, "Your Scraping Requisition Submitted Succcesfully")
        return redirect('info', id=form_data.id)
    return render(request, 'request_form.html')


# ****************************************************** download_file but dynamic path  ******************************************************************
@login_required(login_url='login')
def download_file(request, filename):
    base_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_directory, "uploads", filename)
    print('download_file.........................................................1')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(
                file.read(), content_type='application/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("File not found")


# ****************************************************** update ******************************************************************
@login_required(login_url='login')
def update(request, id):
    if request.method == 'POST':
        obj = Dcs_ScrapingRequisition.objects.get(id=id)
        obj.website = request.POST.get('website')
        obj.csv_file = request.FILES.get('filename')
        obj.priority = request.POST.get('priority')
        obj.choose_website = str(request.POST.getlist('choose_website')).replace("'",'').replace("[",'').replace(']','')
        obj.Reported = request.POST.get('Reported')
        obj.Specific = request.POST.get('Specific')
        obj.save()
        
        # messages.success(request, "Form Updated Succcesfully")
        return redirect('info',id=id)

    result = get_object_or_404(Dcs_ScrapingRequisition, pk=id)
    result1=result.choose_website.split(',')
    # messages.success(request, "Form Submitted Succcesfully")
    return render(request, 'forms-uploads.html', {'result': result,'result1':result1})


# ******************************************************** delete ******************************************************************
@login_required(login_url='login')
def delete(request, id):
    result = get_object_or_404(Dcs_ScrapingRequisition, pk=id)
    result.delete()
    msg = "File Deleted Successfully"
    messages.error(request, "File Deleted Successfully")
    return redirect('home')


# ******************************************************* info *******************************************************************
@login_required(login_url='login')
def info(request, id):
    print('............... info') 
    messages.get_messages(request)
    result = Dcs_ScrapingRequisition.objects.get(pk=id)
    print('result1..................',result)
    result2 = Dcs_ScrapingRequisition.objects.filter(websitelink=result.websitelink)
    print('result2..................', result2)
    return render(request, 'info.html', {'result': result2})


# ******************************************************* HomePage *********************************************************************
@login_required(login_url="/login/")
def HomePage(request):
    # Fetch website links along with specific and id
    with connection.cursor() as cursor:
        query = '''
            SELECT DISTINCT `websitelink`, `specific`, `id`
            FROM `app1_dcs_scrapingrequisition`
            GROUP BY `websitelink`
            ORDER BY `id` DESC
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Extract data from the result
        combined_data = [{'websitelink': row[0], 'specific': row[1], 'id': row[2]} for row in result]
        
    # Fetch data from Dcs_ActionsForms
    sts = Dcs_ActionsForms.objects.all().values()
    
    return render(request, "index.html", {'data': combined_data, 'sts': sts})



# def HomePage(request):
#     print('.................Homepage')
#     # Fetch website links
#     with connection.cursor() as cursor:
#         query = '''
#             SELECT DISTINCT(websitelink), id
#             FROM app1_dcs_scrapingrequisition
#             GROUP BY websitelink
#             ORDER BY id DESC
#         '''
#         cursor.execute(query)
#         result = cursor.fetchall()
        
#         item = [row[0] for row in result]
#         res = [row[1] for row in result]
#         combined_data = [{'websitelink': i, 'id': r} for i, r in zip(item, res)]
#         sts = Dcs_ActionsForms.objects.all().values()
    
#     return render(request, "index.html", {'data': combined_data, 'sts':sts})


# ***************************************************** SignupPage *********************************************************************
"""
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Validate email format
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messages.error(request, "Invalid email format")
            return redirect('signup')

        # Validate password requirements
        if len(pass1) < 5:
            messages.error(request, "Password should be at least 5 characters long")
            return redirect('signup')
        # if not re.search(r'\d', pass1):
        #     messages.error(request, "Password should contain at least one digit")
        #     return redirect('signup')
        # if not re.search(r'[A-Z]', pass1):
        #     messages.error(request, "Password should contain at least one uppercase letter")
        #     return redirect('signup')
        # if not re.search(r'[a-z]', pass1):
        #     messages.error(request, "Password should contain at least one lowercase letter")
        #     return redirect('signup')

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Your password and confirm password do not match")
            return redirect('signup')

        try:
            # Check if email already exists
            if Signup_User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please try a different email")
                return redirect('signup')
            # Create the user
            my_user = Signup_User.objects.create(uname=uname, email=email, pass1=pass1, pass2=pass2)
            my_user.save()
            messages.success(request, "User Name and Password Created")
            return redirect('login')
        except Exception as e:
            print('Exception:', str(e))
            messages.error(request, "An error occurred while creating the user. Please try again")
            return redirect('signup')

    return render(request, "signup.html")
"""



#   -------------------------------------------start upload_csv main function --------------------------------------------------------

def Upload_csv(request, id):
    print("Upload_csv ............................")
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')  # Use get to avoid KeyError
        choose_website = request.POST.get('choose_website')

        # Check if choose_website is empty or None
        # if not choose_website:
        #     return HttpResponse("Choose website value is missing or invalid.")

        # Make sure to handle the case when csv_file is not provided
        if csv_file:
            new_file = saveScapeUrl(file=csv_file, module=choose_website, master_id=id)
            new_file.save()
            print(new_file)

        text_files = saveScapeUrl.objects.filter(master_id=id)
        dropdown = Dcs_ScrapingRequisition.objects.get(pk=id)
        d = dropdown.choose_website.split(',')
        

        return render(request, 'upload_csv.html', {'text_files': text_files, 'dropdown': dropdown, 'd': d})
    else:
        text_files = saveScapeUrl.objects.filter(master_id=id)
        dropdown = Dcs_ScrapingRequisition.objects.get(pk=id)
        d = dropdown.choose_website.split(',')
        
        return render(request, 'upload_csv.html', {'text_files': text_files, 'dropdown': dropdown, 'd': d})

#   -------------------------------------------end upload_csv main function --------------------------------------------------------

@login_required(login_url='login')
def download_csv(request, filename):
    print('download_csv .................')
    base_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_directory, "uploads_Scrape", filename)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            # Determine the file extension
            file_extension = os.path.splitext(filename)[1].lower()

            # Set the appropriate content type based on the file extension
            if file_extension == '.csv':
                content_type = 'application/csv'
            elif file_extension == '.xlsx':
                content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif file_extension == '.zip':
                content_type = 'application/zip'
            else:
                return HttpResponse("Invalid file format")

            response = HttpResponse(file.read(), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("File not found")


# start-------------------------------------------
# ******************************************************* All Ready Scrape Urls and Get Data ********************************************
@login_required(login_url='login')
def ScapeUrlForm(request):
    print('ScapeUrlForm.................')
    if request.method == 'POST':
        url_name = request.POST.get('url_link')
        file_upload = request.FILES.get('filename')
        uploaded_by = request.POST.get('Uploaded')
        save = saveScapeUrl(
            urlname=url_name, file=file_upload, uploaded_by=uploaded_by)
        print("sssssss", save)
        save.save()
        df = pd.read_excel(file_upload)  # Skip the header row

        df1 = pd.DataFrame(df)
        for row in df1.itertuples():
            form_data = Dcs_ScrapingRequisition(
                websitelink=row.Website,
                priority_list=row.Priority,
                # Make sure 'choose_website' is assigned a valid value
                choose_website=row._3,

                reported=row._4,
                specific=row._5
            )
            form_data.save()


        # messages.success(request, "Form Submitted Successfully")
        # Redirect to a success page or another view
        return redirect('home')

    return render(request, "upload_scrape_url.html")



# ------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def UrlShow(request):
    print('UrlShow.....')
    res = saveScapeUrl.objects.all().order_by('-uploaded_time').values()
    return render(request, "download_scrape_url.html", {'res': res})



# ------------------------------------------------------------------------------------------------------------------------------------
def RequisitionHistory(request, st):
    print('RequisitionHistory................................')
    items = Dcs_ScrapingRequisition.objects.all().filter(websitelink=st.replace("jaimatadee",'/')).values()
    # ress = saveScapeUrl.objects.filter(master_id=id)
    # combined_datas = [{'items': i, 'ress': r} for i, r in zip(items, ress)]
    print(items) 

    return render(request, "requisition_history.html", {'combined_datas': items})





# ------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def Url(request, id):
    print("........Url call Views")
    link = Dcs_ScrapingRequisition.objects.all().filter(id=id)
    res = saveScapeUrl.objects.all().filter(master_id=id)
    # print(link)
    for i in link:
        st = i.websitelink
        # print('link..', st)
    item = Dcs_ScrapingRequisition.objects.all().filter(websitelink=st)
    combined_data = [{'item': i, 'res': r} for i, r in zip(item, res)]
    # print("show data")
    # print('................', item)
    return render(request, "download_scrape_url.html", {'combined_data': combined_data})

# -------------------------------------------------------- download files and View-All url_show+https -----------------------------------------------------


@login_required(login_url='login')
def DonwloadScrapeFile(request, filename):
    print('DonwloadScrapeFile.......................')
    base_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_directory, "uploads_Scrape", filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            # Determine the file extension
            file_extension = os.path.splitext(filename)[1].lower()

            # Set the appropriate content type based on the file extension
            if file_extension == '.csv':
                content_type = 'application/csv'
            elif file_extension == '.xlsx':
                content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif file_extension == '.zip':
                content_type = 'application/zip'
            else:
                return HttpResponse("Invalid file format")

            response = HttpResponse(file.read(), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("File not found")


# *********************************************** list of urls ********************************************************
@login_required(login_url='login')
def Website(request):
    print("........Website...running")
    
    with connection.cursor() as cursor:
        query = '''
            SELECT DISTINCT(websitelink), id
            FROM app1_dcs_scrapingrequisition
            GROUP BY websitelink
            ORDER BY id DESC '''
        cursor.execute(query)
        result = cursor.fetchall()

    item = []
    res = []
    for row in result:
        item.append(row[0])
        res.append(row[1])

    combined_data = [{'websitelink': i, 'id': r} for i, r in zip(item, res)]
    
    return render(request, 'website_list_show_data.html', {'lsts': combined_data})




# ----------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def WebsiteListUpload(request):
    print('.......WebsiteListUpload...running')
    if request.method == 'POST':
        website_name = request.POST.get('website_list')
        saves = WebsiteList(website_list=website_name)
        saves.save()
        # messages.success(request, "Form Submitted Successfully")
        # return redirect('website')  # Redirect to a success page or another view
    return render(request, 'website_list_form.html')





# ----------------------------------------------------------------------------------------------------------------------------------------
def is_admin(user):
    return user.is_authenticated and user.is_superuser
@user_passes_test(is_admin,login_url='/not_authorized/')
@login_required(login_url='login')
def ActionFormss(request, websitelink_id):
    print('............................ ActionFormss')
    try:
        default_websitelink_obj = get_object_or_404(Dcs_ScrapingRequisition, pk=websitelink_id)
        default_websitelink = default_websitelink_obj.websitelink
    except Dcs_ScrapingRequisition.DoesNotExist:
        default_websitelink = ""

    website_links = Dcs_ScrapingRequisition.objects.filter(websitelink__icontains=default_websitelink)

    if request.method == 'POST':
        selected_website_id = request.POST.get('Websites')  # Get the selected website ID
        selected_website = get_object_or_404(Dcs_ScrapingRequisition, pk=selected_website_id)
        
        assign_to = request.POST.get('Assign_to')
        assign_time = request.POST.get('Assign_time')
        provided_by = request.POST.get('Provided')
        status = request.POST.get('Status')

        # Create a new Dcs_ActionsForms object with the provided data
        save_form_data = Dcs_ActionsForms.objects.create(
            websitelink=selected_website,  # Assign the instance, not the ID
            websites=default_websitelink_obj.websitelink,
            assign_to=assign_to,assign_time=assign_time,
            provided_by=provided_by,status=status
        )
        save_form_data.save()
        # Redirect after successful form submission
        return redirect('/action_form/')
    
    return render(request, 'actions_to.html', {'default_websitelink': default_websitelink,'website_links': website_links})




# ----------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def ActinFomrGetDetails(request):
    print('ActinFomrGetDetails.........................')
    # Fetch all data from the Dcs_ActionsForms model
    show_data1 = Dcs_ActionsForms.objects.all()
    print(show_data1)
    return render(request, 'action_request_get_details.html', {'show_data1': show_data1})





# ----------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def Not_Authorized(request):
    print('.................Not_Authorized')
    return render(request, 'not_authorized.html')





# ----------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def ProfilUpdate(request):
    print('..............................profileupdate')
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('pass')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        # Validate if new password and confirmation match
        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return redirect('profile')
        # Authenticate user using username and old password
        user = authenticate(username=username, password=old_password)
        if user is not None:
            # Update the password
            user.set_password(new_password)
            user.save()
            # Update the session's authentication hash to prevent logout
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully.")
            return redirect('login')
        else:
            messages.error(request, "Invalid old password.")
            return redirect('profile')

    return render(request, 'profile.html')




# ----------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def ProfileSettings(request):
    print('..............................ProfileSettings')
    return render(request, ('setting.html'))




# ----------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def ReportGetDetails(request, websitelink_id):
    matched_data = Dcs_ScrapingRequisition.objects.filter(id__in=Dcs_ActionsForms.objects.values('websitelink_id')).values('id','choose_website')
    specific_scraping_data = Dcs_ActionsForms.objects.filter(websitelink_id__in=matched_data.values('id')).values('websites', 'assign_to', 'provided_by', 'assign_time')
    dropdown_list = Dcs_ScrapingRequisition.objects.all()  
    # Combine the data
    combined_data = [{'item': i, 'res': r} for i, r in zip(matched_data, specific_scraping_data)]
    # Prepare context
    context = {
        'combined_data': combined_data,
        'dropdown_list': dropdown_list,}

    return render(request, 'report.html', context)

