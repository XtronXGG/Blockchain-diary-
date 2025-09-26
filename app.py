import streamlit as st
import hashlib
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, user, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.user = user
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Use ISO format for timestamp to ensure consistent string representation for hashing
        timestamp_str = self.timestamp.isoformat() if hasattr(self.timestamp, 'isoformat') else str(self.timestamp)
        block_string = str(self.index) + timestamp_str + self.user + self.data + self.previous_hash
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        genesis_timestamp = datetime.now()
        return Block(0, genesis_timestamp, "System", "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, user, new_data):
        latest_block = self.get_latest_block()
        new_index = len(self.chain)  # Correct index calculation
        new_timestamp = datetime.now()
        new_block = Block(new_index, new_timestamp, user, new_data, latest_block.hash)
        self.chain.append(new_block)

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.title("📒 Blockchain-based Digital Diary (Multi-User)")

# Initialize session state for inputs to allow clearing
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "entry_input" not in st.session_state:
    st.session_state.entry_input = ""

# 🔍 Search Section
st.sidebar.header("🔍 Search Diary")
search_id = st.sidebar.text_input("Search by Diary ID (index)")
search_user = st.sidebar.text_input("Search by User Name")

# Add new diary entry
st.subheader("✍️ Add New Entry")
user = st.text_input("Your Name", value=st.session_state.user_input)
entry = st.text_area("Write your diary entry:", value=st.session_state.entry_input, key="entry_area")

if st.button("Add Entry"):
    if user.strip() and entry.strip():
        st.session_state.blockchain.add_block(user, entry)
        st.success(f"Entry added successfully for {user}!")
        # Clear the inputs
        st.session_state.user_input = ""
        st.session_state.entry_input = ""
        st.rerun()
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

    # Format timestamp for display
    formatted_timestamp = block.timestamp.strftime("%Y-%m-%d %H:%M:%S") if hasattr(block.timestamp, 'strftime') else str(block.timestamp)
    
    st.markdown(f"""
    **Diary ID:** {block.index}  
    **User :** {block.user}  
    **Timestamp:** {formatted_timestamp}  
    **Entry:** {block.data}  
    **Hash:** `{block.hash}`  
    **Previous Hash:** `{block.previous_hash}`  
    """)
    st.write("---")
