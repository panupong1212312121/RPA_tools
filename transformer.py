import pandas as pd
from io import BytesIO

class Transformer:
    
    def toExcel(self,dfs,file_extension):
        filename_output = 'output.xlsx'

        if file_extension in ['png', 'jpg','jpeg']:
            dfs.to_xlsx(filename_output)

        elif file_extension in ['pdf',
                                'vnd.openxmlformats-officedocument.presentationml.presentation']:
            with pd.ExcelWriter(filename_output) as writer:
                if len(dfs)>0:
                    for k,v in dfs.items():
                        for idx in range(len(v)):
                            df = pd.DataFrame(v[idx])
                            df.to_excel(writer, sheet_name=f'Page {k} - Table {idx+1}',index=False,header=False)
                else:
                    print("No detected Table")

        elif file_extension in ['vnd.openxmlformats-officedocument.wordprocessingml.document',
                                ]:
            with pd.ExcelWriter(filename_output) as writer:
                if len(dfs)>0:
                    for idx in range(len(dfs)):
                        df = pd.DataFrame(dfs[idx])
                        df.to_excel(writer, sheet_name=f'Table {idx+1}',index=False,header=False)
                else:
                    print("No detected Table")

    def fileUtil(self,file,filename_input):
        in_memory_data = BytesIO(file.read())
        filename_output = f"{filename_input}"  
        with open(filename_output, "wb") as outfile:
            outfile.write(in_memory_data.getvalue())
        return filename_output