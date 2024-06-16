class FileUploader:
    max_upload_files = 3
    key_upload_files = 'file_amount'
        
class LinkInput:
    min_link_inputs = 0
    max_link_inputs = 3
    
    key_link_inputs = 'link_amount'

    def allNull(self,currentState,link_amount):
        if link_amount!=0:
            for key in currentState:
                if 'link' in key and 'amount' not in key:
                    if currentState[key]!='':
                        return False
            return True
        else:
            return False
class SubmitButton:

    def disabled(self,currentState,link_amount):
        file_uploader_obj = FileUploader()
        link_input_obj = LinkInput()

        key_upload_files = file_uploader_obj.key_upload_files
        max_upload_files = file_uploader_obj.max_upload_files

        key_link_inputs = link_input_obj.key_link_inputs
        all_null = link_input_obj.allNull(currentState,link_amount)

        # ถูกแล้ว 
        if currentState[key_upload_files] > max_upload_files or \
            (currentState[key_upload_files] == 0 and all_null) or \
            (currentState[key_upload_files] == 0 and currentState[key_link_inputs]==0):
            return True
        else:
            return False

