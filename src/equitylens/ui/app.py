"""Main Streamlit interface."""


def main() -> None:
    """Render the Day 1 application shell."""
    import streamlit as st

    st.set_page_config(page_title="EquityLens", page_icon="🔎", layout="wide")
    st.title("EquityLens")
    st.caption("A research dashboard for exploring ASX stocks")
    st.info("Project foundation ready. Market analysis arrives in later stages.")
    st.warning("Educational research only — not financial advice.")
