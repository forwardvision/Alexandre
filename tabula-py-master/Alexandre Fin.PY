import tabula
from flask_cors import CORS
from flask import Flask, request, jsonify
import traceback 
import os

app = Flask(__name__)
CORS(app, resources={r"/fetch_data": {"origins": ["http://127.0.0.1:5002"]}})

@app.route('/fetch_data', methods=['GET', 'POST', 'OPTIONS'])
def fetch_data():
    print('called')

    try:
        raw_data = request.get_data(as_text=True)
        print ('raw', raw_data)
        if not raw_data:
            print("No raw data.")
            return jsonify({'error': f'No raw data.'})   
        
        data = parse_json_string(raw_data)
        print ('parser', data)
        if not data:
            print("No parsed data.")
            return jsonify({'error': f'No parsed data.'})
            
        pdf_path = data.get('pdfpathjs', '')
        page = data.get('page', '')
        left_margin = data.get('leftMargin', '')
        right_margin = data.get('rightMargin', '')
        top_margin = data.get('topMargin', '')
        bottom_margin = data.get('bottomMargin', '')

    
    except ValueError as ve:
        print(f"Error decoding JSON: {ve}")
        traceback.print_exc()  
        return jsonify({'error': 'Invalid JSON data'}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    destination_filename = "pdf_for_extraction.pdf"
    destination_path = os.path.join(script_directory, destination_filename)
    
    delete_existing_file(destination_path)
    
    print ('read file from', pdf_path, 'create in',destination_path )
    read_and_store_file(pdf_path, destination_path)
    

#   =========================================================================    
    try:
        json_data = tabula.read_pdf(destination_path,pages=page, output_format="json")
    except ValueError as ve:
        print(f"Tabu Error reading PDF as JSON: {ve}")
        traceback.print_exc()
        return jsonify({'error': 'Tabu Error reading PDF as JSON'}), 400
    except Exception as e:
        print(f"Tabu An unexpected error occurred reading PDF as JSON: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Tabu An unexpected error occurred reading PDF as JSON: {e}'}), 500
    
    
    if not json_data:
        print("No table found in the PDF.")
        return jsonify({'error': f'No table found in the PDF: {pdf_path}'})        


    top_value = json_data[0]['top']
    left_value = json_data[0]['left']
    width_value = json_data[0]['width']
    height_value = json_data[0]['height']    
    right_value = json_data[0]['right']
    bottom_value = json_data[0]['bottom']
    top_margin = float(top_margin)
    left_margin = float(left_margin)
    right_margin = float(right_margin)
    bottom_margin = float(bottom_margin)
    print(top_value, left_value, height_value, width_value, right_value, bottom_value)    
    top_value = top_value - top_margin
    left_value = left_value - left_margin
    width_value = width_value  + right_margin
    height_value = height_value + bottom_margin
    print('========================================================================= ')
    print(top_value, left_value, height_value, width_value, right_value, bottom_value)

    csv_output_path = "output.csv"
    delete_existing_file(csv_output_path)
    tabula.convert_into(pdf_path, csv_output_path, output_format="csv", pages=page, area=[top_value, left_value, bottom_value, right_value])

    return jsonify({'success': 'Data successfully extracted', 'json_data': json_data})

#   =========================================================================    

def delete_existing_file(file_path):

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File deleted: {file_path}")
        else:
            print(f"No File to delete: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

def read_and_store_file(source_path, destination_path):
    try:
        with open(destination_path, 'wb') as destination_file, open(source_path, 'rb') as source_file:
            destination_file.write(source_file.read())
        print(f"File copied from {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error copying file: {e}")

    
def parse_json_string(raw_data):
    key_value_pairs = raw_data.strip('{}').split(',')
    data = {}
    for pair in key_value_pairs:
        key, *value = pair.split(':', 1)
        data[key.strip('"').strip()] = value[0].strip('"').strip() if value else ''
    return data

# tabula.convert_into(pdf_path, csv_output_path, output_format="csv", multiple_tables=True,pages=page, area=[top_value, left_value, bottom_value, right_value])
    # response_data = {'success': 'Data successfully extracted'}
    # status_code = 200
    # response_tuple = jsonify(response_data), status_code
    # return response_tuple


    # json_data = tabula.read_pdf(destination_path, output_format="json")
    # dfs = tabula.read_pdf(destination_path, area=[126,149,212,462], pages=1)
    #         area=[top_value, left_value, bottom_value, right_value],
    #         multiple_tables=True
    # print(len(dfs))
    # dfs[0]
    # return jsonify({'success': 'Data successfully extracted'}), 

#   =========================================================================    
    # try:
    #     # json_data = tabula.read_pdf(destination_path, output_format="json")
    #     dfs = tabula.read_pdf(destination_path, area=[126,149,212,462], pages=1)
    #     dfs[0]
    #     return jsonify({'success': 'Data successfully extracted'}),    
    # except ValueError as ve:
    #     print(f"Tabu Error reading PDF with coord: {ve}")
    #     traceback.print_exc()
    #     return jsonify({'error': 'Tabu Error reading PDF with coord'}), 400
    # except Exception as e:
    #     print(f"Tabu An unexpected error occurred reading PDF with coord: {e}")
    #     traceback.print_exc()
    #     return jsonify({'error': f'Tabu An unexpected error occurred reading PDF with coord: {e}'}), 500

    # return jsonify({'success': 'Data successfully extracted'}),    


    # print(len(dfs))
        
    # if dfs and len(dfs[0]) > 0:
    #     dfs[0] = dfs[0].fillna('')
    # dfs[0]

        
    # json_data = tabula.read_pdf(api_url, pages=page, output_format="json")
    # if json_data:
    #     print("PDF successfully read. JSON data:")
    #     print(json_data)        
    # else:
    #     print("No table found in the PDF.")
    #     return jsonify({'error': f'No table found in the PDF: {pdf_path}'}), 101
    #     pdf_path = api_url
    #     top_value = json_data[0]['top'] - 25
    #     left_value = json_data[0]['left']
    #     width_value = json_data[0]['width']
    #     height_value = json_data[0]['height']
    #     right_value = json_data[0]['right']
    #     bottom_value = json_data[0]['bottom']

    #     print(top_value, left_value, height_value, width_value, right_value, bottom_value)

    #     dfs = tabula.read_pdf(
    #         pdf_path,
    #         area=[top_value, left_value, bottom_value, right_value],
    #         multiple_tables=True
    #     )

    #     print(len(dfs))
        
    #     if dfs and len(dfs[0]) > 0:
    #         dfs[0] = dfs[0].fillna('')

    #     return jsonify({'success': 'Data successfully extracted'}), 


    # raw_data = request.get_data(as_text=True)
    # data = json.loads(raw_data)

    # dynamicInputValue = data.get('dynamicInput', '')
    # pageValue = data.get('page', '')
    # leftMarginValue = data.get('leftMargin', '')
    # rightMarginValue = data.get('rightMargin', '')
    # topMarginValue = data.get('topMargin', '')
    # bottomMarginValue = data.get('bottomMargin', '')

        # Print or use the values as needed
    # print("Dynamic Input:", dynamicInputValue)
    #     print("Page Value:", pageValue)
    #     print("Left Margin:", leftMarginValue)
    #     print("Right Margin:", rightMarginValue)
    #     print("Top Margin:", topMarginValue)
    #     print("Bottom Margin:", bottomMarginValue)
    # print(raw_data)
    
    # data = request.get_json()
    # return jsonify({'good': f'An error occurred:'})
    # values = api_url.split('&')

    # data_dict = {}
    # for pair in values:
    #     key, value = pair.split('=')
    #     data_dict[key] = value

    # dynamicInputValue = data_dict.get('dynamicInput', '')
    # pageValue = data_dict.get('page', '')
    # leftMarginValue = data_dict.get('leftMargin', '')
    # rightMarginValue = data_dict.get('rightMargin', '')
    # topMarginValue = data_dict.get('topMargin', '')
    # bottomMarginValue = data_dict.get('bottomMargin', '')

    # print("Dynamic Input:", dynamicInputValue)
    # print("Page Value:", pageValue)
    # print("Left Margin:", leftMarginValue)
    # print("Right Margin:", rightMarginValue)
    # print("Top Margin:", topMarginValue)
    # print("Bottom Margin:", bottomMarginValue)
    # return jsonify({'values success'})
    # json_data = tabula.read_pdf(pdf_path, output_format="json")
    # if json_data:
    #     print("PDF successfully read. JSON data:")
    #     print(json_data)        
    # else:
    #     print("No table found in the PDF.")
    #     return jsonify({'error': f'No table found in the PDF: {pdf_path}'}), 101
    #     pdf_path = api_url
    #     top_value = json_data[0]['top'] - 25
    #     left_value = json_data[0]['left']
    #     width_value = json_data[0]['width']
    #     height_value = json_data[0]['height']
    #     right_value = json_data[0]['right']
    #     bottom_value = json_data[0]['bottom']

    #     print(top_value, left_value, height_value, width_value, right_value, bottom_value)

    #     dfs = tabula.read_pdf(
    #         pdf_path,
    #         area=[top_value, left_value, bottom_value, right_value],
    #         multiple_tables=True
    #     )

    #     print(len(dfs))
        
    #     if dfs and len(dfs[0]) > 0:
    #         dfs[0] = dfs[0].fillna('')

    #     return jsonify({'success': 'Data successfully extracted'}), 


        # json_data = tabula.read_pdf(pdf_path, output_format="json")

        # if json_data:
        #     print("PDF successfully read. JSON data:")
        #     print(json_data)        
        # else:
        #     print("No table found in the PDF.")
        #     return jsonify({'error': f'No table found in the PDF: {pdf_path}'}), 101
        # pdf_path = api_url
        # top_value = json_data[0]['top'] - 25
        # left_value = json_data[0]['left']
        # width_value = json_data[0]['width']
        # height_value = json_data[0]['height']
        # right_value = json_data[0]['right']
        # bottom_value = json_data[0]['bottom']

        # print(top_value, left_value, height_value, width_value, right_value, bottom_value)

        # dfs = tabula.read_pdf(
        #     pdf_path,
        #     area=[top_value, left_value, bottom_value, right_value],
        #     multiple_tables=True
        # )

        # print(len(dfs))
        
        # if dfs and len(dfs[0]) > 0:
        #     dfs[0] = dfs[0].fillna('')

        # return jsonify({'success': 'Data successfully extracted'}), 200
            # print (request.content_type)
    # try:
    #     api_url = request.args.get('api_url')
    #     # request.args.get
    #     if not api_url:
    #         return jsonify({'error': 'Please check PDF File path'})
    #     print("API URL:", api_url)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     return jsonify({'error': f'An error occurred: {e}'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5111)
