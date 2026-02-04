# Setup Guide - Feature 1.1 & 1.2

## 구현 완료 사항

✅ **Feature 1.1: 프로젝트 환경 설정**
- FastAPI 백엔드 기본 구조
- SQLite 데이터베이스 연결 설정
- CORS 및 환경 변수 설정
- 프론트엔드 기본 페이지

✅ **Feature 1.2: 데이터베이스 스키마 설계**
- FirewallLog 모델 (방화벽 로그)
- User 모델 (사용자 인증/권한)
- AlertRule 모델 (알림 규칙)
- 데이터베이스 초기화 및 시드 스크립트

---

## 빠른 시작

### 1. 백엔드 설정 및 실행

```bash
# 1-1. 백엔드 디렉토리로 이동
cd backend

# 1-2. Python 가상 환경 생성 (권장)
python -m venv venv

# 1-3. 가상 환경 활성화
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 1-4. 의존성 설치
pip install -r requirements.txt

# 1-5. 환경 변수 설정 (선택사항)
copy .env.example .env
# 필요시 .env 파일 수정

# 1-6. 데이터베이스 초기화
python scripts/init_db.py

# 1-7. 테스트 데이터 생성
python scripts/seed_data.py

# 1-8. 백엔드 서버 실행
uvicorn app.main:app --reload --port 8000
```

**백엔드 서버 확인:**
- API 문서: http://localhost:8000/docs
- 헬스체크: http://localhost:8000/health

---

### 2. 프론트엔드 설정 및 실행

```bash
# 2-1. 프론트엔드 디렉토리로 이동 (새 터미널)
cd frontend

# 2-2. 의존성 설치
npm install

# 2-3. 환경 변수 설정 (선택사항)
copy .env.local.example .env.local
# 필요시 .env.local 파일 수정

# 2-4. 개발 서버 실행
npm run dev
```

**프론트엔드 확인:**
- 홈페이지: http://localhost:3000

---

## 검증 방법

### 백엔드 API 테스트

#### 1. 헬스체크
```bash
curl http://localhost:8000/health
```
**예상 결과:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### 2. 로그인 테스트
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```
**예상 결과:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

#### 3. 로그 조회
```bash
curl http://localhost:8000/api/v1/logs?skip=0&limit=5
```

#### 4. 사용자 조회
```bash
curl http://localhost:8000/api/v1/users
```

---

### 데이터베이스 확인

```bash
cd backend/database
sqlite3 firewall_logs.db

# SQLite 프롬프트에서:
.tables
# 예상: firewall_logs  users  alert_rules

SELECT COUNT(*) FROM firewall_logs;
# 예상: 500

SELECT username, role FROM users;
# 예상: admin, operator, viewer

SELECT name, is_enabled FROM alert_rules;
# 예상: 3개 규칙

.exit
```

---

## 테스트 계정

| Username | Password | Role | 권한 |
|----------|----------|------|------|
| admin | admin123 | ADMIN | 전체 권한 |
| operator | operator123 | OPERATOR | 조회 + 설정 관리 |
| viewer | viewer123 | VIEWER | 조회만 가능 |

---

## 생성된 파일 구조

```
module_3/
├── backend/
│   ├── requirements.txt          # Python 의존성
│   ├── .env.example             # 환경 변수 템플릿
│   ├── database/                # SQLite 데이터베이스
│   ├── app/
│   │   ├── main.py              # FastAPI 애플리케이션
│   │   ├── core/
│   │   │   ├── config.py        # 설정 관리
│   │   │   ├── database.py      # DB 연결
│   │   │   └── security.py      # 인증/보안
│   │   ├── models/
│   │   │   ├── firewall_log.py  # 방화벽 로그 모델
│   │   │   ├── user.py          # 사용자 모델
│   │   │   └── alert_rule.py    # 알림 규칙 모델
│   │   ├── schemas/
│   │   │   ├── firewall_log.py  # 로그 스키마
│   │   │   ├── user.py          # 사용자 스키마
│   │   │   └── alert_rule.py    # 알림 규칙 스키마
│   │   └── api/v1/endpoints/
│   │       ├── auth.py          # 인증 API
│   │       ├── logs.py          # 로그 API
│   │       ├── users.py         # 사용자 API
│   │       └── alert_rules.py   # 알림 규칙 API
│   └── scripts/
│       ├── init_db.py           # DB 초기화
│       └── seed_data.py         # 테스트 데이터 생성
├── frontend/
│   ├── .env.local.example       # 환경 변수 템플릿
│   └── src/
│       ├── app/
│       │   ├── globals.css      # 전역 스타일
│       │   ├── layout.js        # 루트 레이아웃
│       │   └── page.js          # 홈페이지
│       └── lib/
│           └── api.js           # API 클라이언트
└── .gitignore                   # Git 제외 파일

총 32개 파일 생성
```

---

## API 엔드포인트

### 인증
- `POST /api/v1/auth/login` - 로그인

### 방화벽 로그
- `GET /api/v1/logs` - 로그 목록 (페이지네이션)
- `GET /api/v1/logs/{id}` - 로그 상세
- `POST /api/v1/logs` - 로그 생성
- `GET /api/v1/logs/count/total` - 로그 총 개수

### 사용자
- `GET /api/v1/users` - 사용자 목록
- `GET /api/v1/users/{id}` - 사용자 상세
- `POST /api/v1/users` - 사용자 생성

### 알림 규칙
- `GET /api/v1/alert-rules` - 알림 규칙 목록
- `GET /api/v1/alert-rules/{id}` - 알림 규칙 상세
- `POST /api/v1/alert-rules` - 알림 규칙 생성
- `PATCH /api/v1/alert-rules/{id}` - 알림 규칙 수정

---

## 데이터베이스 스키마

### firewall_logs (방화벽 로그)
- **필드**: id, timestamp, source_ip, source_port, destination_ip, destination_port, protocol, action, direction, severity, threat_type, bytes_sent, bytes_received, packet_count, log_source, raw_log, description
- **인덱스**: timestamp, source_ip, destination_ip, protocol, action
- **복합 인덱스**: (source_ip, destination_ip), (timestamp, action), (timestamp, severity)

### users (사용자)
- **필드**: id, username, email, hashed_password, role (ADMIN/OPERATOR/VIEWER), is_active, is_verified, last_login, login_count, failed_login_attempts, created_at, updated_at
- **인덱스**: username, email

### alert_rules (알림 규칙)
- **필드**: id, name, description, is_enabled, conditions (JSON), alert_type, alert_target, threshold_count, threshold_period, cooldown_period, last_triggered, priority, created_at, updated_at
- **인덱스**: name, is_enabled

---

## 문제 해결

### 포트 이미 사용 중
```bash
# Windows - 포트 8000 사용 프로세스 확인
netstat -ano | findstr :8000
# 프로세스 종료
taskkill /PID <PID> /F

# 또는 다른 포트 사용
uvicorn app.main:app --reload --port 8001
```

### 데이터베이스 재설정
```bash
cd backend
rm database/firewall_logs.db
python scripts/init_db.py
python scripts/seed_data.py
```

### 의존성 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

---

## 다음 단계 (Feature 2.x)

이제 다음 기능을 구현할 준비가 되었습니다:

1. **Feature 2.1**: 사용자 인증 API (JWT 토큰, 권한 검증)
2. **Feature 2.2**: 방화벽 로그 CRUD API (완전한 구현)
3. **Feature 2.3**: 로그 필터링 및 검색 (날짜, IP, 프로토콜 등)
4. **Feature 2.4**: 로그 통계 API (대시보드용 데이터)

---

## 참고사항

- SQLite는 개발/테스트용으로 사용됩니다
- 프로덕션 환경에서는 PostgreSQL/MySQL 사용 권장
- SECRET_KEY는 반드시 변경해야 합니다
- CORS 설정은 프론트엔드 도메인에 맞게 수정해야 합니다
