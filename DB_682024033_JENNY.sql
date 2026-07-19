-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: gateway01.ap-southeast-1.prod.aws.tidbcloud.com    Database: portfolio_jenny
-- ------------------------------------------------------
-- Server version	8.0.11-TiDB-v8.5.3-serverless

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(190) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  UNIQUE KEY `ix_admins_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'Jenny','jenjeoyy01@gmail.com','scrypt:32768:8:1$nG0UxJhSrcKOv3l4$9daee825c650e833be761803a3a637d3f40c5e160b8829ea8079421181552d305ee886bdf18d5876529a72ef069b17260cf0f7f8f2337b4159c658955787869d','2026-07-11 16:02:22','2026-07-11 16:27:42');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_messages`
--

DROP TABLE IF EXISTS `contact_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `email` varchar(190) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `email_status` varchar(30) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `ix_contact_messages_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_messages`
--

LOCK TABLES `contact_messages` WRITE;
/*!40000 ALTER TABLE `contact_messages` DISABLE KEYS */;
INSERT INTO `contact_messages` VALUES (1,'jessy','682024033@student.uksw.edu','mencoba','hai apa kabar!',1,'sent','2026-07-11 16:43:40','2026-07-11 16:47:52');
/*!40000 ALTER TABLE `contact_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiences`
--

DROP TABLE IF EXISTS `experiences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company` varchar(150) NOT NULL,
  `role` varchar(150) NOT NULL,
  `start_year` varchar(20) NOT NULL,
  `end_year` varchar(20) NOT NULL,
  `description` text NOT NULL,
  `image_url` varchar(500) NOT NULL,
  `image_public_id` varchar(255) NOT NULL,
  `icon` varchar(100) NOT NULL,
  `sort_order` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=60001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiences`
--

LOCK TABLES `experiences` WRITE;
/*!40000 ALTER TABLE `experiences` DISABLE KEYS */;
INSERT INTO `experiences` VALUES (1,'Project Portfolio','UI/UX Designer & Developer','2026','Sekarang','Merancang dan membangun berbagai website akademik dengan fokus pada pengalaman pengguna, konsistensi visual, dan integrasi data.','https://res.cloudinary.com/drzymxjsk/image/upload/v1784447200/portfolio-jenny/experiences/image_v3rpyh.png','portfolio-jenny/experiences/image_v3rpyh','bi-flower1',1,'2026-07-11 16:02:23','2026-07-19 07:46:41'),(3,'Perkuliahan Sistem Informasi','Student Researcher','2024','Sekarang','Mengerjakan analisis proses bisnis, basis data, perancangan sistem, dan implementasi aplikasi berbasis web.','https://res.cloudinary.com/drzymxjsk/image/upload/v1784447461/portfolio-jenny/experiences/image_igs1xp.jpg','portfolio-jenny/experiences/image_igs1xp','bi-leaf',3,'2026-07-11 16:02:23','2026-07-19 07:51:02'),(30001,'ISFEST','Koordinator Divisi Fundreshing','2025','2025','Saya memiliki pengalaman pertama menjadi ketua di salahsatu divisi dan sangat menyenangkan dan menambah pengalaman saya menjadi seorang leader','https://res.cloudinary.com/drzymxjsk/image/upload/v1784447253/portfolio-jenny/experiences/image_rvvlcd.jpg','portfolio-jenny/experiences/image_rvvlcd','bi-flower1',1,'2026-07-12 10:01:09','2026-07-19 07:49:04');
/*!40000 ALTER TABLE `experiences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles`
--

DROP TABLE IF EXISTS `profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `greeting` varchar(100) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `title` varchar(255) NOT NULL,
  `short_description` text NOT NULL,
  `about_text` text NOT NULL,
  `photo_url` varchar(500) NOT NULL,
  `photo_public_id` varchar(255) NOT NULL,
  `resume_url` varchar(500) NOT NULL,
  `email` varchar(190) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `location` varchar(150) NOT NULL,
  `github_url` varchar(500) NOT NULL,
  `linkedin_url` varchar(500) NOT NULL,
  `instagram_url` varchar(500) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles`
--

LOCK TABLES `profiles` WRITE;
/*!40000 ALTER TABLE `profiles` DISABLE KEYS */;
INSERT INTO `profiles` VALUES (1,'Halo! Saya','Jenny Annanda Prasetya','Mahasiswa S1 Sistem Informasi Universitas Kristen Satya Wacana','','Halo, saya Jenny Annanda, mahasiswa Program Studi Sistem Informasi di Universitas Kristen Satya Wacana. Saya memiliki ketertarikan pada bidang pengembangan website, analisis sistem, dan desain antarmuka (UI/UX). Saya senang mempelajari bagaimana teknologi dapat digunakan untuk menciptakan solusi digital yang efektif, mudah digunakan, dan memiliki tampilan yang menarik. Portofolio ini saya buat sebagai media untuk menampilkan perjalanan belajar, kemampuan, pengalaman, serta berbagai proyek yang telah saya kerjakan selama menempuh pendidikan. Melalui setiap proyek, saya terus mengembangkan keterampilan dalam analisis kebutuhan, perancangan sistem, pengembangan aplikasi web, serta pemecahan masalah menggunakan teknologi informasi. Saya percaya bahwa proses belajar adalah perjalanan yang berkelanjutan. Oleh karena itu, saya selalu terbuka untuk mempelajari teknologi baru, menerima tantangan, dan terus meningkatkan kemampuan agar dapat memberikan kontribusi yang bermanfaat di dunia teknologi informasi.','https://res.cloudinary.com/drzymxjsk/image/upload/v1783849362/portfolio-jenny/profile/photo_tjssxb.jpg','portfolio-jenny/profile/photo_tjssxb','','','','Salatiga, Indonesia','','','https://www.instagram.com/jnnyannda_','2026-07-11 16:02:22','2026-07-14 14:45:45');
/*!40000 ALTER TABLE `profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `category` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `technologies` varchar(255) NOT NULL,
  `image_url` varchar(500) NOT NULL,
  `image_public_id` varchar(255) NOT NULL,
  `project_url` varchar(500) NOT NULL,
  `github_url` varchar(500) NOT NULL,
  `sort_order` int NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'Sistem Informasi Portofolio','Flask Web App','Website portofolio dinamis dengan dashboard admin, TiDB Cloud, Cloudinary, dan notifikasi email Resend.','Flask, TiDB, Cloudinary, Resend','https://res.cloudinary.com/drzymxjsk/image/upload/v1784447528/portfolio-jenny/projects/image_w9lihg.png','portfolio-jenny/projects/image_w9lihg','','',1,1,'2026-07-11 16:02:23','2026-07-19 07:52:09'),(2,'Website Hotel Kenangan In','UI/UX & Development','Website Lokal untuk membantu proses kerja di hotel kenangan in dalam memesan','Figma, HTML, CSS, JavaScript','https://res.cloudinary.com/drzymxjsk/image/upload/v1784447814/portfolio-jenny/projects/image_cf1mn2.jpg','portfolio-jenny/projects/image_cf1mn2','','',2,1,'2026-07-11 16:02:23','2026-07-19 07:56:55'),(3,'Sistem Pemesanan Tiket','UI/UX & Development','Aplikasi pendaftaran seminar yang dirancang untuk menangani antrean dan pembaruan data secara terstruktur.','Python, Reach, JavaScript, TiDB, Vercel','https://res.cloudinary.com/drzymxjsk/image/upload/v1784447789/portfolio-jenny/projects/image_crqglg.jpg','portfolio-jenny/projects/image_crqglg','','',3,1,'2026-07-11 16:02:23','2026-07-19 07:56:30');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `icon` varchar(100) NOT NULL,
  `accent` varchar(20) NOT NULL,
  `sort_order` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=60001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills`
--

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
INSERT INTO `skills` VALUES (1,'Figma','Menyusun wireframe, prototipe, dan design system yang konsisten.','bi-vector-pen','pink',1,1,'2026-07-11 16:02:22','2026-07-12 09:51:20'),(3,'Oracle Administrator','Memahami dasar administrasi database Oracle, seperti pengelolaan pengguna, hak akses, backup, recovery, dan pemantauan database.','bi-database','green',2,1,'2026-07-11 16:02:23','2026-07-12 09:50:57'),(4,'Sistem Enterprise','Memahami penerapan sistem terintegrasi untuk membantu pengelolaan proses bisnis dan informasi dalam organisasi.','bi-diagram-3','pink',3,1,'2026-07-11 16:02:23','2026-07-12 09:52:01'),(30001,'Statistika','Memahami pengolahan, analisis, dan interpretasi data untuk menghasilkan informasi yang mendukung pengambilan keputusan.','bi-pie-chart','green',4,1,'2026-07-12 09:54:18','2026-07-12 09:54:52');
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-19 17:36:06
