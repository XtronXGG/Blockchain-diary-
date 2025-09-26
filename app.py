import streamlit as st
from blockchain import Blockchain

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.set_page_config(page_title="📒 Digital Diary", layout="wide")
st.title("📒 Blockchain-based Digital Diary ")

# Metrics
total_entries = len(st.session_state.blockchain.chain) - 1
users = list(set([b.user for b in st.session_state.blockchain.chain if b.index != 0]))
total_users = len(users)
st.metric("Total Entries", total_entries)
st.metric("Total Users", total_users)

# Top search bar
st.subheader("🔍 Search Diary")
col1, col2 = st.columns(2)
with col1:
    search_id = st.text_input("Search by Diary ID")
with col2:
    search_user = st.text_input("Search by User Name")

# Add new entry
st.subheader("✍️ Add New Entry")
user = st.text_input("👤 Enter Your Name", key="name_input")
title = st.text_input("📌 Entry Title", key="title_input")
entry = st.text_area("📝 Diary Entry", key="entry_input")

if st.button("Add Entry"):
    if user.strip() and entry.strip() and title.strip():
        st.session_state.blockchain.add_block(user, title, entry)
        st.success(f"Entry added successfully for {user}!")
    else:
        st.warning("Please enter Name, Title, and Entry.")

# Verify Blockchain
if st.button("🔒 Verify Blockchain Integrity"):
    if st.session_state.blockchain.verify_chain():
        st.success("✅ Blockchain is valid.")
    else:
        st.error("❌ Blockchain integrity compromised!")

# Timeline display
st.subheader("📜 Diary Timeline")
found = False

for block in reversed(st.session_state.blockchain.chain):
    if block.index == 0:
        continue  # skip Genesis Block
    if search_id and block.diary_id != search_id:
        continue
    if search_user and block.user.lower() != search_user.lower():
        continue

    with st.expander(f"{block.title} - {block.user} ({block.diary_id})", expanded=False):
        st.markdown(f"""
        **Diary ID:** {block.diary_id}  \n
        **User:** {block.user}  \n
        **Timestamp:** {block.timestamp}  \n
        **Entry:** {block.data}  \n
        **Hash:** `{block.hash}`  \n
        **Previous Hash:** `{block.previous_hash}`
        """)
    found = True

if not found:
    st.error("❌ No diary entries found.")
