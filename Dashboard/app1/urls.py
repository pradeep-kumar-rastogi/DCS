from django.urls import path
from app1 import views
from .views import *
urlpatterns = [
  
    path('base/', views.BasePage, name='base'),
    path('signup/', views.SignupPage, name='signup'),
    path('',views.LoginPage,name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/',views.LogoutPage,name='logout'),    
    path('info/<str:id>/',views.info,name='info'), # got to to info page here  
    path('home/update/<int:id>/',views.update,name='update'), 
    path('home/delete/<int:id>/',views.delete,name='delete'),
    path('form_show/', views.ShowForm, name='form_show'),   #   Go to the Request Form here
    path('download/uploads/<str:filename>/', download_file, name='download_file'), # dynamic path urls

    path('upload_csv/<int:id>/',views.Upload_csv,name='upload_csv'),         #   Go to the Uploaded Your Scrape Files here
    path('download_csv/uploads_Scrape/<str:filename>/', views.download_csv, name='download_csv'),     #   Go to the download Your Scrape Files here


    #------------------------------------------- list of upload scrape urls and download -----------------------------------------------
    path('Scrape_url/', views.ScapeUrlForm, name='Scrape_url'),   
    path('download_url/uploads_Scrape/<str:filename>/', views.DonwloadScrapeFile, name='download_url'),
    # ---------------------------------------------------------------------------------------------------------------------------------
    # path('url_data/<str:url>/', views.UrlShow, name='url_data'),
    #--------------------------------------------------------------------------------------------
    path('url_show/', views.UrlShow, name='url_show'),
    path('url_data/<int:id>/', views.Url, name='url_data'),

    path('history/<str:st>', views.RequisitionHistory, name='history'),


    # ------------------------------------------- list of website urls -----------------------------------------------------------------
    path('website/', views.Website, name='website'),    
    path('website_list_upload/', views.WebsiteListUpload, name='website_list_upload'),   
     
    # ----------------------------------------profile uptade ------------------------------------------
    path('profile/', views.ProfilUpdate, name='profile'),
    path('settings/', views.ProfileSettings, name='settings'),


    # --------------------------------------------------------------
    path('action_to/<int:websitelink_id>/', views.ActionFormss, name='action_to'),
    path('action_form/', views.ActinFomrGetDetails, name='action_form'),


    path('not_authorized/', views.Not_Authorized, name='not_authorized'),


    path('report/<int:websitelink_id>/', views.ReportGetDetails, name='report'),

    




]