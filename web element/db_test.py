from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
db_name = "D:/Ching/VS code/SBA/database/Sports day helper"

def connect_to_db(db_name):
    """Connect to the SQLite database."""
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row  # To access columns by name
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def fetch_student_by_email(conn, email):
    """Fetch student information by email from the stu_info table."""
    query = "SELECT stu_id, name, clname, clno, gender, dob, house FROM stu_info WHERE gmail = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (email,))
        student_info = cursor.fetchone()
        return dict(student_info) if student_info else None
    except sqlite3.Error as e:
        print(f"Error fetching student info: {e}")
        return None

@app.route('/db.py', methods=['get_by_gmail'])
def get_student_info():
    gmail = request.args.get('gmail')
    if not gmail:
        return jsonify({'error': 'Gmail parameter is missing'}), 400

    conn = connect_to_db(db_name)
    if conn:
        student_data = fetch_student_by_email(conn, gmail)
        conn.close()
        if student_data:
            return jsonify(student_data)
        else:
            return jsonify({'error': 'No student found with that email'}), 404
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

if __name__ == '__main__':
    app.run(debug=True)
