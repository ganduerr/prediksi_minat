import streamlit as st
import pickle
import sqlite3
import os
import pandas as pd

# Load model dan label encoder
with open('model_rf.pkl', 'rb') as f:
    model = pickle.load(f)
with open('label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

# Soal dan bobot tes

ocean_labels = ['O', 'C', 'E', 'A', 'N']
ocean_questions = {
    'O': ["Saya suka mencoba hal baru", "Saya memiliki imajinasi yang kuat", "Saya senang mengeksplorasi ide-ide baru", "Saya terbuka terhadap perubahan", "Saya menikmati tantangan yang tidak biasa"],
    'C': ["Saya terorganisir dalam pekerjaan", "Saya memperhatikan detail", "Saya menyelesaikan tugas tepat waktu", "Saya bekerja dengan penuh tanggung jawab", "Saya memiliki target yang jelas"],
    'E': ["Saya suka berinteraksi dengan orang lain", "Saya aktif berbicara dalam kelompok", "Saya merasa nyaman berada di keramaian", "Saya mudah bergaul", "Saya suka menjadi pusat perhatian"],
    'A': ["Saya memperhatikan perasaan orang lain", "Saya suka membantu orang yang kesulitan", "Saya pemaaf", "Saya menghargai pendapat orang lain", "Saya menghindari konflik"],
    'N': ["Saya sering merasa cemas", "Saya mudah marah", "Saya cepat merasa sedih", "Saya sering merasa tertekan", "Saya sulit mengendalikan emosi"]
}

aptitude_labels = ['Numerical', 'Spatial', 'Logical', 'Abstract', 'Verbal']
aptitude_questions = {
    'Numerical': [
        {
            'question': "Berapa hasil dari 45 + 32?",
            'options': ["75","77","78","80"],
            'answer' : "77"
            },
            {
            'question': "Jika kamu membeli 3 apel seharga Rp4.000 masing-masing, berapa totalnya?",
            'options': ["Rp10.000","Rp11.000","Rp12.000","Rp13.000"],
            'answer' : "Rp12.000"
            },{
            'question': "Dalam 1 jam, mesin menghasilkan 250 unit. Berapa unit yang di hasilkan dalam 5 jam?",
            'options': ["1000","1150","1250","1350"],
            'answer' : "1250"
            },{
            'question': "Diskon 20% dari Rp100.000 adalah?",
            'options': ["Rp.20.000","Rp.30.000","Rp.40.000","Rp.50.000"],
            'answer' : "Rp.20.000"
            },{
            'question': "Jika 5 orang menyelesaikan tugas dalam 10 hari, berapa lama 10 orang menyelesaikannya?",
            'options': ["9","8","7","5"],
            'answer' : "5"
            }
        ],
    'Spatial': [
        {
            'question': "Anda menghadap Utara. Putar 90 derajat searah jarum jam, lalu putar 135 derajat berlawanan arah jarum jam. Arah mana yang Anda hadapi sekarang?",
            'options': ["Barat","Tenggara","Barat laut","Timur laut"],
            'answer' : "Utara"
            },{
            'question': "Sebuah koin berada di atas sebuah buku. Sebuah pensil berada di sebelah kanan buku. Jika Anda melihat dari atas, di mana posisi pensil relatif terhadap koin?",
            'options': ["Kiri bawah","Kanan atas","Kanan bawah","Kiri atas"],
            'answer' : "Kanan bawah"
           },{
            'question': "Sebuah kubus memiliki 6 sisi. Sisi depan berwarna merah, sisi kanan berwarna biru, dan sisi atas berwarna hijau. Sisi merah berhadapan dengan hitam. Sisi biru berhadapan dengan kuning. Warna apa yang berhadapan dengan sisi hijau?",
            'options': ["Putih","Oranye","Ungu","Tidak ada di pilihan"],
            'answer' : "Tidak ada di pilihan"
           },{
            'question': "Anda berjalan 5 meter ke Timur, lalu 5 meter ke Utara. Dari titik awal Anda, ke arah mana Anda sekarang?",
            'options': ["Utara","Timur Laut","Barat Laut","Tenggara"],
            'answer' : "Timur Laut"
           },{
            'question': "Titik X berada 3 meter di selatan Titik Y. Titik Z berada 4 meter di barat Titik Y. Apa jarak lurus terpendek antara Titik X dan Titik Z?",
            'options': ["5 meter","6 meter","7 meter","8 meter"],
            'answer' : "5 meter"
           },
        ],
    'Logical' : [
        {
            'question': "Semua apel manis. Buah ini bukan apel. Kesimpulan yang paling tepat adalah:",
            'options': ["Buah ini pasti pahit","Buah ini belum tentu manis","Buah ini pasti mangga","Buah ini tidak bisa dimakan"],
            'answer' : "Buah ini belum tentu manis"  
        },{
            'question': "Jika hari ini bukan Senin dan besok bukan Selasa, hari apakah kemarin?",
            'options': ["Minggu","jumat","Sabtu","Rabu"],
            'answer' : "Sabtu"
           },{
            'question': "Lanjutkan pola angka ini: 5, 10, 15, 20, ?",
            'options': ["25","15","10","20"],
            'answer' : "25"
           },{
            'question': "Jika cuaca cerah, kita akan piknik. Kita tidak piknik. Kesimpulan yang paling mungkin adalah:",
            'options': ["Cuaca Cerah","Cuaca tidak Cerah","kita tidak suka piknik","piknik dibatalkan karena alesan"],
            'answer' : "Cuaca tidak Cerah"
           },{
            'question': "Jika 3 orang = 3 pekerjaan dalam 6 hari, berapa orang untuk 3 pekerjaan dalam 3 hari?",
            'options': ["8","6","10","3"],
            'answer' : "6"
           },
    ],
    'Abstract': [
        {
            'question': "Apa bentuk berikutnya dalam seri : Persegi → Lingkaran → Segitiga → Persegi → ?",
            'options': ["Lingkaran","Persegi","Segitiga","Oval"],
            'answer' : "Segitiga"
        },{
            'question': "Sebuah panah menghadap ke atas. Kemudian menghadap ke kanan. Lalu ke bawah. Lalu ke kiri. Selanjutnya akan menghadap ke mana?",
            'options': ["Atas","Kanan","Bawah","Kiri"],
            'answer' : "Atas"
           },{
            'question': "Pola ini: Satu garis → Dua garis → Tiga garis → Dua garis → ?",
            'options': ["Satu Garis","Dua Garis","Tiga Garis","Empat Garis"],
            'answer' : "Satu Garis"
           },{
            'question': "● ▲ ■ ● ▲ ■ ● ... Apa Gambar Berikutnya",
            'options': ["▲","■","●","△"],
            'answer' : "▲"
           },{
            'question': "Jika kata “MEJA” diubah menjadi “NFKB”, maka bagaimana kata KURSI diubah?",
            'options': ["LVSTJ","LVRTJ","LVRTK","LVSTK"],
            'answer' : "LVSTJ"
           },
    ],
    'Verbal' : [
        {
            'question': "Pilih kata yang paling dekat maknanya dengan kata CERDAS?",
            'options': ["Bodoh","Pintar","Lambat","Malas"],
            'answer' : "Pintar"
           },{
            'question': "Antonim dari kata KUAT adalah?",
            'options': ["Keras","Lemah","Besar","Cepat"],
            'answer' : "Lemah"
           },{
            'question': "Buku : Membaca = Pisau : ?",
            'options': ["Memotong","Memasak","Menulis","Menjahit"],
            'answer' : "Memotong"
           },{
            'question': "Pilih kata yang paling tepat untuk melengkapi kalimat berikut: 'Dia sangat rajin, _____ selalu menyelesaikan tugas tepat waktu'.?",
            'options': ["tetapi","karena","sehingga","Meskipun"],
            'answer' : "sehingga"
           },{
            'question': "Susun kata-kata berikut menjadi kalimat yang benar dan logis: makan / setiap / pagi / saya / buah / suka",
            'options': ["setiap pagi, saya suka makan buah","suka makan buah saya setiap pagi","saya makan buah suka setiap pagi","Saya suka makan buah setiap pagi."],
            'answer' : "Saya suka makan buah setiap pagi."
           },
    ]
}

options_labels = ['Sangat Tidak Setuju', 'Tidak Setuju', 'Biasa Saja', 'Setuju', 'Sangat Setuju']

# Buat database dan tabel
conn = sqlite3.connect('quiz_results.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    kelas TEXT,
    o REAL, c REAL, e REAL, a REAL, n REAL,
    apt1 REAL, apt2 REAL, apt3 REAL, apt4 REAL, apt5 REAL,
    prediction TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)''')
conn.commit()

# Admin default
c.execute("SELECT * FROM users WHERE username='admin'")
if not c.fetchone():
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', 'admin123', 'admin'))
    conn.commit()

# Sidebar Login
st.sidebar.title("Login Pengguna")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Login"):
    user = c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user[1]
        st.session_state.role = user[3]
        st.success(f"Berhasil login sebagai {user[3].capitalize()}")
    else:
        st.error("Username atau password salah")

if 'logged_in' in st.session_state and st.session_state.logged_in:
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    role = st.session_state.role
    if role == 'admin':
        st.title("Panel Admin - Manajemen Akun Guru")
        st.subheader("Tambah Akun Guru")
        new_username = st.text_input("Username Baru")
        new_password = st.text_input("Password", type="password")
        if st.button("Buat Akun Guru"):
            try:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (new_username, new_password, 'guru'))
                conn.commit()
                st.success("Akun guru berhasil ditambahkan")
            except sqlite3.IntegrityError:
                st.error("Username sudah digunakan")
        st.subheader("Daftar Akun Guru")
        guru_accounts = c.execute("SELECT id, username FROM users WHERE role='guru'").fetchall()
        for uid, uname in guru_accounts:
            col1, col2 = st.columns([3, 1])
            col1.write(uname)
            if col2.button("Hapus", key=f"hapus_{uid}"):
                c.execute("DELETE FROM users WHERE id=?", (uid,))
                conn.commit()
                st.success(f"Akun {uname} dihapus")
                st.rerun()
        st.subheader("Riwayat Tes Siswa")
        results = c.execute("SELECT id, name, kelas, prediction FROM results").fetchall()
        for row in results:
            rid, name, kelas, prediksi = row
        col1, col2, col3 = st.columns([3, 3, 1])
        col1.write(f"{name} ({kelas}) - {prediksi}")
        if col3.button("Hapus", key=f"hapus_hasil_{rid}"):
            c.execute("DELETE FROM results WHERE id=?", (rid,))
            conn.commit()
            st.success(f"Data {name} dihapus.")
            st.rerun()


    elif role == 'guru':
        st.title("Panel Guru - Lihat Hasil Tes Siswa")
        results = c.execute("SELECT name, kelas, o, c, e, a, n, apt1, apt2, apt3, apt4, apt5, prediction FROM results").fetchall()
        columns = ['Nama', 'Kelas', 'O', 'C', 'E', 'A', 'N', 'Apt1', 'Apt2', 'Apt3', 'Apt4', 'Apt5', 'Prediksi Minat']
        df_results = pd.DataFrame(results, columns=columns)
        st.dataframe(df_results)

    elif role == 'user':
        st.info("Silakan kembali ke halaman utama untuk mengerjakan kuis.")

elif 'logged_in' not in st.session_state:
    # Halaman Tes Minat
    if 'step' not in st.session_state:
        st.session_state.step = 1
        st.session_state.input_data = []
        st.session_state.name = ""
        st.session_state.kelas = ""

    if st.session_state.step == 1:
        st.title("Tes Minat SDN 1 Talagahiang")
        st.session_state.name = st.text_input("Nama Lengkap", st.session_state.name)
        st.session_state.kelas = st.text_input("Kelas", st.session_state.kelas)
        if st.session_state.name and st.session_state.kelas:
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Isi nama dan kelas terlebih dahulu.")
            st.stop()

    elif 2 <= st.session_state.step <= 6:
        index = st.session_state.step - 2
        label = ocean_labels[index]
        st.subheader(f"Tes {label}")
        answers = [st.radio(q, options_labels, key=f"{label}_{i}") for i, q in enumerate(ocean_questions[label])]
        converted = [((options_labels.index(s)) * (9 / 4)) + 1 for s in answers]
        avg_score = sum(converted) / len(converted)
        if st.button("Lanjut"):
            st.session_state.input_data.append(round(avg_score, 2))
            st.session_state.step += 1
            st.rerun()

    elif 7 <= st.session_state.step <= 11:
        index = st.session_state.step - 7
        label = aptitude_labels[index]
        st.subheader(f"Tes Aptitude: {label}")
        score = 0
        for i, q_data in enumerate(aptitude_questions[label]):
            selected = st.radio(q_data['question'], q_data['options'], key=f"{label}_{i}")
            if selected == q_data['answer']:
              score += 2  # Jawaban benar dapat 2 poin
        if st.button("Lanjut"):
            st.session_state.input_data.append(score)
            st.session_state.step += 1
            st.rerun()

    elif st.session_state.step == 12:
        st.success("Tes selesai! Menampilkan hasil...")
        input_array = [st.session_state.input_data]
        prediction = model.predict(input_array)[0]
        label_result = le.inverse_transform([prediction])[0]
        st.subheader(f"Rekomendasi Karier: {label_result}")
        c.execute('''INSERT INTO results (name, kelas, o, c, e, a, n, apt1, apt2, apt3, apt4, apt5, prediction)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (st.session_state.name, st.session_state.kelas, *st.session_state.input_data, label_result))
        conn.commit()

        if st.button("Ulangi Tes"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
