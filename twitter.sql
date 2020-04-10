/*
 Navicat MySQL Data Transfer

 Source Server         : ubuntu-ata
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : 172.16.18.166:3306
 Source Schema         : twitter

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 10/04/2020 14:38:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ats
-- ----------------------------
DROP TABLE IF EXISTS `ats`;
CREATE TABLE `ats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_time` int(11) DEFAULT NULL,
  `reciever_id` int(11) DEFAULT NULL,
  `tweet_id` int(11) DEFAULT NULL,
  `comment_id` int(11) DEFAULT NULL,
  `at_viewed` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reciever_id` (`reciever_id`),
  KEY `tweet_id` (`tweet_id`),
  KEY `comment_id` (`comment_id`),
  CONSTRAINT `ats_ibfk_1` FOREIGN KEY (`reciever_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ats_ibfk_2` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`),
  CONSTRAINT `ats_ibfk_3` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of ats
-- ----------------------------
BEGIN;
INSERT INTO `ats` VALUES (1, 1586500632, 1, 1, NULL, 0);
INSERT INTO `ats` VALUES (2, 1586500656, 2, 3, NULL, 0);
COMMIT;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(512) DEFAULT NULL,
  `created_time` int(11) DEFAULT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `tweet_id` int(11) DEFAULT NULL,
  `comment_replied` int(11) DEFAULT NULL,
  `user_replied` varchar(256) DEFAULT NULL,
  `reply_viewed` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sender_id` (`sender_id`),
  KEY `tweet_id` (`tweet_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for follows
-- ----------------------------
DROP TABLE IF EXISTS `follows`;
CREATE TABLE `follows` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  `created_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`),
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of follows
-- ----------------------------
BEGIN;
INSERT INTO `follows` VALUES (2, 1, 1586500656);
COMMIT;

-- ----------------------------
-- Table structure for reposts
-- ----------------------------
DROP TABLE IF EXISTS `reposts`;
CREATE TABLE `reposts` (
  `repost_id` int(11) NOT NULL,
  `reposted_id` int(11) NOT NULL,
  PRIMARY KEY (`repost_id`,`reposted_id`),
  KEY `reposted_id` (`reposted_id`),
  CONSTRAINT `reposts_ibfk_1` FOREIGN KEY (`repost_id`) REFERENCES `tweets` (`id`),
  CONSTRAINT `reposts_ibfk_2` FOREIGN KEY (`reposted_id`) REFERENCES `tweets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for tweets
-- ----------------------------
DROP TABLE IF EXISTS `tweets`;
CREATE TABLE `tweets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(512) DEFAULT NULL,
  `created_time` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tweets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tweets
-- ----------------------------
BEGIN;
INSERT INTO `tweets` VALUES (1, '@游客5427 test', 1586500632, 1);
INSERT INTO `tweets` VALUES (2, '测试', 1586500632, 1);
INSERT INTO `tweets` VALUES (3, '@游客6451 test', 1586500656, 1);
INSERT INTO `tweets` VALUES (4, '测试', 1586500656, 2);
INSERT INTO `tweets` VALUES (5, 'mnmn', 1586500660, 2);
COMMIT;

-- ----------------------------
-- Table structure for tweetsImg
-- ----------------------------
DROP TABLE IF EXISTS `tweetsImg`;
CREATE TABLE `tweetsImg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(512) DEFAULT NULL,
  `created_time` int(11) DEFAULT NULL,
  `tweet_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tweet_id` (`tweet_id`),
  CONSTRAINT `tweetsImg_ibfk_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tweetsImg
-- ----------------------------
BEGIN;
INSERT INTO `tweetsImg` VALUES (1, '/static/tweets_picture/1.jpg', 1586500632, 1);
INSERT INTO `tweetsImg` VALUES (2, '/static/tweets_picture/2.jpg', 1586500632, 1);
INSERT INTO `tweetsImg` VALUES (3, '/static/tweets_picture/3.jpg', 1586500632, 1);
INSERT INTO `tweetsImg` VALUES (4, '/static/tweets_picture/4.jpg', 1586500632, 1);
INSERT INTO `tweetsImg` VALUES (5, '/static/tweets_picture/5.jpg', 1586500632, 1);
INSERT INTO `tweetsImg` VALUES (6, '/static/tweets_picture/6.jpg', 1586500632, 1);
INSERT INTO `tweetsImg` VALUES (7, '/static/tweets_picture/7.jpg', 1586500632, 1);
INSERT INTO `tweetsImg` VALUES (8, '/static/tweets_picture/8.jpg', 1586500632, 1);
INSERT INTO `tweetsImg` VALUES (9, '/static/tweets_picture/9.jpg', 1586500632, 1);
INSERT INTO `tweetsImg` VALUES (10, '/static/tweets_picture/1.jpg', 1586500632, 2);
INSERT INTO `tweetsImg` VALUES (11, '/static/tweets_picture/2.jpg', 1586500632, 2);
INSERT INTO `tweetsImg` VALUES (12, '/static/tweets_picture/3.jpg', 1586500632, 2);
INSERT INTO `tweetsImg` VALUES (13, '/static/tweets_picture/4.jpg', 1586500632, 2);
INSERT INTO `tweetsImg` VALUES (14, '/static/tweets_picture/5.jpg', 1586500632, 2);
INSERT INTO `tweetsImg` VALUES (15, '/static/tweets_picture/6.jpg', 1586500632, 2);
INSERT INTO `tweetsImg` VALUES (16, '/static/tweets_picture/7.jpg', 1586500632, 2);
INSERT INTO `tweetsImg` VALUES (17, '/static/tweets_picture/8.jpg', 1586500632, 2);
INSERT INTO `tweetsImg` VALUES (18, '/static/tweets_picture/9.jpg', 1586500632, 2);
INSERT INTO `tweetsImg` VALUES (19, '/static/tweets_picture/1.jpg', 1586500656, 3);
INSERT INTO `tweetsImg` VALUES (20, '/static/tweets_picture/2.jpg', 1586500656, 3);
INSERT INTO `tweetsImg` VALUES (21, '/static/tweets_picture/3.jpg', 1586500656, 3);
INSERT INTO `tweetsImg` VALUES (22, '/static/tweets_picture/4.jpg', 1586500656, 3);
INSERT INTO `tweetsImg` VALUES (23, '/static/tweets_picture/5.jpg', 1586500656, 3);
INSERT INTO `tweetsImg` VALUES (24, '/static/tweets_picture/6.jpg', 1586500656, 3);
INSERT INTO `tweetsImg` VALUES (25, '/static/tweets_picture/7.jpg', 1586500656, 3);
INSERT INTO `tweetsImg` VALUES (26, '/static/tweets_picture/8.jpg', 1586500656, 3);
INSERT INTO `tweetsImg` VALUES (27, '/static/tweets_picture/9.jpg', 1586500656, 3);
INSERT INTO `tweetsImg` VALUES (28, '/static/tweets_picture/1.jpg', 1586500656, 4);
INSERT INTO `tweetsImg` VALUES (29, '/static/tweets_picture/2.jpg', 1586500656, 4);
INSERT INTO `tweetsImg` VALUES (30, '/static/tweets_picture/3.jpg', 1586500656, 4);
INSERT INTO `tweetsImg` VALUES (31, '/static/tweets_picture/4.jpg', 1586500657, 4);
INSERT INTO `tweetsImg` VALUES (32, '/static/tweets_picture/5.jpg', 1586500657, 4);
INSERT INTO `tweetsImg` VALUES (33, '/static/tweets_picture/6.jpg', 1586500657, 4);
INSERT INTO `tweetsImg` VALUES (34, '/static/tweets_picture/7.jpg', 1586500657, 4);
INSERT INTO `tweetsImg` VALUES (35, '/static/tweets_picture/8.jpg', 1586500657, 4);
INSERT INTO `tweetsImg` VALUES (36, '/static/tweets_picture/9.jpg', 1586500657, 4);
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(256) DEFAULT NULL,
  `password` varchar(256) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `avatar` varchar(256) DEFAULT NULL,
  `created_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES (1, '游客5427', '0890e30f769fe5b17818eb82a4adca19', 2, '/static/avatars/default.jpg', 1586500632);
INSERT INTO `users` VALUES (2, '游客6451', '6e12d729d56f67c2f818227b1af7962c', 2, '/static/avatars/default.jpg', 1586500656);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
