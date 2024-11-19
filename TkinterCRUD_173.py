import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk 

# Fungsi untuk buat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')    # Membuka atau membuat file database bernama 'nilai_siswa.db'.
    cursor = conn.cursor()                      # Membuat cursor untuk eksekusi perintah SQL.
    cursor.execute('''                          
        CREATE TABLE IF NOT EXISTS nilai_siswa (    # Membuat tabel jika belum ada.
            id INTEGER PRIMARY KEY AUTOINCREMENT,   # Kolom 'id' sebagai primary key dengan auto-increment
            nama_siswa TEXT,                        # Kolom 'nama_siswa', tipe teks.                 
            biologi INTEGER,                        # Kolom untuk nilai biologi, tipe integer.
            fisika INTEGER,                         # Kolom untuk nilai fisika, tipe integer.
            inggris INTEGER,                        # Kolom untuk nilai bahasa Inggris, tipe integer.
            prediksi_fakultas TEXT                  # Kolom untuk prediksi fakultas, tipe teks.
        )
    ''')
    conn.commit()   # Menyimpan perubahan pada database.
    conn.close()    # Menutup koneksi ke database.

# Fungsi untuk mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')    # Membuka koneksi ke database.
    cursor = conn.cursor()                      #Membuat Cursor
    cursor.execute("SELECT * FROM nilai_siswa") # Mengambil semua data dari tabel.
    rows = cursor.fetchall()                    # Menyimpan hasil query.
    conn.close()                                # Menutup koneksi ke database
    return rows                                 # Mengembalikan data.

# Fungsi untuk menyimpan data baru ke database 
def save_to_database(nama, biologi, fisika, inggris, prediksi): # Membuka koneksi ke database.
    conn = sqlite3.connect('nilai_siswa.db')    # Membuat cursor.
    cursor = conn.cursor()     
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)  # Menyisipkan data ke tabel.
    ''', (nama, biologi, fisika, inggris, prediksi))    # Data diinput sebagai parameter.
    conn.commit()   #Menyimpan perubahan pada database.
    conn.close()    # Menutup koneksi.

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):   # Membuka koneksi ke database.
    conn = sqlite3.connect('nilai_siswa.db')    # Membuat cursor.
    cursor = conn.cursor()                      # Update data berdasarkan ID.
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?       # Update data berdasarkan ID.
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) # Data dan ID sebagai parameter.
    conn.commit()    # Menyimpan perubahan.
    conn.close()       # Menutup koneksi.

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')    # Membuka koneksi ke database.
    cursor = conn.cursor()                      # Membuat cursor.
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))   # Menghapus data berdasarkan ID.
    conn.commit() # Menyimpan perubahan.
    conn.close() # Menutup koneksi.

# Fungsi untuk menghitung prediksi fakultas
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:  # Jika nilai biologi terbesar.
        return "Kedokteran"                     # Prediksi fakultas Kedokteran.
    elif fisika > biologi and fisika > inggris: # Jika nilai fisika terbesar.
        return "Teknik"                         # Prediksi fakultas Teknik.
    elif inggris > biologi and inggris > fisika:   # Jika nilai Inggris terbesar.
        return "Bahasa"                         # Prediksi fakultas Bahasa.
    else:
        return "Tidak diketahui"                # Jika nilai sama atau tidak diketahui.


# Fungsi untuk menangani tombol submit
def submit():
    try:
        nama = nama_var.get()               # Mengambil input nama siswa.
        biologi = int(biologi_var.get())    # Mengambil input nilai Biologi.
        fisika = int(fisika_var.get())      # Mengambil input nilai Fisika.
        inggris = int(inggris_var.get())    # Mengambil input nilai Inggris.


        if not nama: #jika nama kosong 
            raise Exception("Nama siswa tidak boleh kosong.")
        prediksi = calculate_prediction(biologi, fisika, inggris)   # Menghitung prediksi fakultas.
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data ke database.

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}") #Pesan Sukses
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk menangani tombol update
def update():
    try:
        if not selected_record_id.get():   # Mengecek apakah ada data yang dipilih dari tabel untuk diperbarui
            raise Exception("Pilih data dari tabel untuk diupdate!")    # Jika tidak ada, berikan peringatan.
        
        record_id = int(selected_record_id.get())   # Mendapatkan ID dari data yang dipilih.
        nama = nama_var.get()                       # Mengambil input dari kolom nama dan nilai-nilai.
        biologi = int(biologi_var.get())            # Mengambil nilai Biologi dari input pengguna.
        fisika = int(fisika_var.get())              # Mengambil nilai Fisika dari input pengguna.
        inggris = int(inggris_var.get())            # Mengambil nilai Inggris dari input pengguna.

        if not nama:    # Memeriksa apakah input nama kosong.
            raise ValueError("Nama siswa tidak boleh kosong.")  # Jika kosong, lempar error.

        prediksi = calculate_prediction(biologi, fisika, inggris)   # Menghitung prediksi fakultas berdasarkan nilai-nilai.
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)    # Memperbarui data di database berdasarkan ID.

        messagebox.showinfo("Sukses", "Data berhasil diperbarui")    # Menampilkan pesan sukses kepada pengguna.
        clear_inputs()      # Mengosongkan kolom input setelah update selesai.
        populate_table()    # Memperbarui tabel dengan data terbaru dari database.
    except ValueError as e: # Menangkap error saat input nilai tidak valid.
        messagebox.showerror("Error", f"Kesalahan: {e}")    # Menampilkan pesan kesalahan kepada pengguna.

# Fungsi untuk menangani tombol delete
def delete():
    try:
        if not selected_record_id.get():    # Mengecek apakah ada data yang dipilih dari tabel untuk dihapus.
            raise Exception("Pilih data dari tabel untuk dihapus!") # Jika tidak ada data yang dipilih, lemparkan error.
        
        record_id = int(selected_record_id.get())   # Mendapatkan ID dari data yang dipilih.
        delete_database(record_id)                  # Memanggil fungsi untuk menghapus data berdasarkan ID.
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")     # Menampilkan pesan sukses jika data berhasil dihapus.
        clear_inputs()      # Mengosongkan semua input setelah penghapusan.
        populate_table()    # Memperbarui tabel dengan data terbaru dari database.
    except ValueError as e: # Menangkap error jika input ID tidak valid.
        messagebox.showerror("Error", f"Kesalahan: {e}")     # Menampilkan pesan kesalahan kepada pengguna.

# Fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("")    # Mengosongkan input nama.
    biologi_var.set("") # Mengosongkan input nilai Biologi
    fisika_var.set("")  # Mengosongkan input nilai Fisika.
    inggris_var.set("") # Mengosongkan input nilai Inggris.
    selected_record_id.set("")  # Mengosongkan ID data yang dipilih.

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    # Menghapus semua data yang ada di tabel untuk memperbarui isinya.
    for row in tree.get_children():
        tree.delete(row)
    # Mengambil data dari database dan menambahkannya ke tabel.
    for row in fetch_data():
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi input dengan data dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0] # Mendapatkan item yang dipilih dari tabel.
        selected_row = tree.item(selected_item)['values']   # Mengambil data dari baris yang dipilih berdasarkan item tersebut.
        selected_record_id.set(selected_row[0]) # Mengisi ID data yang dipilih ke dalam variabel `selected_record_id`.
        nama_var.set(selected_row[1])   # Mengisi nama siswa dari baris yang dipilih ke input nama.
        biologi_var.set(selected_row[2]) # Mengisi nilai Biologi dari baris yang dipilih ke input nilai Biologi.
        fisika_var.set(selected_row[3])  # Mengisi nilai Fisika dari baris yang dipilih ke input nilai Fisika.
        inggris_var.set(selected_row[4])  # Mengisi nilai Inggris dari baris yang dipilih ke input nilai Inggris.
    except IndexError:  # Jika tidak ada baris yang dipilih, tangkap error.
        messagebox.showerror("Error", "Pilih data yang valid!") # Menampilkan pesan error kepada pengguna.

# Inisialisasi database
create_database()   # Memanggil fungsi untuk membuat database dan tabel jika belum ada.

# Membuat GUI dengan Tkinter
root = Tk() # Membuat instance utama aplikasi Tkinter.
root.title("Prediksi Fakultas Siswa")   # Memberikan judul pada jendela aplikasi.

# Variabel Tkinter
nama_var = StringVar()  # Variabel untuk menyimpan input nama siswa.
biologi_var = StringVar()   # Variabel untuk menyimpan input nilai Biologi.
fisika_var = StringVar()    # Variabel untuk menyimpan input nilai Fisika.
inggris_var = StringVar()   # Variabel untuk menyimpan ID record yang dipilih dari tabel.
selected_record_id = StringVar() # untuk menyimpan id record yang dipilih

# Elemen GUI
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)   # Label untuk input "Nama Siswa", diletakkan di baris 0, kolom 0.
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5) # Kotak input untuk "Nama Siswa", terhubung ke variabel `nama_var`.

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)    # Label untuk input "Nilai Biologi", diletakkan di baris 1, kolom 0.
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)  #Kotak input untuk "Nilai Biologi", terhubung ke variabel `biologi_var`.

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5) # Label untuk input "Nilai Fisika", diletakkan di baris 2, kolom 0.
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5) # Kotak input untuk "Nilai Fisika", terhubung ke variabel `fisika_var`.

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)    # Label untuk input "Nilai Inggris", diletakkan di baris 3, kolom 0.
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)    # Kotak input untuk "Nilai Inggris", terhubung ke variabel `inggris_var`.

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10) # Tombol "Add" untuk menambahkan data, terhubung ke fungsi `submit`.
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)  # Tombol "Update" untuk memperbarui data, terhubung ke fungsi `update`.
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)  # Tombol "Delete" untuk menghapus data, terhubung ke fungsi `delete`.

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas") # Mendefinisikan kolom untuk tabel.
tree = ttk.Treeview(root, columns=columns, show='headings') # Membuat tabel dengan kolom yang ditentukan, hanya menampilkan header dan data.

# Menyesuaikan posisi teks di setiap kolom ke tengah
for col in columns: 
     # Memberikan nama header di setiap kolom sesuai dengan nama kolom.
    tree.heading(col, text=col.capitalize())
    # Mengatur posisi teks di tengah untuk setiap kolom.
    tree.column(col, anchor='center')   

# Menempatkan tabel pada baris ke-5, menyebar hingga tiga kolom.
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  
# Event untuk memilih data dari tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Mengisi tabel dengan data
populate_table()

# Menjalankan Tkinter
root.mainloop()