import streamlit as st
from extractor import ExtractTable
from widget import *

############################## Criteria ##############################

max_upload_files = FileUploader.max_upload_files

min_link_inputs = LinkInput.min_link_inputs
max_link_inputs = LinkInput.max_link_inputs

key_upload_files = FileUploader.key_upload_files
key_link_inputs = LinkInput.key_link_inputs

############################## UI ##############################

## State
if key_upload_files not in st.session_state:
    st.session_state[key_upload_files] = 0
if key_link_inputs not in st.session_state:
    st.session_state[key_link_inputs] = 0

link_amount = st.session_state[key_link_inputs]
file_amount = st.session_state[key_upload_files]

# def link_amount_state(link_amount):
#     st.session_state[key_link_inputs] = link_amount

st.markdown("<h1 style='text-align: center;'>Table Extraction tools</h1>", unsafe_allow_html=True)
st.warning("Please paste link or file at least 1", icon="⚠️")

col1, col2 = st.columns(2)

################ File uploader ####################
with col1:
    uploaded_files = st.file_uploader(label="Choose a file",
                                    type=['png', 'jpg','jpeg','pdf','docx','pptx'],
                                    accept_multiple_files=True)

    file_amount = len(uploaded_files)
    st.session_state[key_upload_files] = file_amount
    if file_amount > max_upload_files: 
        st.error(f"Don't allow more than {max_upload_files} files.", icon="🚨")

################ Link Input ####################

with col2:   

    st.write(st.session_state)
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Add Link Input",
                     disabled=link_amount==max_link_inputs):
            if link_amount < max_link_inputs:
                st.session_state[key_link_inputs] += 1 ############# Solution 
            else:
                st.warning(f"Can't allow more than {max_link_inputs} link inputs.", icon="🚨")
            st.rerun()

    with col4:
        if st.button("Remove Link Input",
                     disabled=link_amount==min_link_inputs):
            if link_amount > min_link_inputs:
                st.session_state[key_link_inputs] -= 1
            st.rerun()

    with st.container(height = 100):
        for key in range(1,link_amount+1):
            st.text_input("Paste a link",key=f'link_{key}') 

    st.write(st.session_state)

    disabled_SubmitButton = SubmitButton.disabled(st.session_state,link_amount)

st.button('Submit',
          disabled = disabled_SubmitButton)
        #   on_click=ExtractTable().run(uploaded_files,currentState))

#### Next Step : แก้ logic UI (link_key ไม่ยอมหาย)

#### Next Step : Logic read_html 

#### Next Step : Export File in Diff excel name and download path ทำยังไวให้ชื่อมันไม่ซ้ำกันแน่ ๆ (ชื่อ file เดิม + id something?)


#####################################

# import streamlit as st
# import pandas as pd

# if 'name' not in st.session_state:
#     st.session_state['name'] = 'John Doe'

# st.write(st.session_state)

# if st.button('Jane'):
#     st.session_state['name'] = 'Jane Doe'
#     st.rerun()

# if st.button('John'):
#     st.session_state['name'] = 'John Doe'
#     st.rerun()

# st.write(st.session_state)
