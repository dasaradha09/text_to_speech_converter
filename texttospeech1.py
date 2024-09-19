import streamlit as st
from gtts import gTTS
import PyPDF2
import docx
import os

# Function to extract text from PDF
import PyPDF2

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:  # Use reader.pages instead of using numPages
        text += page.extract_text() or ""  # Handle the case where extract_text() might return None
    return text


# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Function to convert text to speech
def text_to_speech(text, language, filename="output.mp3"):
    tts = gTTS(text=text, lang=language)
    tts.save(filename)
    return filename

# List of supported languages
LANGUAGES = {
    "English": "en",
    "Afrikaans": "af",
    "Arabic": "ar",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Catalan": "ca",
    "Czech": "cs",
    "Welsh": "cy",
    "Danish": "da",
    "German": "de",
    "Greek": "el",
    "Spanish": "es",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Gujarati": "gu",
    "Hebrew": "he",
    "Hindi": "hi",
    "Croatian": "hr",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Icelandic": "is",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Korean": "ko",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Malay": "ms",
    "Malayalam": "ml",
    "Nepali": "ne",
    "Dutch": "nl",
    "Norwegian": "no",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Zulu": "zu"
}

# Streamlit app
st.title("Text to Speech Converter")

# Text area for text input
text_input = st.text_area("Enter text here or else upload file below:")

# File uploader for DOCX and PDF
uploaded_file = st.file_uploader("Upload a DOCX or PDF file", type=["pdf", "docx"])

# Select box for language selection
language = st.selectbox("Select Language", list(LANGUAGES.keys()))

# Generate button
if st.button("Generate"):
    if text_input:
        text = text_input
    elif uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Please enter text or upload a file.")
        st.stop()

    # Convert text to speech
    audio_file = text_to_speech(text, LANGUAGES[language])

    # Display audio player with download and play option
    st.audio(audio_file, format='audio/mp3')
    st.download_button(label="Download Audio", data=open(audio_file, 'rb').read(), file_name=audio_file, mime='audio/mp3')

    # Clean up the audio file after usage
    os.remove(audio_file)
