import streamlit as st
from src.web.utils.i18n_utils import I18N


i18n = I18N("locales", st.session_state.lang)
i18n.set_scope("dashboard")

st.title(i18n("dashboard"))
st.subheader(i18n("welcome_message"))
