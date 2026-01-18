import os
import time
import threading
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from google import genai
from dotenv import load_dotenv

# 1. KONFIGURASI
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)
# Global flag untuk kunci mic
is_talking = False

def speak(text):
    global is_talking
    def run_speak():
        global is_talking
        try:
            is_talking = True # KUNCI MIC
            if not mixer.get_init():
                mixer.init()
            
            tts = gTTS(text=text, lang='id')
            filename = f"res_{int(time.time())}.mp3"
            tts.save(filename)
            
            mixer.music.load(filename)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)
            
            mixer.music.unload()
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f"\n❌ Masalah Audio: {e}")
        finally:
            # Kasih jeda 0.5 detik setelah ngomong baru buka mic
            # Biar gema suara terakhir gak ketangkep mic
            time.sleep(0.5) 
            is_talking = False # BUKA MIC

    threading.Thread(target=run_speak, daemon=True).start()

def listen():
    global is_talking
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # VALIDASI KRUSIAL: Jangan pernah masuk mode listen kalau Roti lagi ngomong
        while is_talking:
            time.sleep(0.1)
            
        print("\n[🎙️ Roti dengerin...]")
        r.adjust_for_ambient_noise(source, duration=0.5) 
        
        try:
            # Kita perpendek timeout biar lebih responsif
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("[⚡ Lagi mikir...]")
            query = r.recognize_google(audio, language='id-ID')
            print(f"Lu: {query}")
            return query
        except:
            return ""

# --- Inisialisasi Karakter ---
try:
    with open("context.txt", "r") as f:
        karakter = f.read().strip()
except:
    karakter = "Nama kamu adalah Roti, asisten AI gaul Daffa."

# Deteksi Model
try:
    available_models = [m.name for m in client.models.list()]
    my_model = next((m for m in available_models if "flash" in m), available_models[0])
except:
    my_model = "gemini-1.5-flash"

print("--- 🚀 SISTEM ROTI V5 (ANTI-ECHO) AKTIF ---")

while True:
    # 1. Dengerin (Fungsi ini bakal nunggu sampe is_talking == False)
    user_input = listen()
    
    if user_input:
        if "keluar" in user_input.lower():
            print("Roti: parah, lu ninggalin gua dap!")
            # Proses keluar tanpa thread biar tuntas
            is_talking = True
            if not mixer.get_init(): mixer.init()
            gTTS(text="parah, lu ninggalin gua dap!", lang='id').save("bye.mp3")
            mixer.music.load("bye.mp3")
            mixer.music.play()
            while mixer.music.get_busy(): time.sleep(0.1)
            mixer.music.unload()
            os.remove("bye.mp3")
            break
            
        try:
            # 2. Proses API
            response = client.models.generate_content(
                model=my_model,
                contents=f"Instruksi: {karakter}\nUser: {user_input}"
            )
            
            bot_text = response.text.replace("*", "")
            print(f"Roti: {bot_text}")
            
            # 3. Ngomong (Ini bakal set is_talking jadi True)
            speak(bot_text)
            
            # 4. PAKSA NUNGGU: Jangan balik ke atas (listen) selama Roti masih ngoceh
            while is_talking:
                time.sleep(0.2)
            
        except Exception as e:
            print(f"❌ Masalah API: {e}")
            is_talking = False