import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables safely
env_vars = dotenv_values(r"Frontend\.env")
AssistantVoice = env_vars.get("AssistantVoice", "en-US-JennyNeural")  # Default voice if not found

async def textToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"
    
    # Delete file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Ensure AssistantVoice is valid
    if not AssistantVoice:
        raise ValueError("AssistantVoice is not set properly.")
    
    # Generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+10Hz', rate='+15%')
    await communicate.save(file_path)

def tTS(Text, func=lambda r=None: True):
    try:
        # Run async function properly
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(textToAudioFile(Text))
        
        pygame.mixer.init()
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            if func() is False:
                break
            pygame.time.Clock().tick(10)
        
        return True

    except Exception as e:
        print(f"Error in tTS: {e}")

    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

def textToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")
    
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    
    if len(Data) > 4 and len(Text) >= 250:
        tTS(" ".join(Data[:2]) + ". " + random.choice(responses), func)
    else:
        tTS(Text, func)

if __name__ == "__main__":
    while True:
        textToSpeech(input("Enter the text: "))
