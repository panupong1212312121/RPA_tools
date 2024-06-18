import streamlit as st

from process.all_process import Process
from ui.table_extractor import FileUploader,SaveButton,ToolName
from algo.extractor import ExtractTable

import pandas as pd
import numpy as np

############################## Var ##############################

process_obj = Process()

tool_name_obj = ToolName()
file_uploader_obj = FileUploader()
save_button_obj = SaveButton()

extractTable_obj = ExtractTable()

key_submit_process = process_obj.key_submit_process

key_file_list = file_uploader_obj.key_file_list

key_criteria_data_save_button = save_button_obj.key_criteria_data_save_button
key_clicked_save_button = save_button_obj.key_clicked_save_button

############################## State ##############################

if key_submit_process not in st.session_state:
    st.session_state[key_submit_process] = False

submit_process = st.session_state.get(key_submit_process)
file_list = st.session_state.get(key_file_list)
criteria_data_save_button = st.session_state.get(key_criteria_data_save_button)
clicked_save_button = st.session_state.get(key_clicked_save_button)

############################## Report ##############################

if clicked_save_button:
    df = pd.DataFrame(data=[tool_name_obj.tool_name],columns=['Process Name that you have already saved'])
    st.table(df)

############################## Submit process button  ##############################

#### solution เพื่อเก็บ url_1,2,3,....
for key in st.session_state:
    if 'url' in key and 'amount' not in key:
        st.session_state[key] = st.session_state.get(key)

clicked_submit_process_button = st.button('Submit',
                                            disabled=not submit_process,
                                            on_click = lambda: extractTable_obj.run(st.session_state))
