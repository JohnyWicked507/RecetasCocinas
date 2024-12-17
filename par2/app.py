import pandas as pd
from flask import Flask, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Load the CSV data into a pandas DataFrame
csv_file = "resource.csv"
df = pd.read_csv(csv_file)


# Function to convert the data into a list of dictionaries (for JSON response)
def get_vaccination_data():
    # Remove the first column ('País' and 'Codigo del país')
    df_cleaned = df.drop(
        columns=["País", "Codigo del país", "Nombre indicador", "Codigo", "--->"]
    )
    # Set the year as index for easier access
    df_cleaned.set_index("Año", inplace=True)
    return df_cleaned.to_dict(orient="index")


# Route to get all vaccination data
@app.route("/api/vaccination", methods=["GET"])
def get_all_vaccination_data():
    vaccination_data = get_vaccination_data()
    return jsonify(vaccination_data)


# Route to get vaccination data for a specific year
@app.route("/api/vaccination/<int:year>", methods=["GET"])
def get_vaccination_data_by_year(year):
    vaccination_data = get_vaccination_data()
    if year in vaccination_data:
        return jsonify({year: vaccination_data[year]})
    else:
        return jsonify({"error": "Year not found"}), 404


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
