import streamlit as st
from utils.excel_utils import read_excel_data
from utils.word_utils import process_word_template
from utils.ui_components import (
    excel_upload_section,
    word_upload_section,
    preview_dataframe
)

st.set_page_config(page_title="Excel → Word Processor", layout="centered")
st.title("📄 MS Excel → Word Replacer")

# Initialize session state
if "context" not in st.session_state:
    st.session_state["context"] = {}
if "preview" not in st.session_state:
    st.session_state["preview"] = None
if "output" not in st.session_state:
    st.session_state["output"] = None

# --- Step 1: Upload Excel ---
st.header("1. Upload Excel File")
excel_file, first_row, tag_col, user_input_col = excel_upload_section()

if excel_file and st.button("Read Input Data"):
    context, preview = read_excel_data(excel_file, first_row, tag_col, user_input_col)
    st.session_state["context"] = context
    st.session_state["preview"] = preview

# Show preview if available
if st.session_state["preview"] is not None:
    st.success("✅ Data processed successfully!")
    preview_dataframe(st.session_state["preview"])

# --- Step 2: Upload Word ---
st.header("2. Upload Word Template")
word_file = word_upload_section()

# Debug
# st.write("Context preview:", st.session_state["context"])

if word_file and st.session_state["context"]:
    if st.button("Process File"):
        output = process_word_template(word_file, st.session_state["context"])
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
