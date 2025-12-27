import sqlite3
import logging
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

DATABASE_PATH = 'tasks.db'

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def init_db():
    """Initialize the database with the tasks table."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    status TEXT NOT NULL DEFAULT 'pending'
                )
            ''')
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

def create_task(title: str, description: Optional[str] = None, 
                due_date: Optional[str] = None, status: str = 'pending') -> int:
    """Create a new task and return its ID."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)',
                (title, description, due_date, status)
            )
            task_id = cursor.lastrowid
            logger.info(f"Task created with ID: {task_id}")
            return task_id
    except Exception as e:
        logger.error(f"Failed to create task: {str(e)}")
        raise

def get_all_tasks() -> List[Dict[str, Any]]:
    """Retrieve all tasks from the database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks ORDER BY id DESC')
            rows = cursor.fetchall()
            tasks = [dict(row) for row in rows]
            logger.info(f"Retrieved {len(tasks)} tasks")
            return tasks
    except Exception as e:
        logger.error(f"Failed to retrieve tasks: {str(e)}")
        raise

def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific task by ID."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            if row:
                logger.info(f"Retrieved task with ID: {task_id}")
                return dict(row)
            logger.warning(f"Task with ID {task_id} not found")
            return None
    except Exception as e:
        logger.error(f"Failed to retrieve task {task_id}: {str(e)}")
        raise

def update_task(task_id: int, title: Optional[str] = None, 
                description: Optional[str] = None, due_date: Optional[str] = None, 
                status: Optional[str] = None) -> bool:
    """Update an existing task. Returns True if successful, False if task not found."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # First check if task exists
            cursor.execute('SELECT id FROM tasks WHERE id = ?', (task_id,))
            if not cursor.fetchone():
                logger.warning(f"Task with ID {task_id} not found for update")
                return False
            
            # Build dynamic update query
            updates = []
            params = []
            
            if title is not None:
                updates.append('title = ?')
                params.append(title)
            if description is not None:
                updates.append('description = ?')
                params.append(description)
            if due_date is not None:
                updates.append('due_date = ?')
                params.append(due_date)
            if status is not None:
                updates.append('status = ?')
                params.append(status)
            
            if updates:
                params.append(task_id)
                query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                logger.info(f"Task {task_id} updated successfully")
                return True
            
            return True
    except Exception as e:
        logger.error(f"Failed to update task {task_id}: {str(e)}")
        raise

def delete_task(task_id: int) -> bool:
    """Delete a task by ID. Returns True if successful, False if task not found."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Task {task_id} deleted successfully")
            else:
                logger.warning(f"Task with ID {task_id} not found for deletion")
            return deleted
    except Exception as e:
        logger.error(f"Failed to delete task {task_id}: {str(e)}")
        raise
