import streamlit as st
import pandas as pd
import requests
import io
import json
from io import BytesIO

# Ganti dengan API key OpenRouter kamu
OPENROUTER_API_KEY = "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"

# Konfigurasi halaman
st.set_page_config(
    page_title="Power Query Lite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Power Query Lite dengan Pivot & AI")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'pivot_df' not in st.session_state:
    st.session_state.pivot_df = None
if 'ref_df' not in st.session_state:
    st.session_state.ref_df = None

def is_date_column(col, df):
    """Deteksi apakah kolom berisi data date/datetime"""
    if df is None or col not in df.columns:
        return False
    try:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return True
        sample = df[col].dropna().head(10)
        if len(sample) == 0:
            return False
        success_count = pd.to_datetime(sample, errors='coerce').notna().sum()
        return success_count / len(sample) >= 0.7
    except Exception:
        return False

def load_excel_file(uploaded_file, header_row=1):
    """Baca file Excel/CSV"""
    try:
        ext = uploaded_file.name.split('.')[-1].lower()
        
        if ext == 'txt':
            content = uploaded_file.read().decode('utf-8')
            if '\t' in content[:2048]:
                delimiter = '\t'
            elif ';' in content[:2048]:
                delimiter = ';'
            else:
                delimiter = ','
            df = pd.read_csv(io.StringIO(content), delimiter=delimiter, header=header_row-1)
            df['Sumber File'] = uploaded_file.name
            return df
            
        elif ext in ['xlsx', 'xls']:
            if ext == 'xls':
                df = pd.read_excel(uploaded_file, engine='xlrd', header=header_row-1)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl', header=header_row-1)
            df['Sumber File'] = uploaded_file.name
            return df
            
        elif ext == 'csv':
            df = pd.read_csv(uploaded_file, header=header_row-1)
            df['Sumber File'] = uploaded_file.name
            return df
            
        elif ext == 'json':
            try:
                df = pd.read_json(uploaded_file)
            except:
                df = pd.read_json(uploaded_file, orient='records')
            df['Sumber File'] = uploaded_file.name
            return df
            
        elif ext == 'parquet':
            df = pd.read_parquet(uploaded_file)
            df['Sumber File'] = uploaded_file.name
            return df
            
        elif ext in ['ndjson', 'jsonl']:
            df = pd.read_json(uploaded_file, lines=True)
            df['Sumber File'] = uploaded_file.name
            return df
            
        elif ext == 'feather':
            df = pd.read_feather(uploaded_file)
            df['Sumber File'] = uploaded_file.name
            return df
            
    except Exception as e:
        st.error(f"Error membaca file: {e}")
        return None
    
    return None

# Sidebar - Catatan
with st.sidebar:
    st.header("📝 Catatan Laporan RL 4 & RL 5")
    with st.expander("RL 4 Fields"):
        st.write("""
        - SEX
        - DISCHARGE STATUS
        - NAMA_PASIEN
        - MRN
        - UMUR TAHUN
        - UMUR HARI
        - SEP
        - DIAGLIST 1
        """)
    
    with st.expander("RL 5 Fields"):
        st.write("""
        - SEX
        - DISCHARGE STATUS
        - NAMA_PASIEN
        - MRN
        - UMUR TAHUN
        - UMUR HARI
        - SEP
        - DIAGLIST 1
        - DIAGLIST 2
        """)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📂 Load Data", "🔄 Transform", "🔧 XLOOKUP", "🤖 AI Analysis"])

with tab1:
    st.header("Load Files")
    
    col1, col2 = st.columns(2)
    with col1:
        header_row = st.number_input("Baris Header (mulai dari 1)", min_value=1, value=1)
    
    uploaded_files = st.file_uploader(
        "Pilih file (max 5)",
        accept_multiple_files=True,
        type=['xlsx', 'xls', 'txt', 'csv', 'json', 'parquet', 'feather', 'ndjson', 'jsonl']
    )
    
    if uploaded_files:
        if len(uploaded_files) > 5:
            st.warning("Maksimal 5 file dapat dipilih")
            uploaded_files = uploaded_files[:5]
        
        if st.button("Load Files", key="load_btn"):
            dfs = []
            for uploaded_file in uploaded_files:
                df = load_excel_file(uploaded_file, header_row)
                if df is not None:
                    dfs.append(df)
            
            if dfs:
                st.session_state.df = pd.concat(dfs, ignore_index=True)
                st.session_state.original_df = st.session_state.df.copy()
                st.session_state.pivot_df = None
                st.success(f"Data berhasil dimuat! {len(st.session_state.df)} baris, {len(st.session_state.df.columns)} kolom")
                st.dataframe(st.session_state.df.head(20), use_container_width=True)
            else:
                st.error("Gagal memuat file")
    
    # Download sample data
    if st.session_state.df is not None:
        col1, col2 = st.columns(2)
        with col1:
            csv = st.session_state.df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="data.csv",
                mime="text/csv"
            )
        
        with col2:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                st.session_state.df.to_excel(writer, index=False, sheet_name='Sheet1')
                if st.session_state.pivot_df is not None:
                    st.session_state.pivot_df.to_excel(writer, index=False, sheet_name='Sheet2')
            
            st.download_button(
                label="Download as Excel",
                data=buffer.getvalue(),
                file_name="data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with tab2:
    st.header("Transform Data")
    
    if st.session_state.df is None:
        st.warning("⚠️ Silakan load data terlebih dahulu")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("1. Select Columns")
            cols = list(st.session_state.df.columns)
            selected_cols = st.multiselect(
                "Pilih kolom yang ditampilkan:",
                cols,
                default=cols
            )
            
            if st.button("Use Selected Columns"):
                st.session_state.df = st.session_state.original_df[selected_cols].copy()
                st.success("Kolom berhasil diperbarui")
        
        with col2:
            if st.button("Reset to Original"):
                st.session_state.df = st.session_state.original_df.copy()
                st.session_state.pivot_df = None
                st.success("Data direset ke kondisi awal")
        
        st.divider()
        
        # Filter Data
        st.subheader("2. Filter Data")
        filter_cols = st.multiselect("Pilih kolom untuk filter:", list(st.session_state.df.columns))
        
        if filter_cols:
            filters = {}
            for col in filter_cols:
                if is_date_column(col, st.session_state.df):
                    years = pd.to_datetime(st.session_state.df[col], errors='coerce').dt.year.dropna().unique()
                    years = sorted([int(y) for y in years if pd.notna(y)])
                    selected_year = st.selectbox(f"Tahun untuk '{col}':", years, key=f"year_{col}")
                    filters[col] = ('year', selected_year)
                else:
                    unique_vals = sorted(st.session_state.df[col].dropna().astype(str).unique())
                    selected_val = st.selectbox(f"Nilai untuk '{col}':", unique_vals, key=f"val_{col}")
                    filters[col] = ('value', selected_val)
            
            if st.button("Apply Filter"):
                filtered_df = st.session_state.df.copy()
                try:
                    for col, (filter_type, filter_val) in filters.items():
                        if filter_type == 'year':
                            date_col = pd.to_datetime(filtered_df[col], errors='coerce')
                            filtered_df = filtered_df[date_col.dt.year == filter_val]
                        else:
                            filtered_df = filtered_df[filtered_df[col].astype(str) == filter_val]
                    
                    st.session_state.df = filtered_df
                    st.success(f"Filter diterapkan! {len(filtered_df)} baris tersisa")
                    st.dataframe(filtered_df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        
        st.divider()
        
        # Split Column
        st.subheader("3. Split Kolom")
        split_col = st.selectbox("Pilih kolom untuk di-split:", list(st.session_state.df.columns))
        
        if st.button("Split by ;"):
            try:
                import re
                def smart_split(val):
                    if pd.isna(val):
                        return []
                    s = str(val)
                    match = re.search(r"\[(.*?)\]", s)
                    if match:
                        return match.group(1).split(";")
                    return s.split(";")
                
                new_cols = st.session_state.df[split_col].apply(lambda x: pd.Series(smart_split(x)))
                new_cols.columns = [f"{split_col}_{i+1}" for i in range(new_cols.shape[1])]
                st.session_state.df = st.session_state.df.drop(columns=[split_col]).join(new_cols)
                st.success("Kolom berhasil di-split!")
                st.dataframe(st.session_state.df, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
        
        st.divider()
        
        # Pivot Table
        st.subheader("4. Pivot Table")
        cols = list(st.session_state.df.columns)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            rows = st.selectbox("Rows:", cols)
        with col2:
            columns = st.selectbox("Columns:", cols)
        with col3:
            values = st.selectbox("Values:", cols)
        with col4:
            aggfunc = st.selectbox("Aggfunc:", ["sum", "mean", "count", "min", "max"])
        
        if st.button("Create Pivot"):
            try:
                pivot = pd.pivot_table(
                    st.session_state.df,
                    index=rows,
                    columns=columns,
                    values=values,
                    aggfunc=aggfunc,
                    fill_value=0
                )
                pivot = pivot.reset_index()
                st.session_state.pivot_df = pivot
                st.success("Pivot berhasil dibuat!")
                st.dataframe(pivot, use_container_width=True)
                
                # Sort option
                if st.button("Sort Descending"):
                    numeric_cols = pivot.select_dtypes(include='number').columns
                    if len(numeric_cols) > 0:
                        sort_col = numeric_cols[0]
                        pivot = pivot.sort_values(by=sort_col, ascending=False)
                        st.session_state.pivot_df = pivot
                        st.dataframe(pivot, use_container_width=True)
                    else:
                        st.warning("Tidak ada kolom numerik untuk diurutkan")
            except Exception as e:
                st.error(f"Error: {e}")
        
        st.divider()
        st.subheader("Preview Data")
        st.dataframe(st.session_state.df, use_container_width=True)

with tab3:
    st.header("XLOOKUP - Reference Lookup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Load Reference File")
        ref_file = st.file_uploader(
            "Upload file referensi XLOOKUP",
            type=['xlsx', 'xls', 'csv'],
            key="ref_file"
        )
        
        if ref_file:
            header_row = st.number_input("Baris Header (mulai dari 1) untuk referensi", min_value=1, value=1, key="ref_header")
            
            if st.button("Load Reference", key="load_ref"):
                ref_df = load_excel_file(ref_file, header_row)
                if ref_df is not None:
                    st.session_state.ref_df = ref_df
                    st.success("File referensi berhasil dimuat!")
                    st.dataframe(ref_df.head(10), use_container_width=True)
    
    with col2:
        if st.session_state.ref_df is not None and st.session_state.df is not None:
            st.subheader("XLOOKUP Configuration")
            
            main_key = st.selectbox(
                "Kolom kunci di data utama:",
                list(st.session_state.df.columns),
                key="main_key"
            )
            
            ref_key = st.selectbox(
                "Kolom kunci di referensi:",
                list(st.session_state.ref_df.columns),
                key="ref_key"
            )
            
            ref_vals = st.multiselect(
                "Kolom hasil dari referensi:",
                list(st.session_state.ref_df.columns),
                key="ref_vals"
            )
            
            if st.button("Do XLOOKUP"):
                try:
                    main_series = st.session_state.df[main_key].astype(str)
                    ref_key_series = st.session_state.ref_df[ref_key].astype(str)
                    
                    for ref_val in ref_vals:
                        ref_val_series = st.session_state.ref_df[ref_val]
                        ref_dict = pd.Series(ref_val_series.values, index=ref_key_series).to_dict()
                        st.session_state.df[f"XLOOKUP_{ref_val}"] = main_series.map(ref_dict)
                    
                    st.success("XLOOKUP berhasil diterapkan!")
                    st.dataframe(st.session_state.df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

with tab4:
    st.header("🤖 AI Analysis")
    
    if st.session_state.df is None:
        st.warning("⚠️ Silakan load data terlebih dahulu")
    else:
        st.write("Tanya AI tentang data Anda menggunakan OpenRouter API")
        
        prompt = st.text_area(
            "Masukkan pertanyaan atau instruksi untuk AI:",
            height=5,
            placeholder="Contoh: Berapa total pasien per kategori discharge status?"
        )
        
        if st.button("Send to AI 🚀"):
            if not prompt.strip():
                st.warning("Prompt tidak boleh kosong!")
            else:
                try:
                    with st.spinner("Menunggu respons dari AI..."):
                        sample_data = st.session_state.df.head(10).to_csv(index=False)
                        full_prompt = (
                            f"Saya punya data seperti berikut (hanya 10 baris pertama):\n\n{sample_data}\n\n"
                            f"Tolong bantu dengan instruksi berikut:\n{prompt}\n"
                        )
                        
                        headers = {
                            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        
                        data = {
                            "model": "openai/gpt-3.5-turbo",
                            "messages": [{"role": "user", "content": full_prompt}],
                            "temperature": 0.3
                        }
                        
                        response = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers=headers,
                            json=data,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            ai_reply = result["choices"][0]["message"]["content"]
                            st.success("Respons dari AI:")
                            st.write(ai_reply)
                        else:
                            st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.write("💡 Dibuat dengan Streamlit | Powered by AI")
