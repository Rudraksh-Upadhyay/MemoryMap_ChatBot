import streamlit as st

st.title("Session State")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1
if st.button("Decrement"):
    st.session_state.count -= 1

st.write("Current count : ", st.session_state.count)