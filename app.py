from flask import Flask, request, render_template, url_for
import pandas as pd
import random

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'csv_file' not in request.files:
        return "No file part"

    file = request.files['csv_file']

    if file.filename == '':
        return "No selected file"

    if file:
        try:
            df = pd.read_csv(file, header=0)

            categorical_cols = [col for col in df.columns if df[col].dtype == object]
            numerical_cols = [col for col in df.columns if df[col].dtype not in ['object', 'bool']]

            if not categorical_cols or not numerical_cols:
                return "No categorical or numerical columns found in the CSV."

            bar_x = random.choice(categorical_cols)
            bar_y = random.choice(numerical_cols)

            line_x = random.choice(categorical_cols)
            line_y = random.choice(numerical_cols)

            max_data_points = 10
            if len(df) > max_data_points:
                bar_temp = df.head(max_data_points)
                line_temp = df.tail(max_data_points)
            else:
                bar_temp = df
                line_temp = df

            # Select distinct values from different ranges for bar and line charts
            bar_labels = bar_temp[bar_x].unique().tolist()
            line_labels = line_temp[line_x].unique().tolist()

            return render_template('chart.html',
                                   bar_labels=bar_labels,
                                   line_labels=line_labels,
                                   bar_val=bar_temp[bar_y].tolist(),
                                   line_val=line_temp[line_y].tolist(),
                                   bar_x=bar_x,
                                   bar_y=bar_y,
                                   line_x=line_x,
                                   line_y=line_y)
        except Exception as e:
            return f"Error processing file: {e}"

if __name__ == '__main__':
    app.run(debug=True)