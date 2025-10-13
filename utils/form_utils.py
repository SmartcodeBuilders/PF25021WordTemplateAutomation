import streamlit as st
from datetime import date

def currency_input(label, key, default=0.0):
    """
    Currency input that allows typing, displays $, and formats value when user finishes typing.
    Returns numeric float.
    """
    def format_currency():
        try:
            val = float(st.session_state[key].replace("$", "").replace(",", ""))
            st.session_state[key] = f"${val:,.2f}"
        except ValueError:
            pass

    # Initialize default display if first run
    if key not in st.session_state:
        st.session_state[key] = f"${default:,.2f}"

    # Input field with on_change callback
    user_input = st.text_input(label, key=key, on_change=format_currency)

    # Always return numeric version
    try:
        num_value = float(user_input.replace("$", "").replace(",", ""))
        num_value = f"${num_value:,.2f}"
    except ValueError:
        num_value = user_input 

    return num_value

def render_dynamic_form(fields):
    """Render a form dynamically from a list of field configs (JSON)."""
    context = {}

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
            value = currency_input(field_label, key=field_name, default=field.get("default", 0))
            context[field_name] = value
        elif field_type == "date":
            d = st.date_input(
                field_label,
                field.get("default", date.today()),
                key=field_name
            )
            context[field_name] = d.strftime("%B %d, %Y")
        else:
            context[field_name] = st.text_input(
                field_label,
                field.get("default", ""),
                key=field_name
            )

    return context
