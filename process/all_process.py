import streamlit as st

import ui.table_extractor as table_extractor 

class Process:

    key_submit_process = 'submit_process'

    def submitProcess(self,input_data,tool_name):
        
        allSave = 0
        if tool_name == table_extractor.ToolName().tool_name:
            if len(input_data)>0:
                allSave += 1

        if allSave >=1 :
            st.session_state[self.key_submit_process] = True
        else:
            st.session_state[self.key_submit_process] = False