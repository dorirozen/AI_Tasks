import streamlit as st
import reveal_slides as rs
import json
from utils.Prompts import prompts

if "subject_content" not in st.session_state:
    st.session_state.subject_content = "Python"

st.header("Lesson Presenter")
st.write(f"You are logged in as {st.session_state.role}.")

# NOTES FOR Reveal_Slides syntex
# For making new slides, at the end of some string,
# horizontal slide (left,right), input ---, for a vertical slide (up,down), input --
# For making slide progress the text,
# input at end of string <!-- .element: class="fragment" data-fragment-index="<some number, start from 0>" -->
# For highlight text, input before text ##
# For linking a website link, [chosen string](url link)
# For changing background,input at start of string of slide <!-- .slide: data-background-color="#COLORCODE" -->
def json_to_slides(json_file):
    sample_text = ""
    sample_text = sample_text + f"# Subject Matter: {json_file['subject']}" + '\n' + "Presentation By ClassPilot \n---\n"
    for lesson in json_file["lessons"]:
        sample_text = sample_text + f"## {lesson['title']}" + "\n---\n"
        for page in lesson["pages"]:
            sample_text = sample_text + "\n" + f"### {page['title']}" + "\n" + f"{page['content']}" + "\n---\n"

    sample_text = sample_text + "# End \n ## Good Luck!"

    return sample_text



def set_subject_content(subjects):
    if "subject_content" in st.session_state:
        for subject in subjects["subjects"]:
            if subject["subject"] == st.session_state.subject_content:
                return subject


with open("utils/data/lesson_content.json") as f:
    content = json.load(f)
    subject = set_subject_content(content)
    sample_markdown = json_to_slides(subject)

with st.sidebar:
    st.header("Component Parameters")
    theme = st.selectbox("Theme",
                         ["black", "black-contrast", "blood", "dracula", "moon", "white", "white-contrast", "league",
                          "beige", "sky", "night", "serif", "simple", "solarized"])
    height = st.number_input("Height", value=500, step=10)
    st.subheader("Slide Configuration")
    content_height = st.number_input("Content Height", value=900, step=10)
    content_width = st.number_input("Content Width", value=900, step=10)
    scale_range = st.slider("Scale Range", min_value=0.0, max_value=5.0, value=[0.1, 3.0], step=0.1)
    margin = st.slider("Margin", min_value=0.0, max_value=0.8, value=0.1, step=0.05)
    plugins = st.multiselect("Plugins", ["highlight", "katex", "mathjax2", "mathjax3", "notes", "search", "zoom"], [])
    st.subheader("Initial State")
    hslidePos = st.number_input("Horizontal Slide Position", value=0)
    vslidePos = st.number_input("Vertical Slide Position", value=0)
    fragPos = st.number_input("Fragment Position", value=-1)
    overview = st.checkbox("Show Overview", value=False)
    paused = st.checkbox("Pause", value=False)

currState = rs.slides(sample_markdown,
                      height=height,
                      theme=theme,  # color and font style of text
                      config={
                          "width": content_width,
                          "height": content_height,
                          "minScale": scale_range[0],
                          "center": True,
                          "maxScale": scale_range[1],
                          "margin": margin,
                          "plugins": plugins
                      },
                      initial_state={
                          "indexh": hslidePos,
                          "indexv": vslidePos,
                          "indexf": fragPos,
                          "paused": paused,
                          "overview": overview
                      },
                      markdown_props={"data-separator-vertical": "^--$"},
                      key="foo")


def main():
    pass


if __name__ == "__main__":
    main()
