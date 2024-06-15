import pandas as pd
from io import BytesIO
    
import random
import string

from datetime import datetime

import os

class Transformer:

    ############### attribute #######################
    length_file_key_id = 10

    keep_header = True
    keep_index = True

    datetime_today = datetime.now()
    datetime_key = datetime_today.strftime(("%a_%d_%b_%Y_%H_%M_%S"))

    folder_name_output_path = f'ExtractTable ({datetime_key})'
    #############################################

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_output_path = os.path.join(desktop_path, folder_name_output_path)

    if not os.path.exists(folder_output_path):
        os.makedirs(folder_output_path)
    
    def toExcel(self,dfs,file_extension='',filename_input=''):
        if file_extension != '' and filename_input != '':
            file_key_id = self.genFileKeyID(self.length_file_key_id)

            filename_output = f'{filename_input}_{file_key_id}.xlsx'

            export_path = os.path.join(self.folder_output_path, filename_output)

            if file_extension in ['png', 'jpg','jpeg']:
                dfs.to_xlsx(filename_output)

            elif file_extension in ['pdf',
                                    'vnd.openxmlformats-officedocument.presentationml.presentation']:
                with pd.ExcelWriter(export_path) as writer:
                    if len(dfs)>0:
                        for k,v in dfs.items():
                            for idx in range(len(v)):
                                df = pd.DataFrame(v[idx])
                                df.to_excel(writer, 
                                            sheet_name=f'Page {k} - Table {idx+1}',
                                            index=self.keep_index,
                                            header=self.keep_header)
                    else:
                        print("No detected Table")

            elif file_extension in ['vnd.openxmlformats-officedocument.wordprocessingml.document',
                                    ]:
                with pd.ExcelWriter(export_path) as writer:
                    if len(dfs)>0:
                        for idx in range(len(dfs)):
                            df = pd.DataFrame(dfs[idx])
                            df.to_excel(writer, 
                                        sheet_name=f'Table {idx+1}',
                                        index=self.keep_index,
                                        header=self.keep_header)
                    else:
                        print("No detected Table")

        else:
            #### Urls case #####
            ### finename_output ยังไงดีให้ชื่อไม่ยาวจนเกินไป #### 
            file_key_id = self.genFileKeyID(self.length_file_key_id)

            for k,v in dfs.items():
                filename_output = f'{k}_{file_key_id}.xlsx'
                export_path = os.path.join(self.folder_output_path, filename_output)
                
                with pd.ExcelWriter(export_path) as writer:
                    if len(v)>0:
                        for idx ,dataframe in enumerate(v):
                            df = pd.DataFrame(dataframe)
                            df.to_excel(writer, 
                                        sheet_name=f'Table {idx+1}',
                                        index=self.keep_index,
                                        header=self.keep_header)
                    else:
                        print("No detected Table")
        print(export_path)

    def fileUtil(self,file,filename_input):
        in_memory_data = BytesIO(file.read())
        filename_output = f"{filename_input}"  
        with open(filename_output, "wb") as outfile:
            outfile.write(in_memory_data.getvalue())
        return filename_output
    
    def genFileKeyID(self,length):
        # Define the character set for the ID (alphanumeric)
        alphabet = string.ascii_lowercase + string.digits
        alphabet_key = ''.join(random.choice(alphabet) for _ in range(length))

        file_key_id = alphabet_key + '_'+ self.datetime_key
        return file_key_id