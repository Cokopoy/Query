# ✅ Checklist - Setup Replit dengan GitHub

## Langkah 1: Persiapan Lokal
- [x] File `UltraQueryWeb_Streamlit.py` ada
- [x] File `requirements.txt` ada
- [x] File `.replit` sudah dibuat
- [x] File `.streamlit/config.toml` sudah dibuat
- [x] File `.gitignore` sudah dibuat

## Langkah 2: Push ke GitHub

### Jika belum initialize git:
```bash
cd "d:\Latihan Olah Data\Tools\Query\WEB"
git init
git add .
git commit -m "Initial commit: UltraQueryWeb Streamlit App"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Jika sudah ada git repo:
```bash
cd "d:\Latihan Olah Data\Tools\Query\WEB"
git add .
git commit -m "Update: Aplikasi siap di Replit"
git push origin main
```

## Langkah 3: Setup di Replit

### Option A: Import dari GitHub (Rekomendasi)
1. Buka https://replit.com/new
2. Klik "Import from GitHub"
3. Paste URL repo Anda: `https://github.com/YOUR_USERNAME/YOUR_REPO`
4. Klik "Import"
5. Tunggu selesai (1-2 menit)
6. Klik tombol "Run"

### Option B: Manual Upload
1. Buka https://replit.com/new
2. Pilih bahasa "Python"
3. Beri nama project
4. Upload file-file ini:
   - UltraQueryWeb_Streamlit.py
   - requirements.txt
   - .replit
   - .streamlit/config.toml
5. Klik "Run"

## Langkah 4: Verifikasi Berjalan

Cek terminal Replit, seharusnya muncul:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://IP:8501

  For better performance, install the Streamlit library offline:
  $ pip install streamlit
```

Kemudian lihat URL publik seperti:
```
https://project-name-username.replit.dev
```

## Troubleshooting

### ❌ Error: "ModuleNotFoundError"
**Solusi:**
```bash
pip install -r requirements.txt
```

### ❌ Error: "Address already in use"
**Solusi:** Edit `.replit` dan cek port 8501 tidak tertutup

### ❌ Blank page atau infinite loading
**Solusi:**
1. Tunggu 2-3 menit (loading pertama kali lambat)
2. Hard refresh browser (Ctrl+Shift+R)
3. Clear browser cache

### ❌ Requirements tidak terinstall
**Solusi:**
```bash
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

## File Configuration Explained

### `.replit`
```
run = "streamlit run UltraQueryWeb_Streamlit.py --server.address 0.0.0.0"
```
→ Otomatis jalankan Streamlit saat klik "Run"

### `.streamlit/config.toml`
```
[server]
headless = true
port = 8501
enableXsrfProtection = false
```
→ Konfigurasi Streamlit untuk environment Replit

### `requirements.txt`
```
streamlit==1.28.1
pandas==2.1.1
openpyxl==3.10.10
pyarrow==13.0.0
```
→ Dependencies yang diperlukan aplikasi

## ✨ Selesai!

Aplikasi sudah siap berjalan di Replit! 🎉

**Tips:**
- Upgrade ke Replit Pro untuk unlimited resources
- Atau gunakan Replit Teams untuk collaboration
- Data session di-reset setiap kali browser refresh

---

Jika masih ada masalah, buka terminal Replit dan cek error messages.
