# MSA-CQRS 

## 실행 방법

### 1. 인프라 환경 구축 (Docker)
먼저 Kafka와 데이터베이스(PostgreSQL, MongoDB)를 실행
```bash
docker-compose up -d
```

### 2. Write 서비스 실행 (Port 7000)
```bash
cd cqrs_write/writebook
# 가상환경 활성화 후
python manage.py runserver 7000
```

### 3. Read 서비스 실행 (Port 8000)
```bash
cd cqrs_read/readbook
# 가상환경 활성화 후
python manage.py runserver 8000
```

### 4. 데이터 동기화 엔진(Kafka Consumer) 실행
Write 서비스에서 발생한 이벤트를 Read 서비스(MongoDB)에 반영
```bash
cd cqrs_read/readbook
# 가상환경 활성화 후
python manage.py consume_books
```

### 프론트엔드 실행
```bash
cd react_cqrs
npm install  # 첫 실행 시
npm start
```

---

### 시스템 아키텍처 및 데이터 Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant React as Frontend (React)
    
    box rgba(255, 0, 0, 0.1) Write Side (쓰기 전용)
    participant WriteAPI as Write API (Django:7000)
    database Postgres as PostgreSQL (원본 DB)
    end
    
    participant Kafka as Kafka (Event Broker)
    
    box rgba(0, 0, 255, 0.1) Read Side (읽기 전용)
    participant ReadConsumer as Consumer (동기화)
    database Mongo as MongoDB (조회용 DB)
    participant ReadAPI as Read API (Django:8000)
    end

    Note over User, WriteAPI: 1. 데이터 생성 (Command)
    User->>React: 도서 추가 요청
    React->>WriteAPI: POST /books
    WriteAPI->>Postgres: 데이터 저장
    WriteAPI->>Kafka: BookCreated 이벤트 발행
    WriteAPI-->>React: 201 Created 응답

    Note over Kafka, Mongo: 2. 비동기 동기화 (Eventual Consistency)
    Kafka->>ReadConsumer: 메시지 전달
    ReadConsumer->>Mongo: 조회용 데이터 생성/업데이트

    Note over User, ReadAPI: 3. 데이터 조회 (Query)
    User->>React: 목록 조회 페이지
    React->>ReadAPI: GET /books
    ReadAPI->>Mongo: 최적화된 데이터 조회
    ReadAPI-->>React: JSON 데이터 반환
    React-->>User: 화면 렌더링
```

- **Write Service (Django)**: PostgreSQL을 사용하여 데이터의 생성, 수정, 삭제(Command) 처리
- **Read Service (Django)**: MongoDB를 사용하여 데이터의 조회(Query) 처리
- **Message Broker (Kafka)**: 두 서비스 간의 데이터 동기화를 위한 이벤트 버스 역할
- **Frontend (React)**: 사용자 인터페이스를 제공하며 Write/Read API 각각 호출

## 기술 스택
- **Backend**: Python, Django, Django REST Framework
- **Frontend**: React.js
- **Database**: PostgreSQL (Write), MongoDB (Read)
- **Message Broker**: Apache Kafka
- **DevOps**: Docker, Docker Compose