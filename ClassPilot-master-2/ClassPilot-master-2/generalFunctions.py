import json

MAIN_DATA_PATH = "utils/data/"
STUDENT_DATA_PATH = "student_data.json"
LESSON_CONTENT_PATH = "lesson_content.json"
SECRET_KEYS = "secret_keys.json"
USERS_PATH = "users.json"
SLIDE_CONFIG_PATH = "slide_config.json"



def get_data_from_path(path):

    with open(path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def get_finished_subjects(filter=None):
    f_data = open(MAIN_DATA_PATH+LESSON_CONTENT_PATH)
    f_config = open(MAIN_DATA_PATH+SLIDE_CONFIG_PATH)
    lesson_data = json.load(f_data)
    config = json.load(f_config)
    ready_subjects = {"subjects":[]}
    for subject in lesson_data["subjects"]:
        for config_subject in config["subjects"]:
            if subject["subject"] == config_subject["subject"]:
                ready_subjects["subjects"].append(subject)
                break

    return ready_subjects
def check_subject_ready(subject_content) -> bool:
    with open("utils/data/slide_config.json", 'r') as f:
        ready_subjects = json.load(f)["subjects"]
    for subject in ready_subjects:
        if subject["subject"] == subject_content["subject"]:
            return True
    return False