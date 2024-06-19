import streamlit as st

import ui.table_extractor as table_extractor 

from algo.extractor import ExtractTable

from algo.transformer import Transformer

############################## Var ##############################

table_extractor_tool_name_obj = table_extractor.ToolName()
table_extractor_file_uploader_obj = table_extractor.FileUploader()
table_extractor_link_input_obj = table_extractor.LinkInput()
table_extractor_save_button_obj = table_extractor.SaveButton()

extractTable_obj = ExtractTable()

transform_obj = Transformer()

class Process:

    key_clicked_submit_process_button = 'clicked_submit_process_button'
    key_tool_name_process = 'tool_name_process'

    key_text_in_progress = 'In Progress'
    key_text_complete = 'Completed'

    key_text_view_results = 'Please select your options'

    def proceed(self,curr_state):
        tool_name_process = curr_state[self.key_tool_name_process]
        for tool in tool_name_process:
            self.run(st.session_state,tool)
        
        return True

    def run(self,currentState,tool):

        if tool == table_extractor_tool_name_obj.tool_name:
            file_list = st.session_state[table_extractor_file_uploader_obj.key_file_list]
            has_link = st.session_state[table_extractor_save_button_obj.key_criteria_data_save_button]

            total_file = len(file_list)
            total_url = st.session_state[table_extractor_link_input_obj.key_url_amount]

            progress_text = f"{tool} in progress. Please wait."

            if total_file>0:

                st.toast(f'{table_extractor_file_uploader_obj.key_file_name} ({self.key_text_in_progress})')

                progress_value = 0
                file_progress = st.progress(0, text=progress_text)

                files_list_no_detected_table = []
                urls_list_no_detected_table = []

                for file in file_list:

                    filename_input = file.name
                    file_extension = file.type.split('/')[-1].lower()

                    file_afterTransfrom = transform_obj.fileUtil(file,filename_input)

                    if file_extension in ['png', 'jpg','jpeg']:
                        data = extractTable_obj.image(file_afterTransfrom)
                    elif file_extension in ['pdf']:
                        data = extractTable_obj.pdf(file,file_afterTransfrom)
                    elif file_extension in ['vnd.openxmlformats-officedocument.wordprocessingml.document']:
                        data = extractTable_obj.docx(file_afterTransfrom)
                    elif file_extension in ['vnd.openxmlformats-officedocument.presentationml.presentation']:
                        data = extractTable_obj.pptx(file_afterTransfrom)

                    files_no_detected_table,urls_no_detected_table = transform_obj.toExcel(data,
                                                                                        file_extension,
                                                                                        filename_input,
                                                                                        tool=tool)

                    files_list_no_detected_table.extend(files_no_detected_table)
                    urls_list_no_detected_table.extend(urls_no_detected_table)

                    transform_obj.deleteNewFile(filename_input)

                ################# Progress bar 
                    progress_value += 1/total_file
                    file_progress.progress(progress_value, text=progress_text)                  

                transform_obj.toTxt(files_list_no_detected_table,
                                    urls_list_no_detected_table,
                                    tool=tool)
                
                file_progress.empty()
                st.toast(f'{table_extractor_file_uploader_obj.key_file_name} ({self.key_text_complete})')

            if has_link:
                st.toast(f'{table_extractor_link_input_obj.key_url_name} ({self.key_text_in_progress})')

                progress_value = 0
                url_progress = st.progress(progress_value, text=progress_text)

                dfs_url = {}
                invalid_url_list_name = []

                files_list_no_detected_table = []
                urls_list_no_detected_table = []

                for key in currentState:
                    if 'url' in key and 'amount' not in key:
                        try:
                            url_name = currentState[key]
                            df = extractTable_obj.link(url_name)
                            dfs_url[key] = df
                            files_list_no_detected_table,urls_list_no_detected_table = transform_obj.toExcel(dfs_url,
                                                                                                             url_name=url_name,
                                                                                                             tool=tool)
                        except:
                            invalid_url_list_name.append(url_name)                        

                        progress_value += 1/total_url
                        url_progress.progress(progress_value, text=progress_text) 

                transform_obj.toTxt(files_list_no_detected_table,
                                    urls_list_no_detected_table,
                                    invalid_url_list_name,
                                    tool)
                
                url_progress.empty()
                st.toast(f'{table_extractor_link_input_obj.key_url_name} ({self.key_text_complete})')
