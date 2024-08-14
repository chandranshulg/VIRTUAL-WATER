from flask import Flask, render_template, request

app = Flask(__name__)

# Default water usage data (in liters) for each activity
WATER_USAGE = {
    'shower': 80,  # per shower
    'toilet': 9,   # per flush
    'washing_machine': 150,  # per load
    'dishwasher': 20,  # per load
    'drinking_water': 3,  # per day
    'food': 3000,  # per day (including food production)
    'clothing': 2500  # per outfit (including production)
}

def calculate_water_consumption(data):
    """Calculate total water consumption based on user input."""
    total = 0
    for key, value in data.items():
        total += WATER_USAGE[key] * int(value)
    return total

@app.route('/', methods=['GET', 'POST'])
def index():
    total_water_usage = None
    if request.method == 'POST':
        # Get user input from the form
        user_data = {
            'shower': request.form.get('shower', 0),
            'toilet': request.form.get('toilet', 0),
            'washing_machine': request.form.get('washing_machine', 0),
            'dishwasher': request.form.get('dishwasher', 0),
            'drinking_water': request.form.get('drinking_water', 0),
            'food': request.form.get('food', 0),
            'clothing': request.form.get('clothing', 0)
        }
        # Calculate total water usage
        total_water_usage = calculate_water_consumption(user_data)
    
    return render_template('index.html', total_water_usage=total_water_usage)

if __name__ == '__main__':
    app.run(debug=True)

# HTML content stored as a string for the sake of the example
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Water Usage Calculator</title>
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
        input[type="number"] {{
            width: 100%;
            padding: 10px;
            margin: 5px 0 15px 0;
            display: inline-block;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }}
        input[type="submit"] {{
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}
        input[type="submit"]:hover {{
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
        <h1>Water Usage Calculator</h1>
        <p>Calculate your daily water consumption.</p>
    </header>

    <section>
        <h2>Enter Your Daily Usage</h2>
        <form method="POST">
            <label for="shower">Showers (number of showers):</label>
            <input type="number" id="shower" name="shower" min="0" required>
            
            <label for="toilet">Toilet Flushes (number of flushes):</label>
            <input type="number" id="toilet" name="toilet" min="0" required>
            
            <label for="washing_machine">Washing Machine Loads (number of loads):</label>
            <input type="number" id="washing_machine" name="washing_machine" min="0" required>
            
            <label for="dishwasher">Dishwasher Loads (number of loads):</label>
            <input type="number" id="dishwasher" name="dishwasher" min="0" required>
            
            <label for="drinking_water">Drinking Water (liters per day):</label>
            <input type="number" id="drinking_water" name="drinking_water" min="0" required>
            
            <label for="food">Food Consumption (days):</label>
            <input type="number" id="food" name="food" min="0" required>
            
            <label for="clothing">Clothing Worn (outfits):</label>
            <input type="number" id="clothing" name="clothing" min="0" required>
            
            <input type="submit" value="Calculate">
        </form>

        {% if total_water_usage is not none %}
            <h2>Total Water Consumption: {{ total_water_usage }} liters</h2>
        {% endif %}
    </section>

    <footer>
        <p>&copy; 2024 Water Usage Calculator</p>
    </footer>
</body>
</html>
"""

@app.route('/index.html')
def serve_html():
    return HTML_TEMPLATE

if __name__ == '__main__':
    # Write HTML to file if needed
    with open('templates/index.html', 'w') as f:
        f.write(HTML_TEMPLATE)
    app.run(debug=True)
