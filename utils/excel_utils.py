import pandas as pd

def read_excel_data(excel_file, first_row, tag_col, user_input_col):
    try:
        df = pd.read_excel(excel_file, header=None, skiprows=first_row - 1)

        tags = df.iloc[:, tag_col - 1].dropna().astype(str).tolist()
        user_inputs = df.iloc[:, user_input_col - 1].dropna().astype(str).tolist()

        context = dict(zip(tags, user_inputs))
        preview = pd.DataFrame({"Tag": tags, "User Input": user_inputs})

        return context, preview
    except Exception as e:
        import streamlit as st
        st.error(f"⚠️ Error reading Excel: {e}")
        return {}, None
