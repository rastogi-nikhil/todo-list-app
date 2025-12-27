from flask import Flask, request, jsonify, render_template
import logging
from app.database import (
    init_db, create_task, get_all_tasks, get_task_by_id, 
    update_task, delete_task
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize database on startup
with app.app_context():
    try:
        init_db()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

# Web Interface Routes
@app.route('/')
def index():
    """Render the main page."""
    try:
        logger.info("Rendering index page")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# API Routes

@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    """Create a new task."""
    try:
        data = request.get_json(force=True, silent=True)
        
        if not data:
            logger.warning("Create task: No JSON data provided")
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title')
        if not title or not title.strip():
            logger.warning("Create task: Title is required")
            return jsonify({'error': 'Title is required'}), 400
        
        description = data.get('description')
        due_date = data.get('due_date')
        status = data.get('status', 'pending')
        
        # Validate status
        valid_statuses = ['pending', 'in_progress', 'completed']
        if status not in valid_statuses:
            logger.warning(f"Create task: Invalid status '{status}'")
            return jsonify({'error': f'Status must be one of: {", ".join(valid_statuses)}'}), 400
        
        task_id = create_task(title.strip(), description, due_date, status)
        task = get_task_by_id(task_id)
        
        logger.info(f"Task created successfully: ID {task_id}")
        return jsonify(task), 201
        
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/tasks', methods=['GET'])
def api_get_all_tasks():
    """Get all tasks."""
    try:
        tasks = get_all_tasks()
        logger.info(f"Retrieved {len(tasks)} tasks via API")
        return jsonify(tasks), 200
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def api_get_task(task_id):
    """Get a specific task by ID."""
    try:
        task = get_task_by_id(task_id)
        if task is None:
            logger.warning(f"Task {task_id} not found")
            return jsonify({'error': 'Task not found'}), 404
        
        logger.info(f"Retrieved task {task_id} via API")
        return jsonify(task), 200
    except Exception as e:
        logger.error(f"Error retrieving task {task_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    """Update an existing task."""
    try:
        data = request.get_json(force=True, silent=True)
        
        if not data:
            logger.warning(f"Update task {task_id}: No JSON data provided")
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('due_date')
        status = data.get('status')
        
        # Validate status if provided
        if status is not None:
            valid_statuses = ['pending', 'in_progress', 'completed']
            if status not in valid_statuses:
                logger.warning(f"Update task {task_id}: Invalid status '{status}'")
                return jsonify({'error': f'Status must be one of: {", ".join(valid_statuses)}'}), 400
        
        # Validate title if provided
        if title is not None and not title.strip():
            logger.warning(f"Update task {task_id}: Title cannot be empty")
            return jsonify({'error': 'Title cannot be empty'}), 400
        
        success = update_task(task_id, title, description, due_date, status)
        
        if not success:
            logger.warning(f"Task {task_id} not found for update")
            return jsonify({'error': 'Task not found'}), 404
        
        task = get_task_by_id(task_id)
        logger.info(f"Task {task_id} updated successfully via API")
        return jsonify(task), 200
        
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """Delete a task."""
    try:
        success = delete_task(task_id)
        
        if not success:
            logger.warning(f"Task {task_id} not found for deletion")
            return jsonify({'error': 'Task not found'}), 404
        
        logger.info(f"Task {task_id} deleted successfully via API")
        return jsonify({'message': 'Task deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.url}")
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
