from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import psutil
import os
import re

env_vars = dotenv_values("Frontend\.env")
GroqAPIKey = env_vars.get("GroqAPIKey")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Applewebkit/537.36 (KHTML, like Gecko) Chrome/100.0.142.4896 Safari/537.36"

client = Groq(api_key=GroqAPIKey)
messages = []

SystemChatBot = [{"role": "system", "content": "You're a content writer and assistant. Provide the best content and accurate searches."}]

# ✅ Predefined official sites for common apps
KNOWN_APPS = {
    "youtube": "https://www.youtube.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "whatsapp": "https://web.whatsapp.com",
    "spotify": "https://www.spotify.com",
    "twitter": "https://www.twitter.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "netflix": "https://www.netflix.com",
    "discord": "https://discord.com",
    "telegram": "https://web.telegram.org",
    "zoom": "https://zoom.us",
    "reddit": "https://www.reddit.com",
}

# ✅ Search Google for Official Website
def find_official_website(app_name):
    """
    Searches Google for the official website of an app.

    Args:
        app_name (str): The name of the app.

    Returns:
        str: Official website URL or None if not found.
    """
    search_url = f"https://www.google.com/search?q={app_name}+official+site"
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        match = re.search(r"/url\?q=(https://[^&]+)", href)
        if match:
            links.append(match.group(1))

    # Prioritize sites containing keywords like 'official'
    for link in links:
        if "official" in link.lower() or any(domain in link for domain in [".com", ".org", ".net"]):
            return link

    return links[0] if links else None

# ✅ Open App Locally or Open Official Site
def OpenApp(app_name):
    """
    Attempts to open an application. If not installed, opens the official website.

    Args:
        app_name (str): The name of the application.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print(f"[green]Trying to open {app_name} locally...[/green]")
        appopen(app_name, match_closest=True, output=True, throw_error=True)
        return True
    except:
        print(f"[yellow]App '{app_name}' not found locally. Searching for official website...[/yellow]")

        # Check predefined known apps
        if app_name.lower() in KNOWN_APPS:
            official_site = KNOWN_APPS[app_name.lower()]
        else:
            official_site = find_official_website(app_name)

        if official_site:
            print(f"[green]Opening official website: {official_site}[/green]")
            webopen(official_site)
            return True
        else:
            print(f"[red]No official website found for '{app_name}'.[/red]")
            return False

def get_running_apps():
    """
    Returns a dictionary of running apps with their process IDs (PID).
    """
    running_apps = {}
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            app_name = proc.info['name'].lower()
            running_apps[app_name] = proc.info['pid']  # Store process ID
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return running_apps

def CloseApp(app_name):
    """
    Closes the specified application if running in the background.

    Args:
        app_name (str): The app name to close.

    Returns:
        bool: True if the app was closed, False otherwise.
    """
    app_name = app_name.lower().strip()
    running_apps = get_running_apps()

    # ✅ Step 1: Try closing by exact process name (background apps)
    for process_name, pid in running_apps.items():
        if app_name in process_name:  # Check if app name is in process name
            try:
                print(f"[green]Closing {process_name} (PID: {pid})...[/green]")
                psutil.Process(pid).terminate()  # ✅ Force close the app
                return True
            except Exception as e:
                print(f"[red]Error closing {process_name}: {e}[/red]")
                return False

    # ✅ Step 2: If not found in background, try using `AppOpener`
    try:
        print(f"[yellow]App '{app_name}' not found in processes. Trying AppOpener...[/yellow]")
        close(app_name, match_closest=True, output=True, throw_error=False)
        return True
    except Exception as e:
        print(f"[red]Error closing {app_name} with AppOpener: {e}[/red]")
        return False

    print(f"[red]App '{app_name}' is not running.[/red]")
    return False

# ✅ Content Writing with AI
def Content(Topic):
    def OpenNotepad(file):
        subprocess.Popen(['notepad.exe', file])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("content ", "")
    ContentByAI = ContentWriterAI(Topic)

    file_path = rf"Data\{Topic.lower().replace(' ', '')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(file_path)
    return True

# ✅ Search & Open YouTube Video
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

# ✅ Play First YouTube Video from Search
def PlayYouTube(query):
    playonyt(query)
    return True

# ✅ System Commands (Mute, Volume Control, etc.)
def System(command):
    commands = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume unmute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down"),
    }
    if command in commands:
        commands[command]()
        return True
    return False

# ✅ Process and Execute Commands
async def TranslateAndExecute(commands):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, command.removeprefix("open ")))
        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content ")))
        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")))
        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYouTube, command.removeprefix("play ")))
        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close ")))
        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(System, command.removeprefix("system ")))
        else:
            print(f"[red]No Function Found for '{command}'[/red]")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

# ✅ Execute Commands
async def Automation(commands):
    async for _ in TranslateAndExecute(commands):
        pass
    return True

# ✅ Main Execution
if __name__ == "__main__":
    user_input = input("Enter command: ")  # Example: "open instagram"
    asyncio.run(Automation([user_input]))

# ✅ Expose Automation for other scripts (like GUI)
def run_automation(commands):
    asyncio.run(Automation(commands))
