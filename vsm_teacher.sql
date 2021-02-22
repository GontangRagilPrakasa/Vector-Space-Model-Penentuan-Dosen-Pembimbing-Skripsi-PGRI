-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 22 Feb 2021 pada 15.40
-- Versi server: 10.4.11-MariaDB
-- Versi PHP: 7.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vsm_teacher`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `mst_dosen`
--

CREATE TABLE `mst_dosen` (
  `id` int(20) NOT NULL,
  `nama_dosen` varchar(255) NOT NULL,
  `jumlah_pengajar` int(10) NOT NULL DEFAULT 0,
  `created_by` int(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `mst_dosen`
--

INSERT INTO `mst_dosen` (`id`, `nama_dosen`, `jumlah_pengajar`, `created_by`, `created_at`) VALUES
(1, 'Ahmad Riyadi, S.Si, M.Kom', 30, NULL, NULL),
(2, 'Wibawa, S.Si., M.Kom', 0, NULL, NULL),
(3, 'prakoso', 0, 1, '2021-02-22 11:10:00'),
(4, 'dwi santy', 0, 1, '2021-02-22 14:33:59'),
(5, 'gontang', 0, 1, '2021-02-22 14:37:01');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mst_dosen_judul`
--

CREATE TABLE `mst_dosen_judul` (
  `id_judul` int(20) NOT NULL,
  `dosen_id` int(20) NOT NULL,
  `judul` text NOT NULL,
  `preprocessing` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `mst_dosen_judul`
--

INSERT INTO `mst_dosen_judul` (`id_judul`, `dosen_id`, `judul`, `preprocessing`) VALUES
(1, 1, 'MEDIA PENGENALAN ILMU FARAID BERBASIS MULTIMEDIA', 'media kenal ilmu faraid bas multimedia'),
(2, 1, 'SISTEM PENDUKUNG KEPUTUSAN ALTERNATIF CITY CAR TERBARU DENGAN METODE MULTIFACTOR EVALUATION PROCESS', 'sistem dukung putus alternatif city car baru metode multifactor evaluation process'),
(3, 2, 'SISTEM INFORMASI GEOGRAFI JASA KATERING DI WILAYAH KABUPATEN BANTUL BERBASIS ANDORID', 'sistem informasi geografi jasa katering wilayah kabupaten bantul bas andorid'),
(4, 2, 'GAME PETUALANGAN SI KANTAN BERBASIS ANDORID', 'game tualang si kantan bas andorid'),
(5, 5, 'perjudulan duniawi', 'judul duniawi');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mst_role`
--

CREATE TABLE `mst_role` (
  `id` int(10) NOT NULL,
  `nama_role` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `mst_role`
--

INSERT INTO `mst_role` (`id`, `nama_role`, `created_at`) VALUES
(1, 'Super Admin', '2021-01-19 10:05:13'),
(2, 'Dosen', '2021-01-19 10:05:13'),
(3, 'Mahasiswa', '2021-01-19 10:05:41');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mst_users`
--

CREATE TABLE `mst_users` (
  `user_id` int(10) NOT NULL,
  `role_id` int(10) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `no_telephone` varchar(20) NOT NULL,
  `created_by` int(10) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `mst_users`
--

INSERT INTO `mst_users` (`user_id`, `role_id`, `nama`, `email`, `password`, `no_telephone`, `created_by`, `created_at`, `deleted_at`) VALUES
(1, 2, 'ahmad riyadi', 'ahmad_riyadi@mail.com', 'ahmad', '089671723724', 1, '2021-01-19 10:32:42', NULL),
(2, 1, 'Administrator', 'admin@gmail.com', 'admin', '089671723725', 1, '2021-01-19 10:32:44', NULL),
(3, 3, 'santy', 'santy@mail.com', 'santy', '089671723724', 1, '2021-01-19 11:12:40', NULL);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `mst_dosen`
--
ALTER TABLE `mst_dosen`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `mst_dosen_judul`
--
ALTER TABLE `mst_dosen_judul`
  ADD PRIMARY KEY (`id_judul`),
  ADD KEY `mst_dosen_judul_id` (`dosen_id`);

--
-- Indeks untuk tabel `mst_role`
--
ALTER TABLE `mst_role`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `mst_users`
--
ALTER TABLE `mst_users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `mst_dosen`
--
ALTER TABLE `mst_dosen`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT untuk tabel `mst_dosen_judul`
--
ALTER TABLE `mst_dosen_judul`
  MODIFY `id_judul` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `mst_role`
--
ALTER TABLE `mst_role`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `mst_users`
--
ALTER TABLE `mst_users`
  MODIFY `user_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `mst_dosen_judul`
--
ALTER TABLE `mst_dosen_judul`
  ADD CONSTRAINT `mst_dosen_judul_id` FOREIGN KEY (`dosen_id`) REFERENCES `mst_dosen` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
