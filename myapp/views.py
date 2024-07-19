from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from langchain_community.llms import Ollama
import re
from .models import Artists,Programs,EntitiesMaster
from .serializers import EntitiesMasterSerializer

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


class WebScrapper(APIView):
    """
    API For Scraping Urls
    """
    format = {
        "artists": [{"artist_name": "string", "artist_role": "string"}],
        "programs": [{"program_name": "string", "program composer": "string"}],
        "performances": {"date": "date", "time": "time", "auditorium": "string"}
        
    }

    def post(self, request):
        url = request.data.get("url", None)
        if url is None:
            return Response(
                {"detail": "Provide url", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        driver.get(url)
        page_source = driver.page_source
        parsed_data = BeautifulSoup(page_source, 'html.parser')
        data_section = str(parsed_data.find("section", id="buy"))
        llm = Ollama(model="llama3")
        response = llm.invoke(
            rf"{data_section} Extract the following details from the HTML code: artist name, program name, artist role, Date, time, auditorium as in the format -{self.format} Return the data as a dictionary with the specified keys and no additional text or explanations."
        )
        match = re.search(r'```\s*(\{.*\})\s*```', response, re.DOTALL)
        matched_data = match.group(1)
        json_data =eval(matched_data)
        artists = json_data.get("artists",[])
        program_details = json_data.get("programs",[])
        performances =  json_data.get("performances",{})
        Artists.objects.bulk_create([Artists(**obj) for obj in artists])
        for program in program_details:
            Programs.objects.create(
                program_name = program.get('program_name'),
                program_composer = program.get('program composer',None)
            )
        obj =EntitiesMaster.objects.create(
            date = performances.get('date'),
            time = performances.get('time'),
            auditorium = performances.get('auditorium')
            )
        obj.save()
        obj.programs.add(*Programs.objects.all())
        obj.artists.add(*Artists.objects.all())
        
        return Response(
            {"detail": json_data, "success": True ,
             "message":"details saved"}, status=status.HTTP_200_OK
        )

    def get(self,request):
        serialized_data = EntitiesMasterSerializer(EntitiesMaster.objects.all(),many=True).data
        return Response({"detail":serialized_data,"success":True},
                        status=status.HTTP_200_OK)