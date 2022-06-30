from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class ChatUser(AbstractUser):
	# In case you want to add more fields in Django user table write bellow
	is_active = models.BooleanField(default=True)

	class Meta:
		verbose_name 		= 'ChatUser'
		verbose_name_plural = 'ChatUsers'


class Patterns(models.Model):
	"""docstring for Patterns"""
	question 	= models.CharField(max_length=500, blank=False, null=False) 
	answers  	= ArrayField(models.CharField(max_length=500), blank=False, null=False)
	tag			= models.CharField(max_length=100, blank=False, null=False)
	created_by	= models.ForeignKey(ChatUser, on_delete=models.CASCADE)
	created_at 	= models.DateTimeField(auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name 		= 'Pattern'
		verbose_name_plural = 'Patterns'


class ChatLogs(models.Model):
	"""docstring for ChatLogs"""
	question 			= models.CharField(max_length=500, blank=False, null=False) 
	response  			= models.CharField(max_length=1500, blank=False, null=False)
	tag					= models.CharField(max_length=100, blank=False, null=False)
	asked_by 			= models.EmailField(max_length = 254)
	is_registered		= models.BooleanField(default=False)
	created_at 			= models.DateTimeField(auto_now_add=True)
	updated_at			= models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name 		= 'ChatLog'
		verbose_name_plural = 'ChatLogs'

class InfoTable(models.Model):
	"""docstring for InfoTable"""
	ref_no 									= models.AutoField(primary_key=True)
	model_no  								= models.CharField(max_length=100)
	branch    								= models.CharField(max_length=100)
	email_address							= models.CharField(max_length=200)
	contract_potential 						= models.CharField(max_length=100)
	ship_to_party  							= models.CharField(max_length=100)
	bill_to_party            				= models.CharField(max_length=100)
	ship_to_party_address_1					= models.CharField(max_length=100)
	ship_to_party_address_2					= models.CharField(max_length=100)
	ship_to_party_address_3     			= models.CharField(max_length=100)
	ship_to_party_postcode      			= models.IntegerField(default=None,null=True)
	ship_to_party_city_town     			= models.CharField(max_length=100)
	ship_to_party_state         			= models.CharField(max_length=100)
	ship_to_party_tel_no        			= models.CharField(max_length=100)
	ship_to_party_fax_no 					= models.CharField(max_length=100)
	ship_to_party_price_group   			= models.CharField(max_length=100)
	ship_to_party_customer_group			= models.CharField(max_length=100)
	department_location						= models.CharField(max_length=100)
	person_in_charge				 		= models.CharField(max_length=100)
	commissioning_date 				 		= models.DateField(auto_now_add=True)
	commissioning_reference_no        		= models.CharField(max_length=100)
	agreement_reference_no		      		= models.CharField(max_length=100, null=True)
	warranty_period_start_date        		= models.DateField(auto_now_add=True)
	warranty_period_end_date           		= models.DateField(auto_now_add=True)
	total_no_of_servicing              		= models.IntegerField(default=None,null=True)
	total_months_of_servicing          		= models.IntegerField(default=None,null=True)
	plan_preventive_maintenance		   		= models.CharField(max_length=100)
	payment_mode                       		= models.CharField(max_length=100)
	status    								= models.CharField(max_length=100)
	warranty_type          		 			= models.CharField(max_length=100)
	suspended   							= models.CharField(max_length=100)
	ship_to_party_id       					= models.IntegerField(default=None,null=True)
	ema_number   							= models.CharField(max_length=100)
	ema_number_contract_start       		= models.CharField(max_length=100)
	ema_number_contract_end         		= models.CharField(max_length=100)
	ema_number_status_display       		= models.CharField(max_length=100)
	ema_number_payment_mode_display 		= models.CharField(max_length=100)
	ema_number_payment_mode_display 		= models.CharField(max_length=100)
	model_no_model_number             		= models.CharField(max_length=100)
	model_no_standardised_model_name    	= models.CharField(max_length=100)
	model_no_business_segment_display   	= models.CharField(max_length=100)
	model_no_business_product_display   	= models.CharField(max_length=100)
	model_no_brand_display          	    = models.CharField(max_length=100)
	expiry_date   							= models.DateField(auto_now_add=True)
	bill_to_party_price_group_display  		= models.CharField(max_length=100)
	bill_to_party_customer_group_display 	= models.CharField(max_length=100)
	bill_to_party_customer_name				= models.CharField(max_length=100)
	ship_to_party_customer_name 			= models.CharField(max_length=100)
	ema_number_contract_type_display 		= models.CharField(max_length=100)
	ship_to_party_debtor_code 				= models.CharField(max_length=100)
	bill_to_party_debtor_code 				= models.CharField(max_length=100)


	class Meta:
		verbose_name 		= 'InfoTable'
		verbose_name_plural = 'InfoTables'

	def check_user_exists(self,user_email):
		return InfoTable.objects.filter(email_address=user_email).exists()

	def getUserInfo(self,user_email):
		user_info = None
		try:
		    user_info = InfoTable.objects.get(email_address=user_email)
		except:
		    user_info = None
		return user_info


class Document(models.Model):
	email_address       = models.EmailField(max_length = 254)
	title 				= models.CharField(max_length = 200)
	uploadedFile	 	= models.FileField(upload_to = "Uploaded Files/")
	dateTimeOfUpload 	= models.DateTimeField(auto_now = True)
	
	class Meta:
		verbose_name 		= 'Document'
		verbose_name_plural = 'Documents'