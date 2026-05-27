/*
 Navicat Premium Data Transfer

 Source Server         : MariaDB 10.3
 Source Server Type    : MySQL
 Source Server Version : 100332 (10.3.32-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : pubs

 Target Server Type    : MySQL
 Target Server Version : 100332 (10.3.32-MariaDB)
 File Encoding         : 65001

 Date: 26/05/2026 17:24:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for authors
-- ----------------------------
DROP TABLE IF EXISTS `authors`;
CREATE TABLE `authors`  (
  `au_id` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `au_lname` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `au_fname` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `phone` char(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'UNKNOWN',
  `address` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `city` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `state` char(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `zip` char(5) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `contract` bit(1) NOT NULL,
  PRIMARY KEY (`au_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of authors
-- ----------------------------
INSERT INTO `authors` VALUES ('172-32-1176', 'White', 'Johnson', '408 496-7223', '10932 Bigge Rd.', 'Menlo Park', 'CA', '94025', b'1');
INSERT INTO `authors` VALUES ('213-46-8915', 'Green', 'Marjorie', '415 986-7020', '309 63rd St. #411', 'Oakland', 'CA', '94618', b'1');
INSERT INTO `authors` VALUES ('238-95-7766', 'Carson', 'Cheryl', '415 548-7723', '589 Darwin Ln.', 'Berkeley', 'CA', '94705', b'1');
INSERT INTO `authors` VALUES ('267-41-2394', 'O\'Leary', 'Michael', '408 286-2428', '22 Cleveland Av. #14', 'San Jose', 'CA', '95128', b'1');
INSERT INTO `authors` VALUES ('274-80-9391', 'Straight', 'Dean', '415 834-2919', '5420 College Av.', 'Oakland', 'CA', '94609', b'1');
INSERT INTO `authors` VALUES ('341-22-1782', 'Smith', 'Meander', '913 843-0462', '10 Mississippi Dr.', 'Lawrence', 'KS', '66044', b'0');
INSERT INTO `authors` VALUES ('409-56-7008', 'Bennet', 'Abraham', '415 658-9932', '6223 Bateman St.', 'Berkeley', 'CA', '94705', b'1');
INSERT INTO `authors` VALUES ('427-17-2319', 'Dull', 'Ann', '415 836-7128', '3410 Blonde St.', 'Palo Alto', 'CA', '94301', b'1');
INSERT INTO `authors` VALUES ('472-27-2349', 'Gringlesby', 'Burt', '707 938-6445', 'PO Box 792', 'Covelo', 'CA', '95428', b'1');
INSERT INTO `authors` VALUES ('486-29-1786', 'Locksley', 'Charlene', '415 585-4620', '18 Broadway Av.', 'San Francisco', 'CA', '94130', b'1');
INSERT INTO `authors` VALUES ('527-72-3246', 'Greene', 'Morningstar', '615 297-2723', '22 Graybar House Rd.', 'Nashville', 'TN', '37215', b'0');
INSERT INTO `authors` VALUES ('648-92-1872', 'Blotchet-Halls', 'Reginald', '503 745-6402', '55 Hillsdale Bl.', 'Corvallis', 'OR', '97330', b'1');
INSERT INTO `authors` VALUES ('672-71-3249', 'Yokomoto', 'Akiko', '415 935-4228', '3 Silver Ct.', 'Walnut Creek', 'CA', '94595', b'1');
INSERT INTO `authors` VALUES ('712-45-1867', 'del Castillo', 'Innes', '615 996-8275', '2286 Cram Pl. #86', 'Ann Arbor', 'MI', '48105', b'1');
INSERT INTO `authors` VALUES ('722-51-5454', 'DeFrance', 'Michel', '219 547-9982', '3 Balding Pl.', 'Gary', 'IN', '46403', b'1');
INSERT INTO `authors` VALUES ('724-08-9931', 'Stringer', 'Dirk', '415 843-2991', '5420 Telegraph Av.', 'Oakland', 'CA', '94609', b'0');
INSERT INTO `authors` VALUES ('724-80-9391', 'MacFeather', 'Stearns', '415 354-7128', '44 Upland Hts.', 'Oakland', 'CA', '94612', b'1');
INSERT INTO `authors` VALUES ('756-30-7391', 'Karsen', 'Livia', '415 534-9219', '5720 McAuley St.', 'Oakland', 'CA', '94609', b'1');
INSERT INTO `authors` VALUES ('807-91-6654', 'Panteley', 'Sylvia', '301 946-8853', '1956 Arlington Pl.', 'Rockville', 'MD', '20853', b'1');
INSERT INTO `authors` VALUES ('846-92-7186', 'Hunter', 'Sheryl', '415 836-7128', '3410 Blonde St.', 'Palo Alto', 'CA', '94301', b'1');
INSERT INTO `authors` VALUES ('893-72-1158', 'McBadden', 'Heather', '707 448-4982', '301 Putnam', 'Vacaville', 'CA', '95688', b'0');
INSERT INTO `authors` VALUES ('899-46-2035', 'Ringer', 'Anne', '801 826-0752', '67 Seventh Av.', 'Salt Lake City', 'UT', '84152', b'1');
INSERT INTO `authors` VALUES ('998-72-3567', 'Ringer', 'Albert', '801 826-0752', '67 Seventh Av.', 'Salt Lake City', 'UT', '84152', b'1');

-- ----------------------------
-- Table structure for discounts
-- ----------------------------
DROP TABLE IF EXISTS `discounts`;
CREATE TABLE `discounts`  (
  `discounttype` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stor_id` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `lowqty` smallint NULL DEFAULT NULL,
  `highqty` smallint NULL DEFAULT NULL,
  `discount` decimal(4, 2) NOT NULL,
  INDEX `stor_id`(`stor_id` ASC) USING BTREE,
  CONSTRAINT `discounts_ibfk_1` FOREIGN KEY (`stor_id`) REFERENCES `stores` (`stor_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of discounts
-- ----------------------------
INSERT INTO `discounts` VALUES ('Initial Customer', NULL, NULL, NULL, 10.50);
INSERT INTO `discounts` VALUES ('Volume Discount', NULL, 100, 1000, 6.70);
INSERT INTO `discounts` VALUES ('Customer Discount', '8042', NULL, NULL, 5.00);

-- ----------------------------
-- Table structure for employee
-- ----------------------------
DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee`  (
  `emp_id` char(9) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fname` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `minit` char(1) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `lname` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `job_id` int NOT NULL DEFAULT 1,
  `job_lvl` int NOT NULL DEFAULT 10,
  `pub_id` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '9952',
  `hire_date` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '19950818',
  PRIMARY KEY (`emp_id`) USING BTREE,
  INDEX `job_id`(`job_id` ASC) USING BTREE,
  INDEX `pub_id`(`pub_id` ASC) USING BTREE,
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `employee_ibfk_2` FOREIGN KEY (`pub_id`) REFERENCES `publishers` (`pub_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of employee
-- ----------------------------
INSERT INTO `employee` VALUES ('A-C71970F', 'Aria', '', 'Cruz', 10, 87, '1389', '19911026');
INSERT INTO `employee` VALUES ('A-R89858F', 'Annette', '', 'Roulet', 6, 152, '9999', '19900221');
INSERT INTO `employee` VALUES ('AMD15433F', 'Ann', 'M', 'Devon', 3, 200, '9952', '19910716');
INSERT INTO `employee` VALUES ('ARD36773F', 'Anabela', 'R', 'Domingues', 8, 100, '0877', '19930127');
INSERT INTO `employee` VALUES ('CFH28514M', 'Carlos', 'F', 'Hernadez', 5, 211, '9999', '19890421');
INSERT INTO `employee` VALUES ('CGS88322F', 'Carine', 'G', 'Schmitt', 13, 64, '1389', '19920707');
INSERT INTO `employee` VALUES ('DBT39435M', 'Daniel', 'B', 'Tonini', 11, 75, '0877', '19900101');
INSERT INTO `employee` VALUES ('DWR65030M', 'Diego', 'W', 'Roel', 6, 192, '1389', '19911216');
INSERT INTO `employee` VALUES ('ENL44273F', 'Elizabeth', 'N', 'Lincoln', 14, 35, '0877', '19900724');
INSERT INTO `employee` VALUES ('F-C16315M', 'Francisco', '', 'Chang', 4, 227, '9952', '19901103');
INSERT INTO `employee` VALUES ('GHT50241M', 'Gary', 'H', 'Thomas', 9, 170, '0736', '19880809');
INSERT INTO `employee` VALUES ('H-B39728F', 'Helen', '', 'Bennett', 12, 35, '0877', '19890921');
INSERT INTO `employee` VALUES ('HAN90777M', 'Helvetius', 'A', 'Nagy', 7, 120, '9999', '19930319');
INSERT INTO `employee` VALUES ('HAS54740M', 'Howard', 'A', 'Snyder', 12, 100, '0736', '19881119');
INSERT INTO `employee` VALUES ('JYL26161F', 'Janine', 'Y', 'Labrune', 5, 172, '9901', '19910526');
INSERT INTO `employee` VALUES ('KFJ64308F', 'Karin', 'F', 'Josephs', 14, 100, '0736', '19921017');
INSERT INTO `employee` VALUES ('KJJ92907F', 'Karla', 'J', 'Jablonski', 9, 170, '9999', '19940311');
INSERT INTO `employee` VALUES ('L-B31947F', 'Lesley', '', 'Brown', 7, 120, '0877', '19910213');
INSERT INTO `employee` VALUES ('LAL21447M', 'Laurence', 'A', 'Lebihan', 5, 175, '0736', '19900603');
INSERT INTO `employee` VALUES ('M-L67958F', 'Maria', '', 'Larsson', 7, 135, '1389', '19920327');
INSERT INTO `employee` VALUES ('M-P91209M', 'Manuel', '', 'Pereira', 8, 101, '9999', '19890109');
INSERT INTO `employee` VALUES ('M-R38834F', 'Martine', '', 'Rance', 9, 75, '0877', '19920205');
INSERT INTO `employee` VALUES ('MAP77183M', 'Miguel', 'A', 'Paolino', 11, 112, '1389', '19921207');
INSERT INTO `employee` VALUES ('MAS70474F', 'Margaret', 'A', 'Smith', 9, 78, '1389', '19880929');
INSERT INTO `employee` VALUES ('MFS52347M', 'Martin', 'F', 'Sommer', 10, 165, '0736', '19900413');
INSERT INTO `employee` VALUES ('MGK44605M', 'Matti', 'G', 'Karttunen', 6, 220, '0736', '19940501');
INSERT INTO `employee` VALUES ('MJP25939M', 'Maria', 'J', 'Pontes', 5, 246, '1756', '19890301');
INSERT INTO `employee` VALUES ('MMS49649F', 'Mary', 'M', 'Saveley', 8, 175, '0736', '19930629');
INSERT INTO `employee` VALUES ('PCM98509F', 'Patricia', 'C', 'McKenna', 11, 150, '9999', '19890801');
INSERT INTO `employee` VALUES ('PDI47470M', 'Palle', 'D', 'Ibsen', 7, 195, '0736', '19930509');
INSERT INTO `employee` VALUES ('PHF38899M', 'Peter', 'H', 'Franken', 10, 75, '0877', '19920517');
INSERT INTO `employee` VALUES ('PMA42628M', 'Paolo', 'M', 'Accorti', 13, 35, '0877', '19920827');
INSERT INTO `employee` VALUES ('POK93028M', 'Pirkko', 'O', 'Koskitalo', 10, 80, '9999', '19931129');
INSERT INTO `employee` VALUES ('PSA89086M', 'Pedro', 'S', 'Afonso', 14, 89, '1389', '19901224');
INSERT INTO `employee` VALUES ('PSP68661F', 'Paula', 'S', 'Parente', 8, 125, '1389', '19940119');
INSERT INTO `employee` VALUES ('PTC11962M', 'Philip', 'T', 'Cramer', 2, 215, '9952', '19891111');
INSERT INTO `employee` VALUES ('PXH22250M', 'Paul', 'X', 'Henriot', 5, 159, '0877', '19930819');
INSERT INTO `employee` VALUES ('R-M53550M', 'Roland', '', 'Mendel', 11, 150, '0736', '19910905');
INSERT INTO `employee` VALUES ('RBM23061F', 'Rita', 'B', 'Muller', 5, 198, '1622', '19931009');
INSERT INTO `employee` VALUES ('SKO22412M', 'Sven', 'K', 'Ottlieb', 5, 150, '1389', '19910405');
INSERT INTO `employee` VALUES ('TPO55093M', 'Timothy', 'P', 'O\'Rourke', 13, 100, '0736', '19880619');
INSERT INTO `employee` VALUES ('VPA30890F', 'Victoria', 'P', 'Ashworth', 6, 140, '0877', '19900913');
INSERT INTO `employee` VALUES ('Y-L77953M', 'Yoshi', '', 'Latimer', 12, 32, '1389', '19890611');

-- ----------------------------
-- Table structure for jobs
-- ----------------------------
DROP TABLE IF EXISTS `jobs`;
CREATE TABLE `jobs`  (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `job_desc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'New Position - title not formalized yet',
  `min_lvl` int NOT NULL,
  `max_lvl` int NOT NULL,
  PRIMARY KEY (`job_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of jobs
-- ----------------------------
INSERT INTO `jobs` VALUES (1, 'New Hire - Job not specified', 10, 10);
INSERT INTO `jobs` VALUES (2, 'Chief Executive Officer', 200, 250);
INSERT INTO `jobs` VALUES (3, 'Business Operations Manager', 175, 225);
INSERT INTO `jobs` VALUES (4, 'Chief Financial Officier', 175, 250);
INSERT INTO `jobs` VALUES (5, 'Publisher', 150, 250);
INSERT INTO `jobs` VALUES (6, 'Managing Editor', 140, 225);
INSERT INTO `jobs` VALUES (7, 'Marketing Manager', 120, 200);
INSERT INTO `jobs` VALUES (8, 'Public Relations Manager', 100, 175);
INSERT INTO `jobs` VALUES (9, 'Acquisitions Manager', 75, 175);
INSERT INTO `jobs` VALUES (10, 'Productions Manager', 75, 165);
INSERT INTO `jobs` VALUES (11, 'Operations Manager', 75, 150);
INSERT INTO `jobs` VALUES (12, 'Editor', 25, 100);
INSERT INTO `jobs` VALUES (13, 'Sales Representative', 25, 100);
INSERT INTO `jobs` VALUES (14, 'Designer', 25, 100);

-- ----------------------------
-- Table structure for publishers
-- ----------------------------
DROP TABLE IF EXISTS `publishers`;
CREATE TABLE `publishers`  (
  `pub_id` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pub_name` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `city` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `state` char(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `country` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT 'USA',
  PRIMARY KEY (`pub_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of publishers
-- ----------------------------
INSERT INTO `publishers` VALUES ('0736', 'New Moon Books', 'Boston', 'MA', 'USA');
INSERT INTO `publishers` VALUES ('0877', 'Binnet & Hardley', 'Washington', 'DC', 'USA');
INSERT INTO `publishers` VALUES ('1389', 'Algodata Infosystems', 'Berkeley', 'CA', 'USA');
INSERT INTO `publishers` VALUES ('1622', 'Five Lakes Publishing', 'Chicago', 'IL', 'USA');
INSERT INTO `publishers` VALUES ('1756', 'Ramona Publishers', 'Dallas', 'TX', 'USA');
INSERT INTO `publishers` VALUES ('9901', 'GGG&G', 'M nchen', NULL, 'Germany');
INSERT INTO `publishers` VALUES ('9952', 'Scootney Books', 'New York', 'NY', 'USA');
INSERT INTO `publishers` VALUES ('9999', 'Lucerne Publishing', 'Paris', NULL, 'France');

-- ----------------------------
-- Table structure for roysched
-- ----------------------------
DROP TABLE IF EXISTS `roysched`;
CREATE TABLE `roysched`  (
  `title_id` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `lorange` int NULL DEFAULT NULL,
  `hirange` int NULL DEFAULT NULL,
  `royalty` int NULL DEFAULT NULL,
  INDEX `title_id`(`title_id` ASC) USING BTREE,
  CONSTRAINT `roysched_ibfk_1` FOREIGN KEY (`title_id`) REFERENCES `titles` (`title_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of roysched
-- ----------------------------
INSERT INTO `roysched` VALUES ('BU1032', 0, 5000, 10);
INSERT INTO `roysched` VALUES ('PC1035', 10001, 50000, 18);
INSERT INTO `roysched` VALUES ('BU2075', 0, 1000, 10);
INSERT INTO `roysched` VALUES ('PS2091', 1001, 5000, 12);
INSERT INTO `roysched` VALUES ('PS2106', 5001, 10000, 14);
INSERT INTO `roysched` VALUES ('MC3021', 10001, 12000, 22);
INSERT INTO `roysched` VALUES ('TC3218', 14001, 50000, 24);
INSERT INTO `roysched` VALUES ('PC8888', 0, 5000, 10);
INSERT INTO `roysched` VALUES ('PS7777', 0, 5000, 10);
INSERT INTO `roysched` VALUES ('PS3333', 15001, 50000, 16);
INSERT INTO `roysched` VALUES ('BU1111', 8001, 10000, 14);
INSERT INTO `roysched` VALUES ('PS1372', 40001, 50000, 18);

-- ----------------------------
-- Table structure for sales
-- ----------------------------
DROP TABLE IF EXISTS `sales`;
CREATE TABLE `sales`  (
  `stor_id` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ord_num` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ord_date` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `qty` smallint NOT NULL,
  `payterms` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title_id` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`stor_id`, `ord_num`, `title_id`) USING BTREE,
  INDEX `title_id`(`title_id` ASC) USING BTREE,
  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`title_id`) REFERENCES `titles` (`title_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`stor_id`) REFERENCES `stores` (`stor_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sales
-- ----------------------------
INSERT INTO `sales` VALUES ('6380', '722a', '19940913', 3, 'Net 60', 'PS2091');
INSERT INTO `sales` VALUES ('7066', 'A2976', '19930524', 50, 'Net 30', 'PC8888');
INSERT INTO `sales` VALUES ('7066', 'QA7442.3', '19940913', 75, 'ON invoice', 'PS2091');
INSERT INTO `sales` VALUES ('7067', 'D4482', '19940914', 10, 'Net 60', 'PS2091');
INSERT INTO `sales` VALUES ('7067', 'P2121', '19920615', 40, 'Net 30', 'TC3218');
INSERT INTO `sales` VALUES ('7131', 'N914008', '19940914', 20, 'Net 30', 'PS2091');
INSERT INTO `sales` VALUES ('7131', 'P3087a', '19930529', 25, 'Net 60', 'PS7777');
INSERT INTO `sales` VALUES ('7896', 'QQ2299', '19931028', 15, 'Net 60', 'BU7832');
INSERT INTO `sales` VALUES ('8042', '423LL922', '19940914', 15, 'ON invoice', 'MC3021');
INSERT INTO `sales` VALUES ('8042', 'P723', '19930311', 25, 'Net 30', 'BU1111');

-- ----------------------------
-- Table structure for stores
-- ----------------------------
DROP TABLE IF EXISTS `stores`;
CREATE TABLE `stores`  (
  `stor_id` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stor_name` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `stor_address` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `city` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `state` char(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `zip` char(5) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`stor_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of stores
-- ----------------------------
INSERT INTO `stores` VALUES ('6380', 'Eric the Read Books', '788 Catamaugus Ave.', 'Seattle', 'WA', '98056');
INSERT INTO `stores` VALUES ('7066', 'Barnum\'s', '567 Pasadena Ave.', 'Tustin', 'CA', '92789');
INSERT INTO `stores` VALUES ('7067', 'News & Brews', '577 First St.', 'Los Gatos', 'CA', '96745');
INSERT INTO `stores` VALUES ('7131', 'Doc-U-Mat: Quality Laundry and Books', '24-A Avogadro Way', 'Remulade', 'WA', '98014');
INSERT INTO `stores` VALUES ('7896', 'Fricative Bookshop', '89 Madison St.', 'Fremont', 'CA', '90019');
INSERT INTO `stores` VALUES ('8042', 'Bookbeat', '679 Carson St.', 'Portland', 'OR', '89076');

-- ----------------------------
-- Table structure for titleauthor
-- ----------------------------
DROP TABLE IF EXISTS `titleauthor`;
CREATE TABLE `titleauthor`  (
  `au_id` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title_id` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `au_ord` tinyint NULL DEFAULT NULL,
  `royaltyper` int NULL DEFAULT NULL,
  PRIMARY KEY (`au_id`, `title_id`) USING BTREE,
  INDEX `title_id`(`title_id` ASC) USING BTREE,
  CONSTRAINT `titleauthor_ibfk_1` FOREIGN KEY (`title_id`) REFERENCES `titles` (`title_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of titleauthor
-- ----------------------------
INSERT INTO `titleauthor` VALUES ('172-32-1176', 'PS3333', 1, 100);
INSERT INTO `titleauthor` VALUES ('213-46-8915', 'BU2075', 1, 100);
INSERT INTO `titleauthor` VALUES ('238-95-7766', 'PC1035', 1, 100);
INSERT INTO `titleauthor` VALUES ('267-41-2394', 'BU1111', 2, 40);
INSERT INTO `titleauthor` VALUES ('267-41-2394', 'TC7777', 2, 30);
INSERT INTO `titleauthor` VALUES ('274-80-9391', 'BU7832', 1, 100);
INSERT INTO `titleauthor` VALUES ('409-56-7008', 'BU1032', 1, 60);
INSERT INTO `titleauthor` VALUES ('427-17-2319', 'PC8888', 1, 50);
INSERT INTO `titleauthor` VALUES ('472-27-2349', 'TC7777', 3, 30);
INSERT INTO `titleauthor` VALUES ('486-29-1786', 'PC9999', 1, 100);
INSERT INTO `titleauthor` VALUES ('648-92-1872', 'TC4203', 1, 100);
INSERT INTO `titleauthor` VALUES ('672-71-3249', 'TC7777', 1, 40);
INSERT INTO `titleauthor` VALUES ('712-45-1867', 'MC2222', 1, 100);
INSERT INTO `titleauthor` VALUES ('722-51-5454', 'MC3021', 1, 75);
INSERT INTO `titleauthor` VALUES ('724-80-9391', 'PS1372', 2, 25);
INSERT INTO `titleauthor` VALUES ('756-30-7391', 'PS1372', 1, 75);
INSERT INTO `titleauthor` VALUES ('807-91-6654', 'TC3218', 1, 100);
INSERT INTO `titleauthor` VALUES ('846-92-7186', 'PC8888', 2, 50);
INSERT INTO `titleauthor` VALUES ('899-46-2035', 'MC3021', 2, 25);
INSERT INTO `titleauthor` VALUES ('998-72-3567', 'PS2091', 1, 50);

-- ----------------------------
-- Table structure for titles
-- ----------------------------
DROP TABLE IF EXISTS `titles`;
CREATE TABLE `titles`  (
  `title_id` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` char(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'UNDECIDED',
  `pub_id` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `price` decimal(4, 2) NULL DEFAULT NULL,
  `advance` decimal(10, 2) NULL DEFAULT NULL,
  `royalty` int NULL DEFAULT NULL,
  `ytd_sales` int NULL DEFAULT NULL,
  `notes` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`title_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of titles
-- ----------------------------
INSERT INTO `titles` VALUES ('BU1032', 'The Busy Executive\'s Database Guide', 'business', '1389', 19.99, 5000.00, 10, 4095, 'An overview of available database systems with emphasis on common business applications. Illustrated.');
INSERT INTO `titles` VALUES ('BU1111', 'Cooking with Computers: Surreptitious Balance Sheets', 'business', '1389', 11.95, 5000.00, 10, 3876, 'Helpful hints on how to use your electronic resources to the best advantage.');
INSERT INTO `titles` VALUES ('BU2075', 'You Can Combat Computer Stress!', 'business', '0736', 2.99, 10125.00, 24, 18722, 'The latest medical and psychological techniques for living with the electronic office. Easy-to-understand explanations.');
INSERT INTO `titles` VALUES ('BU7832', 'Straight Talk About Computers', 'business', '1389', 19.99, 5000.00, 10, 4095, 'Annotated analysis of what computers can do for you: a no-hype guide for the critical user.');
INSERT INTO `titles` VALUES ('MC2222', 'Silicon Valley Gastronomic Treats', 'mod_cook', '0877', 19.99, 0.00, 12, 2032, 'Favorite recipes for quick, easy, and elegant meals.');
INSERT INTO `titles` VALUES ('MC3021', 'The Gourmet Microwave', 'mod_cook', '0877', 2.99, 15000.00, 24, 22246, 'Traditional French gourmet recipes adapted for modern microwave cooking.');
INSERT INTO `titles` VALUES ('PC1035', 'But Is It User Friendly?', 'popular_comp', '1389', 22.95, 7000.00, 16, 8780, 'A survey of software for the naive user, focusing on the \'friendliness\' of each.');
INSERT INTO `titles` VALUES ('PC8888', 'Secrets of Silicon Valley', 'popular_comp', '1389', 20.00, 8000.00, 10, 4095, 'Muckraking reporting on the world\'s largest computer hardware and software manufacturers.');
INSERT INTO `titles` VALUES ('PC9999', 'Computer ', 'psychology', '0877', 21.59, 7000.00, 10, 375, 'A must for the specialist, this book examines the difference between those who hate and fear computers and those who don\'t.');
INSERT INTO `titles` VALUES ('PS1372', 'Computer Phobic AND Non-Phobic Individuals: Behavior Variations', 'psychology', '0877', 21.59, 7000.00, 10, 375, 'A must for the specialist, this book examines the difference between those who hate and fear computers and those who don\'t.');
INSERT INTO `titles` VALUES ('PS2091', 'Is Anger the Enemy?', 'psychology', '0736', 10.95, 2275.00, 12, 2045, 'Carefully researched study of the effects of strong emotions on the body. Metabolic charts included.');
INSERT INTO `titles` VALUES ('PS2106', 'Life Without Fear', 'psychology', '0736', 7.00, 6000.00, 10, 111, 'New exercise, meditation, and nutritional techniques that can reduce the shock of daily interactions. Popular audience. Sample menus included, exercise video available separately.');
INSERT INTO `titles` VALUES ('PS3333', 'Prolonged Data Deprivation: Four Case Studies', 'psychology', '0736', 19.99, 2000.00, 10, 4072, 'What happens when the data runs dry?  Searching evaluations of information-shortage effects.');
INSERT INTO `titles` VALUES ('PS7777', 'Emotional Security: A New Algorithm', 'psychology', '0736', 7.99, 4000.00, 10, 3336, 'Protecting yourself and your loved ones from undue emotional stress in the modern world. Use of computer and nutritional aids emphasized.');
INSERT INTO `titles` VALUES ('TC3218', 'Onions, Leeks, and Garlic: Cooking Secrets of the Mediterranean', 'trad_cook', '0877', 20.95, 7000.00, 10, 375, 'Profusely illustrated in color, this makes a wonderful gift book for a cuisine-oriented friend.');
INSERT INTO `titles` VALUES ('TC4203', 'Fifty Years in Buckingham Palace Kitchens', 'trad_cook', '0877', 11.95, 4000.00, 14, 15096, 'More anecdotes from the Queen\'s favorite cook describing life among English royalty. Recipes, techniques, tender vignettes.');
INSERT INTO `titles` VALUES ('TC7777', 'Sushi, Anyone?', 'trad_cook', '0877', 14.99, 8000.00, 10, 4095, 'Detailed instructions on how to make authentic Japanese sushi in your spare time.');

-- ----------------------------
-- View structure for autor_pub
-- ----------------------------
DROP VIEW IF EXISTS `autor_pub`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `autor_pub` AS select p.pub_name,a.au_lname,a.au_fname, 
concat(a.au_lname, " ", a.au_fname) as Nombre, 
concat_ws(" ",a.au_lname, a.au_fname) as Nombre2 
, t.title_id
from publishers as p
inner join titles as t on t.pub_id=p.pub_id 
inner join titleauthor as ta on ta.title_id=t.title_id
inner join authors as a on a.au_id=ta.au_id 
order by p.pub_name,Nombre ;

SET FOREIGN_KEY_CHECKS = 1;