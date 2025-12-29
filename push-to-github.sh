#!/bin/bash

# Push ke GitHub - Pastikan sudah initialize git repo
# Jalankan: bash push-to-github.sh

echo "📤 Pushing ke GitHub..."

git add .
git commit -m "Update: Aplikasi siap di Replit"
git push origin main

echo "✅ Push berhasil!"
echo ""
echo "📍 Sekarang:"
echo "1. Buka https://replit.com"
echo "2. Klik 'Import from GitHub'"
echo "3. Masukkan URL GitHub repo Anda"
echo "4. Replit akan otomatis clone dan setup"
echo ""
echo "🚀 Setelah import selesai, klik 'Run' di Replit"
