# To-Do List Application

A full-featured To-Do List web application built with Python Flask, featuring RESTful APIs, a modern web interface, and comprehensive test coverage.

## Features

- ✅ RESTful API for all CRUD operations
- 🎨 Modern, responsive web interface
- 💾 SQLite database with raw SQL (no ORM)
- 🧪 Comprehensive test suite with pytest
- 📝 Logging and error handling
- 🔒 Input validation

## Technology Stack

- **Backend**: Python 3.x with Flask
- **Database**: SQLite with raw SQL queries
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Testing**: pytest with pytest-flask

## Project Structure

```
todo-list-app/
├── app/
│   ├── __init__.py
│   ├── app.py              # Main Flask application
│   └── database.py         # Database operations (raw SQL)
├── templates/
│   └── index.html          # Web interface template
├── static/
│   └── style.css           # Stylesheet
├── tests/
│   ├── __init__.py
│   └── test_api.py         # API endpoint tests
├── requirements.txt        # Project dependencies
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Repository

```bash
cd todo-list-app
```

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Server

```bash
python -m app.app
```

The application will start on `http://localhost:5000`

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Using the Application

### Web Interface

1. **Add a Task**: Fill in the form at the top of the page with task details and click "Add Task"
2. **View Tasks**: All tasks are displayed in cards below the form
3. **Edit a Task**: Click the "Edit" button on any task card to populate the form and modify the task
4. **Delete a Task**: Click the "Delete" button on any task card (requires confirmation)
5. **Task Status**: Tasks can have three statuses:
   - Pending (yellow)
   - In Progress (blue)
   - Completed (green)

### API Usage

The application provides RESTful APIs that can be accessed programmatically. See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed information.

## Running Tests

The project includes comprehensive test coverage for all API endpoints.

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage Report

```bash
pytest tests/ -v --cov=app
```

### Test Structure

Tests are organized into classes by endpoint:
- `TestCreateTask` - POST /api/tasks
- `TestGetAllTasks` - GET /api/tasks
- `TestGetSingleTask` - GET /api/tasks/<id>
- `TestUpdateTask` - PUT /api/tasks/<id>
- `TestDeleteTask` - DELETE /api/tasks/<id>
- `TestIntegration` - End-to-end workflows

## Database Schema

The application uses SQLite with the following schema:

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    status TEXT NOT NULL DEFAULT 'pending'
)
```

### Fields

- **id**: Unique identifier (auto-generated)
- **title**: Task title (required)
- **description**: Detailed description (optional)
- **due_date**: Due date in YYYY-MM-DD format (optional)
- **status**: One of 'pending', 'in_progress', or 'completed' (default: 'pending')

## Key Design Decisions

### No ORM

Per project requirements, this application uses raw SQL queries instead of an ORM (like SQLAlchemy). All database operations are implemented in `app/database.py` using Python's built-in `sqlite3` module.

### RESTful API Design

The API follows REST principles:
- Resources are identified by URLs (`/api/tasks`)
- HTTP methods indicate operations (GET, POST, PUT, DELETE)
- Status codes communicate results (200, 201, 400, 404, 500)
- JSON format for all request/response bodies

### Logging

All operations are logged with appropriate levels:
- INFO: Successful operations
- WARNING: Client errors (404, validation failures)
- ERROR: Server errors

Logs are written to:
- Console (stdout)
- File (`app.log`)

## Development

### Adding New Features

1. Add database operations to `app/database.py`
2. Add API endpoints to `app/app.py`
3. Update the frontend in `templates/index.html` if needed
4. Write tests in `tests/test_api.py`
5. Update documentation

### Code Quality

- Use type hints for function signatures
- Add docstrings for all functions
- Follow PEP 8 style guidelines
- Write tests for new features
- Handle exceptions appropriately

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, modify the port in `app/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Issues

If you encounter database errors, delete the `tasks.db` file and restart the application. The database will be recreated automatically.

### Import Errors

Ensure you're running commands from the project root directory and that your virtual environment is activated.

## License

This project is created as an assignment submission.

## Author

Created: December 2025

## Submission Information

**Deadline**: Wednesday, December 31, 2025  
**Submission Method**: Email or Google Drive link

---

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
