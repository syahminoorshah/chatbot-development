from bs4 import BeautifulSoup
from urllib.request import urlopen
from ..models import InfoTable

class ChatBotHelper():
	"""docstring for ChatBotHelper"""

	def HandelInfo(tag_value,value,user_email):
		if tag_value == 'city':
			if InfoTable.objects.filter(email_address=user_email).exists():
				InfoTable.objects.filter(email_address=user_email).update(ship_to_party_city_town = value)
			else:
				infoobj = InfoTable(email_address=user_email, ship_to_party_city_town = value)
				infoobj.save()

		if tag_value == 'medical_center':
			if InfoTable.objects.filter(email_address=user_email).exists():
				InfoTable.objects.filter(email_address=user_email).update(ship_to_party = value)
			else:
				infoobj = InfoTable(email_address=user_email, ship_to_party = value)
				infoobj.save()

		if tag_value == 'model':
			if InfoTable.objects.filter(email_address=user_email).exists():
				InfoTable.objects.filter(email_address=user_email).update(model_no_brand_display = value)
			else:
				infoobj = InfoTable(email_address=user_email, model_no_brand_display = value)
				infoobj.save()



class WebScraper():
	"""docstring for WebScraper"""
	def GrabPageText(url):
		page = urlopen(url)
		html = page.read().decode("utf-8")
		soup = BeautifulSoup(html, "html.parser")
		PageInfo = ""
		for div in soup.findAll('div', {'class': 'et_pb_text_inner'}):
			PageInfo = PageInfo +" "+ div.text.strip()
		return PageInfo


class StringRender():
	"""docstring for WebScraper"""
	def _renderString(rowStr, **kwargs):
		return rowStr.format(**kwargs)
