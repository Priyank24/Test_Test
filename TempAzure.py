#To call the AWS key we using boto3
import boto3
#from textract_python_kv_parser import get_kv_map,get_kv_relationship
#converting pdf to image we are using below package
#from pdf2image import convert_from_path

'''it will take image as input and give the data line by line'''
def get_identifypage(file_name):
    print("inside identifypage")
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        #print('Image loaded', file_name)
    # process using image bytes
    client = boto3.client('textract')
    response = client.detect_document_text(Document={'Bytes': bytes_test})

    # Detect columns and print lines
    columns = []
    lines = []
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            column_found = False
            for index, column in enumerate(columns):
                bbox_left = item["Geometry"]["BoundingBox"]["Left"]
                bbox_right = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]
                bbox_centre = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"] / 2
                column_centre = column['left'] + column['right'] / 2

                if (bbox_centre > column['left'] and bbox_centre < column['right']) or (
                        column_centre > bbox_left and column_centre < bbox_right):
                    # Bbox appears inside the column
                    lines.append([index, item["Text"]])
                    column_found = True
                    break
            if not column_found:
                columns.append({'left': item["Geometry"]["BoundingBox"]["Left"],
                                'right': item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"][
                                    "Width"]})
                lines.append([len(columns) - 1, item["Text"]])

    lines.sort(key=lambda x: x[0])
    filename_raca = ''
    filename_ddm=''
    for line in lines:
        line = line[1]
        print(line)
        heading = "Credit Agreement regulated"
        heading1 = "Instruction to your bank or building"
        if line.__contains__(heading):
            filename_raca = file_name
            break
        if line.__contains__(heading1):
            filename_ddm = file_name
            break
    if filename_raca == '':
        pagetype = 0
    if filename_ddm !='':
        pagetype =2
    else:
        pagetype = 1

    return pagetype


get_identifypage("testimage.png")
