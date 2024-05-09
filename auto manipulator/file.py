import pandas as pd
import json
import csv
import os
import xml.etree.ElementTree as ET

def convert_to_json(input_file):
    file_name, _ = os.path.splitext(input_file)
    output_json_file = file_name + '.json'

    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension == '.csv':
        data = pd.read_csv(input_file, encoding='utf-8')
    elif file_extension in ('.xlsx', '.xls'):
        data = pd.read_excel(input_file)
    elif file_extension == '.xml':
        data = xml_to_json(input_file)
    elif file_extension == '.txt':
        data = fixed_width_to_json(input_file)
    else:
        raise ValueError("Unsupported file format")

    serializable_data = convert_data_to_serializable(data)

    with open(output_json_file, 'w') as json_output:
        json.dump(serializable_data, json_output, indent=4)

    return output_json_file

def xlsx_to_json(xlsx_file):
    data = pd.read_excel(xlsx_file)
    data_list = data.to_dict(orient='records')
    return data_list

def xml_to_json(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = []
    for element in root:
        item = {}
        for child in element:
            item[child.tag] = child.text
        data.append(item)
    return data

def fixed_width_to_json(txt_file):
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        item = {
            "Field1": line[0:10],
            "Field2": line[10:20],
            # Define fields and positions as needed
        }
        data.append(item)

    return data

def convert_data_to_serializable(data):
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient='records')
    else:
        return data

def json_to_xml(input_json):
    file_name, _ = os.path.splitext(input_json)
    output_xml_file = file_name + '.xml'

    with open(input_json, 'r') as json_file:
        data = json.load(json_file)

    root = ET.Element('Data')

    if isinstance(data, list):
        for entry in data:
            item = ET.SubElement(root, 'Item')
            for key, value in entry.items():
                sub_element = ET.SubElement(item, key)
                sub_element.text = str(value)
    elif isinstance(data, dict):
        item = ET.SubElement(root, 'Item')
        for key, value in data.items():
            sub_element = ET.SubElement(item, key)
            sub_element.text = str(value)
    else:
        raise ValueError("Unsupported JSON format")

    tree = ET.ElementTree(root)
    tree.write(output_xml_file)

    return output_xml_file

def json_to_csv(input_json):
    file_name, _ = os.path.splitext(input_json)
    output_csv_file = file_name + '.csv'

    with open(input_json, 'r') as json_file:
        data = json.load(json_file)

    with open(output_csv_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    return output_csv_file

def json_to_xlsx(input_json):
    file_name, _ = os.path.splitext(input_json)
    output_xlsx_file = file_name + '.xlsx'

    with open(input_json, 'r') as json_file:
        data = json.load(json_file)

    df = pd.DataFrame(data)
    df.to_excel(output_xlsx_file, index=False)

    return output_xlsx_file

def json_to_text(input_json):
    file_name, _ = os.path.splitext(input_json)
    output_text_file = file_name + '.txt'

    with open(input_json, 'r') as json_file:
        data = json.load(json_file)

    with open(output_text_file, 'w') as text_file:
        for entry in data:
            text_file.write(json.dumps(entry) + '\n')

    return output_text_file

def main():
    input_file = input("Enter the path to the input file: ")
    output_format = input("Enter the output format (xml/csv/xlsx/json): ")

    if output_format == 'json':
        output_file = convert_to_json(input_file)
        print(f"{input_file} has been converted to JSON and saved as {output_file}")
    elif output_format == 'xml':
        output_file = json_to_xml(input_file)
        print(f"{input_file} has been converted to XML and saved as {output_file}")
    elif output_format == 'csv':
        output_file = json_to_csv(input_file)
        print(f"{input_file} has been converted to CSV and saved as {output_file}")
    elif output_format == 'xlsx':
        output_file = json_to_xlsx(input_file)
        print(f"{input_file} has been converted to XLSX and saved as {output_file}")
    elif output_format == 'text':
        output_file = json_to_text(input_file)
        print(f"{input_file} has been converted to Text and saved as {output_file}")
    else:
        print("Unsupported output format.")

if __name__ == "__main__":
    main()
