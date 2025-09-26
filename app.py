import streamlit as st
from blockchain import Blockchain

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.title("📒 Blockchain-based Digital Diary (Multi-User)")

# 🔍 Search Section
st.sidebar.header("🔍 Search Diary")
search_id = st.sidebar.text_input("Search by Diary ID (index)")
search_user = st.sidebar.text_input("Search by User Name")

# Separate section for User Name
st.subheader("👤 User Information")
user = st.text_input("Enter Your Name")

# Section for Diary Entry
st.subheader("✍️ Write Your Diary Entry")
entry = st.text_area("Diary Entry:")

if st.button("Add Entry"):
    if user.strip() and entry.strip():
        st.session_state.blockchain.add_block(user, entry)
        st.success(f"Entry added successfully for {user}!")
    else:
        st.warning("Please enter both name and entry text.")

# Display diary timeline
st.subheader("📜 Diary Timeline")
for block in st.session_state.blockchain.chain:
    # Apply search filters
    if search_id and str(block.index) != search_id:
        continue
    if search_user and block.user.lower() != search_user.lower():
        continue

    st.markdown(f"""
    **Diary ID:** {block.index}  
    **User:** {block.user}  
    **Timestamp:** {block.timestamp}  
    **Entry:** {block.data}  
    **Hash:** `{block.hash}`  
    **Previous Hash:** `{block.previous_hash}`  
    """)
    st.write("---")
