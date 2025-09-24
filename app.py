import streamlit as st
from src.web.utils.i18n_utils import I18N

st.session_state.lang = "en"
i18n = I18N("locales", st.session_state.lang)
i18n.set_scope("dashboard")

st.set_page_config(
    layout="wide",
)


main_page = st.Page(
    "src/web/pages/dashboard/dashboard.py",
    title=f"{i18n('dashboard')}",
    icon="🎈",
)
page_2 = st.Page(
    "src/web/pages/character_resolution/character_resolution.py",
    title=f"{i18n('character_resolution')}",
    icon="❄️",
)

# Set up navigation
pg = st.navigation([main_page, page_2], expanded=True)

# Run the selected page
pg.run()
