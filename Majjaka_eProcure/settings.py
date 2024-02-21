"""
Django settings for Majjaka_eProcure project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

# import django_heroku
import os
SEARCH_FORM1 = "X"  # To enable or disable Extended search form
# import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-p^#04gmm3jl$93p3jx9rm+t1nj4$xl9b_#%192&e_usmw*&nr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# ALLOWED_HOSTS = ['www.procurezy.com', 'procurezy.com'] # for deployment
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eProc_Shopping_Cart',
    'eProc_Email_Notification',
    'eProc_Doc_Search',
    'eProc_Doc_Details',
    'eProc_Basic',
    'eProc_Login',
    'eProc_Registration',
    'eProc_Upload',
    'eProc_User_Settings',
    'eProc_Notes_Attachments',
    'eProc_Org_Model',
    'eProc_Purchase_Order',
    # 'apiLayer',
    # 'dbLayer',
    'eProc_Reports',
    'eProc_Admin_Tool',
    'eProc_User_Admin',
    'eProc_System_Settings',
    'eProc_Attributes',
    'eProc_Configuration',
    'eProc_Purchaser_Cockpit',
    'eProc_Price_Calculator',
    'eProc_Role_authorization',
    'eProc_Catalog',
    'eProc_Workflow',
    'eProc_SAP_Connector',
    'eProc_Calendar_Settings',
    'eProc_Generate_PDF',
    'eProc_Form_Builder',
    'eProc_Notification',
    'channels',
    'eProc_SOBO',
    'eProc_Account_Assignment',
    'eProc_Shop_Home',
    'eProc_Ship_To_Bill_To_Address',
    'eProc_Add_Item',
    'eProc_Org_Support',
    'eProc_Doc_Search_and_Display',
    'eProc_Users',
    'eProc_Suppliers',
    'eProc_Manage_Content',
    'eProc_Emails',
    'eProc_Chat',
    'django_sass',
    'eProc_Basic_Settings',
    'eProc_Master_Settings',
    'eProc_Application_Settings',
    'eProc_Content_Search',
    'eProc_Messages',
    'eProc_Application_Monitoring',
    'eProc_Related_Documents',
    'eProc_Configuration_Check',
    'eProc_Generate_OTP',
    'eProc_New_Client_Setup',
    'eProc_Time_Sheet',
    'eProc_Projects',
    'eProc_Supplier_Order_Management',
    'eProc_Rfq',
    'eProc_Archiving',
    # 'eProc_Marketing',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Django ModelBackend is the default authentication backend.

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'dbLayer.cMiddleWare.CustomMiddleware',
]

ROOT_URLCONF = 'Majjaka_eProcure.urls'

# SESSION_EXPIRE_SECONDS = 120
# SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
# SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60 # group by minute
# SESSION_TIMEOUT_REDIRECT =  '/login/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "MUtilities")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'eProc_Shopping_Cart.context_processors.globalise_context',
            ],
        },
    },
]
ENCRYPT_KEY = b'ZPXWMYf30VUj-L9ZViJJdAqUaYC8s_jezyw6X3uZzLs='
sub_menu = {}
slide_menu = {}
cart_counter = 0

WSGI_APPLICATION = 'Majjaka_eProcure.wsgi.application'
ASGI_APPLICATION = 'Majjaka_eProcure.routing.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# ./manage.py migrate my_app 0010
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Database engine
        'HOST': 'sg2plzcpnl489587.prod.sin2.secureserver.net',  # Database host
        'NAME': 'MEP_MIGRATE_DEV',
        # Database name MEP_MIGRATE_DEV MEP_FIXING MEP_DEPLOYED_NEW_QA_23 MEP_DEPLOYED_NEW_29 MEP_DEPLOYED_NEW_QA_0506
        'USER': 'MajjakaShopEProcure',  # Database username
        'PASSWORD': 'Project@2019',  # Database credentialsgi
        'PORT': '3306',  # Database port number
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',  # Sets the default storage engine
        }
    },
}
SMS_BACKEND = 'sms.backends.console.SmsBackend'
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Hosting related updates for Heroku
# db_from_env = dj_database_url.config()
# DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'Majjaka_eProcure.validators.CustomPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# configuring email for Forgot password
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.hiranya-garbha.com'
EMAIL_PORT = 26
EMAIL_HOST_USER = 'support@hiranya-garbha.com'
EMAIL_HOST_PASSWORD = 'Office@123'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Hiranya-Garbha <support@hiranya-garbha.com>'
# SERVER_EMAIL = 'mail.hiranya-garbha.com'
PHONE_NUM = '9845648568'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'  # Path for static files
################################# Deployment ###########################
STATIC_ROOT = 'staticfiles'  # for deployment
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)  # for deployment
################################# Deployment ###########################

LOGIN_URL = '/'  # Login URL
AUTH_USER_MODEL = 'eProc_Registration.UserData'  # Custom User Model for authentication
SEARCH_FORM = " "  # To enable or disable Extended search form
DATETIME_FORMAT = 'Y-m-d H'  # To get the desired datetime format
ATTACH_PATH = "Files"  # Attachments and PO-PDF file path

# Start of  SC-2S-US15
# Attachments url and folder to be stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Activate Django-Heroku.
# django_heroku.settings(locals())
timeout_IKEA = 300
timeout_850 = 600

# SESSION_COOKIE_AGE = timeout_IKEA # Session will expiry after 30 minutes idle.
SESSION_SAVE_EVERY_REQUEST = True
# LOGGING ={
#     'version':1,
#     'disable_existing_loggers': True,
#     'loggers':{
#         'django':{
#             'handlers':['file','file2'],
#             'level':'DEBUG'
#         }
#     },
#     'handlers':{
#         'file':{
#             'level':'INFO',
#             'class': 'logging.FileHandler',
#             'filename':'./logs/info_logs.log',
#             'formatter':'simpleRe',
#         },
#         'file2':{
#             'level':'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename':'./logs/debug_logs.log',
#             'formatter':'simpleRe',
#         }
#     },
#     'formatters':{
#         'simpleRe': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         }
#
#     }
# }
AUTH_KEY = 'majjaka'
