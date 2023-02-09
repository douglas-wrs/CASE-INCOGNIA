import streamlit as st
from src.pages import case_ato
from src.pages import readme
from src.pages import case
from src.pages import problem
from src.pages import data
from src.pages import exploration

st.set_page_config(layout="wide", page_title="Case Incognia")

PAGES = {
    "README": readme,
    "Case": case,
    "Problem": problem,
    "Data": data,
    "Exploration": exploration
}

def main():
    selection = st.sidebar.radio("Pages", list(PAGES.keys()), index=0)

    page = PAGES[selection]

    page.show()

if __name__ == '__main__':
    main()