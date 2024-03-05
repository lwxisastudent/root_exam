from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = '/www/wwwroot/root_exam_db/roots.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.route('/api/words')
def get_words():
    page_range = request.args.get('pageRange')
    if not page_range:
        return jsonify({'error': 'pageRange is required'}), 400
    try:
        min_page, max_page = map(int, page_range.split('-'))
    except ValueError:
        return jsonify({'error': 'Invalid pageRange format'}), 400
    query = f"SELECT * FROM words WHERE page >= ? AND page <= ? ORDER BY page"
    db = get_db()
    cursor = db.cursor()
    rows = cursor.execute(query, (min_page, max_page)).fetchall()
    db.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/roots')
def get_roots():
    page_range = request.args.get('pageRange')
    if not page_range:
        return jsonify({'error': 'pageRange is required'}), 400
    try:
        min_page, max_page = map(int, page_range.split('-'))
    except ValueError:
        return jsonify({'error': 'Invalid pageRange format'}), 400
    query = f"SELECT * FROM roots WHERE page >= ? AND page <= ? ORDER BY page"
    db = get_db()
    cursor = db.cursor()
    rows = cursor.execute(query, (min_page, max_page)).fetchall()
    db.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/roots/<int:id>')
def get_root(id):
    query = 'SELECT * FROM roots WHERE id = ?'
    db = get_db()
    cursor = db.cursor()
    row = cursor.execute(query, (id,)).fetchone()
    db.close()
    if not row:
        return jsonify({'error': 'Word root not found'}), 404
    return jsonify(dict(row))

if __name__ == '__main__':
    app.run(port=4021)