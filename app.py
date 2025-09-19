# IMPORTS SECTION
# - Streamlit
import streamlit as st
# - Others libraries
import json
# - Own Components
# from utils.excel_utils import read_excel_data [Not currentyl needed]
from utils.form_utils import render_dynamic_form 
from utils.word_utils import process_word_template
from utils.ui_components import (
    excel_upload_section,
    word_upload_section,
    preview_dataframe
)

# 0. Initial load of json with inputs data
with open("data/tags.json", "r") as f:
    fields = json.load(f)


# CONTEXT CREATION
st.set_page_config(page_title="LOI Automator", layout="centered")
st.title("LOI Automator")

# Initialize session state
if "context" not in st.session_state:
    st.session_state["context"] = {}
if "preview" not in st.session_state:
    st.session_state["preview"] = None
if "output" not in st.session_state:
    st.session_state["output"] = None

# 1. Manage .word file upload
st.header("1. Upload Word Template")
word_file = word_upload_section()

# 2. Render and logic for Fill out form
st.header("2. Fill Out Tags Form")
context = render_dynamic_form(fields)
if context is not None:
    st.session_state["context"] = context
# st.session_state["context"] = context


# Debug
# st.write("Context preview:", st.session_state["context"])
if word_file and st.session_state["context"]:
    if st.button("Process File"):
        # --- Fix empty tags ---
        context_fixed = {}
        for key, value in st.session_state["context"].items():
            if value == "" or value is None:
                context_fixed[key] = f"{{{{{key}}}}}"  # keep the tag in Word
            else:
                context_fixed[key] = value

        # --- Process Word template ---
        output = process_word_template(word_file, context_fixed)
        st.session_state["output"] = output

# --- Step 3: Download ---
if st.session_state["output"]:
    st.success("✅ File processed successfully!")
    st.download_button(
        label="⬇️ Download File",
        data=st.session_state["output"],
        file_name="processed.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
