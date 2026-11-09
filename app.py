import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Sistem Pakar Penyakit Mata",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PENGETAHUAN DARI JURNAL (Fitriyani Umar & Aisyah, 2023)
# ============================================================
DISEASES = {
    "PM01": "Katarak",
    "PM02": "Glaukoma",
    "PM03": "Konjungtivitis",
    "PM04": "Refraksi",
    "PM05": "Gangguan Retina",
}
SYMPTOMS = {
    "K01": "Pandangan kabur seperti berkabut",
    "K02": "Penurunan penglihatan pada malam hari",
    "K03": "Rasa silau saat melihat lampu mobil, matahari, atau lampu",
    "K04": "Warna di sekitar terlihat memudar",
    "G01": "Nyeri pada mata",
    "G02": "Sakit kepala",
    "G03": "Melihat bayangan lingkaran di sekeliling cahaya",
    "G04": "Mata memerah",
    "G05": "Mual atau muntah",
    "M01": "Mata merah di satu atau kedua mata",
    "M02": "Mata sering terasa gatal dan seperti ada pasir",
    "M03": "Mata mengeluarkan cairan kental yang membentuk kerak pagi hari",
    "R01": "Sering menyipitkan mata saat melihat",
    "R02": "Mata terasa tegang",
    "R03": "Sakit kepala (refraksi)",
    "N01": "Melihat kilatan cahaya",
    "N02": "Sensitif terhadap cahaya",
    "N03": "Terganggunya kemampuan membedakan warna",
}
EXPERT_CF = {
    "K01": (0.8, 0.2, 0.6), "K02": (1.0, 0.1, 0.9), "K03": (0.8, 0.2, 0.6), "K04": (1.0, 0.1, 0.9),
    "G01": (1.0, 0.1, 0.9), "G02": (0.8, 0.2, 0.6), "G03": (0.8, 0.2, 0.6), "G04": (1.0, 0.1, 0.9), "G05": (0.8, 0.1, 0.7),
    "M01": (0.8, 0.3, 0.5), "M02": (0.6, 0.5, 0.1), "M03": (0.8, 0.2, 0.6),
    "R01": (0.8, 0.2, 0.6), "R02": (0.8, 0.2, 0.6), "R03": (1.0, 0.2, 0.8),
    "N01": (0.8, 0.1, 0.7), "N02": (0.8, 0.3, 0.5), "N03": (0.6, 0.2, 0.4),
}
RULES = {
    "PM01": ["K01", "K02", "K03", "K04"],
    "PM02": ["G01", "G02", "G03", "G04", "G05"],
    "PM03": ["M01", "M02", "M03"],
    "PM04": ["R01", "R02", "R03"],
    "PM05": ["N01", "N02", "N03"],
}
DISEASE_INFO = {
    "PM01": {"icon": "🌫️", "desc": "Lensa mata keruh sehingga pandangan kabur & silau perlahan.", "tips": ["Lindungi mata dari sinar UV dengan kacamata hitam", "Periksa rutin, terutama jika usia > 45 tahun", "Segera ke dokter mata bila ketajaman menurun"]},
    "PM02": {"icon": "⚠️", "desc": "Tekanan dalam bola mata tinggi, berisiko merusak saraf mata.", "tips": ["Segera periksa tekanan bola mata (tonometri)", "Kontrol teratur bila ada riwayat keluarga glaukoma", "Jangan pakai obat tetes mata tanpa resep dokter"]},
    "PM03": {"icon": "👁️", "desc": "Peradangan selaput putih mata, mata merah & gatal.", "tips": ["Jaga kebersihan tangan, hindari mengucek mata", "Jangan berbagi handuk / alat kosmetik", "Istirahatkan mata, waspada gejala menular"]},
    "PM04": {"icon": "🎯", "desc": "Gangguan fokus / bias karena bentuk bola mata tidak normal.", "tips": ["Terapkan aturan 20-20-20 saat menatap layar", "Gunakan kacamata ukuran resep terbaru", "Atur pencahayaan ruangan"]},
    "PM05": {"icon": "✨", "desc": "Gangguan pada retina (lapisan peka cahaya di belakang mata).", "tips": ["Kontrol gula darah & tekanan darah rutin", "Segera ke dokter bila melihat kilatan cahaya", "Hindari benturan/guncangan pada mata"]},
}

# ============================================================
# CSS MINIMAL — hanya untuk blok HTML murni (hero/kartu)
# TIDAK menyentuh widget Streamlit (slider/sidebar/button/header)
# ============================================================
CSS = """
<style>
.hero{background:linear-gradient(135deg,#2563EB,#3B82F6,#60A5FA);border-radius:24px;padding:32px 28px;color:#fff;box-shadow:0 12px 32px rgba(37,99,235,.25);}
.hero h1{font-size:2rem;font-weight:800;margin-bottom:8px;line-height:1.15;}
.hero p{opacity:.95;font-size:1rem;max-width:700px;line-height:1.6;}
.hero-badge{display:inline-flex;gap:8px;align-items:center;background:rgba(255,255,255,.22);border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:6px 14px;font-size:.85rem;font-weight:600;}
.eyebrow{color:#2563EB;font-weight:800;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;margin-bottom:6px;}
.title{font-size:1.6rem;font-weight:800;color:#0F172A;margin-bottom:4px;}
.subtitle{color:#64748B;font-size:.96rem;margin-bottom:16px;}
.card{background:#fff;border:1px solid #E2E8F0;border-radius:18px;padding:18px;box-shadow:0 4px 16px rgba(15,23,42,.05);}
.card h3{font-size:1.02rem;margin:8px 0 6px 0;color:#0F172A;}
.card p{font-size:.92rem;color:#475569;line-height:1.5;margin:0;}
.pill{display:inline-block;background:#EFF6FF;color:#2563EB;border:1px solid #DBEAFE;border-radius:999px;padding:4px 10px;font-size:.78rem;font-weight:700;}
.footer{text-align:center;color:#94A3B8;font-size:.82rem;margin-top:28px;padding:18px 0 6px 0;border-top:1px solid #E2E8F0;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

def combine_cf(cf_list):
    """Gabungkan daftar CF menggunakan rumus kombinasi CF."""
    if not cf_list:
        return 0
    r = cf_list[0]
    for cf in cf_list[1:]:
        r = r + cf * (1 - r)
    return r

def calculate_cf_for_disease(selected_symptoms):
    """Hitung nilai CF untuk tiap penyakit."""
    rows = []
    for dc, codes in RULES.items():
        lst = []
        for c in codes:
            if c in selected_symptoms and selected_symptoms[c] > 0:
                lst.append(EXPERT_CF[c][2] * selected_symptoms[c])
        combined = combine_cf(lst)
        rows.append({"Kode Penyakit": dc, "Nama Penyakit": DISEASES[dc],
                     "CF Gejala": [round(x, 3) for x in lst],
                     "Hasil CF": round(combined, 4),
                     "Persentase": f"{combined*100:.2f}%"})
    df = pd.DataFrame(rows)
    return df.sort_values(by="Hasil CF", ascending=False).reset_index(drop=True)

def get_group(code):
    return {"K": ("Katarak", "🌫️"), "G": ("Glaukoma", "⚠️"), "M": ("Konjungtivitis", "👁️"),
            "R": ("Refraksi", "🎯"), "N": ("Gangguan Retina", "✨")}.get(code[0], ("Gejala", "•"))

def confidence_label(cf):
    if cf >= 0.8: return ("Tingkat Keyakinan Sangat Tinggi", "Segera konsultasikan ke dokter mata.")
    if cf >= 0.6: return ("Tingkat Keyakinan Cukup Tinggi", "Disarankan melakukan pemeriksaan lanjutan.")
    if cf > 0: return ("Tingkat Keyakinan Rendah", "Tetap pantau gejala, konsultasikan bila berlanjut.")
    return ("Belum Ada Gejala Terisi", "Isi gejala di menu Diagnosa terlebih dahulu.")

# ============================================================
# SIDEBAR — tombol sederhana (stabil)
# ============================================================
if "page" not in st.session_state:
    st.session_state["page"] = "Beranda"

st.sidebar.markdown("### 👁️ Sistem Pakar Mata")
st.sidebar.caption("Forward Chaining + Certainty Factor")
st.sidebar.divider()

for key, label in [("Beranda", "🏠 Beranda"), ("Diagnosa", "🩺 Diagnosa"), ("Hasil Diagnosa", "📊 Hasil Diagnosa")]:
    is_active = st.session_state["page"] == key
    btn_type = "primary" if is_active else "secondary"
    if st.sidebar.button(label, key=f"nav_{key}", type=btn_type, use_container_width=True):
        st.session_state["page"] = key
        st.rerun()

menu = st.session_state["page"]
st.sidebar.divider()
st.sidebar.markdown("### 📌 Dasar Teori")
st.sidebar.write("Fitriyani Umar & Aisyah (2023) — Sistem Pakar Berbasis Web untuk Diagnosa Awal Penyakit Mata dengan Penerapan Forward Chaining dan Certainty Factor.")
st.sidebar.caption("⚠️ Hasil sistem ini pendukung, bukan pengganti diagnosis dokter.")
st.sidebar.caption("Cara pakai: klik Diagnosa → geser slider → Proses Diagnosa → Hasil Diagnosa.")

# ============================================================
# BERANDA — modern putih-biru, wall of text minimal
# ============================================================
if menu == "Beranda":
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">👁️ Metode: Forward Chaining &amp; Certainty Factor</div>
      <h1>Diagnosa Awal Penyakit Mata<br>Lebih Cepat &amp; Terarah</h1>
      <p>Isi tingkat keyakinan gejala yang kamu rasakan, sistem akan mengombinasikan CF pakar
      dari jurnal dan menampilkan penyakit yang paling mungkin beserta persentasenya.</p>
      <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
        <span class="hero-badge">✅ 5 Penyakit</span><span class="hero-badge">✅ 18 Gejala Terukur</span><span class="hero-badge">✅ Berbasis Jurnal 2023</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🩺 Mulai Diagnosa", key="home_go_diagnosa", type="primary", use_container_width=True):
            st.session_state["page"] = "Diagnosa"; st.rerun()
    with c2:
        if st.button("📊 Lihat Hasil Diagnosa", key="home_go_hasil", type="secondary", use_container_width=True):
            st.session_state["page"] = "Hasil Diagnosa"; st.rerun()

    st.divider()
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Penyakit Didiagnosis", "5")
    with m2: st.metric("Gejala Terdaftar", "18")
    with m3: st.metric("Metode", "Forward Chaining + CF")

    st.markdown('<div class="eyebrow">CARA KERJA</div><div class="title">Tiga Langkah Mudah</div><div class="subtitle">Iruti langkahnya - selesai dalam kurang dari 1 menit.</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1: st.markdown('<div class="card"><h3>🩺 1. Pilih Diagnosa</h3><p>Masuk ke menu Diagnosa untuk mengisi gejala.</p></div>', unsafe_allow_html=True)
    with s2: st.markdown('<div class="card"><h3>🎚️ 2. Nilai Keyakinan</h3><p>Geser slider 0 (tidak yakin) sampai 1 (sangat yakin) di dalam form.</p></div>', unsafe_allow_html=True)
    with s3: st.markdown('<div class="card"><h3>📊 3. Lihat Hasil</h3><p>Sistem menghitung CF dan menampilkan penyakit paling mungkin beserta grafiknya.</p></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="eyebrow">PENYAKIT</div><div class="title">5 Penyakit yang Didiagnosis</div>', unsafe_allow_html=True)
    for code, name in DISEASES.items():
        info = DISEASE_INFO[code]
        st.markdown(f'<div class="card" style="margin-bottom:10px;"><span class="pill">{code}</span><h3>{info["icon"]} {name}</h3><p>{info["desc"]}</p><p><small>Gejala: {", ".join(RULES[code])}</small></p></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="eyebrow">BASIS PENGETAHUAN</div><div class="title">Aturan Forward Chaining</div>', unsafe_allow_html=True)
    rule_rows = [{"Kode Penyakit": dis, "Nama Penyakit": DISEASES[dis], "Gejala": ", ".join(syms)} for dis, syms in RULES.items()]
    st.dataframe(pd.DataFrame(rule_rows), use_container_width=True, hide_index=True, key="rule_table")

# ============================================================
# DIAGNOSA — form supaya tidak reload tiap geser slider
# ============================================================
elif menu == "Diagnosa":
    st.markdown('<div class="eyebrow">FORM DIAGNOSA</div><div class="title">Nilai Keyakinan Kamu</div><div class="subtitle">Geser slider di dalam form ini, lalu klik Proses Diagnosa. Halaman tidak akan reload tiap geser.</div>', unsafe_allow_html=True)
    st.info("0.0 = Tidak yakin - 0.3 = Agak yakin - 0.6 = Cukup yakin - 0.9 = Hampir pasti - 1.0 = Sangat yakin")

    grouped = {}
    for code in SYMPTOMS:
        g, icon = get_group(code)
        grouped.setdefault(f"{icon} {g}", []).append(code)

    with st.form("diagnosa_form", clear_on_submit=False):
        selected_symptoms = {}
        for group_name, codes in grouped.items():
            st.markdown(f"### {group_name}")
            for code in codes:
                selected_symptoms[code] = st.slider(
                    f"{code} - {SYMPTOMS[code]}",
                    min_value=0.0, max_value=1.0, value=0.0, step=0.1, format="%.1f", key=f"sym_{code}"
                )
            st.divider()
        submitted = st.form_submit_button("🔍 Proses Diagnosa", type="primary", use_container_width=True)

    if submitted:
        filled = sum(1 for v in selected_symptoms.values() if v > 0)
        if filled == 0:
            st.warning("Isi minimal 1 gejala dulu ya - geser slider di atas.")
        else:
            st.session_state["result_df"] = calculate_cf_for_disease(selected_symptoms)
            st.success(f"Diagnosa selesai! {filled} gejala dianalisis. Klik menu Hasil Diagnosa di sidebar untuk melihat grafik & hasil lengkapnya.")

    def _reset_form():
        for code in SYMPTOMS:
            st.session_state[f"sym_{code}"] = 0.0
        if "result_df" in st.session_state:
            del st.session_state["result_df"]

    st.button("↺ Reset Form", key="btn_reset", use_container_width=True, on_click=_reset_form)

# ============================================================
# HASIL — hanya di sini grafik & hasil muncul (tidak di Diagnosa)
# ============================================================
elif menu == "Hasil Diagnosa":
    st.markdown('<div class="eyebrow">HASIL DIAGNOSA</div><div class="title">Kesimpulan Penyakit Mata</div><div class="subtitle">Nilai CF tertinggi adalah penyakit yang paling mungkin berdasarkan gejala yang kamu isi.</div>', unsafe_allow_html=True)

    if "result_df" not in st.session_state:
        st.info("Belum ada hasil diagnosa. Silakan isi gejala di menu Diagnosa lalu klik Proses Diagnosa terlebih dahulu.")
    else:
        df = st.session_state["result_df"]
        top = df.iloc[0]
        info = DISEASE_INFO.get(top["Kode Penyakit"], {"icon": "👁️", "desc": "", "tips": []})
        label, advice = confidence_label(float(top["Hasil CF"]))

        st.success(f"{info['icon']} Penyakit paling mungkin: {top['Nama Penyakit']} ({top['Persentase']})")
        st.markdown(f"**{label}** - {advice}")
        st.markdown(f"**Nilai CF:** {top['Hasil CF']:.4f} ({top['Persentase']})")
        st.progress(float(top["Hasil CF"]))

        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Nilai CF Tertinggi", f"{top['Hasil CF']:.4f}")
        with m2: st.metric("Gejala Berkontribusi", f"{len(top['CF Gejala'])} gejala")
        with m3: st.metric("Penyakit Dibandingkan", "5 penyakit")

        st.divider()
        st.markdown("### Perbandingan Semua Penyakit - Grafik Otomatis")
        st.caption("Grafik ini dibuat otomatis dari data hasil diagnosa (nilai CF).")

        # Matplotlib PNG (stabil, tanpa Altair/Vega yang error di Python 3.14)
        plot_df = df.copy()
        fig, ax = plt.subplots(figsize=(9, 3.6))
        colors = ["#2563EB" if name == top["Nama Penyakit"] else "#93C5FD" for name in plot_df["Nama Penyakit"]]
        bars = ax.barh(plot_df["Nama Penyakit"], plot_df["Hasil CF"], color=colors, height=0.55, edgecolor="white")
        ax.invert_yaxis()
        ax.set_xlim(0, 1.0)
        ax.set_xlabel("Nilai Certainty Factor (CF)", fontsize=10)
        ax.set_title("Perbandingan CF 5 Penyakit Mata", fontsize=12, fontweight="bold", pad=12)
        ax.grid(axis="x", linestyle="--", alpha=0.35)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for bar, cf in zip(bars, plot_df["Hasil CF"]):
            ax.text(bar.get_width() + 0.015, bar.get_y() + bar.get_height() / 2, f"{cf*100:.1f}%", va="center", ha="left", fontsize=9, fontweight="bold", color="#2563EB")
        st.pyplot(fig)
        plt.close(fig)

        st.markdown("### Detail Perhitungan CF")
        st.dataframe(df, use_container_width=True, hide_index=True, key="result_df_view")

        st.markdown("### Rekomendasi & Tips Pencegahan")
        st.write(f"Untuk {top['Nama Penyakit']}:")
        for t in info["tips"]:
            st.write(f"- {t}")

        if top["Hasil CF"] >= 0.8:
            st.success("Tingkat keyakinan sangat tinggi - segera konsultasikan ke dokter mata.")
        elif top["Hasil CF"] >= 0.6:
            st.warning("Tingkat keyakinan cukup tinggi - disarankan melakukan pemeriksaan lanjutan.")
        else:
            st.info("Tingkat keyakinan rendah - tetap pantau gejala dan konsultasikan bila berlanjut.")

        st.write("Catatan: Ini diagnosa awal berbasis sistem pakar, bukan diagnosis medis final. Konsultasikan ke dokter mata untuk pemeriksaan lengkap.")

st.markdown("---")
st.caption("Sistem Pakar Diagnosa Awal Penyakit Mata - Forward Chaining & Certainty Factor - Fitriyani Umar & Aisyah (2023)")
