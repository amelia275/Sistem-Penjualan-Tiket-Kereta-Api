from faker import Faker
import pandas as pd
import random

fake = Faker('id_ID')
Faker.seed(42)
random.seed(42)

# =============================
# JUMLAH DATA UNTUK SEMUA TABEL
# =============================
JUMLAH = 10000

# =============================
# 1. PETUGAS
# =============================
petugas = []
for i in range(1, JUMLAH + 1):
    petugas.append({
        "ID_Petugas": i,
        "Nama_Petugas": fake.name(),
        "Password": fake.password(length=8),
        "Nomor_Telp": fake.phone_number(),
        "Jabatan": random.choice(["Admin", "Kasir", "Petugas Lapangan"])
    })

# =============================
# 2. PENUMPANG
# =============================
penumpang = []
for i in range(1, JUMLAH + 1):
    penumpang.append({
        "NIK": str(random.randint(1000000000000000, 9999999999999999)),
        "Nama_Penumpang": fake.name(),
        "Email": fake.email(),
        "Nomor_Telepon": fake.phone_number()
    })

# =============================
# 3. STASIUN
# =============================
stasiun = []
for i in range(1, JUMLAH + 1):
    stasiun.append({
        "ID_Stasiun": i,
        "Nama_Stasiun": "Stasiun " + fake.city(),
        "Lokasi": fake.city()
    })

# =============================
# 4. KERETA
# =============================
kereta = []
for i in range(1, JUMLAH + 1):
    kereta.append({
        "ID_Kereta": i,
        "Tipe_Layanan": random.choice(["Eksekutif", "Bisnis", "Ekonomi"]),
        "Nama_Kereta": "KA " + fake.first_name()
    })

# =============================
# 5. GERBONG
# =============================
gerbong = []
for i in range(1, JUMLAH + 1):
    gerbong.append({
        "ID_Gerbong": i,
        "Nomor_Gerbong": random.randint(1, 10),
        "Kapasitas": random.choice([40, 50, 60, 80]),
        "ID_Kereta": random.randint(1, JUMLAH)
    })

# =============================
# 6. KURSI
# =============================
kursi = []
for i in range(1, JUMLAH + 1):
    kursi.append({
        "ID_Kursi": i,
        "Nomor_Kursi": f"{random.randint(1,50)}{random.choice(['A','B','C','D'])}",
        "ID_Gerbong": random.randint(1, JUMLAH)
    })

# =============================
# 7. JADWAL PERJALANAN
# =============================
jadwal = []
for i in range(1, JUMLAH + 1):
    st_awal = random.randint(1, JUMLAH)
    st_tujuan = random.choice([x for x in range(1, JUMLAH + 1) if x != st_awal])
    tgl_berangkat = fake.date_between(start_date='+1d', end_date='+30d')
    jadwal.append({
        "ID_Perjalanan": i,
        "ID_StasiunAwal": st_awal,
        "ID_StasiunTujuan": st_tujuan,
        "ID_Kereta": random.randint(1, JUMLAH),
        "Tgl_Keberangkatan": tgl_berangkat,
        "Waktu_Keberangkatan": fake.time(),
        "Tgl_Tiba": tgl_berangkat,
        "Waktu_Tiba": fake.time(),
        "Harga_Tiket": random.choice([150000, 200000, 250000, 300000, 350000])
    })

# =============================
# 8. TRANSAKSI
# =============================
transaksi = []
for i in range(1, JUMLAH + 1):
    transaksi.append({
        "ID_Transaksi": i,
        "ID_Petugas": random.randint(1, JUMLAH),
        "Nama_Pembeli": fake.name(),
        "Tgl_Transaksi": fake.date_between(start_date='-30d', end_date='today'),
        "Metode_Transaksi": random.choice(["Transfer Bank", "QRIS", "Tunai", "Kartu Debit"])
    })

# =============================
# 9. TIKET
# =============================
tiket = []
for i in range(1, JUMLAH + 1):
    tiket.append({
        "ID_Tiket": i,
        "ID_Kursi": random.randint(1, JUMLAH),
        "ID_Perjalanan": random.randint(1, JUMLAH),
        "ID_Transaksi": random.randint(1, JUMLAH),
        "Status_Tiket": random.choice(["Dipesan", "Terbayar", "Dibatalkan"])
    })

# =============================
# EXPORT SEMUA KE FILE CSV
# =============================
pd.DataFrame(petugas).to_csv("petugas.csv", index=False)
pd.DataFrame(penumpang).to_csv("penumpang.csv", index=False)
pd.DataFrame(stasiun).to_csv("stasiun.csv", index=False)
pd.DataFrame(kereta).to_csv("kereta.csv", index=False)
pd.DataFrame(gerbong).to_csv("gerbong.csv", index=False)
pd.DataFrame(kursi).to_csv("kursi.csv", index=False)
pd.DataFrame(jadwal).to_csv("jadwal_perjalanan.csv", index=False)
pd.DataFrame(transaksi).to_csv("transaksi.csv", index=False)
pd.DataFrame(tiket).to_csv("tiket.csv", index=False)

print("✅ Semua tabel berhasil dibuat dengan 10.000 data masing-masing!")
