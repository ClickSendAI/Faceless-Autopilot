# 🚀 Faceless Autopilot AI - Backend Services

Complete backend implementation for the Faceless Autopilot AI system with microservices architecture.

## 🏗️ Architecture Overview

The backend consists of 4 microservices:

- **Frontend** (Port 8560) - React dashboard interface
- **AI Content Service** (Port 8561) - Script generation, voice synthesis, video assembly
- **Platform APIs Service** (Port 8562) - Social media platform integrations
- **Analytics Service** (Port 8563) - Performance tracking and insights
- **User Management Service** (Port 8004) - Authentication and user data

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15.4
- **Cache**: Redis 7.2
- **AI Services**: OpenAI, ElevenLabs, Pexels
- **Video Processing**: FFmpeg
- **Containerization**: Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (running on localhost:5432)
- Redis (running on localhost:6379)
- FFmpeg (for video processing)

### 1. Install Dependencies

```bash
# Install requirements for each service
pip install -r services/ai-content/requirements.txt
pip install -r services/platform-apis/requirements.txt
pip install -r services/analytics/requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
PEXELS_API_KEY=your_pexels_api_key

# Database
DATABASE_URL=postgresql://postgres:tjq5uxt3@localhost:5432/faceless_autopilot_ai

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
```

### 3. Start Services

#### Option A: Using Python Script
```bash
python start_services.py
```

#### Option B: Using Docker Compose
```bash
docker-compose up -d
```

#### Option C: Manual Start
```bash
# Terminal 1 - AI Content Service
cd services/ai-content
uvicorn app.main:app --host 0.0.0.0 --port 8001

# Terminal 2 - Platform APIs Service
cd services/platform-apis
uvicorn app.main:app --host 0.0.0.0 --port 8002

# Terminal 3 - Analytics Service
cd services/analytics
uvicorn app.main:app --host 0.0.0.0 --port 8003
```

### 4. Test APIs

```bash
python test_apis.py
```

## 📚 API Documentation

Once services are running, access the interactive API documentation:

- **Frontend**: http://localhost:8560
- **AI Content Service**: http://localhost:8561/docs
- **Platform APIs Service**: http://localhost:8562/docs
- **Analytics Service**: http://localhost:8563/docs

## 🔧 Service Details

### AI Content Service (Port 8561)

**Endpoints:**
- `POST /api/content/generate` - Generate new content
- `GET /api/content/{id}/status` - Check generation status
- `POST /api/content/{id}/regenerate` - Regenerate content

**Features:**
- OpenAI GPT-4 script generation
- ElevenLabs voice synthesis
- FFmpeg video assembly
- Stock footage integration (Pexels)

### Platform APIs Service (Port 8562)

**Endpoints:**
- `POST /api/platforms/upload` - Upload to platforms
- `GET /api/platforms/status/{id}` - Check upload status
- `POST /api/platforms/schedule` - Schedule uploads

**Features:**
- YouTube Data API v3 integration
- TikTok for Business API
- Instagram Graph API
- Scheduled uploads

### Analytics Service (Port 8563)

**Endpoints:**
- `GET /api/analytics/overview` - User analytics overview
- `GET /api/analytics/content/{id}` - Content-specific analytics
- `GET /api/analytics/insights` - Performance insights
- `POST /api/analytics/sync` - Sync platform data

**Features:**
- Performance tracking
- Revenue analytics
- Content optimization insights
- Platform data synchronization

## 🗄️ Database Schema

The system uses PostgreSQL with the following main tables:

- **users** - User accounts and authentication
- **content** - Generated content metadata
- **analytics** - Performance metrics
- **platform_integrations** - Platform API credentials

## 🔄 Content Generation Workflow

1. **Script Generation** - OpenAI creates engaging scripts
2. **Voice Synthesis** - ElevenLabs generates professional voiceovers
3. **Video Assembly** - FFmpeg combines voice, visuals, and music
4. **Platform Upload** - Automated distribution to social media
5. **Analytics Tracking** - Performance monitoring and optimization

## 🧪 Testing

### Health Checks
```bash
curl http://localhost:8561/health
curl http://localhost:8562/health
curl http://localhost:8563/health
```

### Content Generation Test
```bash
curl -X POST "http://localhost:8561/api/content/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI Productivity Tips",
    "niche": "productivity",
    "format": "short",
    "duration": 60,
    "platforms": ["youtube", "tiktok"]
  }'
```

## 🐳 Docker Deployment

### Build and Run
```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment Variables for Docker
```bash
# Set environment variables
export OPENAI_API_KEY="your_key"
export ELEVENLABS_API_KEY="your_key"
export PEXELS_API_KEY="your_key"
export SECRET_KEY="your_secret"
```

## 🔧 Development

### Project Structure
```
services/
├── ai-content/          # AI content generation
│   ├── app/
│   │   ├── main.py      # FastAPI application
│   │   ├── models.py    # Pydantic models
│   │   ├── services/    # Business logic
│   │   └── core/        # Configuration
│   └── requirements.txt
├── platform-apis/       # Platform integrations
├── analytics/           # Analytics and insights
└── shared/              # Shared utilities
```

### Adding New Features

1. **New API Endpoint**: Add to `main.py` in respective service
2. **New Model**: Add to `models.py` with Pydantic validation
3. **New Service**: Create in `services/` directory
4. **Database Changes**: Update models and run migrations

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure PostgreSQL is running
   - Check connection string in `.env`
   - Verify database exists

2. **Redis Connection Failed**
   - Ensure Redis is running
   - Check Redis URL in configuration

3. **API Key Errors**
   - Verify API keys in `.env` file
   - Check API key permissions and quotas

4. **FFmpeg Not Found**
   - Install FFmpeg: `apt-get install ffmpeg` (Ubuntu) or `brew install ffmpeg` (macOS)

### Logs
```bash
# View service logs
docker-compose logs ai-content
docker-compose logs platform-apis
docker-compose logs analytics
```

## 📈 Performance

- **Concurrent Requests**: Each service handles multiple requests
- **Background Tasks**: Long-running operations use FastAPI background tasks
- **Caching**: Redis for session management and caching
- **Database Pooling**: SQLAlchemy connection pooling

## 🔐 Security

- **JWT Authentication**: Secure API access
- **Input Validation**: Pydantic model validation
- **CORS Configuration**: Cross-origin request handling
- **API Rate Limiting**: Prevent abuse

## 🚀 Next Steps

1. **Frontend Integration** - Connect React dashboard to APIs
2. **Authentication** - Implement user management
3. **Production Deployment** - Cloud deployment setup
4. **Monitoring** - Add logging and monitoring
5. **Testing** - Comprehensive test suite

---

**Ready to generate AI content at scale!** 🎬✨
