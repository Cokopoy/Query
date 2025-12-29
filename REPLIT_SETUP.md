# UltraQueryWeb di Replit

## 📋 Panduan Deployment di Replit

### Langkah 1: Buat Project Baru di Replit
1. Buka https://replit.com
2. Klik "Create" → "New repl"
3. Pilih "Python"
4. Beri nama project (contoh: "UltraQueryWeb")

### Langkah 2: Upload File
1. Download file `UltraQueryWeb_Streamlit.py` dari folder ini
2. Di Replit, klik "Upload file" atau gunakan drag & drop
3. Upload juga `requirements.txt`

### Langkah 3: Install Dependencies
Di terminal Replit, jalankan:
```bash
pip install -r requirements.txt
```

### Langkah 4: Buat File .streamlit/config.toml
Buat folder `.streamlit` dan file `config.toml` dengan isi:
```toml
[client]
showErrorDetails = true

[server]
headless = true
port = 8501
enableXsrfProtection = false
```

Atau di terminal Replit:
```bash
mkdir -p .streamlit
echo '[client]
showErrorDetails = true

[server]
headless = true
port = 8501
enableXsrfProtection = false' > .streamlit/config.toml
```

### Langkah 5: Jalankan Aplikasi
Di terminal Replit, jalankan:
```bash
streamlit run UltraQueryWeb_Streamlit.py --server.address 0.0.0.0
```

Atau buat `replit.nix` untuk otomatis install dan run:

```bash
{ pkgs }: {
    deps = [
        pkgs.python310
        pkgs.python310Packages.pip
    ];
    env = {};
    run = "streamlit run UltraQueryWeb_Streamlit.py --server.address 0.0.0.0";
}
```

### Langkah 6: Akses Web Application
- Replit akan menampilkan URL publik (format: `https://<project-name>.<username>.repl.co`)
- Klik URL tersebut untuk membuka aplikasi web

---

## ⚙️ Fitur-Fitur

### Tab 1: Load Data 📂
- Upload file Excel (.xlsx, .xls), CSV, TXT, JSON, Parquet, Feather, NDJSON/JSONL
- Atur nomor baris header
- Upload hingga 5 file sekaligus
- Download data sebagai CSV atau Excel

### Tab 2: Transform Data 🔄
- **Select Columns**: Pilih kolom yang ingin ditampilkan
- **Filter Data**: Filter berdasarkan nilai atau tahun (untuk date columns)
- **Split Kolom**: Pisahkan nilai dalam kolom menggunakan delimiter `;`
- **Pivot Table**: Buat pivot table dengan configurable rows, columns, values, dan aggregation function
- **Sort**: Urutkan hasil pivot secara descending

### Tab 3: XLOOKUP 🔧
- Upload file referensi terpisah
- Pilih kolom kunci di data utama dan file referensi
- Lookup nilai dari file referensi berdasarkan kunci
- Multiple lookup columns didukung

### Tab 4: AI Analysis 🤖
- Tanya AI tentang data Anda
- Menggunakan OpenRouter API (GPT-3.5-turbo)
- AI melihat sampel 10 baris pertama data Anda
- Respons langsung di aplikasi

---

## 🔐 Konfigurasi API Key

### OpenRouter API Key
1. Dapatkan API key dari https://openrouter.ai
2. Edit file `UltraQueryWeb_Streamlit.py`
3. Ganti `OPENROUTER_API_KEY` dengan key Anda

**Alternatif Aman (Recommended)**:
Di Replit, gunakan Secrets:
1. Klik "Tools" → "Secrets"
2. Tambah variabel: `OPENROUTER_API_KEY` dengan value key Anda
3. Edit file Python untuk membaca dari `os.environ`:
```python
import os
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
```

---

## 🐛 Troubleshooting

### Error: Module not found
Jalankan di terminal:
```bash
pip install -r requirements.txt
```

### Error: xlrd issues
xlrd sudah include di requirements.txt, tapi jika error:
```bash
pip install xlrd
```

### Error: pyarrow not found (untuk feather/parquet)
```bash
pip install pyarrow
```

### Aplikasi terputus
Replit Free plan memiliki sleep timeout. Untuk production, upgrade ke Replit Teams atau deploy ke platform lain (Railway, Heroku, dll).

---

## 📝 Perbedaan Tkinter vs Streamlit Version

| Fitur | Tkinter | Streamlit |
|-------|---------|-----------|
| Interface | Desktop GUI | Web Browser |
| File Upload | File Dialog | Drag & Drop / Upload Button |
| Data Display | Table (TTK Treeview) | Interactive Table |
| Export | Save Dialog | Download Button |
| Deployment | Local Only | Cloud Ready |
| Responsive | Fixed Window | Responsive Design |

---

## 🚀 Tips Performa

1. **Untuk dataset besar** (>100K rows):
   - Filter data sebelum pivot
   - Gunakan aggregation function `count` daripada `mean` untuk kecepatan

2. **Untuk API calls**:
   - AI analysis bisa slow jika dataset besar
   - Limit prompt length untuk respons lebih cepat

3. **Memory usage**:
   - Streamlit caching otomatis
   - Session state manage memory dengan baik

---

## 📧 Support
Jika ada pertanyaan atau error, cek:
- Streamlit docs: https://docs.streamlit.io
- Pandas docs: https://pandas.pydata.org
- OpenRouter docs: https://openrouter.ai/docs

---

Selamat menggunakan UltraQueryWeb! 🎉
