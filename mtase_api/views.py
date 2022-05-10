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

import iso639
from langdetect import detect


from .utils.translate import detect_and_translate
from .utils.extractive_summariser import extractive_summariser
from .utils.keyword_extractor import keyword_extractor
from .utils.abstractive_summariser import abstractive_summariser

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

                with open(file_to_read, encoding='utf8') as f:
                    contents = f.read()
                    text = contents

                if os.path.exists(file_to_read):
                    os.remove(file_to_read)
                else:
                    logging.warning("The file does not exist")

        original_lang = iso639.to_name(detect(text))

        translated_text = detect_and_translate(text, target_lang='en')
        reverse_translation = ""
        
        keywords = []

        if(translated_text == ""):
            abstractive_summary = abstractive_summariser(text)
            extractive_summary = extractive_summariser(text)
            keywords = keyword_extractor(text)
            translated_text_len = 0
        else:
            abstractive_summary = abstractive_summariser(translated_text)
            extractive_summary = extractive_summariser(translated_text)
            keywords = keyword_extractor(translated_text)
            translated_text_len = len(translated_text.split())
            tran_lang = detect(text)
            abs_reverse_translation = detect_and_translate(abstractive_summary, target_lang=tran_lang)
            ext_reverse_translation = detect_and_translate(extractive_summary, target_lang=tran_lang)

        text_len = len(text.split())
        abstractive_summary_len = len(abstractive_summary.split())
        extractive_summary_len = len(extractive_summary.split())


        return Response(
                        {
                            "len": {
                                "text_len": text_len,
                                "translated_text_len": translated_text_len,
                                "abstractive_summary_len": abstractive_summary_len,
                                "extractive_summary_len": extractive_summary_len,
                            },
                            "text": {
                                "text": text,
                                "translated_text": translated_text,
                                "abs_reverse_translation": abs_reverse_translation,
                                "ext_reverse_translation": ext_reverse_translation,
                                "abstractive_summary": abstractive_summary,
                                "extractive_summary": extractive_summary,
                            },
                            "keywords": keywords,
                            "original_lang": original_lang
                        }, status=status.HTTP_201_CREATED)



class TestView(generics.GenericAPIView):

    def get(self, request):
        return Response({'resp': "It's Working"}, status=status.HTTP_200_OK)