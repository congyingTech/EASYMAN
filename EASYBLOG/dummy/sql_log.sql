CREATE TABLE `easyman_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `post_hash` varchar(255) NOT NULL COMMENT 'post唯一标识符',
  `post_content` LONGTEXT NOT NULL COMMENT 'post的内容',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_post_hash` (`post_hash`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;