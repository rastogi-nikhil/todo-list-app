"""
Application runner script.
This script starts the Flask application.
"""

from app.app import app

if __name__ == '__main__':
    print("=" * 60)
    print("To-Do List Application")
    print("=" * 60)
    print("\nStarting server...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
