-- SQL Dump for `moniepoint` database matching Flask models

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- ========================================================
-- Table structure for table `admin`
-- ========================================================
CREATE TABLE `admin` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`email` varchar(120) NOT NULL,
`password` varchar(300) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(1, '[hello@tosineniolorundafoundation.com](mailto:hello@tosineniolorundafoundation.com)', 'scrypt:32768:8:1$VA4acqcH8l6eyJlt$c8d7a3aa2d7c881f61917989d6481597d26907be2cf6a8ce664bd2981260612da8ed9e01f6e6f31d505230657ffe0566015f0b24f0c9456cc439504478cd86dc');

-- ========================================================
-- Table structure for table `alembic_version`
-- ========================================================
CREATE TABLE `alembic_version` (
`version_num` varchar(32) NOT NULL,
PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `alembic_version` (`version_num`) VALUES
('f0f0da5c1fda');

-- ========================================================
-- Table structure for table `user`
-- ========================================================
CREATE TABLE `user` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`fullname` varchar(120) NOT NULL,
`gender` varchar(120) DEFAULT NULL,
`dob` varchar(120) DEFAULT NULL,
`phone` varchar(225) DEFAULT NULL,
`email` varchar(225) DEFAULT NULL,
`state` varchar(200) DEFAULT NULL,
`geo` varchar(120) DEFAULT NULL,
`media` varchar(200) DEFAULT NULL,
`type` varchar(200) DEFAULT NULL,
`role` varchar(200) DEFAULT NULL,
`journalism` varchar(200) DEFAULT NULL,
`finance` varchar(200) DEFAULT NULL,
`supervisor` varchar(300) DEFAULT NULL,
`approved` varchar(120) DEFAULT 'pending',
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `user` (`id`, `fullname`, `gender`, `dob`, `phone`, `email`, `state`, `geo`, `media`, `type`, `role`, `journalism`, `finance`, `supervisor`, `approved`) VALUES
(1, 'James Berner', 'Male', '2005-01-01', '8147319036', '[godspoweelawrence008@gmail.com](mailto:godspoweelawrence008@gmail.com)', 'Lagos', 'Ikeja', 'profile.jpg', 'Student', 'Applicant', 'Writer', 'Basic', 'Dr. Comfort', 'pending');

-- ========================================================
-- Table structure for table `information`
-- ========================================================
CREATE TABLE `information` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`article1` varchar(255) DEFAULT NULL,
`article2` varchar(255) DEFAULT NULL,
`leadership` varchar(120) DEFAULT NULL,
`leadership_desc` text DEFAULT NULL,
`motivation` text DEFAULT NULL,
`knowledge_use` text DEFAULT NULL,
`commitment` varchar(50) DEFAULT NULL,
`signature` varchar(200) DEFAULT NULL,
`sign_date` varchar(120) DEFAULT NULL,
`user_id` int(11) NOT NULL,
PRIMARY KEY (`id`),
KEY `user_id` (`user_id`),
CONSTRAINT `information_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `information` (`id`, `article1`, `article2`, `leadership`, `leadership_desc`, `motivation`, `knowledge_use`, `commitment`, `signature`, `sign_date`, `user_id`) VALUES
(1, 'Article 1 text', 'Article 2 text', 'Team Lead', 'Managed a group project', 'Highly motivated', 'Practical knowledge use', 'High', 'signature.jpg', '2025-12-01', 1);

COMMIT;
