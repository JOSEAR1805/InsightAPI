ALTER TABLE `auth_user_privilege` CHANGE `image` `image` LONGBLOB NULL DEFAULT NULL;

INSERT INTO `auth_user_privilege` (`id`, `profile_id`, `countries_ids`, `tenders`, `webs`, `profiles`, `users`, `image`, `user_id`) VALUES (NULL, '', '', '1', '1', '1', '1', NULL, '1');
