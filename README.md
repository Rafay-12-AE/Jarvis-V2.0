# JARVIS V2.0

JARVIS V2.0 is a cross-platform, voice-controlled AI personal assistant built in Python.

It combines traditional computer automation with AI-powered conversation, live web information retrieval, wake-word detection, speech recognition, text-to-speech, application control, browser/media functions, and an animated state-aware graphical interface.

The project currently supports **Windows and Linux**.

> **Important:** JARVIS does not include API credentials. Anyone installing the project must obtain and configure their own API keys for the services they choose to use.

---

# Features

JARVIS V2.0 currently includes:

* "Hey Jarvis" wake-word activation
* Sleep and wake system
* Voice command recognition
* AI-powered conversation using Groq
* AI intent detection and command routing
* Live web information retrieval using Tavily
* Google search
* YouTube search
* YouTube media playback
* Spotify search
* Application launching
* System utility launching
* Time and date commands
* Cross-platform Windows/Linux support
* Animated Pygame interface
* SLEEPING, LISTENING, THINKING, and SPEAKING UI states
* Platform-specific text-to-speech
* Modular project architecture
* Graceful shutdown

---

# How JARVIS Works

The basic processing sequence is:

```text
Wake Word
    ↓
"Hey Jarvis"
    ↓
Speech Recognition
    ↓
Command Router
    ↓
Intent Detection
    ↓
┌─────────────────────────────┐
│ Local Command               │
│ AI Conversation             │
│ Live Web Search             │
│ Application/System Action   │
└─────────────────────────────┘
    ↓
Response
    ↓
Text-to-Speech
```

The graphical interface simultaneously displays the current state of JARVIS.

---

# Project Structure

```text
Jarvis V2.0/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
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
└── data/
```

### `brain/`

Contains JARVIS's higher-level AI, intent-detection, command-routing, and live-information components.

### `core/`

Contains fundamental systems including voice interaction, wake-word detection, and UI-state management.

### `skills/`

Contains functions that allow JARVIS to interact with browsers, applications, media services, and the operating system.

### `ui/`

Contains the animated graphical interface.

The modular structure is designed to make JARVIS easier to maintain and expand.

---

# Requirements

Before installing JARVIS, you will need:

* Windows or Linux
* A working microphone
* Speakers or headphones
* Internet connection
* Python
* pip
* An API key for the configured LLM provider
* An API key for the configured live web retrieval provider

The standard JARVIS V2.0 configuration uses:

* **Groq** for LLM inference
* **Tavily** for live web information retrieval

---

# Recommended Python Version

**Python 3.11 is strongly recommended.**

The Linux version was developed and tested using **Python 3.11.16**.

Some wake-word and TensorFlow Lite dependencies can have compatibility problems with newer Python and NumPy combinations.

---

# AI and Web Providers

JARVIS V2.0 currently uses **Groq** for LLM inference and **Tavily** for live web information retrieval.

These are the providers used by the current V2.0 implementation, but the overall JARVIS architecture is modular.

The AI and web-retrieval components can therefore be modified by developers to support other compatible services.

For example, the LLM layer could potentially be adapted to use:

* OpenAI
* Google Gemini
* Anthropic
* Other cloud-based LLM providers
* Locally hosted language models
* Ollama or similar local-model systems

Likewise, Tavily could be replaced by another compatible search or information-retrieval service.

However, **alternative providers are not plug-and-play in the current V2.0 release**.

Using another provider requires modifying the appropriate JARVIS module to support that provider's API or SDK. Simply replacing the Groq or Tavily API key with a key from another service will not work.

The installation instructions below therefore use **Groq + Tavily**, because this is the configuration on which JARVIS V2.0 was developed and tested.

---

# API Accounts

## Groq

Groq provides the LLM inference used by the standard JARVIS V2.0 configuration.

Create a Groq account and obtain an API key.

JARVIS expects the following environment variable:

```text
GROQ_API_KEY
```

## Tavily

Tavily provides live web information retrieval.

Create a Tavily account and obtain an API key.

JARVIS expects:

```text
TAVILY_API_KEY
```

> Never place your actual API keys directly inside the Python source code or upload them to a public repository.

---

# WINDOWS INSTALLATION

## Step 1 — Install Python 3.11

Install Python 3.11.

During installation, enabling the option to add Python to PATH is recommended.

Verify the installation:

```powershell
py -3.11 --version
```

You should receive something similar to:

```text
Python 3.11.x
```

If the `py` launcher is unavailable but `python` works, use `python` instead.

---

## Step 2 — Download JARVIS

You can clone the repository using Git:

```powershell
git clone YOUR_REPOSITORY_URL
```

Alternatively:

**GitHub → Code → Download ZIP**

Extract the downloaded ZIP and open PowerShell or another terminal inside the extracted JARVIS directory.

---

## Step 3 — Create a Virtual Environment

Run:

```powershell
py -3.11 -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

The terminal should now show something similar to:

```text
(.venv)
```

---

## Step 4 — Upgrade pip

Run:

```powershell
python -m pip install --upgrade pip
```

---

## Step 5 — Install JARVIS Dependencies

Run:

```powershell
python -m pip install -r requirements.txt
```

The major Python components used by JARVIS include:

* SpeechRecognition
* PyAudio
* Groq
* Tavily
* openWakeWord
* ONNX Runtime
* Pygame
* pywhatkit
* pyttsx3
* Edge TTS
* Requests
* Wikipedia

Some dependencies may install additional supporting packages automatically.

---

# Configure API Keys on Windows

## Step 6 — Configure Groq

For the current PowerShell session:

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Replace the placeholder with your own Groq API key.

---

## Step 7 — Configure Tavily

Run:

```powershell
$env:TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
```

Replace the placeholder with your own Tavily key.

These commands configure the credentials for the current PowerShell session.

If the terminal is closed, they may need to be configured again unless they have been stored persistently as Windows environment variables.

### Persistent Configuration

Users may instead create persistent Windows user environment variables named:

```text
GROQ_API_KEY
TAVILY_API_KEY
```

After adding persistent environment variables, open a new terminal before launching JARVIS.

---

## Step 8 — Verify Environment Variables

PowerShell can verify that the variables exist:

```powershell
echo $env:GROQ_API_KEY
echo $env:TAVILY_API_KEY
```

**Warning:** These commands display the actual credentials. Do not use them while recording, streaming, screen-sharing, or around anyone who should not see the keys.

---

## Step 9 — Start JARVIS

Make sure the virtual environment is active.

Then run:

```powershell
python main.py
```

The graphical interface should launch and JARVIS should initialize.

Once JARVIS reaches its sleeping state, say:

```text
Hey Jarvis
```

JARVIS should detect the wake word and begin listening for a command.

---

# LINUX INSTALLATION

Linux requires several additional audio and compatibility steps.

JARVIS V2.0 has been successfully run using **Python 3.11** on Linux.

---

## Step 1 — Install System Packages

For Debian/Ubuntu-based systems:

```bash
sudo apt update
```

Install common development and audio dependencies:

```bash
sudo apt install python3-dev portaudio19-dev mpg123
```

`mpg123` is used by the Linux JARVIS voice system to play speech generated by Edge TTS.

Other Linux distributions may use different package managers and package names.

---

## Step 2 — Verify Python 3.11

Run:

```bash
python3.11 --version
```

You should receive:

```text
Python 3.11.x
```

If Python 3.11 is unavailable, install it using an appropriate method for your Linux distribution.

---

## Step 3 — Download JARVIS

Using Git:

```bash
git clone YOUR_REPOSITORY_URL
```

Enter the project directory:

```bash
cd "Jarvis V2.0"
```

Alternatively, download and extract the repository ZIP.

---

## Step 4 — Create a Python 3.11 Virtual Environment

Run:

```bash
python3.11 -m venv .venv311
```

Activate it:

```bash
source .venv311/bin/activate
```

Verify:

```bash
python --version
```

The output should report Python 3.11.

---

## Step 5 — Upgrade pip

Run:

```bash
python -m pip install --upgrade pip
```

---

## Step 6 — Install Python Dependencies

Run:

```bash
python -m pip install -r requirements.txt
```

---

# Important Linux NumPy Compatibility

Some Linux TensorFlow Lite/openWakeWord configurations require **NumPy 1.x**.

If JARVIS produces errors similar to:

```text
A module that was compiled using NumPy 1.x
cannot be run in NumPy 2.x
```

or:

```text
_ARRAY_API not found
```

or:

```text
numpy.core.multiarray failed to import
```

activate the JARVIS Python 3.11 environment and run:

```bash
python -m pip install "numpy<2"
```

Then retry JARVIS.

This compatibility adjustment was required during development of the Linux build.

---

# Step 7 — Verify Linux Dependencies

Test Edge TTS:

```bash
python -c "import edge_tts; print('Edge TTS OK')"
```

Test SpeechRecognition:

```bash
python -c "import speech_recognition; print('SpeechRecognition OK')"
```

Test Pygame:

```bash
python -c "import pygame; print('Pygame OK')"
```

Or test the major UI, voice, and speech-recognition dependencies together:

```bash
python -c "import pygame, edge_tts, speech_recognition; print('UI + TTS + STT dependencies OK')"
```

---

# Step 8 — Configure Groq on Linux

Run:

```bash
export GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

---

# Step 9 — Configure Tavily on Linux

Run:

```bash
export TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
```

These values apply to the current terminal session.

Linux users who want persistent variables can configure them using the appropriate shell profile or another secure environment-management method.

---

# Step 10 — Start JARVIS

Run:

```bash
python main.py
```

Once initialization completes, say:

```text
Hey Jarvis
```

---

# Linux Text-to-Speech

Windows and Linux use different speech-output systems.

### Windows

```text
JARVIS
   ↓
pyttsx3
   ↓
Windows speech system
```

### Linux

```text
JARVIS
   ↓
Edge TTS
   ↓
Generated MP3
   ↓
mpg123
   ↓
Speakers
```

The current Linux configuration uses:

```text
en-US-GuyNeural
```

as the default Edge TTS voice.

---

# Wake-Word System

JARVIS uses **openWakeWord** for local wake-word detection.

The primary wake phrase is:

```text
Hey Jarvis
```

On the first launch, openWakeWord may download model files required for wake-word recognition.

This is normal and can make the initial launch take longer than subsequent launches.

Once initialization completes, JARVIS remains in its sleeping state until the wake word is detected.

---

# Interface States

The Pygame interface represents four primary JARVIS states.

## SLEEPING

JARVIS is dormant and waiting for:

```text
Hey Jarvis
```

## LISTENING

JARVIS has awakened and is listening to the microphone.

## THINKING

JARVIS is interpreting or processing the request.

## SPEAKING

JARVIS is delivering its response.

The animated central orb changes its appearance and movement according to the current state.

---

# Example Commands

Wake JARVIS:

```text
Hey Jarvis
```

Then try commands such as:

```text
What time is it?
```

```text
What is the date?
```

```text
Open YouTube.
```

```text
Search YouTube for SR-71 Blackbird.
```

```text
Play [song or video] on YouTube.
```

```text
Search Google for aerospace engineering.
```

```text
Open calculator.
```

```text
Open Visual Studio Code.
```

```text
Explain how a turbofan engine works.
```

```text
What is the latest news about [topic]?
```

Return JARVIS to sleep:

```text
Go to sleep.
```

Wake it again:

```text
Hey Jarvis
```

Shut JARVIS down:

```text
Goodbye Jarvis.
```

Some application-launching commands depend on which programs are installed on the computer.

---

# Troubleshooting

## `pip` Is Not Recognized

Instead of:

```text
pip install ...
```

use:

```bash
python -m pip install ...
```

On Windows, this can also be used when appropriate:

```powershell
py -m pip install ...
```

---

## `git` Is Not Recognized

Git is optional if you download JARVIS using GitHub's ZIP download.

Use:

**GitHub → Code → Download ZIP**

instead of cloning the repository.

---

## `No module named ...`

Make sure the virtual environment is activated.

Then run:

```bash
python -m pip install -r requirements.txt
```

---

## Groq API Key Error

If you receive an error similar to:

```text
The api_key client option must be set
```

JARVIS cannot access your Groq API key.

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Linux:

```bash
export GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Then launch JARVIS from the same terminal session.

---

## Live Web Search Does Not Work

Check that your Tavily API key has been configured.

Windows:

```powershell
$env:TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
```

Linux:

```bash
export TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
```

---

## Linux NumPy / TFLite Error

If errors mention:

```text
NumPy 1.x
NumPy 2.x
_ARRAY_API
multiarray
tflite_runtime
```

activate the Python 3.11 environment and run:

```bash
python -m pip install "numpy<2"
```

Then restart JARVIS.

---

## Microphone Problems

Confirm that:

* The microphone is connected.
* The operating system has granted microphone permission.
* The correct input device is selected.
* PyAudio installed successfully.
* SpeechRecognition can access the microphone.

---

## Linux Has No Voice Output

Verify `mpg123`:

```bash
mpg123 --version
```

If it is unavailable on Debian/Ubuntu:

```bash
sudo apt install mpg123
```

Then verify Edge TTS:

```bash
python -c "import edge_tts; print('Edge TTS OK')"
```

---

## JARVIS Does Not Detect "Hey Jarvis"

Verify openWakeWord:

```bash
python -c "import openwakeword; print('openWakeWord OK')"
```

Make sure the correct microphone is selected and speak the wake phrase clearly.

The first launch may take longer while required model files are downloaded.

---

# Security

This repository does **not intentionally contain API credentials**.

Users must supply their own credentials for the configured external services.

The standard V2.0 configuration expects:

```text
GROQ_API_KEY
TAVILY_API_KEY
```

Never commit:

```text
.env
API keys
passwords
authentication tokens
private credentials
```

The included `.gitignore` excludes common sensitive and unnecessary local files, including:

```text
.env
.venv/
.venv311/
__pycache__/
logs/
```

If you fork or modify JARVIS, keep credentials outside the source code.

---

# Platform Notes

JARVIS's core architecture supports Windows and Linux, but some individual computer-control functions are operating-system dependent.

Application launching can also depend on:

* Which programs are installed
* Installation paths
* Operating-system commands
* Desktop environment
* Browser configuration

The AI, intent-routing, wake-word, voice, UI, and skill architecture is designed so platform-specific components can be modified independently.

---

# Extending JARVIS

JARVIS V2.0 was intentionally organized into separate modules rather than one large script.

Developers can expand areas such as:

```text
brain/
core/
skills/
ui/
```

without redesigning the entire assistant.

This architecture also makes it possible to experiment with alternative LLM providers, web-retrieval systems, voices, interfaces, and computer-control capabilities.

When replacing an external provider, the corresponding module must be adapted to that provider's API or SDK.

---

# JARVIS V2.0

JARVIS began as a basic voice-command experiment.

V2.0 developed that concept into a modular AI assistant combining voice interaction, wake-word detection, computer automation, live information retrieval, AI conversation, cross-platform operation, and a responsive graphical interface.

This repository contains the current working V2.0 implementation and the resources required to configure it on another compatible Windows or Linux computer.
