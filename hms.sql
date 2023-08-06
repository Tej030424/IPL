drop database if exists test;

CREATE database test;

use test;

CREATE TABLE `admin` (
  `employeeid` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
);

INSERT INTO `admin` (`employeeid`, `password`) VALUES
('admin', 'admin');

CREATE TABLE `leaverequests` (
  `id` int AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `regno` varchar(100) NOT NULL,
  `block` varchar(100) NOT NULL,
  `roomno` varchar(100) NOT NULL,
  `fromdate` date NOT NULL,
  `todate` date NOT NULL,
  `reason` varchar(250) NOT NULL,
  `status` varchar(100) NOT NULL DEFAULT 'pending',
  PRIMARY KEY(id)
);

CREATE TABLE `outingrequests` (
  `id` int AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `regno` varchar(100) NOT NULL,
  `block` varchar(100) NOT NULL,
  `roomno` varchar(100) NOT NULL,
  `fromdate` time NOT NULL,
  `todate` time NOT NULL,
  `reason` varchar(250) NOT NULL,
  `status` varchar(100) NOT NULL DEFAULT 'pending',
  PRIMARY KEY(id)
);

CREATE TABLE `users` (
  `name` varchar(100) NOT NULL,
  `regno` varchar(9) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phoneno` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(6) NOT NULL,
  `block` varchar(100) DEFAULT NULL,
  `roomno` int(10) DEFAULT NULL
);

CREATE TABLE complaints (
  `regno` varchar(10),
  `complaint` varchar(300)
);

--
-- Dumping data for table `users`
--

-- INSERT INTO `users` (`name`, `regno`, `email`, `phoneno`, `password`, `gender`, `block`, `roomno`) VALUES
-- ('karthik', '19MIS0240', 'dasarikarthik559@gmail.com', '8885190228', 'BDs4922251@', 'male', 'Kblock', 1),
-- ('divya', '19MIS0241', 'divya@gmail.com', '6305415082', 'BDs4922251@', 'female', 'Qblock', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`employeeid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`regno`);
COMMIT;