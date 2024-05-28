-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 29, 2024 at 12:46 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rso`
--

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `mem_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `position` varchar(255) NOT NULL,
  `mem_org` int(11) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`mem_id`, `name`, `position`, `mem_org`, `date_created`) VALUES
(3, 'John Doe', 'President', 3, '2024-05-23 07:46:25'),
(4, 'Teest', 'President', 1, '2024-05-28 12:16:31'),
(5, 'Mhizzy', '3', 1, '2024-05-28 22:27:37'),
(6, 'John Doe', '1', 1, '2024-05-28 22:27:49');

-- --------------------------------------------------------

--
-- Table structure for table `organizations`
--

CREATE TABLE `organizations` (
  `org_id` int(11) NOT NULL,
  `org_name` varchar(255) NOT NULL,
  `org_logo` varchar(255) NOT NULL,
  `date_createad` timestamp NOT NULL DEFAULT current_timestamp(),
  `vision` text DEFAULT NULL,
  `mission` text DEFAULT NULL,
  `abbreviation` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `organizations`
--

INSERT INTO `organizations` (`org_id`, `org_name`, `org_logo`, `date_createad`, `vision`, `mission`, `abbreviation`) VALUES
(1, 'Adamson Computer Science Students Society (ACOMSS)', '', '2024-05-22 21:44:14', NULL, NULL, NULL),
(3, 'Sample', 'logos\\png-clipart-word-drawing-word-text-logo.png', '2024-05-23 02:29:36', NULL, NULL, NULL),
(4, 'Test', 'logos\\png-clipart-word-drawing-word-text-logo.png', '2024-05-23 07:46:12', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `positions`
--

CREATE TABLE `positions` (
  `pos_id` int(11) NOT NULL,
  `position_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `positions`
--

INSERT INTO `positions` (`pos_id`, `position_name`) VALUES
(1, 'President'),
(2, 'Vice President'),
(3, 'Secretary'),
(4, 'Treasurer'),
(5, 'Member');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`mem_id`);

--
-- Indexes for table `organizations`
--
ALTER TABLE `organizations`
  ADD PRIMARY KEY (`org_id`);

--
-- Indexes for table `positions`
--
ALTER TABLE `positions`
  ADD PRIMARY KEY (`pos_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `mem_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `organizations`
--
ALTER TABLE `organizations`
  MODIFY `org_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `positions`
--
ALTER TABLE `positions`
  MODIFY `pos_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
