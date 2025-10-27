# desktop-pet
                            DESKTOP PET PROJECT - README

PROJECT TITLE: Interactive Desktop Pet - Luchen
AUTHOR: Zihan Xu
DATE: October 2025

THIS PROJECT REQUIRES RUNNING OUTSIDE OF ED ENVIRONMENT 

This project uses several features that are NOT compatible with Ed's 
environment and must be run on a local machine.


                            EXTERNAL LIBRARIES USED

1. PILLOW (PIL) - Image Processing
   Purpose: Loading and processing GIF animations
   Used for: Displaying animated pet sprites
   Install: pip install pillow

2. PYGAME - Audio System
   Purpose: Playing background music and sound effects
   Used for: BGM playback and click sound effects
   Install: pip install pygame

3. REQUESTS - HTTP Library
   Purpose: Fetching weather data from Open-Meteo API
   Used for: Real-time weather information and 7-day forecast
   Install: pip install requests

4. TKINTER - GUI Framework
   Purpose: Creating graphical user interface
   Used for: Main window, canvas, menus, and weather detail window
   Note: Usually comes with Python, but may need separate install on some Linux systems



                          SPECIAL FEATURES REQUIRING ATTENTION

GUI APPLICATION
  Uses Tkinter for full graphical interface
  Interactive windows with buttons, menus, and animations
  Cannot run in terminal-only environment

AUDIO PROCESSING
  Background music (bgm.mp3)
  Sound effects (click.wav)
  Requires audio output device
  Uses pygame.mixer for audio playback

NETWORK-BASED FEATURES
  Connects to Open-Meteo Weather API (https://api.open-meteo.com)
  Fetches real-time weather data
  Requires internet connection
  Makes HTTP GET requests every 30 minutes

GRAPHICS RENDERING
  Displays animated GIF files
  Renders custom shapes (speech bubbles)
  Uses PIL for image processing and display


                          SYSTEM REQUIREMENTS


MINIMUM REQUIREMENTS:
  Python 3.7 or higher
  Operating System: Windows 10/11, macOS 10.14+, or Linux
  Internet connection (for weather features)
  Audio output device (for sound features)
  Display resolution: 1280x720 or higher recommended

DISK SPACE:
  ~50MB for dependencies
  ~10MB for project files and audio

MEMORY:
  ~100MB RAM minimum


                         INSTALLATION INSTRUCTIONS


STEP 1: Install Required Libraries

Run the following command in terminal/command prompt:

    pip install pillow pygame requests


STEP 2: Verify Installation

Run this command to check if libraries are installed:

    python -c "import PIL; import pygame; import requests; import tkinter; print('All libraries installed successfully!')"


STEP 3: Prepare Project Files

Ensure the following file structure:

    desktop-pet/
    ├── pet.py    (Main program)
    ├── sounds/                        (Audio folder)
    │   ├── bgm.mp3                   (Background music)
    │   └── click.wav                 (Click sound)
    ├── pet_config.json               (Configuration file)
    ├── luchen normal.GIF             (Pet animations)
    ├── luchen happy.GIF
    ├── luchen love.GIF
    ├── luchen angry.GIF
    ├── luchen upset.GIF
    ├── luchen excited.GIF
    └── luchen most angry.GIF


STEP 4: Run the Program

Navigate to the project folder and run:

    python pet.py




                    TESTING INSTRUCTIONS


TO TEST THE PROGRAM:

1. BASIC INTERACTION
    Click the pet to see happiness increase
    Drag the pet around the screen
    Double-click to open menu

2. FEEDING
    Select Feed > [Food Item]
    Observe hunger stat increase
    Check for "Yum!" speech bubble
    Verify pet changes to happy mood

3. PLAYING
    Select Play > [Activity]
    Watch happiness increase
    Notice energy and hunger decrease
    Pet should show excited mood

4. SLEEPING
    Select Sleep from menu
    Energy should restore to 100
    "Zzz..." speech bubble appears

5. WEATHER FEATURE
    Click on weather status bar
    Weather detail window should open
    Verify 7-day forecast displays
    Check for current temperature and humidity

6. AUDIO FEATURES
    Listen for background music on startup
    Click pet to hear click sound
    Use Audio menu to adjust volume
    Test pause/resume BGM functionality

7. DATA PERSISTENCE
    Play with pet for a while
    Close the program
    Reopen the program
    Verify stats are restored
