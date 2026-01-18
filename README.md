# 🍞 Roti AI - Voice Chatbot with Gemini

Roti AI adalah asisten virtual berbasis suara yang ditenagai oleh **Google Gemini API**. Proyek ini dirancang untuk berinteraksi secara natural menggunakan Bahasa Indonesia, mulai dari mendengarkan perintah suara hingga merespons kembali dengan suara yang ekspresif.

## Cara Kerja (System Architecture)

Roti AI bekerja dengan mengintegrasikan beberapa modul dalam satu loop komunikasi yang sinkron:

1. **Voice Input (Ear):** Program menggunakan library `SpeechRecognition` untuk menangkap audio dari microphone dan mengirimkannya ke Google Speech Recognition API untuk dikonversi menjadi teks (STT).
2. **Brain Processing (Brain):** Teks hasil konversi dikirim ke **Gemini 1.5 Flash**. Di sini, instruksi dari `context.txt` digabungkan dengan input pengguna untuk menghasilkan respons yang sesuai dengan kepribadian Roti.
3. **Voice Output (Mouth):** Respons teks dari Gemini diubah menjadi file audio `.mp3` menggunakan `gTTS`.
4. **Audio Playback:** File suara diputar menggunakan `pygame.mixer`.
5. **Synchronization:** Menggunakan sistem *flagging* (`is_talking`) dan `threading` untuk memastikan mic tidak aktif saat Roti sedang berbicara (mencegah *feedback loop*).

## Fitur Utama
* **Speech-to-Text (STT):** Mendengarkan suara pengguna menggunakan library `SpeechRecognition`.
* **Intelligence:** Otak utama menggunakan model **Gemini 1.5 Flash** yang responsif.
* **Text-to-Speech (TTS):** Menjawab menggunakan suara lewat `gTTS` (Google Text-to-Speech).
* **Anti-Echo Logic:** Dilengkapi sistem *locking* mic agar Roti tidak mendengarkan suaranya sendiri saat berbicara.
* **Persona Customization:** Kepribadian Roti bisa diatur sesuka hati melalui file `context.txt`.

## Alat Perang (Prasyarat)
Pastikan kalian sudah menginstal:
* Python 3.10+
* VS Code
* Google Gemini API Key ([Dapatkan di sini](https://aistudio.google.com/))

## Cara Instalasi

1. **Clone Repository ini:**
   ```bash
   git clone https://github.com/Daffanich/roti-ai-chatbot.git
   cd roti-ai-chatbot
