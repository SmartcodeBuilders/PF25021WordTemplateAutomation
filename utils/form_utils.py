import streamlit as st
from datetime import date

def render_dynamic_form(fields):
    """Render a form dynamically from a list of field configs (JSON)."""
    context = {}

    with st.form("input_form"):
        for field in fields:
            field_name = field["name"]
            field_label = field.get("label", field_name)
            field_type = field.get("type", "text")

            if field_type == "text":
                context[field_name] = st.text_input(
                    field_label,
                    field.get("default", ""),
                    key=field_name
                )
            elif field_type == "number":
                # context[field_name] = st.number_input(
                #     field_label,
                #     value=field.get("default", 0),
                #     key=field_name
                # )
                value = st.number_input(
                    f"{field_label}",
                    value=field.get("default", 0),
                    key=field_name
                )
                context[field_name] = f"${value:,.2f}"
            elif field_type == "date":
                d = st.date_input(
                    field_label,
                    field.get("default", date.today()),
                    key=field_name
                )
                context[field_name] = d.strftime("%Y-%m-%d")
            else:
                context[field_name] = st.text_input(
                    field_label,
                    field.get("default", ""),
                    key=field_name
                )

        submitted = st.form_submit_button("Save Data")

    return context if submitted else None