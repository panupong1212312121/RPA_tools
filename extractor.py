from img2table.document import Image
import tabula
import fitz as pyMuPDF
from docx import Document
from pptx import Presentation

import pandas as pd

from transformer import Transformer
from widget import *

import requests

class ExtractTable:
    
    def image(self,file_afterTransfrom):
        dfs = Image(file_afterTransfrom)
        return dfs
    
    def pdf(self,file,file_afterTransfrom):
        dfs = {}
        page_amount = pyMuPDF.open(file_afterTransfrom).page_count
        for page_num in range(page_amount):
            tables = tabula.read_pdf(file, pages=page_num+1)
            if tables:
                dfs[page_num+1] = [table for table in tables]
        return dfs
    
    def docx(self,file_afterTransfrom):
        document = Document(file_afterTransfrom)
        dfs = []
        for table in document.tables:
            df = [['' for _ in range(len(table.columns))] for _ in range(len(table.rows))]
            for i, row in enumerate(table.rows):
                for j, cell in enumerate(row.cells):
                    if cell.text:
                        df[i][j] = cell.text
            dfs.append(pd.DataFrame(df))
        return dfs
    
    def pptx(self,file_afterTransfrom):
        presentation = Presentation(file_afterTransfrom)
        dfs = {}
        page = 0
        for slide in presentation.slides:
            df = []
            page += 1
            hasTable = True
            for shape in slide.shapes:
                if not shape.has_table:
                    hasTable = False
                    continue
                table = shape.table
                row_count = len(table.rows)
                col_count = len(table.columns)
                table_data = []
                for row in range(row_count):
                    row_values = []
                    for col in range(col_count):
                        cell = table.cell(row, col)
                        text = ""
                        for paragraph in cell.text_frame.paragraphs:
                            for run in paragraph.runs:
                                text += run.text
                        row_values.append(text)
                    table_data.append(row_values)
                df.append(pd.DataFrame(table_data))
            if hasTable:
                dfs[page] = df
        return dfs
    
    def link(self,currentState):
        dfs = {}
        for link_name in currentState:
            if 'link' in link_name:
                # ถ้า link ผิด -> เตือน , ไม่เจอ table  
                try:
                    df = pd.read_html(link_name)
                    dfs[link_name] = df
                except requests.exceptions.HTTPError as err:
                    print(f'{link_name} is invalid name')
        return dfs
        
    def run(self,uploaded_files,currentState):
        for file in uploaded_files:
            extractTable_obj = ExtractTable()
            transform_obj = Transformer()

            filename_input = file.name
            file_extension = file.type.split('/')[-1].lower()

            # print(file_extension)

            file_afterTransfrom = transform_obj.fileUtil(file,filename_input)

            if file_extension in ['png', 'jpg','jpeg']:
                data = extractTable_obj.image(file_afterTransfrom)
            elif file_extension in ['pdf']:
                data = extractTable_obj.pdf(file,file_afterTransfrom)
            elif file_extension in ['vnd.openxmlformats-officedocument.wordprocessingml.document']:
                data = extractTable_obj.docx(file_afterTransfrom)
            elif file_extension in ['vnd.openxmlformats-officedocument.presentationml.presentation']:
                data = extractTable_obj.pptx(file_afterTransfrom)
            elif LinkInput.is_null(currentState) == False:
                data = extractTable_obj.link(currentState)
            
            transform_obj.toExcel(data,file_extension)