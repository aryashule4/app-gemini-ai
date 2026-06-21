import gradio as gr
import requests
import os

# Mengambil token Hugging Face secara otomatis yang tersimpan di dalam sistem Space
HF_TOKEN = os.environ.get("HF_TOKEN")

# Menggunakan model bahasa gratis yang andal dari Hugging Face (contoh: Llama 3)
API_URL = "https://huggingface.co"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def tanya_ai(pesan, riwayat_obrolan):
    # Menyusun format pesan agar dipahami oleh model AI
    payload = {
        "inputs": f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{pesan}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "parameters": {"max_new_tokens": 512, "temperature": 0.7}
    }
    
    try:
        respons = requests.post(API_URL, headers=headers, json=payload)
        hasil = respons.json()
        
        # Mengambil teks jawaban dari respon API
        if isinstance(hasil, list) and len(hasil) > 0:
            teks_balasan = hasil[0].get("generated_text", "")
            # Membersihkan instruksi sistem agar hanya menampilkan jawaban murni
            if "assistant" in teks_balasan:
                teks_balasan = teks_balasan.split("assistant")[-1].strip()
            return teks_balasan
        else:
            return "Maaf, AI sedang sibuk memproses. Silakan coba sesaat lagi."
            
    except Exception as e:
        return f"Terjadi kesalahan koneksi: {str(e)}"

# Membuat antarmuka Chatbot dengan Gradio
demo = gr.ChatInterface(
    fn=tanya_ai,
    title="Asisten AI Hugging Face 🤖",
    description="Chatbot ini berjalan 100% gratis menggunakan model open-source di Hugging Face Hub.",
    examples=["Halo, apa kabar?", "Berikan saya resep nasi goreng sederhana", "Bagaimana cara kerja kecerdasan buatan?"]
)

if __name__ == "__main__":
    demo.launch()
