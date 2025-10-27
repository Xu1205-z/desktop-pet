import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import random
import os
import json
import time
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timedelta

try:
    from Cocoa import NSColor
    HAS_COCOA = True
except ImportError:
    HAS_COCOA = False

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    print("Warning: pygame not installed. Audio features disabled.")

# Constants
class Constants:
    # State decay rates
    SATIATION_DECAY_RATE = 0.0008
    ENERGY_DECAY_RATE = 0.0003
    HAPPINESS_DECAY_HUNGRY = 0.15
    HAPPINESS_DECAY_TIRED = 0.1
    
    # Thresholds
    HUNGER_THRESHOLD_LOW = 25
    HUNGER_THRESHOLD_MEDIUM = 40
    ENERGY_THRESHOLD_LOW = 25
    HAPPINESS_THRESHOLD_LOW = 40
    HAPPINESS_THRESHOLD_HIGH = 70
    HAPPINESS_THRESHOLD_VERY_HIGH = 85
    
    # Time related
    SAVE_INTERVAL = 3000
    WEATHER_UPDATE_INTERVAL = 1800
    ANIMATION_DELAY = 50
    DOUBLE_CLICK_TIME = 0.3
    FRAME_SPEED = 5
    
    # API
    WEATHER_TIMEOUT = 5
    WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Default coordinates (Sydney)
    DEFAULT_LATITUDE = -33.8688
    DEFAULT_LONGITUDE = 151.2093
    
    # Colors
    BG_COLOR = "#FFF9E6"
    CANVAS_BG = "#FFF9E6"
    STATUS_BG = "#FFF9E6"
    STATUS_TEXT_COLOR = "#5A4A3A"
    BUBBLE_BG = "#FFE5B4"
    BUBBLE_OUTLINE = "#FFB347"
    BUBBLE_TEXT_COLOR = "#4A3728"
    
    # Weather window colors
    WEATHER_BG = "#4A90E2"
    WEATHER_HEADER_BG = "#357ABD"
    WEATHER_CARD_BG = "#5BA3E8"
    WEATHER_TEXT = "#FFFFFF"
    
    # Audio
    DEFAULT_VOLUME = 0.5
    BGM_VOLUME = 0.3
    SFX_VOLUME = 0.7

class Mood(Enum):
    """Pet mood enumeration"""
    NORMAL = "normal"
    HAPPY = "happy"
    LOVE = "love"
    ANGRY = "angry"
    UPSET = "upset"
    EXCITED = "excited"
    MOST_ANGRY = "most_angry"

class AudioManager:
    """Audio management class - simplified version"""
    def __init__(self, sounds_dir: str = "sounds", enable_audio: bool = True):
        self.sounds_dir = sounds_dir
        self.enable_audio = enable_audio and HAS_PYGAME
        self.click_sound = None
        self.sfx_volume = Constants.SFX_VOLUME
        self.bgm_volume = Constants.BGM_VOLUME
        
        if self.enable_audio:
            try:
                pygame.mixer.init()
                self.load_sounds()
                print("Audio system initialized")
            except Exception as e:
                print(f"Audio initialization failed: {e}")
                self.enable_audio = False
    
    def load_sounds(self):
        """Load available sound files"""
        if not self.enable_audio:
            return
        
        click_path = os.path.join(self.sounds_dir, "click.wav")
        if os.path.exists(click_path):
            try:
                self.click_sound = pygame.mixer.Sound(click_path)
                self.click_sound.set_volume(self.sfx_volume)
                print(f"Loaded: click.wav")
            except Exception as e:
                print(f"Failed to load click.wav: {e}")
        
        bgm_path = os.path.join(self.sounds_dir, "bgm.mp3")
        if os.path.exists(bgm_path):
            try:
                pygame.mixer.music.load(bgm_path)
                print(f"Loaded: bgm.mp3")
            except Exception as e:
                print(f"Failed to load bgm.mp3: {e}")
    
    def play_click(self):
        """Play click sound"""
        if not self.enable_audio or not self.click_sound:
            return
        try:
            self.click_sound.play()
        except Exception as e:
            print(f"Failed to play click sound: {e}")
    
    def play_bgm(self, loop: bool = True):
        """Play background music"""
        if not self.enable_audio:
            return
        try:
            pygame.mixer.music.set_volume(self.bgm_volume)
            pygame.mixer.music.play(-1 if loop else 0)
            print("BGM started")
        except Exception as e:
            print(f"Failed to play BGM: {e}")
    
    def stop_bgm(self):
        if not self.enable_audio:
            return
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def pause_bgm(self):
        if not self.enable_audio:
            return
        try:
            pygame.mixer.music.pause()
        except:
            pass
    
    def resume_bgm(self):
        if not self.enable_audio:
            return
        try:
            pygame.mixer.music.unpause()
        except:
            pass
    
    def set_sfx_volume(self, volume: float):
        if not self.enable_audio:
            return
        self.sfx_volume = max(0.0, min(1.0, volume))
        if self.click_sound:
            self.click_sound.set_volume(self.sfx_volume)
    
    def set_bgm_volume(self, volume: float):
        if not self.enable_audio:
            return
        self.bgm_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.bgm_volume)
        except:
            pass

class Config:
    """Configuration management class"""
    def __init__(self, config_file: str = "pet_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        default_config = {
            "pet_size": 150,
            "latitude": Constants.DEFAULT_LATITUDE,
            "longitude": Constants.DEFAULT_LONGITUDE,
            "pet_name": "Luchen",
            "location_name": "Sydney",
            "window_topmost": True,
            "enable_weather": True,
            "enable_audio": True,
            "enable_bgm": True,
            "sfx_volume": Constants.SFX_VOLUME,
            "bgm_volume": Constants.BGM_VOLUME,
            "sounds_dir": "sounds",
            "foods": {
                "Rice": 30,
                "Meat": 50,
                "Fruit": 20,
                "Cake": 40
            },
            "plays": {
                "Hide-and-seek": 25,
                "Running": 15,
                "Dancing": 30,
                "Chat": 20
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    print("Config loaded successfully")
        except Exception as e:
            print(f"Config load failed: {e}")
        
        return default_config
    
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Config save failed: {e}")
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        self.config[key] = value

class WeatherService:
    """Weather service class with forecast support"""
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        self.weather_data: Optional[dict] = None
        self.forecast_data: Optional[list] = None
        self.last_update: float = 0
    
    def fetch_weather(self, max_retries: int = 3) -> bool:
        """Fetch current weather and 7-day forecast"""
        for attempt in range(max_retries):
            try:
                import requests
                
                url = (f"{Constants.WEATHER_API_URL}?"
                       f"latitude={self.latitude}&longitude={self.longitude}"
                       f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,is_day"
                       f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
                       f"&temperature_unit=celsius&timezone=auto&forecast_days=7")
                
                response = requests.get(url, timeout=Constants.WEATHER_TIMEOUT)
                if response.status_code == 200:
                    data = response.json()
                    current = data.get('current', {})
                    daily = data.get('daily', {})
                    
                    self.weather_data = {
                        'temperature': current.get('temperature_2m', 20),
                        'feels_like': current.get('apparent_temperature', 20),
                        'humidity': current.get('relative_humidity_2m', 50),
                        'weather_code': current.get('weather_code', 0),
                        'is_day': current.get('is_day', True),
                        'timestamp': time.time()
                    }
                    
                    # Parse forecast data
                    self.forecast_data = []
                    times = daily.get('time', [])
                    weather_codes = daily.get('weather_code', [])
                    temp_max = daily.get('temperature_2m_max', [])
                    temp_min = daily.get('temperature_2m_min', [])
                    precip = daily.get('precipitation_probability_max', [])
                    
                    for i in range(min(len(times), 7)):
                        self.forecast_data.append({
                            'date': times[i],
                            'weather_code': weather_codes[i] if i < len(weather_codes) else 0,
                            'temp_max': temp_max[i] if i < len(temp_max) else 25,
                            'temp_min': temp_min[i] if i < len(temp_min) else 15,
                            'precipitation': precip[i] if i < len(precip) else 0
                        })
                    
                    self.last_update = time.time()
                    print(f"Weather updated: {self.weather_data['temperature']}°C")
                    return True
            except Exception as e:
                print(f"Weather fetch failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
        
        return False
    
    def get_weather_emoji(self, code: int, is_day: bool = True) -> str:
        """Get weather emoji from code"""
        weather_map = {
            0: "☀️" if is_day else "🌙",
            1: "🌤️", 2: "🌤️", 3: "☁️",
            45: "🌫️", 48: "🌫️",
            51: "🌧️", 53: "🌧️", 55: "🌧️",
            61: "🌧️", 63: "🌧️", 65: "🌧️",
            71: "❄️", 73: "❄️", 75: "❄️",
            80: "🌧️", 81: "🌧️", 82: "🌧️",
            85: "❄️", 86: "❄️",
            95: "⛈️", 96: "⛈️", 99: "⛈️"
        }
        return weather_map.get(code, "🌤️")
    
    def get_weather_description(self) -> str:
        """Get brief weather description"""
        if not self.weather_data:
            return "🌤️ Loading..."
        
        temp = self.weather_data.get('temperature', 20)
        code = self.weather_data.get('weather_code', 0)
        is_day = self.weather_data.get('is_day', True)
        
        emoji = self.get_weather_emoji(code, is_day)
        
        desc_map = {
            0: "Clear", (1, 2): "Partly cloudy", 3: "Overcast",
            (45, 48): "Foggy", (51, 53, 55): "Drizzle",
            (61, 63, 65): "Rain", (71, 73, 75): "Snow",
            (80, 81, 82): "Showers", (85, 86): "Snow showers",
            (95, 96, 99): "Thunderstorm"
        }
        
        desc = "Unknown"
        for key, d in desc_map.items():
            if isinstance(key, tuple):
                if code in key:
                    desc = d
                    break
            elif code == key:
                desc = d
                break
        
        return f"{emoji} {desc}, {temp}°C"
    
    def should_update(self) -> bool:
        return time.time() - self.last_update > Constants.WEATHER_UPDATE_INTERVAL

class WeatherWindow:
    """Weather detail window"""
    def __init__(self, parent, weather_service: WeatherService, location_name: str = "Sydney"):
        self.parent = parent
        self.weather_service = weather_service
        self.location_name = location_name
        
        self.window = tk.Toplevel(parent)
        self.window.title("Weather Forecast")
        self.window.geometry("400x600")
        self.window.configure(bg=Constants.WEATHER_BG)
        self.window.resizable(False, False)
        
        # Make it topmost
        self.window.attributes('-topmost', True)
        
        self._create_ui()
    
    def _create_ui(self):
        """Create weather window UI"""
        # Header
        header_frame = tk.Frame(self.window, bg=Constants.WEATHER_HEADER_BG, height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Location
        location_label = tk.Label(
            header_frame,
            text=f"📍 {self.location_name}",
            font=("Helvetica", 16, "bold"),
            fg=Constants.WEATHER_TEXT,
            bg=Constants.WEATHER_HEADER_BG
        )
        location_label.pack(pady=(10, 0))
        
        # Current temperature
        if self.weather_service.weather_data:
            temp = self.weather_service.weather_data.get('temperature', 20)
            feels_like = self.weather_service.weather_data.get('feels_like', 20)
            code = self.weather_service.weather_data.get('weather_code', 0)
            is_day = self.weather_service.weather_data.get('is_day', True)
            humidity = self.weather_service.weather_data.get('humidity', 50)
            
            emoji = self.weather_service.get_weather_emoji(code, is_day)
            
            temp_label = tk.Label(
                header_frame,
                text=f"{int(temp)}° | Feels like: {int(feels_like)}°",
                font=("Helvetica", 20),
                fg=Constants.WEATHER_TEXT,
                bg=Constants.WEATHER_HEADER_BG
            )
            temp_label.pack()
            
            detail_label = tk.Label(
                header_frame,
                text=f"{emoji} Humidity: {humidity}%",
                font=("Helvetica", 12),
                fg=Constants.WEATHER_TEXT,
                bg=Constants.WEATHER_HEADER_BG
            )
            detail_label.pack(pady=(5, 10))
        
        # Forecast list
        forecast_frame = tk.Frame(self.window, bg=Constants.WEATHER_BG)
        forecast_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(
            forecast_frame,
            text="📅 7-Day Forecast",
            font=("Helvetica", 14, "bold"),
            fg=Constants.WEATHER_TEXT,
            bg=Constants.WEATHER_BG
        )
        title_label.pack(pady=(0, 10))
        
        # Create scrollable frame
        canvas = tk.Canvas(forecast_frame, bg=Constants.WEATHER_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(forecast_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Constants.WEATHER_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add forecast items
        if self.weather_service.forecast_data:
            for i, day_data in enumerate(self.weather_service.forecast_data):
                self._create_forecast_card(scrollable_frame, day_data, i)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        close_btn = tk.Button(
            self.window,
            text="✕ Close",
            command=self.window.destroy,
            font=("Helvetica", 12),
            bg=Constants.WEATHER_HEADER_BG,
            fg=Constants.WEATHER_TEXT,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=5
        )
        close_btn.pack(pady=10)
    
    def _create_forecast_card(self, parent, day_data, index):
        """Create a forecast card for one day"""
        card = tk.Frame(
            parent,
            bg=Constants.WEATHER_CARD_BG,
            relief=tk.FLAT,
            bd=0
        )
        card.pack(fill=tk.X, pady=5, padx=5)
        
        # Date
        date_str = day_data.get('date', '')
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            if index == 0:
                day_label = "Today"
            elif index == 1:
                day_label = "Tomorrow"
            else:
                weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                day_label = weekdays[date_obj.weekday()]
        except:
            day_label = f"Day {index + 1}"
        
        # Left side - Day and weather
        left_frame = tk.Frame(card, bg=Constants.WEATHER_CARD_BG)
        left_frame.pack(side=tk.LEFT, padx=15, pady=10)
        
        day_text = tk.Label(
            left_frame,
            text=day_label,
            font=("Helvetica", 14, "bold"),
            fg=Constants.WEATHER_TEXT,
            bg=Constants.WEATHER_CARD_BG
        )
        day_text.pack(anchor="w")
        
        # Weather emoji and precipitation
        code = day_data.get('weather_code', 0)
        emoji = self.weather_service.get_weather_emoji(code)
        precip = day_data.get('precipitation', 0)
        
        weather_text = tk.Label(
            left_frame,
            text=f"{emoji} {int(precip)}%",
            font=("Helvetica", 12),
            fg=Constants.WEATHER_TEXT,
            bg=Constants.WEATHER_CARD_BG
        )
        weather_text.pack(anchor="w")
        
        # Right side - Temperature
        right_frame = tk.Frame(card, bg=Constants.WEATHER_CARD_BG)
        right_frame.pack(side=tk.RIGHT, padx=15, pady=10)
        
        temp_max = int(day_data.get('temp_max', 25))
        temp_min = int(day_data.get('temp_min', 15))
        
        temp_text = tk.Label(
            right_frame,
            text=f"{temp_min}° ━━ {temp_max}°",
            font=("Helvetica", 14),
            fg=Constants.WEATHER_TEXT,
            bg=Constants.WEATHER_CARD_BG
        )
        temp_text.pack()

class PetState:
    """Pet state management class"""
    def __init__(self, data_file: str = "pet_data.json"):
        self.data_file = data_file
        self.satiation: float = 60.0
        self.energy: float = 80.0
        self.happiness: float = 70.0
        self.mood: Mood = Mood.NORMAL
        self.action: Optional[str] = None
        self.action_timer: int = 0
        
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.satiation = self._clamp(data.get("satiation", 60))
                    self.energy = self._clamp(data.get("energy", 80))
                    self.happiness = self._clamp(data.get("happiness", 70))
                    print("Pet data loaded successfully")
        except Exception as e:
            print(f"Data load failed: {e}")
    
    def save_data(self):
        try:
            data = {
                "satiation": self.satiation,
                "energy": self.energy,
                "happiness": self.happiness,
                "timestamp": time.time()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Data save failed: {e}")
    
    @staticmethod
    def _clamp(value: float, min_val: float = 0, max_val: float = 100) -> float:
        return max(min_val, min(max_val, value))
    
    def update(self):
        self.satiation = max(0, self.satiation - Constants.SATIATION_DECAY_RATE)
        self.energy = max(0, self.energy - Constants.ENERGY_DECAY_RATE)
        
        if self.satiation < Constants.HUNGER_THRESHOLD_MEDIUM:
            self.happiness = max(0, self.happiness - Constants.HAPPINESS_DECAY_HUNGRY)
        if self.energy < Constants.ENERGY_THRESHOLD_LOW:
            self.happiness = max(0, self.happiness - Constants.HAPPINESS_DECAY_TIRED)
        
        self._update_mood()
        
        if self.action_timer > 0:
            self.action_timer -= 1
        else:
            self.action = None
    
    def _update_mood(self):
        if self.energy < Constants.ENERGY_THRESHOLD_LOW:
            self.mood = Mood.NORMAL
        elif self.satiation < Constants.HUNGER_THRESHOLD_LOW:
            self.mood = Mood.UPSET
        elif self.satiation < Constants.HUNGER_THRESHOLD_MEDIUM:
            self.mood = Mood.ANGRY
        elif self.happiness > Constants.HAPPINESS_THRESHOLD_VERY_HIGH:
            self.mood = Mood.LOVE
        elif self.happiness > Constants.HAPPINESS_THRESHOLD_HIGH:
            self.mood = Mood.HAPPY
        elif self.happiness < Constants.HAPPINESS_THRESHOLD_LOW:
            self.mood = Mood.MOST_ANGRY
        else:
            self.mood = Mood.NORMAL
    
    def feed(self, satiation_gain: int, energy_cost: int = 5, happiness_gain: int = 5) -> None:
        self.satiation = self._clamp(self.satiation + satiation_gain)
        self.energy = max(0, self.energy - energy_cost)
        self.happiness = self._clamp(self.happiness + happiness_gain)
        self.mood = Mood.HAPPY
    
    def play(self, happiness_gain: int, energy_cost: int = 20, satiation_cost: int = 10) -> None:
        self.happiness = self._clamp(self.happiness + happiness_gain)
        self.energy = max(0, self.energy - energy_cost)
        self.satiation = max(0, self.satiation - satiation_cost)
        self.mood = Mood.EXCITED
    
    def sleep(self, satiation_cost: int = 5, happiness_gain: int = 5) -> None:
        self.energy = 100
        self.satiation = max(0, self.satiation - satiation_cost)
        self.happiness = self._clamp(self.happiness + happiness_gain)
        self.mood = Mood.NORMAL

class DesktopPet:
    """Desktop pet main class"""
    def __init__(self, gif_files: Dict[str, str], config: Optional[Config] = None):
        self.config = config or Config()
        self.pet_size = self.config.get("pet_size", 150)
        
        # Initialize audio
        self.audio = AudioManager(
            sounds_dir=self.config.get("sounds_dir", "sounds"),
            enable_audio=self.config.get("enable_audio", True)
        )
        
        if self.audio.enable_audio:
            self.audio.set_sfx_volume(self.config.get("sfx_volume", Constants.SFX_VOLUME))
            self.audio.set_bgm_volume(self.config.get("bgm_volume", Constants.BGM_VOLUME))
            
            if self.config.get("enable_bgm", True):
                self.audio.play_bgm()
        
        # Initialize window
        self.window = tk.Tk()
        self._setup_window()
        
        # Load images
        self.pet_images: Dict[str, List[ImageTk.PhotoImage]] = {}
        self.load_gifs(gif_files)
        
        if not self.pet_images:
            print("Error: No images loaded")
            self.window.destroy()
            return
        
        # Initialize state and services
        self.state = PetState()
        self.weather_service = None
        if self.config.get("enable_weather", True):
            self.weather_service = WeatherService(
                self.config.get("latitude", Constants.DEFAULT_LATITUDE),
                self.config.get("longitude", Constants.DEFAULT_LONGITUDE)
            )
            self.weather_service.fetch_weather()
        
        # UI elements
        self.animation_frame = 0
        self.speech_bubble: Optional[str] = None
        self.speech_timer: int = 0
        
        # Interaction state
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.last_click_time = 0
        
        # Bind events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Bind weather label click
        self.status_label.bind("<Button-1>", self.show_weather_window)
        self.status_label.config(cursor="hand2")
        
        # Start animation
        self.animate()
    
    def _setup_window(self):
        self.canvas_width = self.pet_size + 100
        self.canvas_height = self.pet_size
        
        self.window.geometry(f"{self.canvas_width}x{self.canvas_height+80}")
        self.window.config(bg=Constants.BG_COLOR)
        self.window.attributes('-topmost', self.config.get("window_topmost", True))
        self.window.resizable(False, False)
        self.window.title(self.config.get("pet_name", "Luchen"))
        
        if HAS_COCOA:
            try:
                self.window.update()
                self.window.wm_attributes('-transparent', True)
            except:
                pass
        
        self.canvas = Canvas(
            self.window,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=Constants.CANVAS_BG,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.status_frame = tk.Frame(
            self.window, 
            bg=Constants.STATUS_BG, 
            height=80
        )
        self.status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="",
            bg=Constants.STATUS_BG,
            font=("Helvetica", 9),
            fg=Constants.STATUS_TEXT_COLOR,
            justify=tk.CENTER
        )
        self.status_label.pack(pady=5)
    
    def load_gifs(self, gif_files: Dict[str, str]):
        for mood, filepath in gif_files.items():
            if not os.path.exists(filepath):
                print(f"Warning: File not found {filepath}")
                continue
            
            try:
                gif = Image.open(filepath)
                frames = []
                
                i = 0
                while True:
                    try:
                        gif.seek(i)
                        frame = gif.convert("RGBA")
                        frame = frame.resize(
                            (self.pet_size, self.pet_size),
                            Image.Resampling.LANCZOS
                        )
                        photo = ImageTk.PhotoImage(frame)
                        frames.append(photo)
                        i += 1
                    except EOFError:
                        break
                
                if frames:
                    self.pet_images[mood] = frames
                    print(f"Loaded {mood}: {len(frames)} frames")
                    
            except Exception as e:
                print(f"Load failed {filepath}: {e}")
    
    def show_speech(self, text: str, duration: int = 40):
        self.speech_bubble = text
        self.speech_timer = duration
    
    def show_weather_window(self, event=None):
        """Show weather detail window"""
        if self.weather_service and self.weather_service.weather_data:
            location_name = self.config.get("location_name", "Sydney")
            WeatherWindow(self.window, self.weather_service, location_name)
    
    def on_click(self, event):
        current_time = time.time()
        
        if current_time - self.last_click_time < Constants.DOUBLE_CLICK_TIME:
            self.show_menu()
            self.last_click_time = 0
        else:
            self.is_dragging = True
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root
            self.state.happiness = min(100, self.state.happiness + 5)
            self.last_click_time = current_time
            
            self.audio.play_click()
            
            reactions = ["Hehe!", "Tickles!", "More!", "Hahaha!"]
            self.show_speech(random.choice(reactions))
    
    def on_drag(self, event):
        if self.is_dragging:
            dx = event.x_root - self.drag_start_x
            dy = event.y_root - self.drag_start_y
            x = self.window.winfo_x() + dx
            y = self.window.winfo_y() + dy
            self.window.geometry(f"+{x}+{y}")
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root
    
    def on_release(self, event):
        self.is_dragging = False
    
    def show_menu(self):
        menu = tk.Menu(self.window, tearoff=0)
        
        feed_menu = tk.Menu(menu, tearoff=0)
        foods = self.config.get("foods", {})
        for food, gain in foods.items():
            feed_menu.add_command(
                label=f"{food} (+{gain})",
                command=lambda f=food, g=gain: self.feed(f, g)
            )
        menu.add_cascade(label="🍔 Feed", menu=feed_menu)
        
        play_menu = tk.Menu(menu, tearoff=0)
        plays = self.config.get("plays", {})
        for play, gain in plays.items():
            play_menu.add_command(
                label=f"{play} (+{gain})",
                command=lambda p=play, g=gain: self.play_action(p, g)
            )
        menu.add_cascade(label="🎮 Play", menu=play_menu)
        
        menu.add_command(label="😴 Sleep", command=self.sleep_action)
        
        if self.audio.enable_audio:
            menu.add_separator()
            audio_menu = tk.Menu(menu, tearoff=0)
            audio_menu.add_command(label="🔊 Volume +", command=lambda: self.adjust_volume(0.1))
            audio_menu.add_command(label="🔉 Volume -", command=lambda: self.adjust_volume(-0.1))
            audio_menu.add_separator()
            audio_menu.add_command(label="⏸️ Pause BGM", command=self.audio.pause_bgm)
            audio_menu.add_command(label="▶️ Resume BGM", command=self.audio.resume_bgm)
            menu.add_cascade(label="🎵 Audio", menu=audio_menu)
        
        menu.add_separator()
        menu.add_command(label="🌤️ Weather", command=self.show_weather_window)
        menu.add_command(label="❌ Exit", command=self.quit_app)
        
        try:
            menu.post(self.window.winfo_pointerx(), self.window.winfo_pointery())
        except:
            pass
    
    def adjust_volume(self, delta: float):
        new_volume = self.audio.bgm_volume + delta
        self.audio.set_bgm_volume(new_volume)
        self.audio.set_sfx_volume(new_volume)
        self.config.set("bgm_volume", new_volume)
        self.config.set("sfx_volume", new_volume)
        self.show_speech(f"Volume: {int(new_volume * 100)}%", 30)
    
    def feed(self, food_name: str, satiation_gain: int):
        self.state.feed(satiation_gain)
        self.state.action = f"eating_{food_name}"
        self.state.action_timer = 60
        self.show_speech(f"Yum! {food_name}!", 50)
    
    def play_action(self, play_name: str, happiness_gain: int):
        self.state.play(happiness_gain)
        self.state.action = f"playing_{play_name}"
        self.state.action_timer = 70
        self.show_speech(f"Let's {play_name}!", 50)
    
    def sleep_action(self):
        self.state.sleep()
        self.state.action_timer = 120
        self.show_speech("Zzz... Sweet dreams", 60)
    
    def quit_app(self):
        self.audio.stop_bgm()
        self.state.save_data()
        self.config.save_config()
        self.window.quit()
    
    def get_current_mood_key(self) -> str:
        if self.state.action:
            if self.state.action.startswith("eating_"):
                return "happy"
            elif self.state.action.startswith("playing_"):
                return "excited"
        return self.state.mood.value
    
    def draw(self):
        self.canvas.delete("all")
        
        mood_key = self.get_current_mood_key()
        frames = self.pet_images.get(mood_key, self.pet_images.get("normal", None))
        
        if frames:
            frame_index = (self.animation_frame // Constants.FRAME_SPEED) % len(frames)
            self.canvas.create_image(
                self.canvas_width // 2,
                self.canvas_height // 2,
                image=frames[frame_index]
            )
        
        if self.speech_bubble and self.speech_timer > 0:
            self._draw_speech_bubble()
            self.speech_timer -= 1
        
        self._update_status_label()
    
    def _draw_speech_bubble(self):
        bubble_x = self.canvas_width // 2 + 40
        bubble_y = 30
        
        self.canvas.create_oval(
            bubble_x - 45, bubble_y - 16,
            bubble_x + 45, bubble_y + 16,
            fill=Constants.BUBBLE_BG, 
            outline=Constants.BUBBLE_OUTLINE, 
            width=2
        )
        
        self.canvas.create_polygon(
            bubble_x - 25, bubble_y + 16,
            bubble_x - 35, bubble_y + 27,
            bubble_x - 15, bubble_y + 18,
            fill=Constants.BUBBLE_BG, 
            outline=Constants.BUBBLE_OUTLINE
        )
        
        self.canvas.create_text(
            bubble_x, bubble_y,
            text=self.speech_bubble,
            font=("Helvetica", 9, "bold"),
            fill=Constants.BUBBLE_TEXT_COLOR,
            width=80
        )
    
    def _update_status_label(self):
        status_text = ""
        
        if self.weather_service:
            weather_msg = self.weather_service.get_weather_description()
            status_text += f"{weather_msg} (Click for details)\n"
        
        status_text += (
            f"Hunger: {self.state.satiation:.0f}/100  "
            f"Energy: {self.state.energy:.0f}/100\n"
            f"Happy: {self.state.happiness:.0f}/100"
        )
        
        if self.audio.enable_audio:
            status_text += f"  🔊 {int(self.audio.bgm_volume * 100)}%"
        
        self.status_label.config(text=status_text)
    
    def animate(self):
        self.state.update()
        
        if self.animation_frame % Constants.SAVE_INTERVAL == 0:
            self.state.save_data()
        
        if self.weather_service and self.weather_service.should_update():
            self.weather_service.fetch_weather()
        
        self.draw()
        
        self.animation_frame += 1
        
        self.window.after(Constants.ANIMATION_DELAY, self.animate)
    
    def run(self):
        try:
            self.window.mainloop()
        except Exception as e:
            print(f"Runtime error: {e}")
        finally:
            self.audio.stop_bgm()
            self.state.save_data()
            self.config.save_config()

def main():
    """Main function"""
    gif_files = {
        "normal": "luchen normal.GIF",
        "happy": "luchen happy.GIF",
        "love": "luchen love.GIF",
        "angry": "luchen angry.GIF",
        "upset": "luchen upset.GIF",
        "excited": "luchen excited.GIF",
        "most_angry": "luchen most angry.GIF"
    }
    
    try:
        config = Config()
        pet = DesktopPet(gif_files, config)
        pet.run()
        
    except Exception as e:
        print(f"Startup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()