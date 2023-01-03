import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
from io import StringIO
import re
#import PyPDF2
import pdfminer
from pdfminer.high_level import extract_pages
# Replace YOUR_API_KEY with your actual API key
openai.api_key = st.secrets["api_key"]
from st_pages import Page, show_pages, add_page_title
from streamlit.components.v1 import html

st.sidebar.image: st.sidebar.image("SkipText Offiical Logo.png", use_column_width=True)
add_page_title("Play Ground")

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)


@st.cache(suppress_st_warning=True)
def summarize_text(text):
    """Summarizes the given text using GPT-3."""
    #st.write("Summarizing the text ...")
    # Set up the GPT-3 request
    prompt = (
        f"Summarize the following text:\n{text}\n"
        "The summary should be no more than three paragraphs long."
    )
    model = "text-davinci-003"  # You can choose a different GPT-3 model if you prefer
    temperature = 0.5  # Adjust the temperature to control the creativity of the summary
    max_tokens = 128  # Limit the length of the summary to 128 tokens

    # Send the request to GPT-3 and get the summary
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
    summary = response["choices"][0]["text"]
    return summary

#@st.cache(suppress_st_warning=True)
def recurisive_summarization(text_1lakh):
    if len(text_1lakh)< 8000:
        return summarize_text(text_1lakh)
    else:
        return recurisive_summarization(summarize_text(text_1lakh[0:8000]) + "\n "+ text_1lakh[8000:])


@st.cache(suppress_st_warning=True)
def outline_text(text):
    """Creates an outline of the given text using GPT-3."""
    # Set up the GPT-3 request
    #st.write("Outlining the text ...")
    prompt = (
        f"Outline the following text:\n{text}\n"
        "The outline should contain no more than Ten main points, with each point described in one sentence."
    )
    model = "text-davinci-003" # You can choose a different GPT-3 model if you prefer
    temperature = 0.5  # Adjust the temperature to control the creativity of the outline
    max_tokens = 256  # Limit the length of the outline to 256 tokens

    # Send the request to GPT-3 and get the outline
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
    outline = response["choices"][0]["text"]
    return outline

#@st.cache(suppress_st_warning=True)
def recurisive_outline(text_1lakh):
    if len(text_1lakh)< 8000:
        return outline_text(text_1lakh)
    else:
        return recurisive_outline(outline_text(text_1lakh[0:8000]) + "\n "+ text_1lakh[8000:])


@st.cache(suppress_st_warning=True)
def summarize_website(url):
    """Summarizes the content of the given website using GPT-3."""
    # Retrieve the content of the website
    response = requests.get(url)
    html = response.text

    # Extract the main content of the website using a library like BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    text = soup.text
    text = re.sub(r'(\n)+', '\n', text)
    #text = text[0:8000]
    summary = recurisive_summarization(text)
    return summary

@st.cache(suppress_st_warning=True)
def outline_website(url):
    """Summarizes the content of the given website using GPT-3."""
    # Retrieve the content of the website
    response = requests.get(url)
    html = response.text

    # Extract the main content of the website using a library like BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    #main_content = soup.find("div", {"id": "main-content"})
    text = soup.text
    #text = text[0:8000]

    # Use the summarize_text function from the previous example to summarize the text
    outline = recurisive_outline(text)
    return outline


@st.cache(suppress_st_warning=True)
def input_data(data_file):
    ''' This function for taking two excel sheets as input'''
    st.write("Reading data from the file ....")
    file = open(data_file,"r")
    content = file1.read()
    file.close()
    return content
    # try:
    # 	data_df = pd.read_excel(data_file)
    # except ValueError:
    # 	st.write("Valuer error occured, Reading file as a csv")
    # 	data_df = pd.read_csv(data_file)
    # return data_df

if st.session_state["input_type"] == "Enter Text":
    txt = st.text_area('Enter Text here',value ='''''', height = 300)
    with st.form("form3"):
    	submit = st.form_submit_button(label = 'Submit')
    if submit:
        if st.session_state["task_type"] == "Summarize Text":
            summary = recurisive_summarization(txt)
            st.write("SUMMARY:")
            st.write(summary)
        elif st.session_state["task_type"] == "Outline Text":
            outline = recurisive_outline(txt)
            st.write("OUTLINE:")
            st.write(outline)

elif st.session_state["input_type"]  == "Upload File":
    data_file = st.file_uploader("Choose a file .txt file from your system ...")
    if data_file is not None:
        name = data_file.name
        extension = name.split(".")[1]
    if data_file is not None and extension == "txt":
        stringio = StringIO(data_file.getvalue().decode("utf-8"))
        txt = stringio.read()
        #st.write(string_data)
        if st.session_state["task_type"] == "Summarize Text":
            summary = recurisive_summarization(txt)
            st.write("SUMMARY:")
            st.write(summary)
        elif st.session_state["task_type"] == "Outline Text":
            outline = recurisive_outline(txt)
            st.write("OUTLINE:")
            st.write(outline)

    if data_file is not None and extension == "pdf":
        pages_lst = []
        for page_layout in extract_pages(data_file):
            page = ""
            for element in page_layout:
                page = page + str(element)
            pages_lst.append(page)
        txt = "\n".join(pages_lst)

        if st.session_state["task_type"] == "Summarize Text":
            summary = recurisive_summarization(txt)
            st.write("SUMMARY:")
            st.write(summary)
        elif st.session_state["task_type"] == "Outline Text":
            outline = recurisive_outline(txt)
            st.write("OUTLINE:")
            st.write(outline)

elif st.session_state["input_type"] == "Enter website URL":
    url = st.text_input("Enter URL here... ")
    with st.form("form4"):
    	submit = st.form_submit_button(label = 'Submit')
    if submit:
        if st.session_state["task_type"] == "Summarize Text":
            summary = summarize_website(url)
            st.write("SUMMARY:")
            st.write(summary)
        elif st.session_state["task_type"] == "Outline Text":
            outline = outline_website(url)
            st.write("OUTLINE:")
            st.write(outline)

with st.form("form"):
	prev_page = st.form_submit_button(label = 'Go Back')
if prev_page:
    nav_page("Task%20Selection%20Page")
