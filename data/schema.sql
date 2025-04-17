-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema forum_team
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forum_team
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forum_team` DEFAULT CHARACTER SET utf8mb4 ;
USE `forum_team` ;

-- -----------------------------------------------------
-- Table `forum_team`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_team`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `info` VARCHAR(45) NOT NULL,
  `is_private` TINYINT(1) NULL DEFAULT 0,
  `date_created` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  `is_locked` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2;


-- -----------------------------------------------------
-- Table `forum_team`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_team`.`users` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `telephone_number` VARCHAR(20) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `is_admin` TINYINT(1) NULL DEFAULT 0,
  `password` VARCHAR(100) NOT NULL,
  `date_registration` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2;


-- -----------------------------------------------------
-- Table `forum_team`.`categories_has_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_team`.`categories_has_users` (
  `categories_id` INT(11) NOT NULL,
  `users_id` INT(10) UNSIGNED NOT NULL,
  `access_level` TINYINT(1) NOT NULL,
  PRIMARY KEY (`categories_id`, `users_id`),
  INDEX `fk_categories_has_users_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_categories_has_users_categories1_idx` (`categories_id` ASC) VISIBLE,
  CONSTRAINT `fk_categories_has_users_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `forum_team`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_categories_has_users_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_team`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `forum_team`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_team`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `sender_id` INT(10) UNSIGNED NOT NULL,
  `text` VARCHAR(255) NOT NULL,
  `created_at` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  `receiver_id` INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `sender_id` (`sender_id` ASC) VISIBLE,
  INDEX `fk_messages_users1_idx1` (`receiver_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `forum_team`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `messages_ibfk_1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forum_team`.`users` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_team`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_team`.`topics` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `user_id` INT(10) UNSIGNED NOT NULL,
  `category_id` INT(11) NOT NULL,
  `is_locked` TINYINT(1) NULL DEFAULT 0,
  `date_created` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  `best_reply_id` INT(11) NULL DEFAULT NULL,
  `text` MEDIUMTEXT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `category_id` (`category_id` ASC) VISIBLE,
  INDEX `fk_topics_replies1_idx` (`best_reply_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_replies1`
    FOREIGN KEY (`best_reply_id`)
    REFERENCES `forum_team`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `topics_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_team`.`users` (`id`),
  CONSTRAINT `topics_ibfk_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_team`.`categories` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2;


-- -----------------------------------------------------
-- Table `forum_team`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_team`.`replies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `date_created` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  `date_updated` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  `user_id` INT(10) UNSIGNED NOT NULL,
  `topic_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `topic_id` (`topic_id` ASC) VISIBLE,
  CONSTRAINT `replies_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_team`.`users` (`id`),
  CONSTRAINT `replies_ibfk_2`
    FOREIGN KEY (`topic_id`)
    REFERENCES `forum_team`.`topics` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2;


-- -----------------------------------------------------
-- Table `forum_team`.`replies_has_votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_team`.`replies_has_votes` (
  `replies_id` INT(11) NOT NULL,
  `users_id` INT(10) UNSIGNED NOT NULL,
  `vote_type` TINYINT(1) NOT NULL,
  PRIMARY KEY (`replies_id`, `users_id`),
  INDEX `fk_replies_has_users_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_replies_has_users_replies1_idx` (`replies_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_has_users_replies1`
    FOREIGN KEY (`replies_id`)
    REFERENCES `forum_team`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_has_users_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_team`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
