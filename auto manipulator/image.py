import cv2
import pytesseract
import json
import xml.etree.ElementTree as ET

def extract_text_from_image(image_path, output_format='txt'):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    output_file_name = image_path.split('.')[0] + '_extracted_text.' + output_format

    if output_format == 'txt':
        with open(output_file_name, 'w') as f:
            f.write(text)
    elif output_format == 'csv':
        with open(output_file_name, 'w') as f:
            f.write('"{}"'.format(text.replace('"', '""')))
    elif output_format == 'xlsx':
        import pandas as pd
        df = pd.DataFrame({'Text': [text]})
        df.to_excel(output_file_name, index=False)
    elif output_format == 'json':
        with open(output_file_name, 'w') as f:
            json.dump({'text': text}, f, indent=4)
    elif output_format == 'xml':
        root = ET.Element('Text')
        text_elem = ET.SubElement(root, 'Content')
        text_elem.text = text
        tree = ET.ElementTree(root)
        tree.write(output_file_name)
    else:
        print("Unsupported output format.")
        return

    print(f"Extracted text saved to: {output_file_name}")

output_format = input("Enter the output format (txt/csv/xlsx/json/xml): ").lower()
input_image_path = input("Enter the input image file path: ")
extract_text_from_image(input_image_path, output_format)

