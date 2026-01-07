import streamlit as st
import re
from datetime import date, timedelta

def format_for_document(value, currency=False):
    """
    Format a number for the final document:
    - Currency: $ + thousand separator, 2 decimals if needed
    - Non-currency: just thousand separator
    """
    try:
        val = float(value)
    except (ValueError, TypeError):
        return str(value)  # fallback if not a number

    if currency:
        return f"${int(val):,}" if val.is_integer() else f"${val:,.2f}"
    else:
        return f"{int(val):,}" if val.is_integer() else f"{val:,.2f}"


def formatted_number_input(
    label: str,
    key: str,
    default: float = 0.0,
    currency: bool = False
):
    """
    Unified numeric input component.

    Features:
    - Currency formatting if currency=True
    - Thousand separators for non-currency numbers
    - Numeric-only validation
    - Returns float value
    """
    default = float(default or 0)

    def format_value():
        try:
            raw = st.session_state[key]
            raw = raw.replace("$", "").replace(",", "")

            # Allow only digits and a single decimal point
            if not re.fullmatch(r"\d*\.?\d*", raw):
                st.session_state[key] = ""
                return

            if raw == "":
                return

            val = float(raw)

            if currency:
                st.session_state[key] = (
                    f"${int(val):,}" if val.is_integer()
                    else f"${val:,.2f}"
                )
            else:
                st.session_state[key] = (
                    f"{int(val):,}" if val.is_integer()
                    else f"{val:,.2f}"
                )
        except Exception:
            pass

    # Initialize display value
    if key not in st.session_state:
        if currency:
            st.session_state[key] = (
                f"${int(default):,}" if default.is_integer()
                else f"${default:,.2f}"
            )
        else:
            st.session_state[key] = (
                f"{int(default):,}" if default.is_integer()
                else f"{default:,.2f}"
            )

    user_input = st.text_input(
        label=label,
        key=key,
        on_change=format_value
    )

    # Return numeric value
    try:
        return float(user_input.replace("$", "").replace(",", ""))
    except ValueError:
        return 0.0


def render_dynamic_form(fields: list) -> dict:
    """
    Render a dynamic Streamlit form from a field configuration list.

    Field config example:
    {
        "name": "LEASE_RENT",
        "label": "Lease Payment Amount",
        "type": "number",
        "currency": True
    }
    """
    context = {}

    for field in fields:
        field_name = field["name"]
        field_label = field.get("label", field_name)
        field_type = field.get("type", "text")
        is_currency = field.get("currency", False)
        default = field.get("default", "")

        if field_type == "text":
            context[field_name] = st.text_input(
                label=field_label,
                value=default,
                key=field_name
            )

        elif field_type == "number":
            context[field_name] = formatted_number_input(
                label=field_label,
                key=field_name,
                default=default or 0,
                currency=is_currency
            )

        elif field_type == "date":
            d = st.date_input(
                label=field_label,
                value=default or date.today(),
                key=field_name
            )
            context[field_name] = d.strftime("%B %d, %Y")

        elif field_type == "period":
            start_default = field.get("start_default")
            end_offset = field.get("end_offset_days", 0)

            # Resolve start date
            if isinstance(start_default, str):
                start_date = st.session_state.get(start_default, date.today())
            else:
                start_date = date.today()

            end_date = start_date + timedelta(days=end_offset)

            # Render date range picker
            period_value = st.date_input(
                label=field_label,
                value=(start_date, end_date),
                key=field_name
            )

            # Show placeholder until both dates are selected
            if isinstance(period_value, tuple) and len(period_value) == 2:
                start, end = period_value
                context[field_name] = f"{start.strftime('%b %d, %Y')} to {end.strftime('%b %d, %Y')}"
            else:
                # Placeholder text (or you can use "")
                context[field_name] = "Select both start and end dates"


        else:
            context[field_name] = st.text_input(
                label=field_label,
                value=default,
                key=field_name
            )

    return context
