-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 13, 2018 at 11:17 AM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 7.2.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `apmt`
--

-- --------------------------------------------------------

--
-- Table structure for table `project`
--

CREATE TABLE `project` (
  `Project_ID` int(11) NOT NULL,
  `Project` varchar(255) NOT NULL,
  `Client_Name` varchar(255) NOT NULL,
  `Technology` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `project`
--

INSERT INTO `project` (`Project_ID`, `Project`, `Client_Name`, `Technology`) VALUES
(1, 'Hotel Web Agency', 'Spyros', 'Wordpress-CMS'),
(5, 'Setford', 'Ben', 'Drupal'),
(6, 'Legal matters and Tilney', 'Andy', '.NET');

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `Task_ID` int(11) NOT NULL,
  `Task_Name` varchar(225) NOT NULL,
  `Task_description` text NOT NULL,
  `Due_Date` date NOT NULL,
  `Status` varchar(255) NOT NULL,
  `Project_Name` varchar(255) NOT NULL,
  `Assignee` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `task`
--

INSERT INTO `task` (`Task_ID`, `Task_Name`, `Task_description`, `Due_Date`, `Status`, `Project_Name`, `Assignee`) VALUES
(6, 'IE10 script error', 'This is a 4 hour task', '2018-11-21', 'In Progress', 'Whizz Pop Bang', 'Nimantha Perera'),
(26, 'Amendments from Martin', '  Will pass to QA  ', '2018-12-03', 'on Hold', 'Legal matters and Tilney', 'Anuja'),
(28, 'Create a mini portal to make referrals and report back.2', ' gikjluiguoi412 ', '2018-12-19', 'In Progress', 'APMT', 'Kumudini'),
(29, 'Amendments in Legal matters and Tilney1', ' tdyseryuji ', '2018-12-11', 'Completed', 'APMT', 'Kumudini'),
(31, 'Amendments in Legal matters and Tilney12', ' tdyseryuji ', '2018-12-11', 'Completed', 'APMT', 'Kumudini'),
(33, 'Amendments in Legal matters and Tilney13', ' tdyseryuji ', '2018-12-11', 'Completed', 'APMT', 'Kumudini'),
(35, 'Amendments in Legal matters and Tilney15', ' tdyseryuji ', '2018-12-11', 'Completed', 'APMT', 'Kumudini'),
(36, 'Amendments in Legal matters and Tilney16', ' tdyseryuji ', '2018-12-11', 'Completed', 'APMT', 'Kumudini'),
(37, 'Amendments in Legal matters and Tilney21', ' 4156745gjkftshx ', '2018-12-11', 'Completed', 'APMT', 'Kumudini'),
(38, 'Amendments in Legal matters and Tilney20', ' 4156745gjkftshx ', '2018-12-11', 'Completed', 'APMT', 'Kumudini'),
(39, 'Training task – Backend part', ' 564789 ', '2018-12-11', 'In Progress', 'APMT', 'Kumudini'),
(41, 'Training task – Backend part1', ' 564789 ', '2018-12-11', 'In Progress', 'APMT', 'Kumudini'),
(43, 'Training task – Backend part2', ' 53498 ', '2018-12-11', 'In Progress', 'APMT', 'Kumudini'),
(44, 'Training task – Backend part10', ' 8796 ', '2018-12-11', 'In Progress', 'APMT', 'Kumudini'),
(45, 'Training task – Backend part3', ' 53498 ', '2018-12-11', 'In Progress', 'APMT', 'Kumudini'),
(46, 'Training task – Backend part4', ' 53498 ', '2018-12-11', 'In Progress', 'APMT', 'Kumudini');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userId` int(11) NOT NULL,
  `userName` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `userrole_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userId`, `userName`, `Email`, `Password`, `userrole_id`) VALUES
(1, 'Kumudini Perera', 'kumudiniaccura@gmail.com', '$2b$12$wu8o5gIWyCB1jG23UyMKPOuadwC960LVr7bQDywcKU.hUsFK5AIwC', 1),
(2, 'Nimesha Kalinga', 'nimesha@gmail.com', '$2b$12$.y0GnQT5sS1JAhVD3tHafeiIyMWQFYxtCHiOAVNMp57pEnkBTLI/i', 2),
(3, 'Nimantha Perera', 'nimanatha@accura-tech.com', '$2b$12$ZvJxxUxyTY2nOpm3xnk4we0FG8yT2/CA15kqB5YIGBBRGeMapAg1q', 2),
(4, 'mike', 'mike@yahoo.com', '$2b$12$3ACSBmHOvmL9JMDDphV3p.sBK.XhxVXzdTJGagLprgWod2vzmV2wy', 2),
(5, 'kumudini accura', 'kumudini@accura-tech.com', '$2b$12$1yk5J0ogOCFnyWhsQo.EyebnoONGIHi6llHptbtWdA.SrpuaZL09e', 1),
(6, 'Punya Perera', 'punya@gmail.com', '$2b$12$y7//q6EnvPHzu.BuY7tCAOWVNW6hsX2nzYcKAMKMuI9C0.LjDgw7y', 2);

-- --------------------------------------------------------

--
-- Table structure for table `user_role`
--

CREATE TABLE `user_role` (
  `userrole_id` int(11) NOT NULL,
  `user_role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_role`
--

INSERT INTO `user_role` (`userrole_id`, `user_role`) VALUES
(1, 'Admin'),
(2, 'Developer\r\n');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `project`
--
ALTER TABLE `project`
  ADD PRIMARY KEY (`Project_ID`),
  ADD UNIQUE KEY `Project_Name` (`Project`);

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`Task_ID`),
  ADD UNIQUE KEY `Task_ID` (`Task_ID`),
  ADD UNIQUE KEY `Task_Name` (`Task_Name`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userId`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `user_role`
--
ALTER TABLE `user_role`
  ADD PRIMARY KEY (`userrole_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `project`
--
ALTER TABLE `project`
  MODIFY `Project_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `task`
--
ALTER TABLE `task`
  MODIFY `Task_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user_role`
--
ALTER TABLE `user_role`
  MODIFY `userrole_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
