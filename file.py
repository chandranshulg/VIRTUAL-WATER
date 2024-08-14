import flask
from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('water_footprint.db', check_same_thread=False)
c = conn.cursor()

# Create tables
c.execute('''
          CREATE TABLE IF NOT EXISTS users
          (id INTEGER PRIMARY KEY, name TEXT, email TEXT, total_footprint REAL)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS categories
          (id INTEGER PRIMARY KEY, category TEXT, water_usage REAL)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS user_data
          (user_id INTEGER, category_id INTEGER, amount REAL, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(category_id) REFERENCES categories(id))
          ''')

conn.commit()

# Mock data
categories = [
    {'id': 1, 'category': 'Beef', 'water_usage': 15400},
    {'id': 2, 'category': 'Chicken', 'water_usage': 4300},
    {'id': 3, 'category': 'Rice', 'water_usage': 2500},
    {'id': 4, 'category': 'Clothing', 'water_usage': 2000}
]

# Initialize database with mock data
def initialize_db():
    c.executemany('INSERT OR IGNORE INTO categories (id, category, water_usage) VALUES (?, ?, ?)', 
                  [(c['id'], c['category'], c['water_usage']) for c in categories])
    conn.commit()

initialize_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    c.execute('INSERT INTO users (name, email, total_footprint) VALUES (?, ?, ?)', (name, email, 0))
    conn.commit()
    return jsonify({'status': 'User added successfully'})

@app.route('/add_data', methods=['POST'])
def add_data():
    user_id = request.form['user_id']
    category_id = request.form['category_id']
    amount = float(request.form['amount'])
    c.execute('INSERT INTO user_data (user_id, category_id, amount) VALUES (?, ?, ?)', (user_id, category_id, amount))
    conn.commit()
    return jsonify({'status': 'Data added successfully'})

@app.route('/calculate_footprint/<int:user_id>')
def calculate_footprint(user_id):
    c.execute('''
              SELECT SUM(amount * water_usage) FROM user_data
              JOIN categories ON user_data.category_id = categories.id
              WHERE user_id = ?
              ''', (user_id,))
    total_footprint = c.fetchone()[0]
    if total_footprint is None:
        total_footprint = 0
    c.execute('UPDATE users SET total_footprint = ? WHERE id = ?', (total_footprint, user_id))
    conn.commit()
    return jsonify({'total_footprint': total_footprint})

@app.route('/compare_footprint/<int:user_id>')
def compare_footprint(user_id):
    c.execute('SELECT total_footprint FROM users WHERE id = ?', (user_id,))
    user_footprint = c.fetchone()[0]
    
    c.execute('SELECT AVG(total_footprint) FROM users')
    average_footprint = c.fetchone()[0]
    
    return jsonify({'user_footprint': user_footprint, 'average_footprint': average_footprint})

@app.route('/export_pdf/<int:user_id>')
def export_pdf(user_id):
    c.execute('SELECT name, total_footprint FROM users WHERE id = ?', (user_id,))
    user_data = c.fetchone()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = f"Water Footprint Report for {user_data[0]}", ln = True, align = 'C')
    pdf.cell(200, 10, txt = f"Total Water Footprint: {user_data[1]} liters", ln = True, align = 'C')
    
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    
    return send_file(pdf_output, attachment_filename='water_footprint_report.pdf', as_attachment=True)

@app.route('/export_csv/<int:user_id>')
def export_csv(user_id):
    c.execute('''
              SELECT categories.category, user_data.amount, (user_data.amount * categories.water_usage) AS footprint
              FROM user_data
              JOIN categories ON user_data.category_id = categories.id
              WHERE user_id = ?
              ''', (user_id,))
    data = c.fetchall()
    
    df = pd.DataFrame(data, columns=['Category', 'Amount', 'Footprint'])
    csv_output = io.StringIO()
    df.to_csv(csv_output, index=False)
    csv_output.seek(0)
    
    return send_file(io.BytesIO(csv_output.getvalue().encode('utf-8')), attachment_filename='water_footprint_report.csv', as_attachment=True, mimetype='text/csv')

@app.route('/plot_footprint/<int:user_id>')
def plot_footprint(user_id):
    c.execute('''
              SELECT categories.category, user_data.amount, (user_data.amount * categories.water_usage) AS footprint
              FROM user_data
              JOIN categories ON user_data.category_id = categories.id
              WHERE user_id = ?
              ''', (user_id,))
    data = c.fetchall()
    
    df = pd.DataFrame(data, columns=['Category', 'Amount', 'Footprint'])
    plt.figure(figsize=(10, 6))
    plt.bar(df['Category'], df['Footprint'])
    plt.xlabel('Category')
    plt.ylabel('Water Footprint (liters)')
    plt.title('Water Footprint by Category')
    
    plt_output = io.BytesIO()
    plt.savefig(plt_output, format='png')
    plt_output.seek(0)
    
    return send_file(plt_output, attachment_filename='water_footprint_plot.png', as_attachment=True, mimetype='image/png')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Virtual Water Footprint Calculator</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }}
        header {{
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        section {{
            margin: 20px;
            padding: 20px;
            background-color: white;
            border-radius: 5px;
        }}
        h2 {{
            color: #4CAF50;
        }}
        .input-box, .button-box {{
            margin: 20px 0;
            text-align: center;
        }}
        .input-box input, .input-box select {{
            padding: 10px;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .button-box button {{
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        .button-box button:hover {{
            background-color: #45a049;
        }}
        footer {{
            text-align: center;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            position: fixed;
            bottom: 0;
            width: 100%;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Virtual Water Footprint Calculator</h1>
    </header>

    <section>
        <h2>Calculate Your Water Footprint</h2>
        <div class="input-box">
            <input type="text" id="user_name" placeholder="Enter your name">
            <input type="email" id="user_email" placeholder="Enter your email">
            <button onclick="addUser()">Add User</button>
        </div>
        <div class="input-box">
            <input type="number" id="amount" placeholder="Enter amount">
            <select id="category">
                <!-- Categories will be populated here -->
            </select>
            <button onclick="addData()">Add Data</button>
        </div>
        <div class="button-box">
            <button onclick="calculateFootprint()">Calculate Footprint</button>
            <button onclick="compareFootprint()">Compare with Average</button>
            <button onclick="exportPDF()">Export PDF</button>
            <button onclick="exportCSV()">Export CSV</button>
            <button onclick="plotFootprint()">Plot Footprint</button>
        </div>
    </section>

    <section>
        <h2>Your Results</h2>
        <div id="results">
            <!-- Results will be populated here -->
        </div>
    </section>

    <footer>
        <p>&copy; 2024 Virtual Water Footprint Calculator</p>
    </footer>

    <script>
        function populateCategories() {{
            fetch('/categories')
                .then(response => response.json())
                .then(data => {{
                    const categorySelect = document.getElementById('category');
                    data.forEach(cat => {{
                        const option = document.createElement('option');
                        option.value = cat[0];
                        option.text = cat[1];
                        categorySelect.add(option);
                    }});
                }});
        }}

        function addUser() {{
            const name = document.getElementById('user_name').value;
            const email = document.getElementById('user_email').value;
            fetch('/add_user', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded'
                }},
                body: `name=${{name}}&email=${{email}}`
            }})
            .then(response => response.json())
            .then(data => alert(data.status));
        }}

        function addData() {{
            const userId = 1;  // For simplicity, assume user ID is 1
            const categoryId = document.getElementById('category').value;
            const amount = document.getElementById('amount').value;
            fetch('/add_data', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded'
                }},
                body: `user_id=${{userId}}&category_id=${{categoryId}}&amount=${{amount}}`
            }})
            .then(response => response.json())
            .then(data => alert(data.status));
        }}

        function calculateFootprint() {{
            const userId = 1;  // For simplicity, assume user ID is 1
            fetch(`/calculate_footprint/${{userId}}`)
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('results').innerHTML = `Total Water Footprint: ${{data.total_footprint}} liters`;
                }});
        }}

        function compareFootprint() {{
            const userId = 1;  // For simplicity, assume user ID is 1
            fetch(`/compare_footprint/${{userId}}`)
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('results').innerHTML = `
                        Your Footprint: ${{data.user_footprint}} liters<br>
                        Average Footprint: ${{data.average_footprint}} liters
                    `;
                }});
        }}

        function exportPDF() {{
            const userId = 1;  // For simplicity, assume user ID is 1
            window.location.href = `/export_pdf/${{userId}}`;
        }}

        function exportCSV() {{
            const userId = 1;  // For simplicity, assume user ID is 1
            window.location.href = `/export_csv/${{userId}}`;
        }}

        function plotFootprint() {{
            const userId = 1;  // For simplicity, assume user ID is 1
            window.location.href = `/plot_footprint/${{userId}}`;
        }}

        // Populate categories on page load
        populateCategories();
    </script>
</body>
</html>
"""

# Save the HTML template
with open('templates/index.html', 'w') as f:
    f.write(HTML_TEMPLATE)

if __name__ == '__main__':
    print("Starting Virtual Water Footprint Calculator...")
    
    # Initialize database with mock data
    initialize_db()
    
    # Start the Flask web server
    app.run(debug=True)
