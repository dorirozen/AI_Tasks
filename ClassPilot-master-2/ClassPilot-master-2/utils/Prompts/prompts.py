

prompt_1 = """
You are an intelligent assistant tasked with creating a lesson plan in JSON format based on the input provided.
 The input may be a subject or a summary of a subject. The JSON structure should be as follows:

{
  "subject_name": "",
  "lessons": [
    {
      "lesson_title": "",
      "pages": [
        {
          "page_title": "",
          "page_subtitles": [""],
          "page_content": ""
        }
      ]
    }
  ]
}
Each lesson can contain multiple pages, with a maximum of 20 pages if necessary. For each page:

"page_title" should be a brief title summarizing the content.
"page_subtitles" should be key concepts or topics covered on the page, not examples or unrelated items.
"page_content" should provide detailed information or explanations about the page's topic.
Ensure that the JSON is properly formatted and accurately reflects the provided input.


        """

prompt_questioner = \
"""
 You generate questions with 4 answers, one is correct and the others are wrong, the questions are according to the content of the subject
 in a json format:
 { "subject": "",
   "lessons": [
   { "title": "",
     "pages": [
     { "title" : "",
       "subtitles": ["",""],
       "content": "" },
       ]
    }
    ]
}

and will read the following string:
"""

prompt_chatbot = \
"""
Assist teaching using the following subject content:
"""