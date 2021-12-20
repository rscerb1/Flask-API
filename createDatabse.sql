-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema androidproject
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema androidproject
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `androidproject` DEFAULT CHARACTER SET utf8 ;
USE `androidproject` ;

-- -----------------------------------------------------
-- Table `androidproject`.`account_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `androidproject`.`account_info` (
  `username` VARCHAR(10) NOT NULL,
  `password` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`username`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `androidproject`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `androidproject`.`users` (
  `username` VARCHAR(10) NOT NULL,
  `wins` INT NULL DEFAULT '0',
  `ties` INT NULL DEFAULT '0',
  `loses` INT NULL DEFAULT '0',
  PRIMARY KEY (`username`),
  CONSTRAINT `username_account_info`
    FOREIGN KEY (`username`)
    REFERENCES `androidproject`.`account_info` (`username`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `androidproject`.`games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `androidproject`.`games` (
  `player0` VARCHAR(10) NOT NULL,
  `player1` VARCHAR(10) NOT NULL,
  `board` VARCHAR(27) NULL DEFAULT '000000000000000000000000000',
  `turn` TINYINT(1) NULL DEFAULT '0',
  `status` TINYINT NULL DEFAULT NULL,
  PRIMARY KEY (`player0`, `player1`),
  INDEX `active_player0_idx` (`player0` ASC) VISIBLE,
  INDEX `active_player1_idx` (`player1` ASC) VISIBLE,
  CONSTRAINT `active_player0`
    FOREIGN KEY (`player0`)
    REFERENCES `androidproject`.`users` (`username`),
  CONSTRAINT `active_player1`
    FOREIGN KEY (`player1`)
    REFERENCES `androidproject`.`users` (`username`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
