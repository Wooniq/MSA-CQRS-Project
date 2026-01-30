from .models import Book
from .serializers import BookSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

#카프카에 게시를 하기 위한 라이브러리
from kafka import KafkaProducer
import json

#Producer 클래스
class MessageProducer:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic

        self.producer = KafkaProducer(
            bootstrap_servers = self.broker,
            value_serializer = lambda x: json.dumps(x).encode("utf-8"),
            acks=1,
            api_version = (2, 5, 0),
            key_serializer = str.encode,
            retries=3,
        )

    def send_message(self, msg, auto_close=True):
        try:
            #토픽 전송
            future = self.producer.send(self.topic, value=msg, key="key")
            self.producer.flush()

            if auto_close:
                self.producer.close()
            future.get(timeout=2)
            return {"status_code":200, "error":None}

        except Exception as exc:
            raise exc

@api_view(['GET'])
def helloAPI(request):
    return Response('hello workd')

#POST 방식의 요청이 온 경우 처리
@api_view(['POST'])
def bookAPI(request):
    #클라이언트에서 넘겨준 데이터를 가져오기
    data = request.data
    #웹에서 넘어온 데이터는 문자열이므로 숫자로 변환
    data['pages'] = int(data['pages'])
    data['price'] = int(data['price'])
    #데이터베이스에 삽입 가능하도록 변환
    serializer = BookSerializer(data=data)
    #삽입
    if(serializer.is_valid()):
        #데이터 삽입
        serializer.save()
        #카프카에 이벤트를 발행
        broker = ["localhost:9092"]
        topic = "cqrstopic"
        pd = MessageProducer(broker, topic)
        #데이터 와 작업 내역을 한꺼번에 전송
        msg = {"task":"insert", "data": serializer.data}
        res = pd.send_message(msg)
        print(res)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
