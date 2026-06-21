import gradio as gr
from google import generativeai as genai
import os

# 1. Konfigurasi Kunci API Gemini Anda secara aman
# Anda perlu memasukkan kuncinya di menu Settings -> Variables and secrets di Hugging Face nanti
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# 2. Fungsi untuk memproses obrolan dengan AI
def instruksi_ai(pesan, riwayat_obrolan):
    if not GEMINI_API_KEY:
        return "Error: Kunci API Gemini belum diatur di pengaturan Hugging Face Anda!"
    
    try:
        # Menggunakan model Gemini paling stabil saat ini
        model = genai.GenerativeModel("gemini-1.5-flash")
        respons = model.generate_content(pesan)
        return respons.text
    except Exception as e:
        return f"Terjadi kesalahan saat memproses: {str(e)}"

# 3. Membuat tampilan aplikasi Chatbot menggunakan Gradio
demo = gr.ChatInterface(
    fn=instruksi_ai, 
    title="Asisten AI Saya 🤖",
    description="Tanya apa saja kepada chatbot bertenaga Google Gemini ini.",
    examples=["Halo, siapa kamu?", "Buatkan saya puisi pendek tentang teknologi", "Tips belajar coding lewat HP"]
)

# 4. Menjalankan aplikasi
if __name__ == "__main__":
    demo.launch()
