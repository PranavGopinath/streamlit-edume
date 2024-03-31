import streamlit as st
import os

st.title('📚🌐EduMe.ai')
st.write('Hello, welcome to EduMe.ai a personalized learning journey designed for learners with disabilities, making education accessible, engaging, and effective. To get started, please answer the following questions!')

st.markdown("___")
st.subheader('📝Diagnostic Quiz:')
name = st.text_input("What is your name?")
age = st.text_input("How old are you?")


learningCategory = ""
disability = ""

# Questions list
questions_list = [
    "Which learning style works best for you?",
    "Which type of content do you find most accessible or engaging?",
    "Do you prefer interactive learning materials (e.g., quizzes, simulations, interactive exercises) or more traditional formats (e.g., textbooks, lectures)?",
    "Amongst the following learning strategies or techniques, which do you find particularly effective for retaining information?",
    "When learning new concepts, do you prefer step-by-step instructions, visual diagrams, or verbal explanations?",
    "How do you prefer to organize and review study materials?"
]

# Answers list
answers_list = [
    ["a) visual", "b) auditory", "c) kinesthetic"],
    ["a) text", "b) audio", "c) video"],
    ["a) both", "b) traditional methods", "c) interactive learning materials"],
    ["a) active recall", "b) practice testing", "c) multi-sensory learning"],
    ["a) visual diagrams", "b) verbal explanations", "c) step-by-step instructions"],
    ["a) written notes", "b) verbal repetition", "c) digital flashcards"],
]

responses = []

# Iterate through each question and its corresponding answers
for question, answers in zip(questions_list, answers_list):
    # Display the question and dropdown for answers
    # Prepend choices with an unselectable default option
    response = st.selectbox(question, ['Select an option'] + answers, format_func=lambda x: x.split(')')[1].strip() if x != 'Select an option' else x)
    responses.append(response)

# Button to submit the responses
if st.button('Submit'):
    score_counter = 0
    for response in responses:
        if response.startswith('a'):
            score_counter += 1
        elif response.startswith('b'):
            score_counter += 2
        elif response.startswith('c'):
            score_counter += 3
    # Determine the learning category
    learningCategory = ""
    if 5 <= score_counter < 9:
        learningCategory = "cat1"
    elif 9 <= score_counter < 13:
        learningCategory = "cat2"
    elif 13 <= score_counter <= 18:
        learningCategory = "cat3"
    
# Display the score and category
if (learningCategory == "cat1"):
    disability = "auditory processing disorder (APD), Non verbal learning disabilities(NVLD"
elif (learningCategory == "cat2"):
    disability = "dysgraphia or visual motor deficit"
elif (learningCategory == "cat3"):
    disability = "ADHD or dyslexia"

st.markdown("___")
st.subheader('💡Results:')
st.write(f"You may be affected by qualities similar to those experiencing {disability}")

##############################################################################################
from openai import OpenAI

client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'))

messages = []
system_msg = f"You are a special needs tutor teaching {name} who is {age} years old. They have trouble learning the conventional way and have {disability}. They need you, a special tutor, to help them with their learning."
messages.append({"role": "system", "content": system_msg})
message =  f"Provide a percentage split of how much of their learning should be text, and how much should be video based on their {disability}.Provide in the format (percentage of video) and (percentage of text) on the next line. Do not provide any other information Only display the two percentages without the percent sign on two separate lines (just numbers and no text)."
messages.append({"role": "user", "content": message})
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=messages)
content = response.choices[0].message.content

video = 0
text = 0

lines = content.split('\n')

video = (int(lines[0]))/10
text = (int(lines[1]))/10

if text == 0:
    text = 1

from googleapiclient.discovery import build

content = st.text_input("What would you like to learn today?")

st.write("We believe that the following breakdown of educational content would help you learn best: \n\n")


api_key = 'AIzaSyAhVyAGLIpRWjkKO_wdXHuLrXULzNK_bqc'
youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.search().list(
    part="snippet",
    q=content,  
    maxResults= video,
    type="video"
)

response = request.execute()


for item in response['items']:
    title = item['snippet']['title']
    video_id = item['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    thumbnail_url = item['snippet']['thumbnails']['high']['url']
    
    st.markdown("___")
    st.subheader("▶️ Video Resources:")
    st.write(f"Title: {title}")
    st.write(f"Video URL: {video_url}") 
    st.write("\n")

sentences = text*3

message =  f"Provide a description to the person that is easy to understand and takes into account their {disability}. Make sure to explain the concept in a way that they can understand. Make the description of {content} only {sentences} number of sentences."
messages.append({"role": "user", "content": message})
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=messages)
content = response.choices[0].message.content

st.markdown("___")
st.subheader("✍️Written Resources:")
st.write(content)
st.write("Thank you for using our services. We hope we were of assistance of you today!")