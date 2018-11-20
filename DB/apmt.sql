-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 20, 2018 at 04:08 AM
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
(1, 'Hotel Web Agency', 'Spyros', 'Wordpress'),
(3, 'Setford', 'Ben', 'Drupal');

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
(1, 'Fix issue where Subscription start dates are overwritten', 'qwerty', '2018-11-14', 'Completed', 'Whizz Pop Bang', 'Nimantha Perera'),
(2, 'Fix issue where Subscription start dates are overwritten-1', 'zaqwe', '2018-11-14', 'Hold', 'Whizz Pop Bang', 'Nimantha Perera'),
(5, 'Fix issue where Subscription start dates are overwritten-2', 'NEW ONE', '0000-00-00', 'Hold', 'Whizz Pop Bang', 'Nimantha Perera'),
(6, 'IE10 script error', 'This is a 4 hour task', '0000-00-00', 'In Progress', 'Whizz Pop Bang', 'Nimantha Perera');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userId` int(11) NOT NULL,
  `userName` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userId`, `userName`, `Email`, `Password`) VALUES
(1, 'Kumudini Perera', 'kumudini12@gmail.com', '$2b$12$JwScgzfzA0libRcKxxE.6etWCxNbTz2hlFsr2AqhlDiGbkM.6iXCq'),
(2, 'Nimesha Kalinga', 'nimesha@gmail.com', '$2b$12$.y0GnQT5sS1JAhVD3tHafeiIyMWQFYxtCHiOAVNMp57pEnkBTLI/i');

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
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `project`
--
ALTER TABLE `project`
  MODIFY `Project_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `task`
--
ALTER TABLE `task`
  MODIFY `Task_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
