class FileUploader:
    max_upload_files = 3
    key_upload_files = 'file_amount'
        
class LinkInput:
    min_link_inputs = 0
    max_link_inputs = 3
    key_link_inputs = 'link_amount'
    key_click_add_amount = 'click_add_amount'
    key_click_remove_amount = 'click_remove_amount'

    def is_all_null(currentState,link_amount):
        if link_amount!=0:
            for key in currentState:
                if 'link' in key and 'amount' not in key:
                    if currentState[key]!='':
                        return False
            return True
        else:
            return False

class AddLinkButton:
    key_add_link_button = 'add_link_button'
    
    def disabled(link_amount):
        if link_amount==LinkInput().max_link_inputs:
            return True
        else:
            return False
        
class RemoveLinkButton:
    key_remove_link_button = 'remove_link_button'
    
    def disabled(link_amount):
        if link_amount==LinkInput().min_link_inputs:
            return True
        else:
            return False
    
class SubmitButton:

    def disabled(currentState,link_amount):
        is_null = LinkInput.is_all_null(currentState,link_amount)
        if currentState['file_amount'] > FileUploader.max_upload_files or \
            (currentState['file_amount'] == 0 and is_null) or \
            (currentState['file_amount'] == 0 and currentState['link_amount']==0)    :
            return True
        else:
            return False
 
    