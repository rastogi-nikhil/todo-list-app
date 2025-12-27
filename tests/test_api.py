import pytest
import json
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app
from app.database import init_db, create_task
import sqlite3

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    
    # Use a separate test database
    import app.database as db
    db.DATABASE_PATH = 'test_tasks.db'
    
    # Initialize the test database
    init_db()
    
    with app.test_client() as client:
        yield client
    
    # Clean up test database after tests
    try:
        os.remove('test_tasks.db')
    except:
        pass

@pytest.fixture
def sample_task():
    """Return sample task data."""
    return {
        'title': 'Test Task',
        'description': 'This is a test task',
        'due_date': '2025-12-31',
        'status': 'pending'
    }

class TestCreateTask:
    """Tests for POST /api/tasks endpoint."""
    
    def test_create_task_success(self, client, sample_task):
        """Test successful task creation."""
        response = client.post('/api/tasks', 
                               data=json.dumps(sample_task),
                               content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == sample_task['title']
        assert data['description'] == sample_task['description']
        assert data['due_date'] == sample_task['due_date']
        assert data['status'] == sample_task['status']
        assert 'id' in data
    
    def test_create_task_no_data(self, client):
        """Test task creation with no data."""
        response = client.post('/api/tasks',
                               data='',
                               content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_task_missing_title(self, client):
        """Test task creation without title."""
        task_data = {'description': 'Test description'}
        response = client.post('/api/tasks',
                               data=json.dumps(task_data),
                               content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'title' in data['error'].lower()
    
    def test_create_task_empty_title(self, client):
        """Test task creation with empty title."""
        task_data = {'title': '   '}
        response = client.post('/api/tasks',
                               data=json.dumps(task_data),
                               content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_task_invalid_status(self, client):
        """Test task creation with invalid status."""
        task_data = {'title': 'Test', 'status': 'invalid_status'}
        response = client.post('/api/tasks',
                               data=json.dumps(task_data),
                               content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data['error'].lower()
    
    def test_create_task_minimal_data(self, client):
        """Test task creation with only required fields."""
        task_data = {'title': 'Minimal Task'}
        response = client.post('/api/tasks',
                               data=json.dumps(task_data),
                               content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'Minimal Task'
        assert data['status'] == 'pending'

class TestGetAllTasks:
    """Tests for GET /api/tasks endpoint."""
    
    def test_get_all_tasks_empty(self, client):
        """Test retrieving tasks when database is empty."""
        response = client.get('/api/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_all_tasks_with_data(self, client, sample_task):
        """Test retrieving tasks when database has data."""
        # Create some tasks
        client.post('/api/tasks', 
                   data=json.dumps(sample_task),
                   content_type='application/json')
        
        task2 = sample_task.copy()
        task2['title'] = 'Second Task'
        client.post('/api/tasks',
                   data=json.dumps(task2),
                   content_type='application/json')
        
        response = client.get('/api/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 2

class TestGetSingleTask:
    """Tests for GET /api/tasks/<id> endpoint."""
    
    def test_get_task_success(self, client, sample_task):
        """Test retrieving a specific task."""
        # Create a task
        create_response = client.post('/api/tasks',
                                     data=json.dumps(sample_task),
                                     content_type='application/json')
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        # Retrieve the task
        response = client.get(f'/api/tasks/{task_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id
        assert data['title'] == sample_task['title']
    
    def test_get_task_not_found(self, client):
        """Test retrieving a non-existent task."""
        response = client.get('/api/tasks/9999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

class TestUpdateTask:
    """Tests for PUT /api/tasks/<id> endpoint."""
    
    def test_update_task_success(self, client, sample_task):
        """Test successful task update."""
        # Create a task
        create_response = client.post('/api/tasks',
                                     data=json.dumps(sample_task),
                                     content_type='application/json')
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        # Update the task
        update_data = {
            'title': 'Updated Title',
            'status': 'completed'
        }
        response = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated Title'
        assert data['status'] == 'completed'
        assert data['description'] == sample_task['description']
    
    def test_update_task_not_found(self, client):
        """Test updating a non-existent task."""
        update_data = {'title': 'Updated'}
        response = client.put('/api/tasks/9999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_task_no_data(self, client, sample_task):
        """Test updating task with no data."""
        # Create a task
        create_response = client.post('/api/tasks',
                                     data=json.dumps(sample_task),
                                     content_type='application/json')
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        response = client.put(f'/api/tasks/{task_id}',
                             data='',
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_task_empty_title(self, client, sample_task):
        """Test updating task with empty title."""
        # Create a task
        create_response = client.post('/api/tasks',
                                     data=json.dumps(sample_task),
                                     content_type='application/json')
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        update_data = {'title': '   '}
        response = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_task_invalid_status(self, client, sample_task):
        """Test updating task with invalid status."""
        # Create a task
        create_response = client.post('/api/tasks',
                                     data=json.dumps(sample_task),
                                     content_type='application/json')
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        update_data = {'status': 'invalid'}
        response = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_task_partial(self, client, sample_task):
        """Test partial task update."""
        # Create a task
        create_response = client.post('/api/tasks',
                                     data=json.dumps(sample_task),
                                     content_type='application/json')
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        # Update only status
        update_data = {'status': 'in_progress'}
        response = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'in_progress'
        assert data['title'] == sample_task['title']

class TestDeleteTask:
    """Tests for DELETE /api/tasks/<id> endpoint."""
    
    def test_delete_task_success(self, client, sample_task):
        """Test successful task deletion."""
        # Create a task
        create_response = client.post('/api/tasks',
                                     data=json.dumps(sample_task),
                                     content_type='application/json')
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        # Delete the task
        response = client.delete(f'/api/tasks/{task_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        
        # Verify task is deleted
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404
    
    def test_delete_task_not_found(self, client):
        """Test deleting a non-existent task."""
        response = client.delete('/api/tasks/9999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_task_workflow(self, client):
        """Test complete CRUD workflow."""
        # Create
        task_data = {
            'title': 'Workflow Test',
            'description': 'Testing complete workflow',
            'due_date': '2025-12-31',
            'status': 'pending'
        }
        create_response = client.post('/api/tasks',
                                     data=json.dumps(task_data),
                                     content_type='application/json')
        assert create_response.status_code == 201
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        # Read
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 200
        
        # Update
        update_data = {'status': 'completed'}
        update_response = client.put(f'/api/tasks/{task_id}',
                                     data=json.dumps(update_data),
                                     content_type='application/json')
        assert update_response.status_code == 200
        updated_task = json.loads(update_response.data)
        assert updated_task['status'] == 'completed'
        
        # Delete
        delete_response = client.delete(f'/api/tasks/{task_id}')
        assert delete_response.status_code == 200
        
        # Verify deletion
        final_get = client.get(f'/api/tasks/{task_id}')
        assert final_get.status_code == 404
