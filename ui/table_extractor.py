import streamlit as st

class ToolName:
    tool_name = '1_Table_Extractor'

class FileUploader:
    max_file_amount = 3

    key_file_list = 'file_list'
    key_file_amount = 'file_amount'
    key_changed_file = 'changed_file'
            
class LinkInput:
    min_url_amount = 0
    max_url_amount = 3
    
    key_url_amount = 'url_amount'
    key_changed_url = 'changed_url'

    def allNull(self,currentState):
        url_amount = st.session_state.get(self.key_url_amount)
        if url_amount!=0:
            for key in currentState:
                if 'url' in key and 'amount' not in key:
                    if currentState[key]!='':
                        return False
            return True
        else:
            return False
class SaveButton:

    key_criteria_data_save_button = 'criteria_data_save_button'
    key_clicked_save_button = 'clicked_save_button'

    def criteriaData(self,currentState):
        file_uploader_obj = FileUploader()
        link_input_obj = LinkInput()

        key_file_amount = file_uploader_obj.key_file_amount
        max_file_amount = file_uploader_obj.max_file_amount

        key_url_amount = link_input_obj.key_url_amount
        all_null = link_input_obj.allNull(currentState)

        if currentState[key_file_amount] > max_file_amount or \
            (currentState[key_file_amount] == 0 and all_null) or \
            (currentState[key_file_amount] == 0 and currentState[key_url_amount]==0):
            return False
        else:
            return True

