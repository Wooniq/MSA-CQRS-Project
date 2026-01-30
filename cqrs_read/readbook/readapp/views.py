from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from pymongo import MongoClient
from bson import json_util
import json

@api_view(['GET'])
def bookAPI(request):
    conn = MongoClient('127.0.0.1')
    db = conn.cqrs
    collect = db.books

    result = collect.find()
    data = []
    for r in result:
        data.append(r)

    return Response(json.loads(json_util.dumps(data)),
    status=status.HTTP_201_CREATED)