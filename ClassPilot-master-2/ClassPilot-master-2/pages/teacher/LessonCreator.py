

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import streamlit as st
import reveal_slides as rs  # Import the reveal_slides module
import generalFunctions as gf


# def get_subject_file_paths(subject):
#     base_name = subject.lower().replace(' ', '_')
#     return {
#         'content': DATA_DIR / f"{base_name}_lesson_content.json",
#         'config': DATA_DIR / f"{base_name}_slide_config.json"
#     }
class SlideComponent:
    def __init__(self, content: str, config: dict, initial_state: dict):
        self.content = content
        self.config = config
        self.initial_state = initial_state

    def render(self):
        return rs.slides(
            self.content,
            height=self.config.get('height', '100%'),
            theme=self.config.get('theme', 'black'),
            config=self.config,
            initial_state=self.initial_state,
            markdown_props={"data-separator-vertical": "^--$"},
            key=f"slides_{self.config.get('base_font_size', 24)}_{self.config.get('heading_scale', 1.5)}"
        )


class LessonPresenter:
    def __init__(self, content: dict):
        self.subject = st.session_state.json_content
        self.content = content
        self.callback_func = None  # Callback function placeholder

    def set_subject_content(self, subject: str):
        if subject is None:
            self.subject = {"subject": "Unknown", "lessons": []}
            return
        if subject.lower() == self.subject.get("subject","").lower():
            return
        for s in self.content.get("subjects", []):
            if s.get("subject", "").lower() == subject.lower():
                st.session_state.json_content = s
                st.rerun()

        print(f"Warning: Subject '{subject}' not found in JSON data")
        self.subject = {"subject": "Unknown", "lessons": []}

    def json_to_slides(self) -> str:
        subject_name = self.subject.get('subject', 'Unknown Subject')
        slides = f"# Subject Matter: {subject_name}\nPresentation By ClassPilot\n---\n"
        
        for lesson in self.subject.get("lessons", []):
            slides += f"## {lesson.get('title', 'Untitled Lesson')}\n---\n"
            for page in lesson.get("pages", []):
                slides += f"\n### {page.get('title', 'Untitled Page')}\n"
                for subtitle in page.get("subtitles", []):
                    slides += f"#### {subtitle}\n"
                slides += f"{page.get('content', '')}\n---\n"
        
        if not self.subject.get("lessons"):
            slides += "## No lessons available for this subject\n---\n"
        
        slides += "# End\n## Good Luck!"
        return slides

    def update_page(self, selected_lesson: str, selected_page: str, new_title: str, new_subtitles: str, new_content: str) -> bool:
        lesson_data = next((l for l in self.subject.get("lessons", []) if l["title"] == selected_lesson), None)
        if lesson_data:
            page_data = next((p for p in lesson_data.get("pages", []) if p["title"] == selected_page), None)
            if page_data:
                page_data["title"] = new_title
                page_data["subtitles"] = new_subtitles.split("\n")
                page_data["content"] = new_content
                
                # Save the updated content
                if self.save_content(self.subject):
                #if self.save_content("python"):
                    # Call the callback function if provided
                    if self.callback_func:
                        self.callback_func(self.content)
                    return True
        return False

    def set_callback_func(self, func):
        self.callback_func = func

    def create_slide_component(self, content: str, config: dict, initial_state: dict):
        full_content = self.generate_custom_css(config.get('base_font_size', 24), config.get('heading_scale', 1.5)) + content
        return SlideComponent(full_content, config, initial_state)

    def generate_custom_css(self, base_font_size: int, heading_scale: float) -> str:
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
        .reveal p, .reveal li {{ font-size: {base_font_size}px !important; }}

        .reveal pre {{
            background: #050505;
            border: 1px solid #ddd;
            border-left: 3px solid #f36d33;
            color: #999;
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
            margin: 15px 0 !important;
            padding: 10px !important;
            border-radius: 5px !important;
        }}
        .reveal pre code {{
            max-height: 400px !important;
            font-size: {base_font_size * 0.7}px !important;
            line-height: 1.3em !important;
            padding: 0 !important;
        }}
        .hljs {{ background: transparent !important; }}
        .reveal.white pre, .reveal.beige pre {{ background-color: rgba(0,0,0,0.05) !important; }}
        .reveal.white pre code, .reveal.beige pre code {{ color: #333 !important; }}
        .reveal.black pre, .reveal.league pre, .reveal.night pre {{ background-color: rgba(255,255,255,0.1) !important; }}
        .reveal.black pre code, .reveal.league pre code, .reveal.night pre code {{ color: #f0f0f0 !important; }}
        </style>
        """
    def save_content(self,subject_content):

        json_path = gf.MAIN_DATA_PATH+gf.LESSON_CONTENT_PATH
        try:
            content = gf.get_data_from_path(json_path)
            for i in range(len(content["subjects"])):
                if content["subjects"][i].get("subject") == subject_content.get("subject"):
                    content["subjects"][i] = subject_content
                    break
            gf.save_json(content,json_path)
            st.success("Content saved successfully")
            return True
        except Exception as e:
            st.error(f"Error saving content: {str(e)}")
            return False


def load_content():

    json_path = gf.MAIN_DATA_PATH+gf.LESSON_CONTENT_PATH
    try:
        content = gf.get_data_from_path(json_path)
        print("JSON file loaded successfully in load_content")
    except FileNotFoundError:
        print(f"Error: Could not find the file at {json_path}")
        content = {"subjects": []}
    except json.JSONDecodeError:
        print(f"Error: The file at {json_path} is not a valid JSON file")
        content = {"subjects": []}

    return content

def save_config(config,subject_name):
    config_data = {
        "subject":subject_name,
        "config": config,
    }

    config_path = gf.MAIN_DATA_PATH+gf.SLIDE_CONFIG_PATH
    all_config_data = gf.get_data_from_path(config_path)
    if all_config_data != {}:
        new_config = True
        for i in range(len(all_config_data["subjects"])):
            if all_config_data["subjects"][i].get("subject") == config_data.get("subject"):
                all_config_data["subjects"][i] = config_data
                new_config = False
                break
        if new_config:
            all_config_data["subjects"].append(config_data)
    
        gf.save_json(all_config_data,config_path)
        st.success("Config Saved")
    else:
        st.error("Config didn't saved")

def create_editor_screen(presenter: LessonPresenter):
    st.title("Lesson Presentation System")
    subjects = [s["subject"] for s in presenter.content["subjects"]]
    selected_subject = st.sidebar.selectbox("Select Subject", subjects,None)
    if selected_subject:
        presenter.set_subject_content(selected_subject)
    else:
        presenter.set_subject_content(st.session_state.json_content.get("subject",""))
    with st.expander("Edit Page Content", expanded=False):
        lessons = [l["title"] for l in presenter.subject.get("lessons", [])]
        selected_lesson = st.selectbox("Select Lesson", lessons)
        selected_lesson_data = next((l for l in presenter.subject.get("lessons", []) if l["title"] == selected_lesson), None)

        if selected_lesson_data:
            pages = [p["title"] for p in selected_lesson_data.get("pages", [])]
            selected_page = st.selectbox("Select Page", pages)
            selected_page_data = next((p for p in selected_lesson_data.get("pages", []) if p["title"] == selected_page), None)

            if selected_page_data:
                new_title = st.text_input("Edit Page Title", selected_page_data["title"])
                new_subtitles = st.text_area("Edit Subtitles (one per line)", "\n".join(selected_page_data.get("subtitles", [])))
                new_content = st.text_area("Edit Page Content", selected_page_data["content"], height=300)
                
                if st.button("Update Page"):
                    if presenter.update_page(selected_lesson, selected_page, new_title, new_subtitles, new_content):
                        st.success("Page updated and saved successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update and save page. Please check your input.")

    st.sidebar.header("Slide Design")
    config = {
        "base_font_size": st.sidebar.number_input("Base Font Size (px)", value=24, min_value=10, max_value=50, step=1),
        "heading_scale": st.sidebar.slider("Heading Scale", min_value=1.0, max_value=3.0, value=1.5, step=0.1),
        "theme": st.sidebar.selectbox("Theme", ["black", "white", "league", "beige", "sky", "night", "serif", "simple", "solarized"], index=0),
        "height": st.sidebar.number_input("Container Height", value=600, step=50),
        "scrollable": True,
    }
    if st.sidebar.button("Finish"):
        save_config(config,presenter.subject.get("subject",""))
        presenter.save_content(presenter.subject)
        st.sidebar.success("Configuration saved successfully!")
        st.rerun()
    if st.button("Return to Main Page"):
        st.session_state.current_page = "home"
        st.rerun()

    slides_component = presenter.create_slide_component(presenter.json_to_slides(), config, initial_state={})
    slides_component.render()
    


class LessonContentGenerator:
    def __init__(self, api_key):
        self.llm = ChatGroq(api_key=api_key)

    def generate_content(self, subject, num_lessons, pages_per_lesson, subtitles_per_page, sentences_per_page):
        prompt_template = PromptTemplate(
            input_variables=["subject", "num_lessons", "pages_per_lesson", "subtitles_per_page", "sentences_per_page"],
            template="""
            Create a detailed lesson plan on the subject of {subject}. 
            Provide EXACTLY the following:
            1. {num_lessons} lesson titles
            2. For each lesson, EXACTLY {pages_per_lesson} page titles
            3. For each page, EXACTLY {subtitles_per_page} subtitles
            4. For each page, a content summary of EXACTLY {sentences_per_page} sentences

            Format your response as a JSON structure with the following format:
            {{
            "subject": "{subject}",
            "lessons": [
                {{
                    "title": "Lesson Title",
                    "pages": [
                        {{
                            "title": "Page Title",
                            "subtitles": ["Subtitle 1", "Subtitle 2", ...],
                            "content": "Detailed content for the page (EXACTLY {sentences_per_page} sentences)"
                        }},
                        ...
                    ]
                }},
                ...
            ]
            }}

            Ensure the content is informative, relevant to the subject of {subject}, and follows this exact JSON structure. 
            Do not use any backslashes in the JSON keys.
            IMPORTANT: Strictly adhere to the numbers provided: {num_lessons} lessons, {pages_per_lesson} pages per lesson, {subtitles_per_page} subtitles per page, and {sentences_per_page} sentences per page.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        result = chain.invoke({
            "subject": subject,
            "num_lessons": num_lessons,
            "pages_per_lesson": pages_per_lesson,
            "subtitles_per_page": subtitles_per_page,
            "sentences_per_page": sentences_per_page
        })
        
        return self._process_content(result['text'], subject, num_lessons, pages_per_lesson, subtitles_per_page, sentences_per_page)

    def _process_content(self, content, subject, num_lessons, pages_per_lesson, subtitles_per_page, sentences_per_page):
        try:
            content = json.loads(content)
            processed_content = {
                "subject": subject,
                "lessons": []
            }
            
            for i in range(num_lessons):
                lesson = content['lessons'][i] if i < len(content['lessons']) else {"title": f"Lesson {i+1}", "pages": []}
                processed_lesson = {
                    "title": lesson['title'],
                    "pages": []
                }
                
                for j in range(pages_per_lesson):
                    page = lesson['pages'][j] if j < len(lesson.get('pages', [])) else {"title": f"Page {j+1}", "subtitles": [], "content": ""}
                    processed_page = {
                        "title": page['title'],
                        "subtitles": page.get('subtitles', [])[:subtitles_per_page],
                        "content": '. '.join(page.get('content', '').split('.')[:sentences_per_page]) + '.'
                    }
                    
                    while len(processed_page['subtitles']) < subtitles_per_page:
                        processed_page['subtitles'].append(f"Subtitle {len(processed_page['subtitles'])+1}")
                    
                    processed_lesson['pages'].append(processed_page)
                
                processed_content['lessons'].append(processed_lesson)
            
            return json.dumps(processed_content, indent=2)
        except json.JSONDecodeError:
            raise ValueError("The generated content is not valid JSON.")
        except Exception as e:
            raise Exception(f"An error occurred while processing the content: {str(e)}")

class ContentEditor:
    def __init__(self, llm):
        self.llm = llm

    def expand_content(self, subtitle, page_title, content):
        prompt = PromptTemplate(
            input_variables=["subtitle", "page_title", "content"],
            template="Expand on '{subtitle}' in the context of {page_title}. Original content: {content}"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        expanded_content = chain.invoke({
            "subtitle": subtitle,
            "page_title": page_title,
            "content": content
        })
        return expanded_content['text']

    def summarize_content(self, page_title, summary_length, content):
        prompt = PromptTemplate(
            input_variables=["page_title", "summary_length", "content"],
            template="Summarize the content about {page_title} in a {summary_length} summary. Original content: {content}"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        summarized_content = chain.invoke({
            "page_title": page_title,
            "summary_length": summary_length.lower(),
            "content": content
        })
        return summarized_content['text']

class App:
    def __init__(self):

        api_key = get_key()
        self.generator = LessonContentGenerator(api_key)
        self.editor = ContentEditor(ChatGroq(api_key=api_key))
        self.lessonPresentor = None
    def run(self):
        
        if st.session_state.current_page == "home":
            self._show_home_page()
        elif st.session_state.current_page == "edit":
            content = load_content() # need to reload content after making new content
            self.lessonPresentor = LessonPresenter(content)
            create_editor_screen(self.lessonPresentor)
        else:
            self._show_editor_page()

    def _show_home_page(self):
        st.title("Home Page")
        st.write("Welcome to the Interactive Lesson Content Editor!")
        
        if st.button("Create New Lesson Content"):
            st.session_state.current_page = "editor"
            st.session_state.content_generated = False
            st.session_state.json_content = {"subject": "", "lessons": []}
            st.rerun()
        
        # Display saved lesson contents
        with open("utils/data/lesson_content.json",'r') as f:
            saved_subjects = json.load(f)["subjects"]

        col1, col2 = st.columns([2,5])
        with col1:
            for subject in saved_subjects: #subject in saved_subjects:
                if st.button(f"Edit {subject['subject'].capitalize()}",key=subject["subject"]+"edit"):
                    st.session_state.json_content = subject
                    st.session_state.content_generated = True
                    st.session_state.current_page = "editor"
                    st.rerun()
        with col2:
            for subject in saved_subjects: #subject in saved_subjects:
                if gf.check_subject_ready(subject):
                    if st.button(f"Present Lesson {subject['subject']}",key=subject["subject"]):
                        st.session_state.subject_content = subject["subject"]
                        st.switch_page("pages/teacher/TeacherLessonPresenter.py")
                else:
                    st.write("###")
    def _show_editor_page(self):
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h1 style="margin: 0;">Interactive Lesson Content Editor</h1>
            <div id="restart-button-container"></div>
        </div>
        """, unsafe_allow_html=True)

        if 'json_content' not in st.session_state:
            st.session_state.json_content = {"subject": "", "lessons": []}
        if 'content_generated' not in st.session_state:
            st.session_state.content_generated = False

        if st.session_state.content_generated:
            self._show_restart_button()
            self._handle_content_editing()
        else:
            self._handle_content_generation()

    def _show_restart_button(self):
        if st.button("Restart and select a new subject"):
            temp_role = st.session_state.role
            st.session_state.clear()
            st.session_state.role = temp_role
            st.rerun()

    def _handle_content_generation(self):
        subject = st.text_input("Enter the subject for the lesson content:")
        col1, col2 = st.columns(2)
        with col1:
            num_lessons = st.number_input("Number of lesson titles:", min_value=1, value=2, step=1)
            pages_per_lesson = st.number_input("Pages per lesson:", min_value=1, value=2, step=1)
        with col2:
            subtitles_per_page = st.number_input("Subtitles per page:", min_value=1, value=3, step=1)
            sentences_per_page = st.number_input("Sentences per page:", min_value=1, value=3, step=1)
        col11, col12 = st.columns([1,5])
        with col11:
            if st.button("Back to Home Page"):
                st.session_state.current_page = "home"
                st.rerun()
        with col12:
            if subject and subject != st.session_state.json_content.get("subject", ""):
                if st.button("Generate Content"):
                    with st.spinner("Generating lesson content..."):
                        try:
                            generated_content = self.generator.generate_content(
                                subject, num_lessons, pages_per_lesson, subtitles_per_page, sentences_per_page
                            )
                            st.session_state.json_content = json.loads(generated_content)
                            st.session_state.content_generated = True
                            st.success("Lesson content generated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}. Please try again.")

    def _handle_content_editing(self):
        if not st.session_state.json_content.get("lessons"):
            st.warning("No lessons available. Please generate content first.")
            return

        st.header("Lesson Content Editor")
        _, _, page_title, page = self._select_lesson_and_page()

        st.subheader(f"📝 Content: {page_title}")
        with st.expander("View original content", expanded=True):
            st.write(page.get("content", "No content available."))

        with st.expander("View subtitles"):
            for subtitle in page.get("subtitles", []):
                st.write(f"• {subtitle}")

        st.subheader("🛠️ Edit Content")
        action = st.radio("What would you like to do with the content?", ["Accept", "Expand", "Summarize"])

        if action == "Accept":
            st.success("Content accepted without changes.")
        elif action == "Expand":
            self._handle_expand_action(page, page_title)
        elif action == "Summarize":
            self._handle_summarize_action(page, page_title)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Changes"):
                self._save_changes()
        with col2:
            if st.button("Next Step"):
                self._save_changes()
                st.session_state.current_page = "edit"
                st.rerun()

    def _select_lesson_and_page(self):
        col1, col2 = st.columns([1,4])
        with col1:
            lesson_titles = [lesson.get("title", f"Lesson {i+1}") for i, lesson in enumerate(st.session_state.json_content["lessons"])]
            lesson_title = st.selectbox("📚 Select a lesson", lesson_titles)
            lesson_index = lesson_titles.index(lesson_title)
            lesson = st.session_state.json_content["lessons"][lesson_index]

        with col2:
            if not lesson.get("pages"):
                st.warning(f"No pages available for lesson: {lesson_title}")
                return None, None, None, None

            page_titles = [page.get("title", f"Page {i+1}") for i, page in enumerate(lesson["pages"])]
            page_title = st.selectbox("📄 Select a page", page_titles)
            page_index = page_titles.index(page_title)
            page = lesson["pages"][page_index]

        return lesson_title, lesson, page_title, page

    def _handle_expand_action(self, page, page_title):
        subtitles = page.get("subtitles", [])
        if subtitles:
            subtitle = st.selectbox("Select a subtitle to expand", subtitles)
            if st.button("Expand Content"):
                with st.spinner("Expanding content..."):
                    expanded_content = self.editor.expand_content(subtitle, page_title, page.get("content", ""))
                    st.subheader("Expanded Content")
                    st.write(expanded_content)
                    page["content"] = expanded_content
                    st.success("Content expanded successfully!")
        else:
            st.warning("No subtitles available for expansion.")

    def _handle_summarize_action(self, page, page_title):
        summary_length = st.select_slider("Select summary length", options=["Short", "Medium", "Long"])
        if st.button("Summarize Content"):
            with st.spinner("Summarizing content..."):
                summarized_content = self.editor.summarize_content(page_title, summary_length, page.get("content", ""))
                st.subheader("Summarized Content")
                st.write(summarized_content)
                page["content"] = summarized_content
                st.success("Content summarized successfully!")

    def _save_changes(self):
        try:
            with open("utils/data/lesson_content.json",'r') as file:
                content_lessons = json.load(file)
        except FileNotFoundError:
            print(FileNotFoundError)
        new_lesson = True
        for i in range(len(content_lessons["subjects"])):
            if content_lessons["subjects"][i].get("subject") == st.session_state.json_content["subject"]:
                content_lessons["subjects"][i] = st.session_state.json_content
                new_lesson = False
                break
        if new_lesson:
            content_lessons["subjects"].append(st.session_state.json_content)
        with open("utils/data/lesson_content.json",'w') as file:
            json.dump(content_lessons,file,indent=2)

        # filename = f'{st.session_state.json_content["subject"].replace(" ", "_").lower()}_lesson_content.json'
        # with open(filename, 'w') as f:
        #     json.dump(st.session_state.json_content, f, indent=2)
        st.success(f"Changes saved successfully!")


if __name__ == "__main__":
    api_key = ""
    
    #debug
    app = App()
    app.run()
def get_key():
    with open("utils/data/secret_keys.json") as key_file:
        keys = json.load(key_file)
        for key in keys["Keys"]:
            if key["Api Name"] == "ChatGroq":
                return  key["Key"]


app = App()
if st.session_state.role in ["Teacher","Admin"]:
    app.run()

# def run():
#     app.run()