# API Documentation

This document provides detailed information about the RESTful API endpoints available in the To-Do List application.

## Base URL

```
http://localhost:5000/api
```

## Content Type

All requests and responses use JSON format:
- Request Header: `Content-Type: application/json`
- Response Header: `Content-Type: application/json`

## API Endpoints

### 1. Create Task

Create a new task in the database.

**Endpoint:** `POST /api/tasks`

**Request Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "due_date": "string (optional, YYYY-MM-DD format)",
  "status": "string (optional, default: 'pending')"
}
```

**Valid Status Values:**
- `pending`
- `in_progress`
- `completed`

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API and README documentation",
    "due_date": "2025-12-31",
    "status": "in_progress"
  }'
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API and README documentation",
  "due_date": "2025-12-31",
  "status": "in_progress"
}
```

**Error Responses:**

- **400 Bad Request** - Missing or invalid data
  ```json
  {
    "error": "Title is required"
  }
  ```

- **400 Bad Request** - Invalid status
  ```json
  {
    "error": "Status must be one of: pending, in_progress, completed"
  }
  ```

- **500 Internal Server Error** - Server error
  ```json
  {
    "error": "Internal server error"
  }
  ```

---

### 2. Get All Tasks

Retrieve all tasks from the database.

**Endpoint:** `GET /api/tasks`

**Example Request:**
```bash
curl http://localhost:5000/api/tasks
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive API and README documentation",
    "due_date": "2025-12-31",
    "status": "in_progress"
  },
  {
    "id": 2,
    "title": "Review code",
    "description": "Perform code review and testing",
    "due_date": "2025-12-30",
    "status": "pending"
  }
]
```

**Notes:**
- Returns an empty array `[]` if no tasks exist
- Tasks are ordered by ID in descending order (newest first)

**Error Response:**

- **500 Internal Server Error** - Server error
  ```json
  {
    "error": "Internal server error"
  }
  ```

---

### 3. Get Single Task

Retrieve a specific task by its ID.

**Endpoint:** `GET /api/tasks/{id}`

**Path Parameters:**
- `id` (integer, required) - The unique identifier of the task

**Example Request:**
```bash
curl http://localhost:5000/api/tasks/1
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API and README documentation",
  "due_date": "2025-12-31",
  "status": "in_progress"
}
```

**Error Responses:**

- **404 Not Found** - Task does not exist
  ```json
  {
    "error": "Task not found"
  }
  ```

- **500 Internal Server Error** - Server error
  ```json
  {
    "error": "Internal server error"
  }
  ```

---

### 4. Update Task

Update an existing task. Only provided fields will be updated.

**Endpoint:** `PUT /api/tasks/{id}`

**Path Parameters:**
- `id` (integer, required) - The unique identifier of the task

**Request Body:**
All fields are optional. Only include fields you want to update.
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "due_date": "string (optional, YYYY-MM-DD format)",
  "status": "string (optional)"
}
```

**Example Request:**
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API and README documentation",
  "due_date": "2025-12-31",
  "status": "completed"
}
```

**Error Responses:**

- **400 Bad Request** - No data provided
  ```json
  {
    "error": "No data provided"
  }
  ```

- **400 Bad Request** - Empty title
  ```json
  {
    "error": "Title cannot be empty"
  }
  ```

- **400 Bad Request** - Invalid status
  ```json
  {
    "error": "Status must be one of: pending, in_progress, completed"
  }
  ```

- **404 Not Found** - Task does not exist
  ```json
  {
    "error": "Task not found"
  }
  ```

- **500 Internal Server Error** - Server error
  ```json
  {
    "error": "Internal server error"
  }
  ```

---

### 5. Delete Task

Delete a task by its ID.

**Endpoint:** `DELETE /api/tasks/{id}`

**Path Parameters:**
- `id` (integer, required) - The unique identifier of the task

**Example Request:**
```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

**Success Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses:**

- **404 Not Found** - Task does not exist
  ```json
  {
    "error": "Task not found"
  }
  ```

- **500 Internal Server Error** - Server error
  ```json
  {
    "error": "Internal server error"
  }
  ```

---

## HTTP Status Codes

The API uses standard HTTP status codes:

| Status Code | Description |
|------------|-------------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 404 | Not Found - Resource does not exist |
| 500 | Internal Server Error - Server error occurred |

## Error Handling

All errors return a JSON object with an `error` key describing the issue:

```json
{
  "error": "Description of the error"
}
```

## Data Validation

### Title
- Required when creating a task
- Cannot be empty or contain only whitespace
- If provided during update, cannot be empty

### Description
- Optional field
- Can be null or empty string

### Due Date
- Optional field
- Should be in YYYY-MM-DD format
- No date validation is performed (any string accepted)

### Status
- Must be one of: `pending`, `in_progress`, or `completed`
- Defaults to `pending` when creating a task
- Invalid status values will return a 400 error

## Examples Using Python

### Create a Task
```python
import requests

url = "http://localhost:5000/api/tasks"
data = {
    "title": "My New Task",
    "description": "Task description",
    "due_date": "2025-12-31",
    "status": "pending"
}

response = requests.post(url, json=data)
print(response.json())
```

### Get All Tasks
```python
import requests

url = "http://localhost:5000/api/tasks"
response = requests.get(url)
tasks = response.json()
print(tasks)
```

### Update a Task
```python
import requests

task_id = 1
url = f"http://localhost:5000/api/tasks/{task_id}"
data = {"status": "completed"}

response = requests.put(url, json=data)
print(response.json())
```

### Delete a Task
```python
import requests

task_id = 1
url = f"http://localhost:5000/api/tasks/{task_id}"

response = requests.delete(url)
print(response.json())
```

## Examples Using JavaScript (Fetch API)

### Create a Task
```javascript
fetch('http://localhost:5000/api/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'My New Task',
    description: 'Task description',
    due_date: '2025-12-31',
    status: 'pending'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Get All Tasks
```javascript
fetch('http://localhost:5000/api/tasks')
  .then(response => response.json())
  .then(tasks => console.log(tasks));
```

### Update a Task
```javascript
const taskId = 1;
fetch(`http://localhost:5000/api/tasks/${taskId}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    status: 'completed'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Delete a Task
```javascript
const taskId = 1;
fetch(`http://localhost:5000/api/tasks/${taskId}`, {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

## Rate Limiting

Currently, there is no rate limiting implemented. This should be added for production use.

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## CORS

Cross-Origin Resource Sharing (CORS) is not configured. If you need to access the API from a different domain, CORS headers will need to be added to the Flask application.

---

For general application information, see [README.md](README.md)
