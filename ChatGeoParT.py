import os
import streamlit as st
import reveal_slides as rs
from code_editor import code_editor

if 'markdown' not in st.session_state:
    st.session_state.markdown = ""

with st.sidebar:
    list_of_games_in_dir = []
    for file in os.listdir(os.getcwd() + "/games"):
        if file.endswith(".md"):
            list_of_games_in_dir.append(file.removesuffix(".md"))

    option = st.selectbox("Select a game", list_of_games_in_dir)
if option:
    with open("games/" + option + ".md", "r") as f:
        st.session_state.markdown = f.read()

btn_settings_editor_btns = [{
                                "name": "copy",
                                "feather": "Copy",
                                "hasText": True,
                                "alwaysOn": True,
                                "commands": ["copyAll"],
                                "style": {"top": "0rem", "right": "0.4rem"}
                            },
                            {
                                "name": "Save",
                                "feather": "Save",
                                "hasText": True,
                                "commands": [["response","save"]],
                                "style": {"top": "3rem", "right": "0.4rem"}
                            },
                            {
                                "name": "update",
                                "feather": "RefreshCw",
                                "primary": True,
                                "hasText": True,
                                "showWithIcon": True,
                                "commands": ["submit"],
                                "style": {"bottom": "0rem", "right": "0.4rem"}
                            }]

if 'css' not in st.session_state:
    if os.path.isfile(os.getcwd() + "/style.css"):
        st.write("found")
        with open(os.getcwd() + "/style.css", "r") as f:
            st.session_state.css = f.read()
    else:
        st.session_state.css = """
body.reveal-viewport {
    background: #2b09cf;             /*slide background color*/
}
.reveal table {
    background: #1f069d;             /*Jeopardy board background color*/
}
.reveal table thead {                /*top|category row*/
    border: 14px solid #000000;  
}
.reveal table tr {                   /*all rows below top*/
    border: 11px solid #000000; 
}
.reveal table th, .reveal table td { /*every element of table*/
    width: 11rem;
    height: 9.5rem;
    border: 11px solid #000000;
}
.reveal table th {                   /*category element of table*/
    color: white;
    font-weight: bold;
    font-size: 0.6em;
    height: 10rem;
    text-shadow: 4px 4px #000000;
}
.reveal table td {                   /*non-category elements of table*/
    color: #ffc69675;
    font-weight: bold;
    font-size: 1.65em;
}
.reveal table td a {                 /*links in table*/
    text-shadow: 4px 4px #000000;
}
.reveal section > h1 a {             /*header 1 links outside table*/
    font-size: 2.5em; 
}
.reveal section > h2 a {             /*header 2 links outside table*/
    font-size: 1.75em;
}
.reveal section > h3 a {             /*header 3 links outside table*/
    font-size: 1.55em;
}

.reveal table td a.clicked {         /*links in table after clicked*/
    pointer-events: none; 
    cursor: default;
    color: #ffc69675;
    text-shadow: none;
}
"""
with st.expander("Customize"):
    css_response_dict = code_editor(st.session_state.css, lang="css", height=15, buttons=btn_settings_editor_btns, allow_reset=True, key="css_editor")
    if css_response_dict['type'] == "submit" and len(css_response_dict['text']) != 0:
        st.session_state.css = css_response_dict['text']
    if css_response_dict['type'] == "save":
        st.session_state.css = css_response_dict['text']
        with open(os.getcwd() + "/style.css", "w") as f:
            f.write(css_response_dict['text'])

reveal_state = rs.slides(st.session_state.markdown, 
                         height=410,
                         config={
                                 "width": 1800, 
                                 "height": 1000, 
                                 "minScale": 0.1,
                                 "center": True, 
                                 "maxScale": 4, 
                                 "margin": 0.09,
                                 "controls": False,
                                 "history": True,
                                 "plugins": ["markdown", "highlight", "katex", "notes", "search", "zoom"]
                                }, 
                         theme="night",
                         css=st.session_state.css,
                         allow_unsafe_html=True,
                         key="game"
                        )