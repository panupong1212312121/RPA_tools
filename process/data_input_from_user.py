from ui.table_extractor import SaveButton,ToolName

import streamlit as st

table_extractor_tool_name_obj = ToolName()
table_extractor_save_button_obj = SaveButton()
class DataInputFromUser:

    key_submit_input_user = 'submit_input_user'

    def tableExtractor(self,curr_state):
        input_value = []
        export_value = []
        save = table_extractor_save_button_obj.key_clicked_save_button
        if save in curr_state.keys():
            if curr_state[save]:
                input_value = [curr_state]
                export_value.append(input_value)
                if len(export_value)>1:
                    export_value.pop(0)
        return export_value
    
    def submitProcess(self,input_data,tool_name):
        allSave = 0
        if tool_name == table_extractor_tool_name_obj.tool_name:
            if len(input_data)>0:
                allSave += 1

        if allSave >=1 :
            st.session_state[self.key_submit_input_user] = True
        else:
            st.session_state[self.key_submit_input_user] = False