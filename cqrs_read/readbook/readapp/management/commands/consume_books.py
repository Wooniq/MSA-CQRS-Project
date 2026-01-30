import json
import threading
import time
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from pymongo import MongoClient

# [1] 백그라운드에서 실행될 스레드 클래스 정의
class BookConsumerThread(threading.Thread):
    def __init__(self, broker, topic):
        super().__init__()
        self.broker = broker
        self.topic = topic
        # 데몬 스레드로 설정: 메인 프로세스(Command) 종료 시 함께 종료됨
        self.daemon = True  

    def run(self):
        """스레드가 시작(start)되면 실제로 수행하는 로직"""
        try:
            # Kafka Consumer 설정
            consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.broker,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='earliest',  # 가장 처음 메시지부터 읽음
                enable_auto_commit=True,
                group_id='my-group',
                api_version=(2, 5, 0)          # 사용 중인 Kafka 버전 명시
            )

            # MongoDB 연결 설정
            client = MongoClient('mongodb://localhost:27017/')
            db = client.cqrs
            collection = db.books

            print(f"[*] [Thread] '{self.topic}' 토픽 구독 시작...")

            # 메시지 무한 루프 수신
            for message in consumer:
                msg_data = message.value          # 1. Kafka에서 메시지(Postgres의 데이터)를 꺼냄
                task = msg_data.get("task")       # 2. 어떤 작업(Insert, Update 등)인지 확인
                book_data = msg_data.get("data")  # 3. 실제 데이터(책 정보)를 추출

                if task == "insert":              # 4. "만약 Postgres에 데이터가 추가되었다면?"
                    # MongoDB에 데이터 삽입
                    collection.insert_one(book_data)
                    print(f"[OK] [Thread] MongoDB 동기화 완료: {book_data.get('title')}")
        
        except Exception as e:
            print(f"[Error] [Thread] 컨슈머 구동 중 에러 발생: {e}")

# [2] Django가 인식하는 커스텀 명령어 클래스
class Command(BaseCommand):
    help = 'Kafka 메시지를 스레드 방식으로 구독하여 MongoDB에 저장합니다.'

    def handle(self, *args, **options):
        # 환경 설정
        broker = ["localhost:9092"]
        topic = "cqrstopic"

        self.stdout.write(self.style.SUCCESS(f"[*] '{topic}' 전용 컨슈머 스레드 가동 준비 중..."))

        # 1. 스레드 객체 생성
        consumer_thread = BookConsumerThread(broker, topic)

        # 2. 스레드 시작 (내부의 run 메서드가 백그라운드에서 실행됨)
        consumer_thread.start()

        self.stdout.write(self.style.SUCCESS(f"[*] 동기화 엔진이 백그라운드에서 실행 중입니다."))
        self.stdout.write(self.style.SUCCESS(f"[*] 종료하려면 Ctrl+C를 누르세요."))

        # 3. 메인 프로세스가 바로 종료되지 않도록 무한 루프로 대기
        try:
            while True:
                time.sleep(1)  # 1초마다 대기하며 프로세스 유지
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\n[!] 사용자에 의해 동기화 엔진이 중단되었습니다."))