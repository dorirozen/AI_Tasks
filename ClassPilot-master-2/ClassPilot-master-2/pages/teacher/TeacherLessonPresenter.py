import streamlit as st
import reveal_slides as rs
import json
from utils.Prompts import prompts
import generalFunctions as gf



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

def get_subject_config():

    subjects = gf.get_data_from_path(gf.MAIN_DATA_PATH+gf.SLIDE_CONFIG_PATH)
    for subject in subjects["subjects"]:
        if subject["subject"] == st.session_state.subject_content:
            return subject["config"]


st.header("Lesson Presenter")
if st.session_state.subject_content == "":
    st.error("No lesson was chosen, please go back to main page")
    st.stop()

def generate_custom_css(base_font_size: int, heading_scale: float) -> str:
        return f"""
        <style>
        .reveal .slides section {{
            height: 100%;
            overflow-y: auto !important;
            overflow-x: hidden !important;
        }}
        .reveal {{
            height: 100% !important;
            font-size: {base_font_size}px !important;
        }}
        .reveal .slides {{
            height: 100% !important;
        }}
        .reveal h1 {{ font-size: {base_font_size * heading_scale}px !important; }}
        .reveal h2 {{ font-size: {base_font_size * (heading_scale * 0.9)}px !important; }}
        .reveal h3 {{ font-size: {base_font_size * (heading_scale * 0.8)}px !important; }}
        .reveal p, .reveal li {{
            font-size: {base_font_size}px !important; 
            color: #000;
        }}
        .reveal .slides section {{ color: #f0f0f0 !important; }}
        .reveal pre {{
            background: #f4f4f4;
            border: 1px solid #ddd;
            border-left: 3px solid #f36d33;
            color: #666;
            page-break-inside: avoid;
            font-family: monospace;
            font-size: 15px;
            line-height: 1.6;
            margin-bottom: 1.6em;
            max-width: 100%;
            overflow: auto;
            padding: 1em 1.5em;
            display: block;
            word-wrap: break-word;
        }}
        .reveal pre code {{
            max-height: 400px !important;
            font-size: {base_font_size * 0.7}px !important;
            line-height: 1.3em !important;
            padding: 0 !important;
        }}
        .reveal.white pre, .reveal.beige pre {{ background-color: rgba(0,0,0,0.05) !important; }}
        .reveal.white pre code, .reveal.beige pre code {{ color: #333 !important; }}
        .reveal.black pre, .reveal.league pre, .reveal.night pre {{ background-color: rgba(255,255,255,0.1) !important; }}
        .reveal.black pre code, .reveal.league pre code, .reveal.night pre code {{ color: #f0f0f0 !important; }}
        </style>
        """

content = gf.get_data_from_path(gf.MAIN_DATA_PATH+gf.LESSON_CONTENT_PATH)
subject = set_subject_content(content)
sample_markdown = json_to_slides(subject)


config = get_subject_config()
sample_markdown = generate_custom_css(config.get("base_font_size",24),config.get("heading_scale",1.5)) + sample_markdown
currState = rs.slides(sample_markdown,
                      height=config["height"],
                      theme=config["theme"],  # color and font style of text
                      config={
                          # add the css cutsom font size
                          "center": True
                      },
                      markdown_props={"data-separator-vertical": "^--$"},
                      key="foo")


def main():
    pass


if __name__ == "__main__":
    main()
