# Contributing to 3D Logo Video Generator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker 24+
- Git

### Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/logo3d-video-generator.git
cd logo3d-video-generator
```

3. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

4. Set up development environment:
```bash
# Start infrastructure services
docker-compose -f docker-compose.dev.yml up -d

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Frontend setup
cd ../frontend
npm install
```

## Development Workflow

### Backend Development

1. Make changes to backend code
2. Run tests:
```bash
cd backend
pytest
```

3. Check code quality:
```bash
black app/
flake8 app/
mypy app/
```

4. Run backend locally:
```bash
uvicorn app.main:app --reload
```

### Frontend Development

1. Make changes to frontend code
2. Run linter:
```bash
cd frontend
npm run lint
```

3. Run development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

### Database Migrations

When modifying models:

1. Create migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

2. Review generated migration
3. Apply migration:
```bash
alembic upgrade head
```

## Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New features include tests
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive

### PR Guidelines

1. **Title**: Use descriptive titles
   - Good: "Add 4K resolution support"
   - Bad: "Update code"

2. **Description**: Include:
   - What changes were made
   - Why the changes were needed
   - Any breaking changes
   - Screenshots (for UI changes)

3. **Size**: Keep PRs focused
   - One feature/fix per PR
   - Split large changes into multiple PRs

### Review Process

1. Automated checks must pass
2. At least one maintainer approval required
3. Address all review comments
4. Maintain clean commit history

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 100 characters
- Use Black for formatting
- Write docstrings for public functions

```python
def process_image(image_path: str, options: Dict[str, Any]) -> ProcessedImage:
    """
    Process an uploaded image.

    Args:
        image_path: Path to the image file
        options: Processing options

    Returns:
        ProcessedImage instance

    Raises:
        ValueError: If image is invalid
    """
    pass
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow [Airbnb Style Guide](https://github.com/airbnb/javascript)
- Use functional components and hooks
- Prop-types are not needed (use TypeScript interfaces)

```typescript
interface ButtonProps {
  onClick: () => void
  disabled?: boolean
  children: React.ReactNode
}

export function Button({ onClick, disabled = false, children }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  )
}
```

### Git Commits

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat: add background gradient support
fix: resolve memory leak in video encoder
docs: update API documentation
refactor: simplify upload validation logic
```

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_upload.py

# Run with coverage
pytest --cov=app --cov-report=html
```

### Writing Tests

```python
def test_upload_valid_image(client, sample_image):
    """Test uploading a valid image."""
    response = client.post(
        "/api/v1/upload/",
        files={"file": ("logo.png", sample_image, "image/png")}
    )
    assert response.status_code == 200
    assert "upload_id" in response.json()
```

### Frontend Tests

```bash
# Run tests
npm test

# Run tests in watch mode
npm test -- --watch
```

## Adding New Features

### New Animation Preset

1. Add preset definition in `backend/app/core/presets.py`
2. Define keyframes with transformations
3. Test with various logos
4. Update documentation

```python
"new_preset": AnimationPreset(
    name="New Preset",
    description="Description of animation",
    keyframes=[
        {
            "frame": 0,
            "object_rotation": (0, 0, 0),
            # ... other properties
        },
        # ... more keyframes
    ]
)
```

### New API Endpoint

1. Create endpoint in `backend/app/api/v1/endpoints/`
2. Add Pydantic schemas if needed
3. Write tests
4. Update API documentation
5. Add frontend integration

### New UI Component

1. Create component in appropriate directory
2. Use TypeScript for type safety
3. Follow existing component patterns
4. Add to Storybook (if applicable)
5. Write tests

## Documentation

### Code Documentation

- Document all public APIs
- Include usage examples
- Explain complex algorithms
- Document configuration options

### User Documentation

- Update README.md for user-facing features
- Add screenshots/GIFs for visual features
- Include code examples
- Keep troubleshooting section updated

## Performance Considerations

### Backend

- Optimize database queries
- Use async/await appropriately
- Profile rendering performance
- Cache frequently accessed data

### Frontend

- Minimize bundle size
- Use React.memo for expensive components
- Implement virtual scrolling for long lists
- Optimize images and assets

## Security

### Reporting Security Issues

- Email: security@example.com
- Do not open public issues for security vulnerabilities

### Security Best Practices

- Validate all inputs
- Sanitize file uploads
- Use parameterized queries
- Implement rate limiting
- Follow OWASP guidelines

## Release Process

1. Update version in `package.json` and `__init__.py`
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Create release tag
6. Deploy to production
7. Announce release

## Need Help?

- Check existing issues and PRs
- Join community discussions
- Read documentation thoroughly
- Ask questions in issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to 3D Logo Video Generator!
