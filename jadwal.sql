CREATE TABLE Jadwal_Perjalanan (
    ID_Perjalanan VARCHAR(10) PRIMARY KEY,
    ID_StasiunAwal VARCHAR(10) NOT NULL,
    ID_StasiunTujuan VARCHAR(10) NOT NULL,
    ID_Kereta VARCHAR(10) NOT NULL,
    Tgl_Keberangkatan DATE NOT NULL,
    Waktu_Keberangkatan TIME NOT NULL,
    Tgl_Tiba DATE NOT NULL,
    Waktu_Tiba TIME NOT NULL,
    Harga_Tiket NUMERIC(12,2) NOT NULL,
    FOREIGN KEY (ID_StasiunAwal) REFERENCES Stasiun(ID_Stasiun)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (ID_StasiunTujuan) REFERENCES Stasiun(ID_Stasiun)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (ID_Kereta) REFERENCES Kereta(ID_Kereta)
        ON UPDATE CASCADE ON DELETE CASCADE
);
