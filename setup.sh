#!/bin/bash

# Setup script untuk Replit
# Jalankan sekali untuk setup awal

echo "🚀 Memulai setup UltraQueryWeb di Replit..."

# Create .streamlit directory
mkdir -p .streamlit

# Create config file
cat > .streamlit/config.toml << 'EOF'
[client]
showErrorDetails = true

[server]
headless = true
port = 8501
enableXsrfProtection = false

[logger]
level = "info"
EOF

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup selesai!"
echo ""
echo "🎯 Untuk menjalankan aplikasi, gunakan perintah:"
echo "   streamlit run UltraQueryWeb_Streamlit.py --server.address 0.0.0.0"
echo ""
echo "💡 URL aplikasi akan tampil di terminal."
echo ""
