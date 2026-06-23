# Code Review Instructions

## Overview
These instructions guide code reviews for Python APIs (FastAPI) with focus on **security**, **best practices**, **performance**, and **maintainability**.

## Security Review Checklist

### Input Validation & Sanitization
- [ ] All user inputs are validated (type, length, format)
- [ ] No unvalidated data is used in database queries (use parameterized queries)
- [ ] File uploads are restricted by type and size
- [ ] No hardcoded secrets, API keys, or credentials in code
- [ ] Environment variables used for sensitive data
- [ ] SQL injection risks are mitigated
- [ ] XSS vulnerabilities are prevented (output encoding)

### Authentication & Authorization
- [ ] Authentication mechanisms are properly implemented
- [ ] Password hashing uses strong algorithms (bcrypt, argon2)
- [ ] JWT tokens have proper expiration and refresh logic
- [ ] Authorization checks are in place for all endpoints
- [ ] Rate limiting is implemented to prevent brute force attacks
- [ ] CORS is properly configured (not `*` in production)

### API Security
- [ ] HTTPS is enforced in production
- [ ] Sensitive data is not logged or exposed in error messages
- [ ] API responses don't leak internal system information
- [ ] Proper HTTP status codes are used
- [ ] Content-Type headers are set correctly
- [ ] No debug mode enabled in production

### Dependencies
- [ ] All dependencies are from trusted sources
- [ ] No known vulnerabilities in dependencies (check with `pip audit`)
- [ ] Dependencies are pinned to specific versions in `requirements.txt`
- [ ] Regular updates scheduled for security patches

---

## Code Quality Checklist

### Python Style & Standards
- [ ] Code follows PEP 8 (use `black`, `flake8`, `pylint`)
- [ ] Type hints are used for all function parameters and returns
- [ ] Docstrings document all public functions/classes
- [ ] No unused imports or variables
- [ ] Magic numbers are replaced with named constants
- [ ] Maximum line length is 88 characters (Black standard)

### Testing
- [ ] Unit tests cover happy path, edge cases, and error scenarios
- [ ] Test coverage is at least 80%
- [ ] Tests are independent and can run in any order
- [ ] Mock external dependencies
- [ ] No hardcoded test data; use fixtures
- [ ] Tests have descriptive names
- [ ] `pytest` is used as the testing framework

### Error Handling
- [ ] Exceptions are caught explicitly (not bare `except:`)
- [ ] Custom exceptions are used for domain-specific errors
- [ ] Error messages are informative but don't expose sensitive data
- [ ] Logging is implemented for debugging
- [ ] No silent failures

### FastAPI Specific
- [ ] Request models use `Pydantic` with proper validation
- [ ] Response models are typed with `Pydantic`
- [ ] Path parameters are validated with type hints
- [ ] Query parameters have proper defaults and types
- [ ] Status codes are correct (201 for creation, 204 for deletion, etc.)
- [ ] Error responses are consistent and documented

---

## Performance & Efficiency

### Database & I/O
- [ ] Database queries are optimized (no N+1 queries)
- [ ] Indexes are used on frequently queried columns
- [ ] Connection pooling is implemented
- [ ] Pagination is used for large datasets
- [ ] Async/await is used for I/O operations when applicable

### Resource Management
- [ ] Memory usage is reasonable (no memory leaks)
- [ ] Large files are streamed, not loaded entirely into memory
- [ ] Database connections are properly closed
- [ ] External API calls have timeouts

### Caching
- [ ] Frequently accessed data is cached
- [ ] Cache invalidation strategy is clear
- [ ] Cache TTL is appropriate

---

## Maintainability & Architecture

### Code Organization
- [ ] Functions are small and focused (single responsibility)
- [ ] DRY principle is followed (no code duplication)
- [ ] Functions have maximum complexity threshold
- [ ] Classes follow SOLID principles
- [ ] Separation of concerns (models, routes, services, utils)

### Documentation
- [ ] README explains project setup and usage
- [ ] API endpoints are documented (use FastAPI's auto-docs)
- [ ] Complex logic has inline comments
- [ ] CHANGELOG is maintained
- [ ] Architecture decisions are documented

### Version Control
- [ ] Commits are atomic and logical
- [ ] Commit messages are descriptive (not "fix" or "update")
- [ ] Branch naming follows convention (feature/..., bugfix/..., etc.)
- [ ] No merge commits without review

---

## Review Process

### Pre-Review
1. Run `black` for formatting
2. Run `flake8` or `pylint` for linting
3. Run all tests: `pytest test_app.py -v`
4. Check test coverage: `pytest --cov`

### Code Review Steps
1. **Read the PR description** - understand the intent
2. **Check for security issues** - use security checklist
3. **Review architecture** - is the design sound?
4. **Check code quality** - consistency and maintainability
5. **Verify tests** - adequate coverage and quality
6. **Performance check** - identify bottlenecks

### Approval Criteria
- ✅ All security checks passed
- ✅ Code follows project style guide
- ✅ Tests pass and coverage is adequate
- ✅ No breaking changes (unless documented)
- ✅ Performance impact is acceptable
- ✅ Documentation is updated

---

## Common Issues to Watch For

### 🔴 Critical
- Hardcoded credentials or secrets
- SQL injection vulnerabilities
- Missing input validation
- Unhandled exceptions in production code
- Weak authentication/authorization

### 🟡 Major
- Missing type hints
- Insufficient test coverage (<70%)
- Unoptimized database queries
- Poor error messages
- Not following project conventions

### 🟢 Minor
- Style inconsistencies (fixable with `black`)
- Missing docstrings
- Inefficient algorithms (when not critical)
- Unclear variable names

---

## Tools & Commands

```bash
# Format code
black .

# Lint code
flake8 . --max-line-length=88
pylint api_*.py

# Type checking
mypy .

# Test with coverage
pytest --cov=. --cov-report=html test_*.py -v

# Security audit
pip audit

# Check for security issues
bandit -r .
```

---

## FastAPI Endpoints Review Template

For each endpoint, verify:

```python
@app.get("/endpoint", response_model=ResponseModel, status_code=200)
def get_endpoint(param: str = Query(..., min_length=1, max_length=100)) -> ResponseModel:
    """
    Clear description of what this endpoint does.
    
    Args:
        param: Description of parameter
        
    Returns:
        ResponseModel: Description of response
        
    Raises:
        ValueError: When input is invalid
    """
```

✅ Checklist:
- [ ] Proper HTTP method (GET, POST, PUT, DELETE)
- [ ] Correct status code
- [ ] Input parameters validated with `Query()` or `Path()`
- [ ] Request body uses Pydantic model
- [ ] Response uses Pydantic model
- [ ] Error cases documented
- [ ] Docstring follows Google style
- [ ] Tests cover success and error cases
