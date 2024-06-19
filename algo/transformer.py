from img2table.ocr import EasyOCR

import pandas as pd
from io import BytesIO
    
import random
import string

from datetime import datetime

import os

class GenID:

    length_file_key_id = 10

    datetime_today = datetime.now()

    def datetimeKey(self):
        year = self.datetime_today.strftime(("%Y"))
        month = self.datetime_today.strftime(("%B"))
        date = self.datetime_today.strftime(("%d"))
        time = self.datetime_today.strftime(("%H_%M_%S"))
        datetime = self.datetime_today.strftime(("%a-%d-%b-%Y_%H_%M_%S"))

        # return dict
        return [year,month,date,time,datetime]

    def genFileKeyID(self,length_file_key_id):
        # Define the character set for the ID (alphanumeric)
        alphabet = string.ascii_lowercase + string.digits
        alphabet_key = ''.join(random.choice(alphabet) for _ in range(length_file_key_id))

        file_key_id = alphabet_key + '_'+ self.datetimeKey()[-1]

        return file_key_id
    
class FolderOutputPath(GenID):
        
    def folderNameOutputPath(self):
        folder_name_output_path = f'RPA results'
        sub_folder = self.datetimeKey()[:-1]

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        folder_output_path = os.path.join(desktop_path, folder_name_output_path)

        if not os.path.exists(folder_output_path):
            os.makedirs(folder_output_path)

        for folder in sub_folder:
            folder_output_path = os.path.join(folder_output_path,str(folder))
            if not os.path.exists(folder_output_path):
                os.makedirs(folder_output_path)
        
        return folder_output_path
        
class Transformer(FolderOutputPath):

    keep_header = True
    keep_index = True
    
    def toExcel(self,dfs,file_extension='',filename_input='',url_name='',tool=''):
        files_no_detected_table = []
        urls_no_detected_table = []
        
        folder_output_path = os.path.join(self.folderNameOutputPath(),str(tool))

        if not os.path.exists(folder_output_path):
            os.makedirs(folder_output_path)

        if file_extension != '' and filename_input != '':
            file_key_id = self.genFileKeyID(self.length_file_key_id)

            filename_output = f'{filename_input}_{file_key_id}.xlsx'

            export_path = os.path.join(folder_output_path, filename_output)

            if file_extension in ['png', 'jpg','jpeg']:
                ocr = EasyOCR(lang=['en','th'])
                extracted_tables = dfs.extract_tables(ocr=ocr,
                                                    implicit_rows=False,
                                                    borderless_tables=False,
                                                    min_confidence=50)
                if len(extracted_tables)>0:
                    dfs.to_xlsx(dest=export_path,
                                ocr=ocr,
                                implicit_rows=False,
                                borderless_tables=False,
                                min_confidence=50)
                else:
                    files_no_detected_table.append(filename_input)

            elif file_extension in ['pdf',
                                    'vnd.openxmlformats-officedocument.presentationml.presentation']:
                if len(dfs)>0:
                    with pd.ExcelWriter(export_path) as writer:
                        for k,v in dfs.items():
                            for idx in range(len(v)):
                                df = pd.DataFrame(v[idx])
                                df.to_excel(writer, 
                                            sheet_name=f'Page {k} - Table {idx+1}',
                                            index=self.keep_index,
                                            header=self.keep_header)
                else:
                    files_no_detected_table.append(filename_input)

            elif file_extension in ['vnd.openxmlformats-officedocument.wordprocessingml.document',
                                    ]:
                if len(dfs)>0:
                    with pd.ExcelWriter(export_path) as writer:
                        for idx in range(len(dfs)):
                            df = pd.DataFrame(dfs[idx])
                            df.to_excel(writer, 
                                        sheet_name=f'Table {idx+1}',
                                        index=self.keep_index,
                                        header=self.keep_header)
                else:
                    files_no_detected_table.append(filename_input)

        else:
            file_key_id = self.genFileKeyID(self.length_file_key_id)

            for k,v in dfs.items():
                filename_output = f'{k}_{file_key_id}.xlsx'
                export_path = os.path.join(folder_output_path, filename_output)
                
                with pd.ExcelWriter(export_path) as writer:
                    if len(v)>0:
                        for idx ,dataframe in enumerate(v):
                            df = pd.DataFrame(dataframe)
                            df.to_excel(writer, 
                                        sheet_name=f'Table {idx+1}',
                                        index=self.keep_index,
                                        header=self.keep_header)
                    else:
                        urls_no_detected_table.append(url_name)

        return files_no_detected_table,urls_no_detected_table

    def toTxt(self,files_list_no_detected_table=[],urls_list_no_detected_table=[],invalid_url_list_name=[],tool=''):

        lenght = 60

        datetime_key = self.datetimeKey()[-1]

        sharp_format = '#'*lenght

        header = f'{sharp_format}\n{datetime_key:^{lenght}}\n{sharp_format}\n'

        folder_output_path = os.path.join(self.folderNameOutputPath(),str(tool))

        if not os.path.exists(folder_output_path):
            os.makedirs(folder_output_path)
            
        ########## write No table ##########
        file_name_no_detected_table = f"No detected table ({datetime_key}).txt"
        export_path = os.path.join(folder_output_path, file_name_no_detected_table)
        
        body = ''
        header_textfile = 'file'
        header_texturl = 'link'

        if len(files_list_no_detected_table) > 0 or len(urls_list_no_detected_table) > 0:
            if len(files_list_no_detected_table) > 0:
                i = 1
                body += f'\n{header_textfile:#^{int(lenght/2)}}'
                for file in files_list_no_detected_table:
                    body += f'\n{i}.\t{file}'
                    i+=1

            if len(urls_list_no_detected_table) > 0:
                i = 1
                body += f'\n{header_texturl:#^{int(lenght/2)}}'
                for url in urls_list_no_detected_table:
                    body += f'\n{i}.\t{url}'
                    i+=1

            with open(export_path, "w") as outfile:
                detail = header+body
                outfile.write(detail)

        ########## write invalid url ##########
        file_name_invalid_url = f"invalid link name ({datetime_key}).txt"
        export_path = os.path.join(folder_output_path, file_name_invalid_url)
        
        body = ''
        
        if len(invalid_url_list_name) > 0:
            i = 1
            body += f'\n{header_texturl:#^{int(lenght/2)}}'
            for invalid_url in invalid_url_list_name:
                body += f'\n{i}.\t{invalid_url}'
                i+=1

            with open(export_path, "w") as outfile:
                detail = header+body
                outfile.write(detail)

    def fileUtil(self,file,filename_input):
        in_memory_data = BytesIO(file.read())
        filename_output = f"{filename_input}"  
        with open(filename_output, "wb") as outfile:
            outfile.write(in_memory_data.getvalue())
        return filename_output

    def deleteNewFile(self,filename_input):
        curr_dir = os.getcwd()
        path_delete = os.path.join(curr_dir,filename_input)
        os.remove(path_delete)
    