# 3D Logo Video Generator

Transform your 2D logos into stunning 3D animated videos with AI-powered rendering. A professional-grade web application built with FastAPI, Blender, React, and Docker.

## Features

- **Drag & Drop Upload**: Easy logo upload with support for PNG, JPG, and SVG formats
- **AI Background Removal**: Automatically remove backgrounds using advanced ML models
- **8 Animation Presets**: Choose from cinematic animations including:
  - Classic Spin
  - Orbital Reveal
  - Zoom & Rotate
  - Flip Card
  - Rising Star
  - Cinematic Pan
  - Bounce In
  - Elegant Reveal
- **5 Lighting Setups**: Dramatic, Soft, Corporate, Neon, and Golden Hour
- **Customizable Parameters**: Adjust duration, speed, extrusion depth, and more
- **Multiple Resolutions**: Render in 1080p or 4K
- **Real-time Progress**: Track rendering progress with live updates
- **Preview Mode**: Quick low-quality previews before final render
- **Background Options**: Solid colors, gradients, transparent, or HDRI environments

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Blender 3.6**: Professional 3D rendering engine
- **Celery**: Distributed task queue for async rendering
- **PostgreSQL**: Robust database for job management
- **Redis**: In-memory data store for caching and queuing
- **MinIO**: S3-compatible object storage
- **rembg**: AI-powered background removal
- **SQLAlchemy**: ORM for database operations

### Frontend
- **React 18**: Modern UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Lightning-fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Powerful data fetching
- **Zustand**: Lightweight state management
- **Axios**: HTTP client

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and load balancer

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Browser   │─────▶│    Nginx     │─────▶│   FastAPI   │
│  (React)    │◀─────│ (Reverse     │◀─────│   Backend   │
└─────────────┘      │  Proxy)      │      └─────────────┘
                     └──────────────┘             │
                                                  │
                     ┌──────────────┐             │
                     │  PostgreSQL  │◀────────────┤
                     └──────────────┘             │
                                                  │
                     ┌──────────────┐             │
                     │    Redis     │◀────────────┤
                     └──────────────┘             │
                                                  │
                     ┌──────────────┐             │
                     │ Celery Worker│◀────────────┤
                     │  (Blender)   │             │
                     └──────────────┘             │
                                                  │
                     ┌──────────────┐             │
                     │    MinIO     │◀────────────┘
                     │  (Storage)   │
                     └──────────────┘
```

## Quick Start

### Prerequisites

- Docker 24+
- Docker Compose 2.20+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/logo3d-video-generator.git
cd logo3d-video-generator
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Start all services:
```bash
docker-compose up -d
```

4. Wait for services to be ready (1-2 minutes), then access:
- **Frontend**: http://localhost
- **API Docs**: http://localhost/api/docs
- **MinIO Console**: http://localhost:9001

### Development Mode

For development with hot-reloading:

1. Start infrastructure services:
```bash
docker-compose -f docker-compose.dev.yml up -d
```

2. Run backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

3. Run Celery worker:
```bash
cd backend
celery -A app.core.celery_app worker --loglevel=info
```

4. Run frontend:
```bash
cd frontend
npm install
npm run dev
```

## Usage

### Creating a 3D Logo Video

1. **Upload Logo**
   - Drag and drop your logo file (PNG, JPG, or SVG)
   - Maximum file size: 10MB
   - Optionally remove background using AI

2. **Configure Animation**
   - Select animation preset
   - Choose lighting setup
   - Adjust duration (3-15 seconds)
   - Set 3D depth/extrusion
   - Select resolution (1080p or 4K)
   - Choose quality (standard or high)

3. **Render**
   - Click "Preview" for quick low-quality preview
   - Click "Final Render" for high-quality output
   - Monitor progress in real-time
   - Download completed video

### API Usage

The application exposes a REST API for programmatic access:

#### Upload Logo
```bash
curl -X POST http://localhost:8000/api/v1/upload/ \
  -F "file=@logo.png"
```

#### Get Presets
```bash
curl http://localhost:8000/api/v1/render/presets
```

#### Create Render
```bash
curl -X POST http://localhost:8000/api/v1/render/final \
  -H "Content-Type: application/json" \
  -d '{
    "upload_id": "uuid-here",
    "config": {
      "preset": "classic_spin",
      "duration": 5.0,
      "lighting": "soft",
      "resolution": "1080p",
      "quality": "standard"
    }
  }'
```

#### Check Job Status
```bash
curl http://localhost:8000/api/v1/jobs/{job_id}
```

See full API documentation at http://localhost:8000/api/docs

## Project Structure

```
logo3d-video-generator/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Celery tasks & presets
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── alembic/            # Database migrations
│   ├── scripts/            # Helper scripts
│   └── tests/              # Unit tests
├── frontend/               # React frontend
│   ├── src/
│   │   ├── api/            # API client
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── store/          # Zustand stores
│   │   └── types/          # TypeScript types
│   └── public/             # Static assets
├── nginx/                  # Nginx configuration
└── docker-compose.yml      # Docker orchestration
```

## Configuration

### Environment Variables

#### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `S3_ENDPOINT`: MinIO/S3 endpoint
- `S3_ACCESS_KEY`: S3 access key
- `S3_SECRET_KEY`: S3 secret key
- `BLENDER_PATH`: Path to Blender executable
- `RENDER_OUTPUT_DIR`: Output directory for renders

#### Frontend
- `VITE_API_URL`: Backend API URL

### Animation Presets

Customize or add new presets in `backend/app/core/presets.py`:
- Keyframe-based animation system
- Support for object and camera transformations
- Customizable timing and easing

### Lighting Setups

Modify lighting configurations in `backend/app/core/presets.py`:
- Three-point lighting system
- Customizable energy and color
- Support for different lighting moods

## Performance

### Render Times (Approximate)

| Resolution | Quality  | Duration | Estimated Time |
|------------|----------|----------|----------------|
| 1080p      | Standard | 5s       | 5-8 minutes    |
| 1080p      | High     | 5s       | 10-15 minutes  |
| 4K         | Standard | 5s       | 20-30 minutes  |
| 4K         | High     | 5s       | 40-60 minutes  |

*Times vary based on hardware and complexity*

### Optimization Tips

- Use preview mode for testing configurations
- Start with standard quality for faster iterations
- Consider 1080p for most use cases
- Use background removal only when needed

## Troubleshooting

### Common Issues

**Blender not found**
```bash
# Check Blender installation
docker exec -it <container> blender --version
```

**Database connection error**
```bash
# Check PostgreSQL status
docker-compose ps postgres
docker-compose logs postgres
```

**Render stuck/failed**
```bash
# Check Celery worker logs
docker-compose logs celery_worker
```

**Upload fails**
```bash
# Check file size (max 10MB)
# Verify file format (PNG, JPG, SVG)
```

### Getting Help

- Check logs: `docker-compose logs <service-name>`
- Review API docs: http://localhost:8000/api/docs
- Open an issue on GitHub

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests (if added)
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
black app/
flake8 app/

# Frontend linting
cd frontend
npm run lint
```

### Database Migrations

```bash
# Create migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Deployment

### Production Checklist

- [ ] Set strong passwords in `.env`
- [ ] Configure CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging
- [ ] Scale Celery workers based on load
- [ ] Configure CDN for static assets

### Scaling

- Horizontal scaling: Add more Celery workers
- Vertical scaling: Increase CPU/RAM for rendering
- Database: Use connection pooling
- Storage: Use S3 for production

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

- Built with [Blender](https://www.blender.org/)
- Background removal by [rembg](https://github.com/danielgatis/rembg)
- UI components by [shadcn/ui](https://ui.shadcn.com/)

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/logo3d-video-generator/issues
- Documentation: https://github.com/yourusername/logo3d-video-generator/wiki

---

**Made with ❤️ by the 3DSprinted Team**
