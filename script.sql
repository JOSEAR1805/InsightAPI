ALTER TABLE `auth_user_privilege` ADD `image` BLOB NULL DEFAULT NULL AFTER `user_id`;
ALTER TABLE `auth_user_privilege` CHANGE `image` `image` LONGBLOB NULL DEFAULT NULL;