from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from django.shortcuts import render
from .models import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer, TextSerializer

from django.conf import settings
from pathlib import Path

import os
import logging

# Create your views here.

class SummariseAnalyseView(generics.GenericAPIView):

    def post(self, request):

        text = ""

        if 'file' not in request.data:
            text = request.data.get('text')
        else:
            print("yes !")
            serializer = FileSerializer(data=request.data)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                record = File.objects.latest('timestamp')
                filename = str(record.file)
                txt_folder_path = Path(settings.MEDIA_ROOT)
                file_to_read = txt_folder_path / filename

                with open(file_to_read) as f:
                    contents = f.read()
                    print(contents)
                    text = contents

                if os.path.exists(file_to_read):
                    os.remove(file_to_read)
                else:
                    logging.warning("The file does not exist")


        return Response({
                        "text": text
                      }, status=status.HTTP_201_CREATED)



class TestView(generics.GenericAPIView):

    def get(self, request):
        return Response({'resp': "It's Working"}, status=status.HTTP_200_OK)