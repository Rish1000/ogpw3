# Contributing to OGPW

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/ogpw.git
   cd ogpw
   ```

3. Set up development environment:
   ```bash
   # Install dependencies
   npm install
   cd backend && pip install -r requirements.txt
   ```

4. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style

### Frontend (TypeScript/React)
- Use TypeScript for all new code
- Follow ESLint configuration
- Use Tailwind CSS for styling
- Components should be functional with hooks

### Backend (Python)
- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions
- Handle exceptions appropriately

## Testing

### Frontend
```bash
npm run test
```

### Backend
```bash
cd backend
python -m pytest
```

## Submitting Changes

1. Ensure all tests pass
2. Update documentation if needed
3. Commit with descriptive messages
4. Push to your fork
5. Create a pull request

## Feature Requests

- Open an issue with the "enhancement" label
- Describe the use case and expected behavior
- Include mockups or examples if helpful

## Bug Reports

- Use the bug report template
- Include steps to reproduce
- Provide system information
- Attach relevant logs or screenshots