import streamlit as st
from extractor import ExtractTable
from table_extractor import FileUploader,LinkInput,SaveButton,EditButton

def firstPage():
    st.header('Welcome to RPA tools')

def tableExtractor():

    file_uploader_obj = FileUploader()
    link_input_obj = LinkInput()
    extract_table_obj = ExtractTable()
    save_button_obj = SaveButton()
    edit_button_obj = EditButton()

    max_upload_files = file_uploader_obj.max_upload_files
    key_upload_files = file_uploader_obj.key_upload_files

    min_link_inputs = link_input_obj.min_link_inputs
    max_link_inputs = link_input_obj.max_link_inputs
    key_link_inputs = link_input_obj.key_link_inputs

    key_disabled_save_button = save_button_obj.key_disabled_save_button
    key_clicked_save_button = save_button_obj.key_clicked_save_button

    key_disabled_edit_button = edit_button_obj.key_disabled_edit_button
    key_clicked_edit_button = edit_button_obj.key_clicked_edit_button

    ############################## UI ##############################

    ## State
    if key_upload_files not in st.session_state:
        st.session_state[key_upload_files] = 0
        
    if key_link_inputs not in st.session_state:
        st.session_state[key_link_inputs] = 0

    if key_disabled_save_button not in st.session_state:
        st.session_state[key_disabled_save_button] = True
    if key_clicked_save_button not in st.session_state:
        st.session_state[key_clicked_save_button] = False

    if key_disabled_edit_button not in st.session_state:
        st.session_state[key_disabled_edit_button] = True
    if key_clicked_edit_button not in st.session_state:
        st.session_state[key_clicked_edit_button] = False   

    file_amount = st.session_state[key_upload_files]

    link_amount = st.session_state[key_link_inputs]
    
    disabled_save_button = st.session_state[key_disabled_save_button]
    clicked_save_button = st.session_state[key_clicked_save_button]

    disabled_edit_button = st.session_state[key_disabled_edit_button]
    clicked_edit_button = st.session_state[key_clicked_edit_button]

    st.markdown("<h1 style='text-align: center;'>Table Extraction</h1>", unsafe_allow_html=True)
    st.warning("Please paste link or file at least 1", icon="⚠️")

    col1, col2 = st.columns(2)

    ################ File uploader ####################
    with col1:
        uploaded_files = st.file_uploader(label=f"Choose your files (Max : {max_upload_files})",
                                        type=['png', 'jpg','jpeg','pdf','docx','pptx'],
                                        accept_multiple_files=True)

        file_amount = len(uploaded_files)
        st.session_state[key_upload_files] = file_amount
        if file_amount > max_upload_files: 
            st.error(f"Don't allow more than {max_upload_files} files.", icon="🚨")

    ################ Link Input ####################

    with col2:   

        # st.write(st.session_state)
        st.caption(f'Choose your urls (Max : {max_link_inputs})')

        with st.container(height = 100):
            for key in range(1,link_amount+1):
                st.text_input(f"Url {key}",key=f'link_{key}') 

        col3, col4 = st.columns(2)
        with col3:
            if st.button("Add Link Input",
                        disabled=link_amount==max_link_inputs):
                if link_amount < max_link_inputs:
                    st.session_state[key_link_inputs] += 1 ############# Solution 
                st.rerun()

        with col4:
            if st.button("Remove Link Input",
                        disabled=link_amount==min_link_inputs):
                if link_amount > min_link_inputs:
                    st.session_state[key_link_inputs] -= 1
                st.rerun()

        disabled_save_button = save_button_obj.disabled(st.session_state,link_amount)
        st.session_state[key_disabled_save_button] = disabled_save_button

        # แจ้งเตือนครั้งเดียวพอ 
        if link_amount == max_link_inputs:
            st.toast(f"You can add link inputs up to {max_link_inputs} maximum.", icon="🚨")

        # st.write(st.session_state)
    
    ################ Save & Edit Button ####################

    clicked_save_button = st.button('Save',
                                    disabled = disabled_save_button or clicked_save_button) # Solution 
        
    clicked_edit_button = st.button('Edit',
                                    disabled = disabled_edit_button or clicked_edit_button) # Solution 
        
    if clicked_save_button:
        st.session_state[key_clicked_save_button] = clicked_save_button
        st.session_state[key_disabled_edit_button] = not clicked_save_button

        st.session_state[key_clicked_edit_button] = not clicked_save_button
        st.rerun()

    if clicked_edit_button:
        st.session_state[key_clicked_edit_button] = clicked_edit_button
        st.session_state[key_clicked_save_button] = not clicked_edit_button
        st.rerun() 

    st.write(st.session_state)

page_names_to_funcs = {
    # "First Page": firstPage,
    "Table Extractor": tableExtractor
}

demo_name = st.sidebar.selectbox("Choose your tools", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

with st.sidebar:
    # enable เมื่อปุ่ม save ถูก click อย่างน้อย 1 อัน 
    st.warning('Please make sure you click save button in all tools')
    st.button('Submit',disabled=True)


# on_click = lambda: extractTable_obj.run(uploaded_files,st.session_state,disabled_SaveButton)