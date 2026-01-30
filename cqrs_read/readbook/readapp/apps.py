from django.apps import AppConfig

import psycopg2
from pymongo import MongoClient
from datetime import datetime

class ReadappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'readapp'
    def ready(self):
        print("시작하자 마자 실행")
        #postgresql에 접속
        con = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="wnddkd",
            port="5432"
        )
        
        #MongoDB 연결
        conn = MongoClient('mongodb://localhost:27017')
        #기존 데이터 삭제
        db = conn.cqrs
        collect = db.books
        collect.delete_many({})

        #postgresql에서 데이터 읽어오기
        cursor = con.cursor()
        cursor.execute("select * from writeapp_book")
        data = cursor.fetchall()
        print(data)

        #데이터를 읽어서 MongoDB에 삽입
        for imsi in data:
            date = imsi[6].strftime("%Y-%m-%d")
            
            doc = {'bid':imsi[0], 'title':imsi[1], 'author':imsi[2],
            'category':imsi[3], 'pages':imsi[4], 'price':imsi[5],
            'published_date':date, 'description':imsi[7]}

            collect.insert_one(doc)
        con.close()