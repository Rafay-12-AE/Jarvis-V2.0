JARVIS V2.0

JARVIS V2.0 is a modular, voice-controlled AI personal assistant built in Python. It began as a simple experiment with speech recognition and predefined commands and has evolved into a cross-platform assistant capable of wake-word activation, AI conversation, live web information retrieval, application and browser control, media searches, and a responsive animated interface.

The project currently runs on Windows and Linux. The Linux version has also been tested on a repurposed laptop running Linux through ChromeOS, which I use as a dedicated "Slabtop" Jarvis machine.

Project Evolution
JARVIS V1

The original version of Jarvis was a relatively simple Python voice assistant.

Its main purpose was to prove that I could create a program that listened to spoken commands, interpreted basic instructions, and performed actions on a computer.

V1 included features such as:

Speech recognition
Text-to-speech responses
Opening Google
Opening YouTube
Opening basic applications
Telling the current time and date
Basic system commands
Simple predefined responses

Most commands were handled through direct conditional logic.

V1 established the foundation of the project, but its intelligence and flexibility were limited.

JARVIS V2.0

V2.0 represents a major redesign.

Instead of simply adding more if/else commands to V1, the project was reorganized into a modular architecture containing separate components for voice processing, wake-word detection, AI processing, intent detection, web information retrieval, system actions, application launching, browser functions, and the graphical interface.

This makes Jarvis considerably easier to expand and maintain.

Major Features
Wake-Word Detection

Jarvis can remain dormant until the user says:

"Hey Jarvis"

Wake-word detection is handled locally using openWakeWord.

This allows Jarvis to behave more like a dedicated voice assistant instead of constantly processing every spoken sentence as a command.

Jarvis can return to its sleeping state and later be awakened again.

Voice Interaction

Jarvis accepts spoken commands through the computer's microphone.

Speech is converted into text and routed through the command-processing system.

The current implementation uses:

SpeechRecognition for speech input
Google Speech Recognition for speech-to-text

Jarvis then responds using text-to-speech.

On Windows, Jarvis uses:

pyttsx3

On Linux, Jarvis uses:

Microsoft Edge TTS
mpg123 for audio playback

The Linux implementation uses the en-US-GuyNeural voice.

AI Conversation

Jarvis V2.0 is not restricted to predefined commands.

When a request is conversational rather than a direct computer command, Jarvis can route it to an LLM using the Groq API.

This allows questions such as:

"Explain why the SR-71 Blackbird was so fast."

to receive a generated conversational response rather than requiring a hard-coded answer.

AI Intent Routing

V2.0 contains an intent-detection layer.

Instead of assuming every unfamiliar sentence is ordinary conversation, Jarvis can determine what type of action the user is requesting.

Examples of intents include:

Opening an application
Opening YouTube
Opening Google
Opening Chrome
Searching YouTube
Playing content on YouTube
Searching Google
Searching Spotify
Getting the current time
Getting the current date
Performing a live web search
Exiting Jarvis
General AI conversation

This creates a hybrid system where deterministic computer commands and AI reasoning can work together.

Live Web Information

Jarvis can retrieve current information from the internet instead of relying exclusively on the knowledge available to the language model.

Live information retrieval is handled using the Tavily API.

This allows Jarvis to answer questions involving information that may have changed recently.

The intent router determines when a request should be sent to the live web system instead of ordinary AI conversation.

Browser and Media Functions

Jarvis currently supports several browser and media commands.

Examples include:

Open Google
Open YouTube
Open Chrome
Search Google
Search YouTube
Play something on YouTube
Search Spotify
Play/search for content on Spotify

For example:

"Play [song name] on YouTube."

Jarvis can interpret the request and launch the relevant content.

System and Application Control

Jarvis can launch several system utilities and applications.

Examples include:

Calculator
Notepad
File Explorer
Paint
Settings
Task Manager
Visual Studio Code

V2.0 also includes a more generic application launcher so the architecture is not limited entirely to individually hard-coded programs.

Some application commands are naturally operating-system dependent.

Animated JARVIS Interface

V2.0 introduces a graphical interface built with Pygame.

The interface contains an animated central energy orb and changes its appearance according to Jarvis's current state.

The four primary states are:

SLEEPING

Jarvis is dormant and waiting for the wake word.

LISTENING

Jarvis has awakened and is listening for a command.

THINKING

Jarvis is processing the user's request.

SPEAKING

Jarvis is delivering its response.

The animation, colors, movement, and energy effects change depending on the current state.

The interface therefore provides visual feedback about what Jarvis is doing rather than simply displaying a static window.

The UI also closes automatically when Jarvis is shut down.

Cross-Platform Design

Jarvis V2.0 has been developed to operate on both:

Windows
Linux

Platform-specific functionality is handled separately where necessary.

For example, the text-to-speech system automatically uses the appropriate implementation:

Windows

pyttsx3

Linux

Edge TTS → MP3 → mpg123

This allowed the same overall Jarvis architecture to operate on both my normal Windows development computer and the Linux-based Slabtop.

The Slabtop

One of the main goals of this project was to give useful new life to older hardware.

I converted an older laptop with its original display removed into a Slabtop-style computer connected to an external display.

Jarvis V2.0 was then adapted to run on this machine.

Porting the project to Linux involved solving several compatibility problems involving:

Python versions
Python virtual environments
Wake-word dependencies
TensorFlow Lite
NumPy compatibility
Linux text-to-speech
Audio playback
Pygame
UI/audio conflicts

The final Slabtop version supports the same core Jarvis experience while using Linux-specific components where necessary.

Project Structure

The project is divided into several modules.

Jarvis V2.0/
│
├── main.py
│
├── brain/
│   ├── command_router.py
│   ├── intent.py
│   ├── llm.py
│   └── web_answer.py
│
├── core/
│   ├── voice.py
│   ├── wake_word.py
│   ├── ui_state.py
│   └── ...
│
├── skills/
│   ├── browser.py
│   ├── system.py
│   ├── apps.py
│   └── ...
│
├── ui/
│   ├── jarvis_ui.py
│   └── ...
│
├── data/
│
└── logs/
brain/

Contains the higher-level intelligence and decision-making systems.

core/

Contains fundamental Jarvis systems such as voice interaction, wake-word detection, and UI state management.

skills/

Contains functions that allow Jarvis to interact with applications, browsers, media services, and the operating system.

ui/

Contains the animated Jarvis graphical interface.

This modular structure makes future development easier because new abilities can be implemented as additional components instead of continually expanding one enormous script.

Installation
Requirements

You will need:

Python
A working microphone
Internet access for online speech recognition, AI features, live web retrieval, and Edge TTS
A Groq API key
A Tavily API key

Python 3.11 is recommended, particularly on Linux, because some wake-word/TensorFlow Lite dependencies may not work correctly with newer Python versions.

Windows Setup
1. Download the project

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL

Then enter the project:

cd "Jarvis V2.0"

Alternatively, download the repository as a ZIP file and extract it.

2. Create a virtual environment
py -3.11 -m venv .venv

Activate it:

.venv\Scripts\activate

If your system uses python instead of the Windows Python launcher, use the corresponding Python command.

3. Install Python dependencies

Install the dependencies listed by the project:

pip install -r requirements.txt

Depending on your Python installation and operating system, audio or wake-word dependencies may require additional platform-specific setup.

4. Configure API keys

Jarvis requires API credentials for its AI and live-web features.

You will need your own:

Groq API key
Tavily API key

Never publish API keys directly inside source code or commit them to GitHub.

Configure the environment variables expected by the project before launching Jarvis.

For example, in PowerShell:

$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
$env:TAVILY_API_KEY="YOUR_TAVILY_API_KEY"

The exact variable names should match those referenced by the source code.

5. Run Jarvis

From the root project directory:

py main.py

Once initialized, Jarvis should display its interface and enter its sleeping/wake-word state.

Say:

"Hey Jarvis"

to begin interacting with it.

Linux Setup

The Linux version has been tested using Python 3.11.

1. Download the repository
git clone YOUR_GITHUB_REPOSITORY_URL
cd "Jarvis V2.0"
2. Create a Python 3.11 virtual environment

If Python 3.11 is already installed:

python3.11 -m venv .venv311

Activate it:

source .venv311/bin/activate

Verify the version:

python --version

Python 3.11 is recommended for compatibility with the wake-word stack.

3. Install dependencies
pip install -r requirements.txt
4. Install mpg123

The Linux voice implementation uses mpg123 to play speech generated by Edge TTS.

On Debian/Ubuntu-based systems:

sudo apt update
sudo apt install mpg123

Additional microphone/audio packages may be required depending on the Linux distribution and hardware.

5. Configure API keys

Set your own API credentials:

export GROQ_API_KEY="YOUR_GROQ_API_KEY"
export TAVILY_API_KEY="YOUR_TAVILY_API_KEY"

Again, never commit real credentials to the repository.

6. Start Jarvis
python main.py

Jarvis should launch the animated interface and begin waiting for the wake word.

Say:

"Hey Jarvis"

to wake the assistant.

Example Commands

Once Jarvis is running, try commands such as:

Hey Jarvis

What time is it?

What is the date?

Open YouTube.

Search YouTube for SR-71 Blackbird.

Play [song or video] on YouTube.

Search Google for aerospace engineering.

Open calculator.

Open Visual Studio Code.

Explain how a turbofan engine works.

What is the latest news about [topic]?

Go to sleep.

Hey Jarvis.

Goodbye Jarvis.

Some commands and application-launching abilities depend on the operating system and the applications installed on the user's computer.

Important Security Note

Before uploading or distributing your own modified version of Jarvis, make sure you do not publish:

API keys
.env files containing credentials
Personal information
Authentication tokens
Private logs
Machine-specific secrets

Use environment variables for credentials.

A .gitignore file should also exclude virtual environments and sensitive/local files.

For example:

.venv/
.venv311/
.env
__pycache__/
*.pyc
logs/
