CREATE TABLE Transaksi (
    ID_Transaksi VARCHAR(10) PRIMARY KEY,
    ID_Petugas VARCHAR(10) NOT NULL,
    Nama_Pembeli VARCHAR(100) NOT NULL,
    Tgl_Transaksi DATE NOT NULL,
    Metode_Transaksi VARCHAR(50),
    FOREIGN KEY (ID_Petugas) REFERENCES Petugas(ID_Petugas)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
