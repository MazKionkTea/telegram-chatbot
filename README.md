Berikut adalah rangkuman, alur kerja (*workflow*), dan ringkasan teknis dari kode bot Telegram yang terintegrasi dengan `llama.cpp` menggunakan format Markdown yang scannable.

---

## 📝 Ringkasan Kode (Summary)

Kode ini adalah skrip Python untuk membangun sebuah **Telegram Bot bertenaga AI**. Bot ini bertindak sebagai jembatan antara pengguna Telegram dan model bahasa lokal (LLM) yang dijalankan melalui `llama.cpp` (menggunakan API yang kompatibel dengan format OpenAI).

Setiap kali pengguna mengirimkan pesan teks, bot akan meneruskannya ke server lokal `llama.cpp`, mengambil respons AI, dan mengirimkannya kembali ke pengguna.

---

## 🔄 Alur Kerja Bot (Workflow)

Secara garis besar, alur interaksi data berjalan sebagai berikut:

```
[ Pengguna Telegram ] 
       │  ▲
       │  │ (Pesan Balasan AI)
       ▼  │
 [ Skrip Bot Telegram ] 
       │  ▲
       │  │ (Respons JSON OpenAI Format)
       ▼  │
 [ Llama-Server (Localhost:8080) ]

```

### 1. Inisialisasi & Setup (Fungsi `main`)

* Skrip membaca `TELEGRAM_BOT_TOKEN` dan membangun aplikasi bot menggunakan pustaka `python-telegram-bot`.
* Mendaftarkan dua jenis penanganan pesan (*handlers*):
* **Command Handler**: Menangani perintah `/start`.
* **Message Handler**: Menangani semua pesan teks biasa dari pengguna (bukan perintah).


* Bot mulai berjalan dan aktif mendengarkan pesan masuk menggunakan metode **Polling** (`run_polling`).

### 2. Penanganan Perintah `/start` (Fungsi `start`)

* Ketika pengguna pertama kali memulai bot atau mengetik `/start`, bot langsung merespons dengan pesan sambutan otomatis secara *asynchronous*.

### 3. Pemrosesan Pesan & Integrasi AI (Fungsi `handle_message`)

Jika pengguna mengirimkan pesan teks biasa, runtutan proses berikut akan terjadi:

* **Ekstraksi Teks**: Bot mengambil teks yang dikirimkan oleh pengguna (`update.message.text`).
* **Penyusunan Payload**: Teks dibungkus ke dalam format JSON yang kompatibel dengan API OpenAI (menyertakan parameter `temperature` dan `max_tokens`).
* **HTTP POST Request**: Bot mengirimkan data tersebut ke `http://localhost:8080/v1/chat/completions` menggunakan pustaka `requests`.
* **Parsing & Penanganan Eror**:
* **Kondisi Sukses**: Bot mengekstrak teks jawaban AI dari struktur JSON hasil respons server.
* **Kondisi Gagal (Error)**: Jika server lokal mati atau *timeout*, eror akan dicatat di log, dan bot menyiapkan pesan kegagalan standar.


* **Kirim Balik**: Bot mengirimkan teks hasil akhir (baik dari AI maupun pesan eror) kembali ke ruang obrolan pengguna di Telegram.

---

## 🛠️ Komponen Teknis & Dependensi

| Komponen | Deskripsi |
| --- | --- |
| **Pustaka Utama** | `python-telegram-bot` (v20+) untuk interaksi dengan API Telegram, `requests` untuk HTTP API calls ke server AI. |
| **Logging** | Diatur pada level `INFO` untuk memantau aktivitas bot dan mendeteksi eror jaringan di konsol. |
| **Sistem AI** | Di-host secara mandiri (*self-hosted*) menggunakan `llama.cpp` pada port lokal `8080`. |
| **Metode Sinkronisasi** | Menggunakan arsitektur *Asynchronous* (`async`/`await`) khas Telegram Bot modern agar dapat menangani banyak pengguna sekaligus tanpa *blocking*. |

> ⚠️ **Catatan Penting:** > Agar kode ini dapat berfungsi sepenuhnya di dunia nyata, nilai variabel `TELEGRAM_BOT_TOKEN` harus diganti dengan token bot asli dari @BotFather, dan server `llama.cpp` harus sudah aktif berjalan di latar belakang komputer pada port `8080`.
