import streamlit as st
from memory import TemporaryMemory
from memory import PermanentMemory
from memory import get_euron_response

st.set_page_config(page_title="MemoryMap", page_icon="🗺️")
st.title("🗺️ MemoryMap - Chatbot with Memory")
st.caption("Temporary + Permanent memory demo using Streamlit + OPENAI API")

# if "messages" not in st.session_state:
#     st.session_state.messages = []
if "temp_memory" not in st.session_state:
    st.session_state.temp_memory = TemporaryMemory()

if "perm_memory" not in st.session_state:
    st.session_state.perm_memory = PermanentMemory()


#display the history
for msg in st.session_state.temp_memory.get_history():
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"🙋 **You:** {msg['content']}")
    else:
        with st.chat_message("assistant"):
            st.markdown(f"🤖 **Bot:** {msg['content']}")

#user input
if prompt := st.chat_input("💬 Type your message here..."):
    # st.session_state.messages.append({"role":"user", "content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    history = st.session_state.temp_memory.get_history().copy()
    history.append({"role":"user", "content":prompt})

    try:
        response = get_euron_response(history)
    except Exception as e:
        response = f"Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.temp_memory.add(prompt, response)

#memory controls

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💾 Save Memory"):
        st.session_state.perm_memory.save(st.session_state.temp_memory)
        with st.chat_message("system"):
            st.markdown("Memory saved to file!")

with col2:
    if st.button("📂 Load Memory"):
        loaded = st.session_state.perm_memory.load()
        st.session_state.temp_memory.conversation = loaded
        with st.chat_message("system"):
            st.markdown("📂 Memory loaded from file!")

with col3:
    if st.button("🗑️ Reset Memory"):
        st.session_state.temp_memory.reset()
        with st.chat_message("system"):
            st.markdown("🗑️ Temporary Memory saved to file!")