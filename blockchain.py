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

# For the Streamlit app, we'll hardcode the user as "Diary User" since no user input is provided
# If you want dynamic users, add a text input for username

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.title("📒 Blockchain-based Digital Diary")

# Optional: Add a username input
username = st.text_input("Enter your username (optional, defaults to 'Diary User'):", value="Diary User")

entry = st.text_area("Write your diary entry:")
if st.button("Add Entry"):
    if entry.strip():
        # Use provided username or default
        user_to_use = username if username.strip() else "Diary User"
        st.session_state.blockchain.add_block(user_to_use, entry)
        st.success("Entry added successfully!")
        # Clear the text area
        st.rerun()

st.subheader("📜 Diary Timeline")
for i, block in enumerate(st.session_state.blockchain.chain):
    # Format timestamp for display
    formatted_timestamp = block.timestamp.strftime("%Y-%m-%d %H:%M:%S") if hasattr(block.timestamp, 'strftime') else str(block.timestamp)
    st.markdown(f"""
    **Index:** {block.index}  
    **Timestamp:** {formatted_timestamp}  
    **User :** {block.user}  
    **Entry:** {block.data}  
    **Hash:** `{block.hash}`  
    **Previous Hash:** `{block.previous_hash}`  
    """)
    if i < len(st.session_state.blockchain.chain) - 1:
        st.write("---")
