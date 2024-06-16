import streamlit as st
from extractor import ExtractTable
from widget import *

############################## Criteria ##############################

max_upload_files = FileUploader().max_upload_files
key_upload_files = FileUploader().key_upload_files

min_link_inputs = LinkInput().min_link_inputs
max_link_inputs = LinkInput().max_link_inputs
key_link_inputs = LinkInput().key_link_inputs

extractTable_obj = ExtractTable()

submit_button_obj = SubmitButton()

############################## UI ##############################

## State
if key_upload_files not in st.session_state:
    st.session_state[key_upload_files] = 0
if key_link_inputs not in st.session_state:
    st.session_state[key_link_inputs] = 0

link_amount = st.session_state[key_link_inputs]
file_amount = st.session_state[key_upload_files]

st.markdown("<h1 style='text-align: center;'>Table Extraction tools</h1>", unsafe_allow_html=True)
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

    disabled_SubmitButton = submit_button_obj.disabled(st.session_state,link_amount)

    # แจ้งเตือนครั้งเดียวพอ 
    if link_amount == max_link_inputs:
        st.toast(f"You can add link inputs up to {max_link_inputs} maximum.", icon="🚨")

    # st.write(st.session_state)

st.button('Submit',
          disabled = disabled_SubmitButton,
          on_click = lambda: extractTable_obj.run(uploaded_files,st.session_state,disabled_SubmitButton)) # Solution 

############################ Test & Next Steps ###########################
#### Next Step : after submit logic 

#### Next Step : # เวลา eatract table ให้มันไม่จำเป็นต้องสร้าง file ใหม่ 

#### Next Step : # แจ้งเตือน toast ครั้งเดียวพอ 

#### Test case : 
# 1.file 2 , link 3 ว่าง 1 ถูก 1 ผิด 1 

###########################################################################################
