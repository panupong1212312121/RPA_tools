from ui.table_extractor import SaveButton

class DataInputFromUser:
    def tableExtractor(self,curr_state):
        save_button_obj = SaveButton()
        input_value = []
        export_value = []
        save = save_button_obj.key_clicked_save_button
        if save in curr_state.keys():
            if curr_state[save]:
                input_value = [curr_state]
                export_value.append(input_value)
                if len(export_value)>1:
                    export_value.pop(0)
        return export_value