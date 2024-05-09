from flask import Flask, render_template, request, send_file
from file import convert_to_json
from clean import clean_data
from image import extract_text_from_image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert_file', methods=['POST'])
def convert_file():
    input_file = request.files['file']
    output_format = request.form['output_format']
    output_file = convert_to_json(input_file, output_format)
    return send_file(output_file, as_attachment=True)

@app.route('/clean_data', methods=['POST'])
def clean_data():
    input_file = request.files['file']
    output_file = clean_data(input_file)
    return send_file(output_file, as_attachment=True)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    input_image = request.files['image']
    output_format = request.form['output_format']
    output_file = extract_text_from_image(input_image, output_format)
    return send_file(output_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
