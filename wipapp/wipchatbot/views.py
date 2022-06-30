from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import *
from .models import ChatUser, Document, InfoTable
from .chatbot.chat import send_to_chatbot
from .helper.chathelper import ChatBotHelper, WebScraper, StringRender
import ast

# Create your views here.

class LoginView(APIView):
	permission_classes = (AllowAny,)
	def post(self,request):
		username = request.data.get("username")
		password = request.data.get("password")
		if username is None or password is None:
			return Response({'error': 'Please provide both username and password'},
							status=status.HTTP_400_BAD_REQUEST)
		user = authenticate(username=username, password=password)
		if not user:
			return Response({'error': 'Invalid Credentials'},
				status=status.HTTP_404_NOT_FOUND)

		serializer 				= UserSerializer(user)
		token 					= TokenObtainPairSerializer().validate(request.data)

		userInfo 				= InfoTable() 
		user_info 				= userInfo.getUserInfo(serializer.data['email'])
		if user_info:
			res  					= send_to_chatbot("inbuilt_tag_confirmation")
			res["result"]["res"] 	= StringRender._renderString(
													  rowStr 		= res["result"]["res"], 
													  name 			= serializer.data['username'],
													  email_address = serializer.data['email'],
													  ship_to_party = userInfo.ship_to_party if userInfo else None,
													  ship_to_party_city_town = userInfo.ship_to_party_city_town if userInfo else None,
													  model_no_brand_display = userInfo.model_no_brand_display if userInfo else None
													)
		else:
			res  = send_to_chatbot("inbuilt_greeting_tag")
		response = {
					'token'	: token, 
					'user' 	: serializer.data,
					'botres': res["result"]
					}
		return Response(response,status=status.HTTP_200_OK)

# Create your views here.
class UserRegister(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):

		email = request.data['email']
		if ChatUser.objects.filter(email = email).exists():
			err_response = {
								'status'	: False,
								'message'	: f"{email} is allready taken.",
								'data'		: None
							}
			return Response(err_response, status=status.HTTP_200_OK)

		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			u_obj       = serializer.save()
			user 		= authenticate(username=request.data["username"], password=request.data["password"])
			token 		= TokenObtainPairSerializer().validate(request.data)
			res  	 	= send_to_chatbot("inbuilt_tag_hospital")
			response    = {
								'status'	: True,
								'message'	: 'User created successfully.',
								'data'		: serializer.data,
								'token'		: token,
								'botres'	: res["result"]
						   }
			
			return Response(response,status=status.HTTP_200_OK)
		else:
			err_response = {
								'status'	: False,
								'message'	: serializer.errors,
								'data'		: None
							}
			return Response(err_response, status=status.HTTP_200_OK)

class ChatBotView(APIView):
	# permission_classes = (AllowAny,)
	def post(self,request):

		res  	 = send_to_chatbot(request.data["msg"])
		userInfo = InfoTable() 

		if res["tag"] == "tagged_answer_positive":
			userInfo 		= userInfo.getUserInfo(request.user.email)
			res["result"] 	= StringRender._renderString(
													  rowStr 			= res["result"], 
													  name 				= request.user.username
													)
			return Response({'response': res["result"]},status=status.HTTP_200_OK)


		if res["tag"] == "tagged_as_issue":
			userInfo 				= userInfo.getUserInfo(request.user.email)
			res["result"]["res"] 	= StringRender._renderString(
													  rowStr 			= res["result"]["res"], 
													  name 				= request.user.username,
													  email_address 	= request.user.email,
													  ship_to_party 	= userInfo.ship_to_party if userInfo else None,
													  model_no_brand_display = userInfo.model_no_brand_display if userInfo else None
													)
			return Response({'response': res["result"]},status=status.HTTP_200_OK)

		if res["tag"] == "inbuilt_tag_getoldchat":
			oldChats 	= ChatLogs.objects.filter(asked_by = request.user.email).all()
			response 	= []

			for oldChat in oldChats:
				
				response.append({
								"speaks" : "user",
								"text" 	 : oldChat.question,
								"opt" 	 : []
								})

				try :
					respo = ast.literal_eval(oldChat.response)
				except:
					respo = oldChat.response

				if isinstance(respo,dict):
					response.append({
									"speaks" : 'bot',
									"text" 	 :  respo["res"],
									"opt" 	 :  respo["opt"]
									})
				else:
					response.append({
									"speaks" : 'bot',
									"text" 	 :  respo,
									"opt" 	 :  []
									})

			return Response({'response': response},status=status.HTTP_200_OK)


		if res['tag'] == "website":
			PageInfo 		= WebScraper.GrabPageText("https://www.abexmedical.com.my/company-profile/")
			res["result"] 	= PageInfo

		ChatBotHelper.HandelInfo(res["tag"],request.data["msg"],request.user.email)
		serializer  = ChatLogsSerializer(data=
											{ "question"  : request.data["msg"],
											  "response"  : str(res["result"]),
											  "tag"		  : res["tag"],
											  "asked_by"  : request.user.email
											})
		if serializer.is_valid():
			serializer.save()
			return Response({'response': res["result"]},status=status.HTTP_200_OK)

		err_response = {
							'status'	: False,
							'message'	: serializer.errors,
							'data'		: None
						}
		return Response(err_response, status=status.HTTP_200_OK)

class UploadFile(APIView):
	def post(self,request):
		try :
			uploadedFile = request.FILES["file"]
			document = Document(
				email_address	= request.user.email,
				title 			= uploadedFile.name,
				uploadedFile 	= uploadedFile
			)
			document.save()
			return Response({'response':f'Uploaded SuccessFully!'},status=status.HTTP_200_OK)
		except:
			return Response({'response':'Problem In File Uploaded !'},status=status.HTTP_404_NOT_FOUND)
