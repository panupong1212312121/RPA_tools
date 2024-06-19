import streamlit as st

from process.data_input_from_user import DataInputFromUser

from ui.table_extractor import ToolName,FileUploader,LinkInput,SaveButton

############################## Var ##############################

data_input_from_user_obj = DataInputFromUser()

tool_name_obj = ToolName()
file_uploader_obj = FileUploader()
link_input_obj = LinkInput()
save_button_obj = SaveButton()

max_file_amount = file_uploader_obj.max_file_amount
key_file_amount = file_uploader_obj.key_file_amount
key_file_list = file_uploader_obj.key_file_list

min_url_amount = link_input_obj.min_url_amount
max_url_amount = link_input_obj.max_url_amount
key_url_amount = link_input_obj.key_url_amount

key_criteria_data_save_button = save_button_obj.key_criteria_data_save_button
key_clicked_save_button = save_button_obj.key_clicked_save_button

############################## State ##############################

if key_file_amount not in st.session_state:
    st.session_state[key_file_amount] = 0
if key_file_list not in st.session_state:
    st.session_state[key_file_list] = []

if key_url_amount not in st.session_state:
    st.session_state[key_url_amount] = 0

if key_criteria_data_save_button not in st.session_state:
    st.session_state[key_criteria_data_save_button] = False
if key_clicked_save_button not in st.session_state:
    st.session_state[key_clicked_save_button] = False 

file_amount = st.session_state[key_file_amount]

url_amount = st.session_state[key_url_amount]

criteria_data_save_button = st.session_state[key_criteria_data_save_button]
clicked_save_button = st.session_state[key_clicked_save_button]

st.markdown("<h1 style='text-align: center;'>Table Extraction</h1>", unsafe_allow_html=True)
st.warning("Please paste link or file at least 1", icon="⚠️")

col1, col2 = st.columns(2)

################ File uploader ####################
with col1:
    uploaded_files = st.file_uploader(label=f"Choose your files (Max : {max_file_amount})",
                                    type=['png', 'jpg','jpeg','pdf','docx','pptx'],
                                    accept_multiple_files=True)
    
    st.session_state[key_file_list] = uploaded_files

    file_amount = len(uploaded_files)
    st.session_state[key_file_amount] = file_amount
    if file_amount > max_file_amount: 
        st.error(f"Don't allow more than {max_file_amount} files.", icon="🚨")

    st.session_state[key_clicked_save_button] = False

################ Link Input ####################

with col2:   

    st.caption(f":black[Choose your urls (Max : {max_url_amount})]",unsafe_allow_html=False)

    with st.container(height = 100):
        for key in range(1,url_amount+1):
            st.text_input(f"Url {key}",key=f'url_{key}') 

    col3, col4 = st.columns(2)
    with col3:
        if st.button("Add Link Input",
                    disabled=url_amount==max_url_amount,
                    use_container_width=True):
            if url_amount < max_url_amount:
                st.session_state[key_url_amount] += 1 
            st.rerun()

    with col4:
        if st.button("Remove Link Input",
                    disabled=url_amount==min_url_amount,
                    use_container_width=True):
            if url_amount > min_url_amount:
                st.session_state[key_url_amount] -= 1
            st.rerun()

    st.session_state[key_clicked_save_button] = False

    criteria_data_save_button = save_button_obj.criteriaData(st.session_state)
    st.session_state[key_criteria_data_save_button] = criteria_data_save_button

################ Save Button #################### 

clicked_save_button = st.button('Save',
                                disabled = not criteria_data_save_button,
                                ) 
    
if clicked_save_button:
    st.session_state[key_clicked_save_button] = clicked_save_button

if criteria_data_save_button and clicked_save_button:
    st.success('Already Saved')  
    table_extraction_input = data_input_from_user_obj.tableExtractor(st.session_state)

    data_input_from_user_obj.submitProcess(table_extraction_input,tool_name_obj.tool_name)

############################################################