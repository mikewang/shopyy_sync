/*
Navicat MySQL Data Transfer

Source Server         : 192.168.1.4
Source Server Version : 50562
Source Host           : 192.168.1.2:3306
Source Database       : jslive

Target Server Type    : MYSQL
Target Server Version : 50562
File Encoding         : 65001

Date: 2021-01-24 08:59:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `client`
-- ----------------------------
DROP TABLE IF EXISTS `client`;
CREATE TABLE `client` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `mac` char(17) NOT NULL,
  `hotelid` int(5) DEFAULT NULL,
  `expdata` varchar(30) DEFAULT NULL,
  `clientname` varchar(20) DEFAULT NULL,
  `status` int(1) NOT NULL DEFAULT '1',
  `lastlogintime` varchar(50) DEFAULT NULL,
  `room` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mac` (`mac`),
  KEY `hotelid` (`hotelid`)
) ENGINE=MyISAM AUTO_INCREMENT=281 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of client
-- ----------------------------
INSERT INTO `client` VALUES ('268', '5c:34:00:4c:00:9d', '9', null, null, '0', '1611280091', '8312');
INSERT INTO `client` VALUES ('250', '5c:34:00:4c:00:40', '9', null, null, '0', '1611216959', '8213');
INSERT INTO `client` VALUES ('273', '5c:34:00:49:d2:05', '9', null, null, '0', '1611282353', '8302');
INSERT INTO `client` VALUES ('249', '5c:34:00:49:d2:c6', '9', null, null, '0', '1611217003', '8218');
INSERT INTO `client` VALUES ('248', '5c:34:00:4c:00:22', '9', null, null, '0', '1611217038', '8215');
INSERT INTO `client` VALUES ('267', '5c:34:00:2c:34:cd', '9', null, null, '0', '1611279745', '8316');
INSERT INTO `client` VALUES ('247', '5c:34:00:2c:34:b2', '9', null, null, '0', '1611217077', '8220');
INSERT INTO `client` VALUES ('246', '5c:34:00:4c:00:be', '9', null, null, '0', '1611217113', '8217');
INSERT INTO `client` VALUES ('266', '5c:34:00:2c:34:d1', '9', null, null, '0', '1611279422', '8309');
INSERT INTO `client` VALUES ('245', '5c:34:00:4c:00:a3', '9', null, null, '0', '1611212363', '8102');
INSERT INTO `client` VALUES ('244', '5c:34:00:4c:00:00', '9', null, null, '0', '1611212018', '8101');
INSERT INTO `client` VALUES ('265', '5c:34:00:2c:34:cf', '9', null, null, '0', '1611279174', '8318');
INSERT INTO `client` VALUES ('243', '5c:34:00:4c:00:a9', '9', null, null, '0', '1611211681', '8106');
INSERT INTO `client` VALUES ('272', '5c:34:00:49:d1:f5', '9', null, null, '0', '1611282046', '8303');
INSERT INTO `client` VALUES ('242', '5c:34:00:2c:34:c5', '9', null, null, '0', '1611211370', '8103');
INSERT INTO `client` VALUES ('264', '5c:34:00:49:d1:8d', '9', null, null, '0', '1611278764', '8311');
INSERT INTO `client` VALUES ('241', '5c:34:00:4c:00:20', '9', null, null, '0', '1611210945', '8108');
INSERT INTO `client` VALUES ('240', '5c:34:00:49:d1:fc', '9', null, null, '0', '1611210997', '8105');
INSERT INTO `client` VALUES ('280', '5c:34:00:49:d1:f4', '9', null, null, '0', '1611292341', null);
INSERT INTO `client` VALUES ('279', '5c:34:00:4c:00:a8', '9', null, null, '0', '1611291892', null);
INSERT INTO `client` VALUES ('278', '5c:34:00:4c:00:1e', '9', null, '', '0', '1611292506', '2310');
INSERT INTO `client` VALUES ('277', '5c:34:00:4c:00:9c', '9', null, null, '0', '1611313058', null);
INSERT INTO `client` VALUES ('276', '5c:34:00:2c:35:27', '9', null, null, '0', '1611336117', null);
INSERT INTO `client` VALUES ('275', '5c:34:00:49:d1:99', '9', null, null, '0', '1611290028', null);
INSERT INTO `client` VALUES ('239', '5c:34:00:49:d2:26', '9', null, null, '0', '1611210159', '8110');
INSERT INTO `client` VALUES ('263', '5c:34:00:49:d1:db', '9', null, null, '0', '1611278369', '8320');
INSERT INTO `client` VALUES ('238', '5c:34:00:49:d2:1b', '9', null, null, '0', '1611278388', '8107');
INSERT INTO `client` VALUES ('271', '5c:34:00:49:d2:7d', '9', null, null, '0', '1611281396', '8308');
INSERT INTO `client` VALUES ('237', '5c:34:00:4c:00:9b', '9', null, null, '0', '1611208512', '8111');
INSERT INTO `client` VALUES ('236', '5c:34:00:49:d2:90', '9', null, null, '0', '1611207395', '8116');
INSERT INTO `client` VALUES ('262', '5c:34:00:2c:34:d2', '9', null, null, '0', '1611278507', '8313');
INSERT INTO `client` VALUES ('235', '5c:34:00:4c:00:2a', '9', null, null, '0', '1611206906', '8113');
INSERT INTO `client` VALUES ('234', '5c:34:00:49:d2:0a', '9', null, null, '0', '1611277293', null);
INSERT INTO `client` VALUES ('233', '5c:34:00:49:d2:3c', '9', null, null, '0', '1611215630', '8109');
INSERT INTO `client` VALUES ('251', '5c:34:00:36:bc:f4', '9', null, null, '0', '1611215684', '8216');
INSERT INTO `client` VALUES ('252', '5c:34:00:2c:34:bf', '9', null, null, '0', '1611216074', '8211');
INSERT INTO `client` VALUES ('253', '5c:34:00:49:d2:b8', '9', null, null, '0', '1611217934', '8212');
INSERT INTO `client` VALUES ('254', '5c:34:00:49:d1:8f', '9', null, null, '0', '1611218337', '8207');
INSERT INTO `client` VALUES ('255', '5c:34:00:49:d1:9c', '9', null, null, '0', '1611218668', '8210');
INSERT INTO `client` VALUES ('256', '5c:34:00:2c:35:12', '9', null, null, '0', '1611219079', '8205');
INSERT INTO `client` VALUES ('257', '5c:34:00:49:d1:ee', '9', null, null, '0', '1611219387', '8208');
INSERT INTO `client` VALUES ('258', '5c:34:00:4c:00:af', '9', null, null, '0', '1611219746', '8203');
INSERT INTO `client` VALUES ('259', '5c:34:00:4c:00:21', '9', null, null, '0', '1611220101', '8206');
INSERT INTO `client` VALUES ('260', '5c:34:00:4c:00:9f', '9', null, null, '0', '1611220360', '8201');
INSERT INTO `client` VALUES ('261', '5c:34:00:2c:34:d5', '9', null, null, '0', '1611220620', '8202');
INSERT INTO `client` VALUES ('269', '5c:34:00:4c:00:19', '9', null, null, '0', '1611280390', '8307');
INSERT INTO `client` VALUES ('270', '5c:34:00:4c:00:1f', '9', null, null, '0', '1611280743', '8310');
INSERT INTO `client` VALUES ('274', '5c:34:00:49:d1:d9', '9', null, null, '0', '1611282679', '8301');
