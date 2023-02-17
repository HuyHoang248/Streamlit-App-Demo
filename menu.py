import streamlit as st
from streamlit_option_menu import option_menu
from apps import overview, store, dept  # import your app modules here

st.set_page_config(page_title="Weave Services", layout="wide")

apps = [
    {"func": overview.app, "title": "Overview"},
    {"func": store.app, "title": "Store"},
    {"func": dept.app, "title": "Dept"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        options=titles,
        menu_icon="cast",
        default_index=default_index,
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break