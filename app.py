# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os

# Konfigurasi halaman utama Streamlit
st.set_page_config(
    page_title="Sistem Pakar Kepribadian & Rekomendasi Bidang Kerja",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS eksternal dari style.css
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ==========================================
# DEFINISI DATA (HARDCODED DICTIONARIES)
# ==========================================

# 1. Daftar Fakta/Gejala (G) - MUTLAK SESUAI JURNAL
FAKTA_GEJALA = {
    "G01": "Saya sangat mudah berteman dan akrab dengan orang baru",
    "G02": "Saya senang dan merasa nyaman saat menjadi pusat perhatian",
    "G03": "Saya sangat suka bercerita panjang lebar mengenai banyak hal",
    "G04": "Saya cenderung melihat sisi positif dan optimis dalam segala hal",
    "G05": "Saya suka menceriakan suasana dan menghibur orang-orang di sekitar saya",
    "G06": "Saya cenderung menuntut kesempurnaan (perfeksionis) dalam pekerjaan",
    "G07": "Saya selalu menyusun rencana kegiatan secara rinci dan detail",
    "G08": "Saya selalu memikirkan konsekuensi secara mendalam sebelum bertindak",
    "G09": "Saya cenderung sensitif dan memikirkan secara mendalam masukan atau kritik orang lain",
    "G10": "Saya merasa cukup sulit untuk melupakan atau memaafkan kesalahan orang lain",
    "G11": "Saya sebisa mungkin menghindari konfrontasi atau konflik dengan orang lain",
    "G12": "Saya sangat mudah menyesuaikan diri ketika berada di lingkungan baru",
    "G13": "Saya cenderung tenang dan jarang menunjukkan emosi atau kemarahan saya",
    "G14": "Saya memiliki tingkat kesabaran yang tinggi dalam menghadapi sikap orang lain",
    "G15": "Saya cenderung pasif dan lebih memilih mengikuti keputusan kelompok",
    "G16": "Saya suka mengambil inisiatif untuk memimpin dan mengatur jalannya tugas",
    "G17": "Saya dapat mengambil keputusan yang tegas dalam waktu singkat",
    "G18": "Saya tetap tenang dan cepat bertindak mencari solusi dalam kondisi darurat",
    "G19": "Saya memiliki visi dan target pencapaian yang jelas untuk masa depan saya",
    "G20": "Saya merasa bersemangat ketika menghadapi tantangan atau tugas baru",
    "G22": "Saya mudah terbawa suasana atau terpengaruh oleh kondisi emosional sekitar",
    "G23": "Saya selalu mengumpulkan fakta dan data lengkap sebelum mengambil kesimpulan",
    "G24": "Saya sering kali merasa cemas berlebihan ketika memikirkan masa depan",
    "G25": "Saya rela mengalah dan menahan pendapat pribadi demi kedamaian hubungan",
    "G26": "Saya lebih suka berkontribusi di belakang layar daripada tampil di depan",
    "G27": "Saya berani menyuarakan kebenaran atau pendapat yang kurang populer",
    "G28": "Saya merasa percaya diri saat berbicara atau presentasi di hadapan publik",
    "G29": "Saya merasa sangat senang jika pekerjaan berjalan sesuai rencana semula",
    "G30": "Saya merasa lebih terpacu dan berenergi saat bersaing dengan orang lain"
}

# Pembagian Pertanyaan untuk Kuesioner Bertahap (4 Bagian)
STEP_QUESTIONS = {
    1: {
        "title": "Karakter Sosial & Interaksi (Sanguinis)",
        "keys": ["G01", "G02", "G03", "G04", "G05", "G22", "G28"]
    },
    2: {
        "title": "Karakter Analitis & Kerja Detail (Melankolis)",
        "keys": ["G06", "G07", "G08", "G09", "G10", "G23", "G24", "G29"]
    },
    3: {
        "title": "Karakter Emosi & Keharmonisan (Plegmatis)",
        "keys": ["G11", "G12", "G13", "G14", "G15", "G25", "G26"]
    },
    4: {
        "title": "Karakter Kepemimpinan & Kompetisi (Koleris)",
        "keys": ["G16", "G17", "G18", "G19", "G20", "G27", "G30"]
    }
}

# 2. Definis Aturan (Rules) R1 - R12 - MUTLAK SESUAI JURNAL
# K1 = Sanguinis, K2 = Melankolis, K3 = Plegmatis, K4 = Koleris
ATURAN_INFERENSI = {
    "R1": {"facts": ["G01", "G02", "G03", "G04", "G05"], "target": "K1", "target_name": "Sanguinis"},
    "R2": {"facts": ["G01", "G02", "G22", "G28"], "target": "K1", "target_name": "Sanguinis"},
    "R3": {"facts": ["G03", "G04", "G22", "G28"], "target": "K1", "target_name": "Sanguinis"},
    "R4": {"facts": ["G06", "G07", "G08", "G09", "G10"], "target": "K2", "target_name": "Melankolis"},
    "R5": {"facts": ["G06", "G07", "G23", "G29"], "target": "K2", "target_name": "Melankolis"},
    "R6": {"facts": ["G08", "G09", "G24", "G29"], "target": "K2", "target_name": "Melankolis"},
    "R7": {"facts": ["G11", "G12", "G13", "G14", "G15"], "target": "K3", "target_name": "Plegmatis"},
    "R8": {"facts": ["G11", "G13", "G25", "G26"], "target": "K3", "target_name": "Plegmatis"},
    "R9": {"facts": ["G12", "G14", "G25", "G26"], "target": "K3", "target_name": "Plegmatis"},
    "R10": {"facts": ["G16", "G17", "G18", "G19", "G20"], "target": "K4", "target_name": "Koleris"},
    "R11": {"facts": ["G16", "G17", "G27", "G30"], "target": "K4", "target_name": "Koleris"},
    "R12": {"facts": ["G18", "G19", "G27", "G30"], "target": "K4", "target_name": "Koleris"},
}

# 3. Data Kepribadian & Generalisasi Rekomendasi Bidang Kerja
DETAIL_KEPRIBADIAN = {
    "K1": {
        "nama": "Sanguinis (The Popular)",
        "badge_class": "badge-sanguinis",
        "deskripsi": "Tipe kepribadian Sanguinis dikenal sebagai pribadi yang optimis, ceria, penuh energi, berjiwa sosial tinggi, dan senang berkomunikasi. Anda sangat pandai mencairkan suasana, menyukai variasi, dan beradaptasi dalam lingkungan sosial yang dinamis.",
        "karakteristik": "Ekspresif, komunikatif, antusias, bersahabat, namun kadang mudah terbawa suasana atau kurang disiplin pada detail.",
        "rekomendasi": [
            "**Komunikasi & Hubungan Masyarakat (Public Relations)**: Menghubungkan organisasi dengan publik melalui kemampuan interpersonal yang persuasif.",
            "**Manajemen Sumber Daya Manusia (HRD)**: Terutama bagian rekrutmen, pelatihan, dan hubungan karyawan yang membutuhkan kehangatan komunikasi.",
            "**Industri Kreatif & Penyiaran**: Content creator, presenter, periklanan, penulisan kreatif, atau penasihat media sosial.",
            "**Pariwisata & Event Organizer**: Pengelolaan acara, kepemanduan wisata, dan perencanaan hiburan.",
            "**Pelayanan Pelanggan (Customer Success)**: Membangun kepuasan dan loyalitas pelanggan secara langsung."
        ],
        "emoji": ""
    },
    "K2": {
        "nama": "Melankolis (The Perfect)",
        "badge_class": "badge-melankolis",
        "deskripsi": "Tipe kepribadian Melankolis dikenal sangat analitis, perfeksionis, teratur, disiplin, dan teliti. Anda menyukai segala sesuatu berjalan sesuai rencana, pandai memecahkan masalah kompleks berbasis data, dan memiliki standar kualitas yang tinggi.",
        "karakteristik": "Teratur, detail, analitis, artistik, sensitif, namun kadang cenderung cemas berlebihan atau terlalu kritis terhadap diri sendiri.",
        "rekomendasi": [
            "**Keuangan & Akuntansi**: Penyusunan anggaran, audit keuangan, dan pembukuan presisi tinggi yang menuntut akurasi mutlak.",
            "**Analisis Data & Riset Pasar**: Menganalisis data statistik, menemukan tren tersembunyi, dan melakukan pemodelan data.",
            "**Quality Assurance (QA) & Kontrol Mutu**: Pengujian kualitas sistem, kepatuhan produk terhadap regulasi, dan sertifikasi standar.",
            "**Administrasi Presisi**: Manajemen database, pengarsipan dokumen hukum/korporat, dan penyusunan SOP.",
            "**Penelitian & Riset Ilmiah (R&D)**: Bekerja di laboratorium atau riset akademis yang membutuhkan fokus tinggi dan kesabaran."
        ],
        "emoji": ""
    },
    "K3": {
        "nama": "Plegmatis (The Peaceful)",
        "badge_class": "badge-plegmatis",
        "deskripsi": "Tipe kepribadian Plegmatis dikenal tenang, sabar, loyal, damai, dan menghindari konflik. Anda adalah pendengar yang sangat baik, kooperatif dalam tim, konsisten dalam bekerja, dan mampu menjaga keharmonisan kelompok.",
        "karakteristik": "Tenang, sabar, diplomatis, pendengar baik, stabil, namun terkadang pasif atau kurang berani mengambil risiko besar.",
        "rekomendasi": [
            "**Pelayanan Masyarakat & Pekerja Sosial**: Konseling, mediasi hubungan masyarakat, atau pendampingan komunitas sosial.",
            "**Kesehatan & Medis**: Perawat, terapis fisik, apoteker, atau psikolog yang memerlukan empati mendalam dan ketenangan.",
            "**Pendidikan**: Guru anak usia dini, pengajar sekolah dasar, atau tutor bimbingan belajar yang mendidik secara sabar.",
            "**Dukungan Teknis (Technical Support)**: Membantu memecahkan masalah klien secara sabar melalui telepon atau chat.",
            "**Logistik & Manajemen Supply Chain**: Koordinasi pengiriman barang dan operasional rutin yang membutuhkan stabilitas."
        ],
        "emoji": ""
    },
    "K4": {
        "nama": "Koleris (The Powerful)",
        "badge_class": "badge-koleris",
        "deskripsi": "Tipe kepribadian Koleris dikenal sebagai pemimpin alami yang tegas, visioner, fokus pada hasil akhir, mandiri, dan menyukai tantangan baru. Anda cepat mengambil tindakan, percaya diri tinggi, dan bersemangat ketika bersaing.",
        "karakteristik": "Tegas, visioner, pemimpin, kompetitif, fokus hasil, namun kadang tidak sabaran atau kurang sensitif terhadap emosi orang lain.",
        "rekomendasi": [
            "**Teknologi Informasi & Rekayasa Perangkat Lunak**: Lead Developer, IT Solution Architect, atau pengarah strategi teknologi.",
            "**Manajemen Proyek (Project Management)**: Memimpin eksekusi proyek skala besar dengan target ketat dan koordinasi lintas divisi.",
            "**Kewirausahaan (Entrepreneurship)**: Membangun bisnis sendiri, merintis startup, dan mengambil keputusan bisnis yang berisiko.",
            "**Teknik (Engineering)**: Desain industri, manajemen pabrik, atau perancangan infrastruktur teknik sipil.",
            "**Kepemimpinan Eksekutif**: Posisi manajemen strategis seperti Manager, Direktur, atau Chief Officer organisasi."
        ],
        "emoji": ""
    }
}

# ==========================================
# LOGIKA INFERENSI FORWARD CHAINING
# ==========================================

def hitung_kepribadian(pilihan_user):
    """
    Fungsi untuk memproses data input pengguna menggunakan metode Forward Chaining.
    Menerima set/list kode gejala (Gxx) yang dipilih pengguna.
    Mengembalikan dict hasil evaluasi kecocokan rule dan kepribadian dominan.
    """
    user_facts = set(pilihan_user)
    rule_results = {}
    
    # Inisialisasi skor tertinggi per tipe kepribadian
    personality_scores = {
        "K1": 0.0,
        "K2": 0.0,
        "K3": 0.0,
        "K4": 0.0
    }
    
    # Iterasi melalui setiap rule (Forward Chaining)
    for rule_id, rule_info in ATURAN_INFERENSI.items():
        rule_facts = set(rule_info["facts"])
        matched_facts = user_facts.intersection(rule_facts)
        
        # Hitung persentase kecocokan: (fakta cocok / total fakta di rule x 100)
        percentage = (len(matched_facts) / len(rule_facts)) * 100
        
        rule_results[rule_id] = {
            "percentage": round(percentage, 2),
            "matched": list(matched_facts),
            "total_facts_count": len(rule_facts),
            "matched_facts_count": len(matched_facts),
            "personality": rule_info["target"],
            "personality_name": rule_info["target_name"]
        }
        
        # Simpan persentase tertinggi untuk setiap kepribadian target
        target_personality = rule_info["target"]
        if percentage > personality_scores[target_personality]:
            personality_scores[target_personality] = round(percentage, 2)
            
    # Cari nilai persentase kecocokan tertinggi di antara semua tipe kepribadian
    max_score = max(personality_scores.values())
    
    # Kepribadian dengan rule berpersentase tertinggi menjadi hasil dominan (bisa lebih dari satu jika seri)
    dominant_personalities = []
    if max_score > 0:
        dominant_personalities = [p_id for p_id, score in personality_scores.items() if score == max_score]
        
    return {
        "rule_results": rule_results,
        "personality_scores": personality_scores,
        "dominant": dominant_personalities,
        "max_score": max_score
    }

# ==========================================
# INISIALISASI SESSION STATE
# ==========================================

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

if 'test_hasil' not in st.session_state:
    st.session_state.test_hasil = None

if 'test_step' not in st.session_state:
    st.session_state.test_step = 1

if 'answers' not in st.session_state:
    st.session_state.answers = {k: False for k in FAKTA_GEJALA.keys()}

def ubah_halaman(nama_halaman):
    st.session_state.current_page = nama_halaman

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:
    st.markdown("""
    <div class='sidebar-title-container'>
        <div class='sidebar-logo'>SP</div>
        <div class='sidebar-title-text'>Sistem Pakar Kepribadian</div>
        <div class='sidebar-subtitle-text'>Forward Chaining Method</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigasi Menu yang disederhanakan
    menu_options = [
        "Beranda",
        "Tes Kepribadian",
        "Basis Pengetahuan",
        "Tentang Aplikasi & Metode"
    ]
    
    # Radio button yang sinkron dengan session state (tanpa key agar tidak write-lock saat programmatic redirect)
    pilihan_navigasi = st.radio(
        "Navigasi Halaman:",
        menu_options,
        index=menu_options.index(st.session_state.current_page)
    )
    
    # Sinkronisasi ketika user memilih radio button
    if pilihan_navigasi != st.session_state.current_page:
        st.session_state.current_page = pilihan_navigasi
        st.rerun()

# ==========================================
# HALAMAN 1: BERANDA
# ==========================================

if st.session_state.current_page == "Beranda":
    st.markdown("<h1 class='main-title'>Sistem Pakar Identifikasi Kepribadian & Rekomendasi Bidang Kerja</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Menggunakan Metode Forward Chaining Berdasarkan Karakteristik Psikologis</p>", unsafe_allow_html=True)
    
    # Card Sambutan & Intro
    st.markdown("""
    <div class='custom-card'>
        <h3 style='color: #1E3A8A; margin-top: 0;'>Selamat Datang di Sistem Pakar Karakter!</h3>
        <p>Setiap orang memiliki keunikan cara berpikir, bertindak, dan merespon lingkungan di sekitarnya. 
        Melalui sistem pakar ini, Anda dapat mengidentifikasi <b>tipe kepribadian dominan</b> Anda dari 4 tipe kepribadian klasik (Sanguinis, Melankolis, Plegmatis, dan Koleris) 
        berdasarkan landasan akademis jurnal penelitian.</p>
        <p>Sistem ini mengevaluasi ciri kepribadian Anda secara logis menggunakan metode <b>Forward Chaining</b>, lalu memberikan <b>rekomendasi bidang pekerjaan</b> yang paling harmonis dengan kecenderungan psikologis Anda agar produktivitas dan kepuasan kerja Anda dapat tercapai secara optimal.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Preview Tipe Kepribadian
    st.markdown("<div class='section-header'>Mengenal 4 Tipe Kepribadian</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='custom-card' style='border-left: 5px solid #EC407A;'>
            <h4 style='color: #EC407A; margin: 0 0 10px 0;'>Sanguinis (Populer)</h4>
            <p style='font-size: 0.95rem; line-height: 1.5;'>Individu yang penuh semangat, optimis, senang berbicara, dan mudah bergaul. Mereka senang menjadi pusat perhatian dan membawa kegembiraan di lingkungan kerja.</p>
            <span class='badge badge-sanguinis'>Ekspresif</span>
            <span class='badge badge-sanguinis'>Sosial</span>
            <span class='badge badge-sanguinis'>Ceria</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='custom-card' style='border-left: 5px solid #0D9488;'>
            <h4 style='color: #0D9488; margin: 0 0 10px 0;'>Plegmatis (Damai)</h4>
            <p style='font-size: 0.95rem; line-height: 1.5;'>Individu yang tenang, sabar, cinta damai, dan menghindari konflik. Mereka adalah mediator yang hebat, loyal, dan menyukai stabilitas serta kenyamanan kerja.</p>
            <span class='badge badge-plegmatis'>Sabar</span>
            <span class='badge badge-plegmatis'>Tenang</span>
            <span class='badge badge-plegmatis'>Loyal</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='custom-card' style='border-left: 5px solid #1E88E5;'>
            <h4 style='color: #1E88E5; margin: 0 0 10px 0;'>Melankolis (Sempurna)</h4>
            <p style='font-size: 0.95rem; line-height: 1.5;'>Individu yang mendalam, analitis, perfeksionis, dan teratur. Mereka sangat menyukai detail, akurasi, dan perencanaan matang sebelum mengambil keputusan.</p>
            <span class='badge badge-melankolis'>Analitis</span>
            <span class='badge badge-melankolis'>Perfeksionis</span>
            <span class='badge badge-melankolis'>Disiplin</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='custom-card' style='border-left: 5px solid #F97316;'>
            <h4 style='color: #F97316; margin: 0 0 10px 0;'>Koleris (Kuat)</h4>
            <p style='font-size: 0.95rem; line-height: 1.5;'>Individu yang tegas, berorientasi pada target, berani, dan suka memimpin. Mereka menyukai tantangan baru, cepat mengambil tindakan, dan sangat kompetitif.</p>
            <span class='badge badge-koleris'>Tegas</span>
            <span class='badge badge-koleris'>Pemimpin</span>
            <span class='badge badge-koleris'>Kompetitif</span>
        </div>
        """, unsafe_allow_html=True)

    # Cara Menggunakan
    st.markdown("""
    <div class='custom-card'>
        <h4 style='color: #1E3A8A; margin-top: 0;'>Langkah-Langkah Mengikuti Tes:</h4>
        <ol style='padding-left: 20px; line-height: 1.6;'>
            <li>Buka halaman <b>Tes Kepribadian</b> melalui menu sidebar atau tombol di bawah.</li>
            <li>Jawab kuesioner bertahap yang dibagi menjadi 4 bagian secara berurutan.</li>
            <li>Pada langkah terakhir, klik <b>"Lihat Hasil Analisis"</b>.</li>
            <li>Hasil kepribadian dan rekomendasi kerja Anda akan <b>langsung tampil seketika</b> di halaman yang sama!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button
    st.write("")
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("Mulai Tes Kepribadian Sekarang"):
            ubah_halaman("Tes Kepribadian")
            st.rerun()

# ==========================================
# HALAMAN 2: TES KEPRIBADIAN & HASIL (UX BERTINGKAT & INSTANT RESULT)
# ==========================================

elif st.session_state.current_page == "Tes Kepribadian":
    
    # JIKA HASIL TES SUDAH ADA, TAMPILKAN HASIL LANGSUNG DI HALAMAN INI
    if st.session_state.test_hasil is not None:
        st.markdown("<h1 class='main-title'>Hasil Analisis & Rekomendasi Karier</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Berikut adalah rangkuman analisis kepribadian dominan Anda beserta saran bidang kerja yang relevan.</p>", unsafe_allow_html=True)
        
        hasil = st.session_state.test_hasil
        dominant_list = hasil["dominant"]
        max_score = hasil["max_score"]
        scores = hasil["personality_scores"]
        
        # 1. Menampilkan Tipe Kepribadian Dominan
        st.markdown("<div class='section-header'>Kepribadian Dominan Anda</div>", unsafe_allow_html=True)
        
        if not dominant_list:
            st.markdown("""
            <div class='custom-card' style='text-align: center; border-left: 5px solid #95A5A6;'>
                <h2 style='color: #7F8C8D;'>Tidak Teridentifikasi secara Spesifik</h2>
                <p>Ciri-ciri kepribadian yang Anda centang belum memicu kecocokan aturan dari basis pengetahuan jurnal. 
                Cobalah ulangi tes dan centang ciri-ciri yang lebih spesifik mencerminkan diri Anda.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for p_id in dominant_list:
                info = DETAIL_KEPRIBADIAN[p_id]
                st.markdown(f"""
                <div class='custom-card' style='border-top: 4px solid #EC407A;'>
                    <h2 style='margin: 0; color: #1E3A8A;'>Tipe Kepribadian: {info["nama"]}</h2>
                    <p style='margin: 5px 0 0 0; font-size: 1.1rem; color: #E91E63; font-weight: bold;'>
                        Persentase Keakuratan Aturan: {max_score}%
                    </p>
                    <hr style='border: 0; border-top: 1px solid rgba(0,0,0,0.1); margin: 20px 0;'>
                    <h5 style='color: #2C3E50; margin-bottom: 5px;'><b>Deskripsi Karakter:</b></h5>
                    <p style='font-size: 1rem; line-height: 1.6; color: #4A5568;'>{info["deskripsi"]}</p>
                    <h5 style='color: #2C3E50; margin-bottom: 5px;'><b>Karakteristik Kunci:</b></h5>
                    <p style='font-size: 1rem; line-height: 1.6; color: #4A5568; font-style: italic;'>"{info["karakteristik"]}"</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Rekomendasi Bidang Kerja untuk kepribadian dominan
                st.markdown(f"""
                <div class='custom-card' style='background-color: rgba(255, 255, 255, 0.95); border-left: 6px solid #42A5F5;'>
                    <h3 style='color: #1E3A8A; margin-top: 0; margin-bottom: 15px;'>Rekomendasi Bidang Kerja / Karier:</h3>
                    <p style='color: #5E6E82; font-size: 0.95rem; margin-bottom: 20px;'>
                        Bidang karier berikut direkomendasikan berdasarkan kecocokan alami tipe kepribadian {info["nama"]} demi mengoptimalkan performa dan kenyamanan profesional:
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Rendering rekomendasi kerja secara terstruktur dengan bullet point
                for rec in info["rekomendasi"]:
                    st.markdown(f"- {rec}")
                st.write("")
        
        # 2. Progress Bar untuk keempat Tipe Kepribadian
        st.markdown("<div class='section-header'>Skor Kecocokan Tipe Kepribadian</div>", unsafe_allow_html=True)
        st.markdown("""
        <p style='color: #5E6E82; font-size: 0.9rem; margin-top: -10px; margin-bottom: 15px;'>
            Persentase berikut dihitung berdasarkan kecocokan aturan inferensi (Rule) tertinggi yang aktif untuk masing-masing kepribadian.
        </p>
        """, unsafe_allow_html=True)
        
        col_s, col_m = st.columns(2)
        with col_s:
            # Sanguinis
            val_s = scores["K1"] / 100.0
            st.markdown(f"""
            <div class='progress-label-container'>
                <span>Sanguinis (K1)</span>
                <span style='color: #EC407A;'>{scores["K1"]}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(val_s)
            
            # Plegmatis
            val_p = scores["K3"] / 100.0
            st.markdown(f"""
            <div class='progress-label-container'>
                <span>Plegmatis (K3)</span>
                <span style='color: #0D9488;'>{scores["K3"]}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(val_p)
            
        with col_m:
            # Melankolis
            val_m = scores["K2"] / 100.0
            st.markdown(f"""
            <div class='progress-label-container'>
                <span>Melankolis (K2)</span>
                <span style='color: #1E88E5;'>{scores["K2"]}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(val_m)
            
            # Koleris
            val_k = scores["K4"] / 100.0
            st.markdown(f"""
            <div class='progress-label-container'>
                <span>Koleris (K4)</span>
                <span style='color: #F97316;'>{scores["K4"]}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(val_k)
            
        st.write("")
        st.write("")

        # 3. Fakta yang Dipilih Pengguna
        with st.expander("Karakteristik Diri (Fakta Gejala) yang Anda Centang"):
            st.markdown("Berikut adalah daftar gejala/fakta psikologis yang Anda centang dalam kuesioner:")
            selected_symptoms = [k for k, v in st.session_state.answers.items() if v]
            for sym_code in selected_symptoms:
                st.markdown(f"- **{sym_code}**: {FAKTA_GEJALA[sym_code]}")
        
        # 4. Detail Logika Forward Chaining yang Aktif
        with st.expander("Detail Logika Forward Chaining & Aturan (Rule) yang Terpicu"):
            st.markdown("""
            Sistem pakar menggunakan penalaran maju (Forward Chaining). Persentase dihitung dengan rumus:<br>
            <b>Kecocokan Rule (%) = (Jumlah Gejala Terpenuhi / Total Gejala Rule) x 100%</b>
            """, unsafe_allow_html=True)
            
            rules_detailed_data = []
            for r_id, r_res in hasil["rule_results"].items():
                facts_string = ", ".join(ATURAN_INFERENSI[r_id]["facts"])
                matched_string = ", ".join(r_res["matched"]) if r_res["matched"] else "-"
                
                if r_res["percentage"] == 100.0:
                    status = "Aktif Sempurna (100%)"
                elif r_res["percentage"] > 0:
                    status = f"Terpenuhi Sebagian ({r_res['percentage']}%)"
                else:
                    status = "Tidak Terpenuhi (0%)"
                    
                rules_detailed_data.append({
                    "Rule": r_id,
                    "Target Kepribadian": f"{r_res['personality']} ({r_res['personality_name']})",
                    "Gejala Aturan": facts_string,
                    "Gejala Terpenuhi": matched_string,
                    "Persentase": f"{r_res['percentage']}%",
                    "Status Aturan": status
                })
                
            df_rules_detail = pd.DataFrame(rules_detailed_data)
            st.dataframe(df_rules_detail, use_container_width=True, hide_index=True)
            
        # 5. Aksi Ulangi Tes
        st.write("")
        col_reset, _ = st.columns([1, 2])
        with col_reset:
            if st.button("Ulangi Tes Kepribadian"):
                st.session_state.test_hasil = None
                st.session_state.answers = {k: False for k in FAKTA_GEJALA.keys()}
                st.session_state.test_step = 1
                st.rerun()

    # JIKA HASIL TES BELUM ADA, TAMPILKAN FORM PERTANYAAN SECARA BERTAHAP
    else:
        st.markdown("<h1 class='main-title'>Tes Identifikasi Kepribadian</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Isilah kuesioner bertahap di bawah ini untuk mengidentifikasi kepribadian Anda secara akurat.</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-box'>
            <b>Panduan Pengisian:</b><br>
            Kuesioner ini dibagi menjadi <b>4 bagian bertahap</b> untuk memudahkan Anda menilai diri sendiri. 
            Centang pernyataan yang sangat sesuai dengan perilaku Anda, lalu tekan <b>Lanjut</b> untuk melangkah ke bagian berikutnya.
        </div>
        """, unsafe_allow_html=True)
        
        # Konfigurasi warna aksen dinamis per langkah untuk mendukung kecocokan visual tipe kepribadian
        step_colors = {
            1: {"color": "#EC407A", "rgba": "rgba(236, 64, 122, 0.05)", "rgba_shadow": "rgba(236, 64, 122, 0.08)"}, # Sanguinis - Pink
            2: {"color": "#1E88E5", "rgba": "rgba(30, 136, 229, 0.05)", "rgba_shadow": "rgba(30, 136, 229, 0.08)"}, # Melankolis - Blue
            3: {"color": "#0D9488", "rgba": "rgba(13, 148, 136, 0.05)", "rgba_shadow": "rgba(13, 148, 136, 0.08)"}, # Plegmatis - Teal
            4: {"color": "#F97316", "rgba": "rgba(249, 115, 22, 0.05)", "rgba_shadow": "rgba(249, 115, 22, 0.08)"}  # Koleris - Orange
        }
        sc = step_colors[st.session_state.test_step]

        # Suntikkan CSS dinamis agar checkbox yang dicentang mengikuti warna kepribadian saat itu
        st.markdown(f"""
        <style>
        /* Warnai kotak centang native secara dinamis menggunakan accent-color */
        div[data-testid="stCheckbox"] input[type="checkbox"] {{
            accent-color: {sc["color"]} !important;
        }}
        
        /* Baris Checkbox tercentang */
        .stCheckbox:has(input:checked) {{
            background: {sc["rgba"]} !important;
            border-bottom-color: {sc["color"]} !important;
        }}
        
        .stCheckbox:has(input:checked) label p {{
            color: {sc["color"]} !important;
            font-weight: 600 !important;
        }}
        </style>
        """, unsafe_allow_html=True)

        # Hitung Nilai Progress Bar Langkah
        progress_val = float(st.session_state.test_step - 1) / 4.0
        st.progress(progress_val)
        
        # Judul Langkah Saat Ini
        step_title = STEP_QUESTIONS[st.session_state.test_step]["title"]
        step_keys = STEP_QUESTIONS[st.session_state.test_step]["keys"]
        
        # Header langkah tanpa kotak (card), bersih dan elegan dengan garis aksen kiri
        st.markdown(f"""
        <div style='border-left: 5px solid {sc["color"]}; padding-left: 18px; margin: 15px 0 25px 0;'>
            <div style='font-size: 0.85rem; font-weight: 700; color: {sc["color"]}; text-transform: uppercase; letter-spacing: 1.5px;'>Langkah {st.session_state.test_step} dari 4</div>
            <h2 style='margin: 4px 0 0 0; font-size: 1.65rem; color: #0F172A; font-family: "Outfit", sans-serif; font-weight: 800;'>{step_title}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Render Checkbox Khusus untuk Langkah/Bagian Aktif
        col1, col2 = st.columns(2)
        half = (len(step_keys) + 1) // 2
        
        with col1:
            for k in step_keys[:half]:
                # Tampilkan pernyataan langsung (lebih bersih dan profesional tanpa kode teknis G01)
                st.session_state.answers[k] = st.checkbox(
                    FAKTA_GEJALA[k], 
                    value=st.session_state.answers[k],
                    key=f"chk_{k}"
                )
        with col2:
            for k in step_keys[half:]:
                st.session_state.answers[k] = st.checkbox(
                    FAKTA_GEJALA[k], 
                    value=st.session_state.answers[k],
                    key=f"chk_{k}"
                )
        
        st.write("")
        st.write("")
        
        # Tombol Navigasi Halaman
        col_prev, col_next = st.columns([1, 1])
        
        with col_prev:
            if st.session_state.test_step > 1:
                if st.button("Kembali ke Bagian Sebelumnya", use_container_width=True):
                    st.session_state.test_step -= 1
                    st.rerun()
                    
        with col_next:
            if st.session_state.test_step < 4:
                if st.button("Lanjut ke Bagian Berikutnya", use_container_width=True):
                    st.session_state.test_step += 1
                    st.rerun()
            else:
                if st.button("Lihat Hasil Analisis", use_container_width=True):
                    # Kumpulkan gejala terpilih
                    selected_symptoms = [k for k, checked in st.session_state.answers.items() if checked]
                    
                    if not selected_symptoms:
                        st.error("Validasi Error: Anda belum memilih satu pun ciri kepribadian! Silakan centang minimal satu karakteristik yang menggambarkan diri Anda.")
                    else:
                        # Menjalankan mesin inferensi forward chaining
                        hasil = hitung_kepribadian(selected_symptoms)
                        st.session_state.test_hasil = hasil
                        st.rerun()

# ==========================================
# HALAMAN 3: BASIS PENGETAHUAN
# ==========================================

elif st.session_state.current_page == "Basis Pengetahuan":
    st.markdown("<h1 class='main-title'>Basis Pengetahuan Sistem Pakar</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Basis pengetahuan berupa fakta dan aturan (rule) formal yang diimplementasikan dari jurnal penelitian.</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <b>Informasi Jurnal Acuan:</b><br>
        Seluruh kode gejala dan pemetaan relasi aturan (rules) di bawah ini diadopsi secara presisi dari jurnal: 
        <i>"Sistem Pakar Untuk Menentukan Departemen Sesuai Kepribadian Calon Karyawan dengan Menggunakan Metode Forward Chaining"</i> 
        (Lely Panca Andriyanto, Meidy Fajar Wahyu).
    </div>
    """, unsafe_allow_html=True)
    
    tab_gejala, tab_aturan = st.tabs(["Daftar Gejala (Fakta)", "Aturan Inferensi (Rules)"])
    
    with tab_gejala:
        st.markdown("<div class='section-header'>Daftar Gejala & Karakteristik Psikologis</div>", unsafe_allow_html=True)
        st.markdown("Berikut adalah 29 gejala kepribadian yang digunakan sebagai parameter kuesioner:")
        
        gejala_data = [{"Kode Gejala": k, "Ciri-Ciri Karakteristik / Gejala": v} for k, v in FAKTA_GEJALA.items()]
        df_gejala = pd.DataFrame(gejala_data)
        st.dataframe(df_gejala, use_container_width=True, hide_index=True)
        
    with tab_aturan:
        st.markdown("<div class='section-header'>Aturan Inferensi Kepribadian (Rule Base)</div>", unsafe_allow_html=True)
        st.markdown("Berikut adalah 12 aturan (R1 hingga R12) yang memetakan kombinasi gejala ke tipe kepribadian:")
        
        rules_table_data = []
        for r_id, r_info in ATURAN_INFERENSI.items():
            kombinasi_gejala = " AND ".join(r_info["facts"])
            rules_table_data.append({
                "Kode Rule": r_id,
                "Logika Aturan (IF - THEN)": f"IF {kombinasi_gejala} THEN {r_info['target']} ({r_info['target_name']})",
                "Kepribadian Hasil": f"{r_info['target_name']} ({r_info['target']})"
            })
        df_rules = pd.DataFrame(rules_table_data)
        st.dataframe(df_rules, use_container_width=True, hide_index=True)

# ==========================================
# HALAMAN 4: TENTANG APLIKASI & METODE
# ==========================================

elif st.session_state.current_page == "Tentang Aplikasi & Metode":
    st.markdown("<h1 class='main-title'>Tentang Aplikasi & Metode Inferensi</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Informasi akademis, penjelasan metode penalaran logika, dan detail pengembangan.</p>", unsafe_allow_html=True)
    
    # Academic Disclaimer
    st.markdown("""
    <div class='warning-box' style='padding: 20px;'>
        <h4 style='color: #880E4F; margin-top: 0; margin-bottom: 10px;'>DISCLAIMER AKADEMIS</h4>
        <p style='margin: 0; font-size: 1rem; line-height: 1.6;'>
            Aplikasi ini menggunakan mesin logika (Daftar Fakta Gejala dan Aturan Inferensi) murni dari jurnal penelitian 
            yang dilakukan di <b>PT Surya Toto Indonesia Tbk</b>. Namun, untuk menjangkau manfaat yang lebih luas bagi 
            masyarakat umum, rekomendasi akhir yang aslinya berupa penempatan <b>"Departemen Pabrik"</b> (seperti Departemen Faucet, 
            Fitting, Workshop, dll.) telah <b>digeneralisasi menjadi "Rekomendasi Bidang Kerja Umum"</b> oleh pengembang 
            tanpa mengubah orisinalitas proses logika forward chaining yang ada di jurnal tersebut.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Penjelasan Forward Chaining & Rumus
    st.markdown("<div class='section-header'>Mekanisme Logika: Forward Chaining</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='custom-card'>
        <h3 style='color: #1E3A8A; margin-top: 0;'>Apa itu Forward Chaining?</h3>
        <p><b>Forward Chaining (Penalaran Maju)</b> adalah metode pencarian dalam sistem pakar yang berorientasi pada data (data-driven). Proses inferensi dimulai dari pengumpulan fakta-fakta awal (data input dari kuesioner pengguna) menuju kesimpulan akhir (tipe kepribadian).</p>
        <p>Secara sederhana, mesin inferensi akan menganalisis fakta yang ada dan mencoba mencocokkannya dengan premis (bagian <i>IF</i>) dari aturan-aturan yang ada di basis pengetahuan. Jika premis terpenuhi, maka aturan tersebut akan aktif dan menghasilkan konklusi (bagian <i>THEN</i>).</p>  
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Metadata Jurnal
    st.markdown("<div class='section-header'>Jurnal Penelitian Rujukan</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='custom-card'>
        <table style='width: 100%; border-collapse: collapse;'>
            <tr style='border-bottom: 1px solid #E2E8F0;'>
                <td style='padding: 10px 0; font-weight: bold; width: 25%; color: #1E3A8A;'>Judul Jurnal</td>
                <td style='padding: 10px 0; color: #4A5568;'>Sistem Pakar Untuk Menentukan Departemen Sesuai Kepribadian Calon Karyawan dengan Menggunakan Metode Forward Chaining</td>
            </tr>
            <tr style='border-bottom: 1px solid #E2E8F0;'>
                <td style='padding: 10px 0; font-weight: bold; color: #1E3A8A;'>Penulis</td>
                <td style='padding: 10px 0; color: #4A5568;'>Lely Panca Andriyanto, Meidy Fajar Wahyu</td>
            </tr>
            <tr style='border-bottom: 1px solid #E2E8F0;'>
                <td style='padding: 10px 0; font-weight: bold; color: #1E3A8A;'>Publikasi</td>
                <td style='padding: 10px 0; color: #4A5568;'>Journal of Information System Research (JOSH), Vol. 7, No. 2, 2026.</td>
            </tr>
            <tr>
                <td style='padding: 10px 0; font-weight: bold; color: #1E3A8A;'>Studi Kasus Asli</td>
                <td style='padding: 10px 0; color: #4A5568;'>PT Surya Toto Indonesia Tbk.</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Teknologi Stack
    st.markdown("<div class='section-header'>Teknologi & Pengembangan</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='custom-card'>
        <p>Aplikasi ini dideploy secara dinamis dengan spesifikasi teknis berikut:</p>
        <ul style='padding-left: 20px; line-height: 1.7;'>
            <li><b>Bahasa Pemrograman:</b> Python</li>
            <li><b>Framework Antarmuka:</b> Streamlit (untuk antarmuka web interaktif yang modern, clean, dan profesional)</li>
            <li><b>Pengolahan Data:</b> Pandas (untuk menyusun dan menampilkan tabel basis pengetahuan secara modular)</li>
            <li><b>Manajemen State:</b> <code>st.session_state</code> (tanpa database eksternal untuk portabilitas penuh)</li>
            <li><b>Pencocokan Logika:</b> Python Set Intersection untuk kalkulasi rules Forward Chaining yang cepat dan efisien.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
