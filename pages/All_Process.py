import streamlit as st

from process.all_process import Process
from process.data_input_from_user import DataInputFromUser

import ui.table_extractor as table_extractor

from algo.transformer import FolderOutputPath

import pandas as pd

import os

############################## Object ##############################

data_input_from_user_obj = DataInputFromUser()
process_obj = Process()

table_extractor_tool_name_obj = table_extractor.ToolName()
table_extractor_file_uploader_obj = table_extractor.FileUploader()
table_extractor_save_button_obj = table_extractor.SaveButton()

folder_output_path_obj = FolderOutputPath()

############################## Var ##############################

key_submit_process = data_input_from_user_obj.key_submit_input_user
key_clicked_submit_process_button = process_obj.key_clicked_submit_process_button
key_tool_name_process = process_obj.key_tool_name_process

key_table_extractor_file_list = table_extractor_file_uploader_obj.key_file_list

key_table_extractor_criteria_data_save_button = table_extractor_save_button_obj.key_criteria_data_save_button
key_table_extractor_clicked_save_button = table_extractor_save_button_obj.key_clicked_save_button

############################## State ##############################

if key_submit_process not in st.session_state:
    st.session_state[key_submit_process] = False
if key_clicked_submit_process_button not in st.session_state:
    st.session_state[key_clicked_submit_process_button] = False
if key_tool_name_process not in st.session_state:
    st.session_state[key_tool_name_process] = []

table_extractor_file_list = st.session_state[key_table_extractor_file_list]
table_extractor_criteria_data_save_button = st.session_state[key_table_extractor_criteria_data_save_button]
table_extractor_clicked_save_button = st.session_state[key_table_extractor_clicked_save_button]

submit_process = st.session_state[key_submit_process]
clicked_submit_process_button = st.session_state[key_clicked_submit_process_button]
tool_name_process = st.session_state[key_tool_name_process]

############################## Report ##############################

####### Condition Report 
st.session_state[key_tool_name_process] = [table_extractor_tool_name_obj.tool_name,
                                            ]
#######

if table_extractor_clicked_save_button:
    df = pd.DataFrame(data=tool_name_process,
                      columns=['Process Name that you have already saved'],
                      )
    
    df = df.set_index(df.index + 1)

    st.table(df)

############################## Submit process button  ##############################

#### solution เพื่อเก็บ url_1,2,3,....
for key in st.session_state:
    if 'url' in key and 'amount' not in key:
        st.session_state[key] = st.session_state.get(key)

if st.button('Submit',
            disabled=not submit_process,
            ):

    st.session_state[key_clicked_submit_process_button] = True
    st.rerun()

# st.write(st.session_state)

# Display loading message
if clicked_submit_process_button:
    end_process = process_obj.proceed(st.session_state) 
    if end_process:  
        st.success("Processing completed! Choose a result to view:")

        result_options = [process_obj.key_text_view_results]+tool_name_process

        selected_option = st.selectbox("View Result:",
                                        options=result_options,
                                        placeholder="Choose an option")
        
        if selected_option != process_obj.key_text_view_results:
            clicked_view_result_button = st.button(f'Click to view :blue[ "{selected_option}" ] results')
            if clicked_view_result_button:
                if selected_option == table_extractor_tool_name_obj.tool_name:
                    des_path = os.path.join(folder_output_path_obj.folderNameOutputPath(),str(selected_option))
                    os.startfile(des_path) # solution 

        # refresh = st.button('Refresh & Go Home')

        # if refresh:
        #     st.page_link('Home.py')
        