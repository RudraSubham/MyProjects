import os
import time
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import mtranslate as mt

# Load environment variables
env_vars = dotenv_values("Frontend\.env")
InputLanguage = env_vars.get("InputLanguage")

# HTML template for speech recognition (Selenium method)
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replacing language input
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Save the HTML file for Selenium to use
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# Get the current directory
currrent_dir = os.getcwd()

# HTML file path for Selenium
Link = f"{currrent_dir}/Data/Voice.html"

# Configure Chrome options for Selenium
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Applewebkit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Set up the Chrome driver for Selenium
Service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service, options=chrome_options)

# Temporary directory for files
TempDirPath = rf"{currrent_dir}/Frontend/Files"

# Function to set the assistant's status
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify queries
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "can you"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

# Function to translate text to English
def universalTranslator(Text):
    try:
        english_translation = mt.translate(Text, "en", "auto")
        return english_translation.capitalize()
    except Exception as e:
        print(f"Error translating text: {e}")
        return Text

# Function for Selenium speech recognition
def seleniumSpeechRecognition():
    try:
        driver.get(f"file:///{Link}")
        driver.find_element(by=By.ID, value="start").click()

        start_time = time.time()
        while True:
            try:
                Text = driver.find_element(by=By.ID, value="output").text
                
                if Text:
                    driver.find_element(by=By.ID, value="end").click()

                    # If language is English or contains "en", process the text as is
                    if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                        return QueryModifier(Text)
                    else:
                        SetAssistantStatus("Translating...")
                        return QueryModifier(universalTranslator(Text))

                # If no text is found, wait for 1 second and try again
                if time.time() - start_time > 10:
                    print("Speech recognition timed out")
                    return ""
                time.sleep(1)
            except Exception as e:
                print(f"Error in Selenium speech recognition: {e}")
                return ""
    except Exception as e:
        print(f"Error in Selenium speech recognition: {e}")
        return ""

# Function for microphone-based speech recognition using `speech_recognition`
def microphoneSpeechRecognition():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening... Please speak now.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("⏰ Listening timed out. No speech detected.")
            return "I didn't catch that."

    try:
        query = recognizer.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError as e:
        return f"Request failed; {e}"

# Function to select the recognition method
def speechRecognition():
    # Check which method to use (browser-based or microphone-based)
    if InputLanguage.lower() == "microphone":
        return microphoneSpeechRecognition()
    else:
        return seleniumSpeechRecognition()

# Main loop
if __name__ == "__main__":
    while True:
        Text = speechRecognition()
        print(Text)
