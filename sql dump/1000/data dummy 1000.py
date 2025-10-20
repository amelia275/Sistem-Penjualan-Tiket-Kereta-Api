# generate_all_dummy.py
from faker import Faker
import pandas as pd
import random
from datetime import timedelta, datetime

fake = Faker('id_ID')
random.seed(42)
Faker.seed(42)

# Ubah kalau mau ukuran lain / subset
jumlah_data = [10, 100, 1000, 10000]

# Helper: format ID dengan padding
def fmt(prefix, i, width):
    return f"{prefix}{i:0{width}d}"

# 1) STASIUN
def buat_stasiun(n):
    rows = []
    for i in range(1, n+1):
        rows.append({
            "ID_Stasiun": fmt("ST", i, 5),
            "Nama_Stasiun": f"Stasiun {fake.city()}",
            "Lokasi": fake.city()
        })
    return pd.DataFrame(rows)

# 2) KERETA
def buat_kereta(n):
    layanan = ["Eksekutif", "Bisnis", "Ekonomi"]
    rows = []
    for i in range(1, n+1):
        rows.append({
            "ID_Kereta": fmt("KRT", i, 5),
            "Tipe_Layanan": random.choice(layanan),
            "Nama_Kereta": f"KA {fake.word().capitalize()}"
        })
    return pd.DataFrame(rows)

# 3) GERBONG
def buat_gerbong(n, kereta_df):
    rows = []
    kereta_ids = list(kereta_df["ID_Kereta"])
    for i in range(1, n+1):
        rows.append({
            "ID_Gerbong": fmt("GB", i, 5),
            "Nomor_Gerbong": str(random.randint(1, 20)),
            "Kapasitas": random.choice([40, 50, 60, 72, 80]),
            "ID_Kereta": random.choice(kereta_ids)
        })
    return pd.DataFrame(rows)

# 4) KURSI
def buat_kursi(n, gerbong_df):
    rows = []
    gerbong_ids = list(gerbong_df["ID_Gerbong"])
    for i in range(1, n+1):
        rows.append({
            "ID_Kursi": fmt("KS", i, 6),
            "Nomor_Kursi": str(random.randint(1, 100)),
            "ID_Gerbong": random.choice(gerbong_ids)
        })
    return pd.DataFrame(rows)

# 5) PETUGAS
def buat_petugas(n):
    rows = []
    jabatan = ["Admin", "Kasir", "Petugas Loket", "Supervisor"]
    for i in range(1, n+1):
        rows.append({
            "ID_Petugas": fmt("PTG", i, 5),
            "Nama_Petugas": fake.name(),
            "Password": fake.password(length=10),
            "Nomor_Telp": fake.phone_number(),
            "Jabatan": random.choice(jabatan)
        })
    return pd.DataFrame(rows)

# 6) TRANSAKSI
def buat_transaksi(n, petugas_df):
    rows = []
    petugas_ids = list(petugas_df["ID_Petugas"])
    metode = ["Tunai", "Transfer", "QRIS", "Kartu Debit"]
    for i in range(1, n+1):
        created = fake.date_between(start_date='-1y', end_date='today')
        rows.append({
            "ID_Transaksi": fmt("TRX", i, 7),
            "ID_Petugas": random.choice(petugas_ids),
            "Nama_Pembeli": fake.name(),
            "Tgl_Transaksi": created.isoformat(),
            "Metode_Transaksi": random.choice(metode)
        })
    return pd.DataFrame(rows)

# 7) PENUMPANG
def buat_penumpang(n):
    rows = []
    for i in range(1, n+1):
        rows.append({
            "NIK": fake.unique.numerify(text="################"),
            "Nama_Penumpang": fake.name(),
            "Email": fake.email(),
            "Nomor_Telepon": fake.phone_number()
        })
    return pd.DataFrame(rows)

# 8) JADWAL_PERJALANAN
def buat_jadwal(n, stasiun_df, kereta_df):
    rows = []
    st_ids = list(stasiun_df["ID_Stasiun"])
    kereta_ids = list(kereta_df["ID_Kereta"])
    for i in range(1, n+1):
        # ambil 2 stasiun berbeda
        awal, tujuan = random.sample(st_ids, 2)
        # tanggal berangkat dalam 30 hari ke depan
        depart_date = fake.date_between(start_date='today', end_date='+30d')
        depart_time = fake.time()
        # buat estimasi tiba beberapa jam setelahnya
        depart_dt = datetime.combine(depart_date, datetime.strptime(depart_time, "%H:%M:%S").time())
        travel_hours = random.randint(1, 8)
        arrive_dt = depart_dt + timedelta(hours=travel_hours)
        price = random.randint(30000, 500000)
        rows.append({
            "ID_Perjalanan": fmt("PRJ", i, 7),
            "ID_StasiunAwal": awal,
            "ID_StasiunTujuan": tujuan,
            "ID_Kereta": random.choice(kereta_ids),
            "Tgl_Keberangkatan": depart_dt.date().isoformat(),
            "Waktu_Keberangkatan": depart_dt.time().isoformat(),
            "Tgl_Tiba": arrive_dt.date().isoformat(),
            "Waktu_Tiba": arrive_dt.time().isoformat(),
            "Harga_Tiket": price
        })
    return pd.DataFrame(rows)

# 9) TIKET
def buat_tiket(n, kursi_df, perjalanan_df, transaksi_df):
    rows = []
    kursi_ids = list(kursi_df["ID_Kursi"])
    perjalanan_ids = list(perjalanan_df["ID_Perjalanan"])
    transaksi_ids = list(transaksi_df["ID_Transaksi"])
    for i in range(1, n+1):
        rows.append({
            "ID_Tiket": fmt("TKT", i, 8),
            "ID_Kursi": random.choice(kursi_ids),
            "ID_Perjalanan": random.choice(perjalanan_ids),
            "ID_Transaksi": random.choice(transaksi_ids),
            "Status_Tiket": random.choice(["Terjual", "Tersedia", "Dibatalkan"])
        })
    return pd.DataFrame(rows)

# Fungsi utama: generate untuk setiap n dan simpan CSV
def generate_all(n):
    print(f"--- Generating dataset n={n} ---")
    stasiun = buat_stasiun(n)
    kereta = buat_kereta(n)
    gerbong = buat_gerbong(n, kereta)
    kursi = buat_kursi(n, gerbong)
    petugas = buat_petugas(n)
    transaksi = buat_transaksi(n, petugas)
    penumpang = buat_penumpang(n)
    jadwal = buat_jadwal(n, stasiun, kereta)
    tiket = buat_tiket(n, kursi, jadwal, transaksi)

    # Simpan CSV (nama file: <tabel>_<n>.csv)
    stasiun.to_csv(f"stasiun_{n}.csv", index=False)
    kereta.to_csv(f"kereta_{n}.csv", index=False)
    gerbong.to_csv(f"gerbong_{n}.csv", index=False)
    kursi.to_csv(f"kursi_{n}.csv", index=False)
    petugas.to_csv(f"petugas_{n}.csv", index=False)
    transaksi.to_csv(f"transaksi_{n}.csv", index=False)
    penumpang.to_csv(f"penumpang_{n}.csv", index=False)
    jadwal.to_csv(f"jadwal_{n}.csv", index=False)
    tiket.to_csv(f"tiket_{n}.csv", index=False)

    print(f"Saved CSVs for n={n}")

if __name__ == "__main__":
    for n in jumlah_data:
        generate_all(n)
    print("✅ All datasets generated.")