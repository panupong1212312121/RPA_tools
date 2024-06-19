import streamlit as st

st.header("Welcome to RPA tools")

recommendation = '''
You can select desired RPA tool menus in sidebar at the left hand side

Then , don't forget to make sure that you have already clicked 'save button' in each selected tools for begin

If you want to proceed all processes , you have to click 'All Process' menu and then click 'submit button'

After that ,please wait for results

'''
st.divider()

st.write(recommendation)

caution = '''
If you finish process 1 time , I recommed you to click 'Home' menu and then refresh for begin again 
'''
st.warning(caution, icon="🚨")