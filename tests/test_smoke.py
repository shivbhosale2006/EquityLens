"""Day 1 smoke tests."""


def test_package_imports() -> None:
    import equitylens
    from equitylens.config import get_settings
    from equitylens.ui.app import main

    assert equitylens.__version__ == "0.1.0"
    assert get_settings().environment == "development"
    assert callable(main)


def test_streamlit_entry_point_imports() -> None:
    import streamlit_app

    assert callable(streamlit_app.main)
