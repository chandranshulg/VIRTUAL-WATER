# Virtual Water Footprint Calculator

## Overview
The Virtual Water Footprint Calculator is a web application that helps users calculate their water footprint based on various categories like food consumption and clothing usage. It provides options to compare the footprint with the average user, export reports in PDF and CSV formats, and visualize the data through plots.

## Features
- **User Management**: Add users with their name and email.
- **Data Entry**: Record the amount of each category the user consumes or uses.
- **Water Footprint Calculation**: Calculate the total water footprint for a user based on the recorded data.
- **Comparison**: Compare the user's footprint with the average footprint of all users.
- **Export Reports**: Export water footprint data as PDF and CSV files.
- **Visualization**: Generate bar plots to visualize the water footprint by category.

## Technologies Used
- **Flask**: The main web framework used to build the application.
- **SQLite**: The database used for storing user data and categories.
- **Pandas**: Used for data manipulation and exporting data to CSV.
- **Matplotlib**: Used for generating plots of the water footprint.
- **FPDF**: Used for generating PDF reports.
- **HTML/CSS**: For the frontend design and user interface.

## Installation
### Prerequisites
- Python 3.x
- `pip` package manager

### Step-by-Step Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/VIRTUAL-WATER.git
    cd VIRTUAL-WATER
    ```

2. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    ```bash
    python app.py
    ```

4. **Access the Application**:
    Open your web browser and navigate to `http://127.0.0.1:5000/`.


## Usage
### Adding a User
1. Enter the user's name and email.
2. Click "Add User".

### Adding Data
1. Select a category and enter the amount.
2. Click "Add Data".

### Calculating and Comparing Water Footprint
1. Click "Calculate Footprint" to get the total water footprint for the user.
2. Click "Compare with Average" to see how the user's footprint compares to the average.

### Exporting Reports
1. Click "Export PDF" to download the water footprint report as a PDF.
2. Click "Export CSV" to download the data as a CSV file.
3. Click "Plot Footprint" to download a bar plot of the water footprint by category.

## Contribution
Feel free to contribute to this project by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.
