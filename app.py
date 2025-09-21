import streamlit as st
import json
from utils.form_utils import render_dynamic_form
from utils.word_utils import process_word_template
from utils.ui_components import word_upload_section

# 0. Load field definitions
with open("data/tags.json", "r") as f:
    fields = json.load(f)

# 1. Page config
st.set_page_config(page_title="LOI Automator", layout="centered")
st.title("LOI Automator")

# 2. Initialize session state 
for key in ["context", "output"]:
    if key not in st.session_state:
        st.session_state[key] = {}

# 3. Upload Word template
st.header("1. Upload Word Template")
word_file = word_upload_section()

# 4. Fill out dynamic form
st.header("2. Fill Out Tags Form")
context = render_dynamic_form(fields)
if context is not None:
    st.session_state["context"] = context


# 5. Filename input
st.header("3. File Name and Processing")
filename = st.text_input(
    "Enter file name for download:", value="processed.docx", key="download_filename"
)

# 6. Process Word button
if word_file and st.session_state.get("context"):
    if st.button("Generate LOI"):
        # Preserve empty tags in Word template
        context_fixed = {
            key: (f"{{{{{key}}}}}" if value in ["", None] else value)
            for key, value in st.session_state["context"].items()
        }
        st.session_state["output"] = process_word_template(word_file, context_fixed)
        if st.session_state["output"]:
            st.success("✅ File processed successfully!")

# Download button (visible if output exists)
if st.session_state.get("output"):
    st.download_button(
        label="⬇️ Download File",
        data=st.session_state["output"],
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
