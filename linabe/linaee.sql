/*
SQLyog Ultimate v8.63 
MySQL - 5.5.5-10.4.14-MariaDB-1:10.4.14+maria~bionic : Database - linaee
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
USE `linaee`;

/*Table structure for table `auth_group` */

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `auth_group` */

insert  into `auth_group`(`id`,`name`) values (3,'Bodega'),(5,'Contabilidad'),(4,'Gerencia'),(1,'Ventas'),(2,'Ventas Admin');

/*Table structure for table `auth_group_permissions` */

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `auth_group_permissions` */

insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values (5,1,21),(1,1,24),(7,1,54),(10,1,55),(9,1,62);

/*Table structure for table `auth_permission` */

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=latin1;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Compañía',6,'add_cia'),(22,'Can change Compañía',6,'change_cia'),(23,'Can delete Compañía',6,'delete_cia'),(24,'Can view Compañía',6,'view_cia'),(25,'Can add user',7,'add_user'),(26,'Can change user',7,'change_user'),(27,'Can delete user',7,'delete_user'),(28,'Can view user',7,'view_user'),(29,'Access to CRM Module',7,'view_crm_module'),(30,'Access to Sales Module',7,'view_sales_module'),(31,'Access to Purchase Module',7,'view_purchase_module'),(32,'Access to Inventory Module',7,'view_inv_module'),(33,'Access to HR Module',7,'view_hr_module'),(34,'Access to Accounting Module',7,'view_accounting_module'),(35,'Access to Logistics Module',7,'view_logistics_module'),(36,'Access to BI Module',7,'view_linabi_module'),(37,'Access to System Module',7,'view_sys_module'),(38,'Can add Token',8,'add_token'),(39,'Can change Token',8,'change_token'),(40,'Can delete Token',8,'delete_token'),(41,'Can view Token',8,'view_token'),(42,'Can add token',9,'add_tokenproxy'),(43,'Can change token',9,'change_tokenproxy'),(44,'Can delete token',9,'delete_tokenproxy'),(45,'Can view token',9,'view_tokenproxy'),(46,'Can add Secuencia',10,'add_gensequence'),(47,'Can change Secuencia',10,'change_gensequence'),(48,'Can delete Secuencia',10,'delete_gensequence'),(49,'Can view Secuencia',10,'view_gensequence'),(50,'Can add Tipo Generico',11,'add_tipogenerico'),(51,'Can change Tipo Generico',11,'change_tipogenerico'),(52,'Can delete Tipo Generico',11,'delete_tipogenerico'),(53,'Can view Tipo Generico',11,'view_tipogenerico'),(54,'Access to CRM Module',7,'view_module_crm'),(55,'Access to Sales Module',7,'view_module_sales'),(56,'Access to Purchase Module',7,'view_module_purchase'),(57,'Access to Inventory Module',7,'view_module_inv'),(58,'Access to HR Module',7,'view_module_hr'),(59,'Access to Accounting Module',7,'view_module_accounting'),(60,'Access to Logistics Module',7,'view_module_logistics'),(61,'Access to BI Module',7,'view_module_linabi'),(62,'Access to System Module',7,'view_module_sys'),(63,'Can add Stakeholder',12,'add_stakeholder'),(64,'Can change Stakeholder',12,'change_stakeholder'),(65,'Can delete Stakeholder',12,'delete_stakeholder'),(66,'Can view Stakeholder',12,'view_stakeholder'),(67,'View Customers details or list',12,'view_cliente'),(68,'Create Customer',12,'create_cliente'),(69,'Update Customer',12,'update_cliente'),(70,'Edit Customer Credit',12,'change_cliente_cr'),(71,'View Provider details or list',12,'view_proveedor'),(72,'Create Provider',12,'create_proveedor'),(73,'Update Provider',12,'update_proveedor'),(74,'Edit Provider Credit',12,'change_proveedor_cr'),(75,'View Bank details or list',12,'view_banco'),(76,'Create Bank',12,'create_banco'),(77,'Update Bank',12,'update_banco'),(78,'View Partner details or list',12,'view_socio'),(79,'Create Partner',12,'create_socio'),(80,'Update Partner',12,'update_socio');

/*Table structure for table `authtoken_token` */

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `authtoken_token` */

insert  into `authtoken_token`(`key`,`created`,`user_id`) values ('02b59f1a272bd2f0f56b52ab674c618050446e1d','2020-11-16 03:58:51.563723',34),('0dffed776834c0e0e0391c49695e0140b4b6d8f5','2020-11-16 00:33:09.988266',30),('37c8b5fa6142c2bfb2b37009929ded88a9ae8f96','2020-11-15 02:26:09.490194',26),('474ffb8b05d78e77d79bb140df44ad77d172f800','2020-11-16 03:47:46.876710',33),('47a6a9cbfac33d31d8557488aa347b6451dd3e3a','2020-11-14 03:50:59.104973',23),('627011deec9410c8b087b8778596f71712917511','2020-11-13 03:48:18.224356',3),('7eb4adf8e3732fc7eb20e2c7f5b27101496770a1','2020-11-14 02:47:38.736290',14),('895149dfd518321ac89d5d8deb054bebf2cabd38','2020-11-16 15:22:40.122956',35),('a1ffa704dc8d2922af672374447ad42c98245e1a','2020-11-08 17:33:53.784374',1),('ad6ec4eff12f2b7243e82b86349dd2c875b3fbb0','2020-11-08 17:35:17.888093',2),('b54d774a8ccf0a0c185a83f7d357ea69d98640f7','2020-11-13 21:57:40.909630',8),('b5d4c7fd28fbf95b2241064a887a46f2459b2f69','2020-11-14 03:07:19.069331',18),('b5f6467ba10bd4d088f55dee67df642867566099','2020-11-16 03:41:41.286531',32),('b7fad1e9619e59600d9c5436f7a9a058dcb8cc52','2020-11-14 02:52:28.340677',16),('be4c1f56c5f0d0beca00056a4e13a37c6603b109','2020-11-16 00:23:43.891826',29),('c06ec7e6075d0129699ab875a38b06e26d642dcc','2020-11-16 15:33:41.420425',36),('c205a0af914032cf4ecffd080e0ddb36879a86ff','2020-11-13 21:47:39.472765',6),('c2921108b79a8ab43c6e185a3fca62575288a6cf','2020-11-13 04:20:05.143898',4),('ce6a44ffdad9ec01855e0d936b1c1d3435a7ef80','2020-11-15 22:59:06.669826',28),('d0b991588006b3a6457de4927beeda636de60685','2020-11-14 20:31:27.153123',25),('da39f0aee30dfd348ccba6efbba2111fb5bc02a4','2020-11-15 22:42:30.930218',27),('e1d041ebef760ddfbe45af6afa72e5451158fd55','2020-11-14 16:45:00.102842',24),('e26bcf2478fdc169b08983d1f2236cb6f93b05e5','2020-11-16 00:35:59.753274',31),('e7c279ef016d29b01dab804e6ff2b06dc2dfc445','2020-11-13 22:40:33.033787',10),('ed6018627c7eb8e6728751a4c41b7060a52365c2','2020-11-14 03:48:24.625966',22),('f14057156233e8227d25dc43a563449a9469b679','2020-11-13 22:58:36.810531',12),('f49e96d7cfb400134d40f310cd0cf7acac1cac23','2020-11-14 03:11:41.170124',20);

/*Table structure for table `core_user` */

CREATE TABLE `core_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `dni` varchar(30) NOT NULL,
  `direccion` varchar(60) NOT NULL,
  `tel1` varchar(15) NOT NULL,
  `tel2` varchar(15) NOT NULL,
  `tel3` varchar(15) NOT NULL,
  `nombre_corto` varchar(10) NOT NULL,
  `localization` varchar(5) NOT NULL,
  `foto` varchar(100) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `bio` longtext DEFAULT NULL,
  `city` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `cia_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `core_user_cia_id_8ae75a28_fk_lina_core_cia_id` (`cia_id`),
  CONSTRAINT `core_user_cia_id_8ae75a28_fk_lina_core_cia_id` FOREIGN KEY (`cia_id`) REFERENCES `lina_core_cia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;

/*Data for the table `core_user` */

insert  into `core_user`(`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`,`dni`,`direccion`,`tel1`,`tel2`,`tel3`,`nombre_corto`,`localization`,`foto`,`birth_date`,`bio`,`city`,`country`,`modified_at`,`cia_id`) values (1,'pbkdf2_sha256$216000$FNY9gWS8AvKx$z/412dn8Z4hhnO/8FebUQfCUVhYa4/1ZhvLeYXBVW/c=','2021-01-18 21:12:32.740727',1,'root','Moisés','Galván Niño','soporte@numentec.net',1,1,'2020-10-16 01:03:38.323086','','','','','','root','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-13 04:29:36.275110',NULL),(2,'pbkdf2_sha256$216000$KMNcbv9El1Qg$l201bEIpMLH/K1KjiXX8P8/CuzcI+qcafmZ6sYK/qAc=','2020-11-03 23:47:25.000000',0,'venta01','Antigio','Ramirez','anti@numentec.net',1,1,'2020-10-16 20:49:48.641421','3-94-1880','Nuevo Rio, Cuipo','66362581','','','antigio','es_PA','images/profiles/no_image_user.png','1974-11-06','<p>XX</p>','Colón','PA','2020-11-13 04:31:41.531357',1),(3,'pbkdf2_sha256$216000$vczCfSk1zGOu$gckbGnOMUC5hLXjrxz4ujTqZq86UlHKxmMDhprxfJAo=',NULL,0,'ventadmin','Delmy','Atencio','datencio@numentec.net',0,1,'2020-11-13 03:48:17.588296','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-12-01 02:55:29.316487',NULL),(4,'pbkdf2_sha256$216000$PKJpz9AimcHg$AutOHh0qfRo6JdiyEfEsdgesZdIR4aResoYfcuiXrU4=',NULL,0,'venta02','Luisa','Pulido','lpulido@numentec.net',0,1,'2020-11-13 04:20:03.747730','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-12-01 02:55:38.375177',NULL),(6,'pbkdf2_sha256$216000$ODCLFmRSs3fk$1l8BjvHG3Exz77LpHuk0T2K/XeN1GJpQH7DAH1wevuI=',NULL,0,'admin1','Victor','Pineda','vpineda@gmail.com',0,1,'2020-11-13 21:47:38.388659','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-13 21:47:39.466976',NULL),(8,'pbkdf2_sha256$216000$tylS26BdYFYe$TK2TNeUzNuPSPUx7oP9bov3VFDQnWPxQltYC6Is/pO8=',NULL,0,'balalaiko','Bala','Laiko','balalaiko@hotmail.com',0,1,'2020-11-13 21:57:39.895551','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-13 21:57:40.882588',NULL),(10,'pbkdf2_sha256$216000$8wQVQ01aZ29w$bMooPhaX3gj2Z734+9SvlA4DPw9E8zZv+04Pr90vM9s=',NULL,0,'azkel','Azkel','Valdéz','avaldez@edwincenter.com',0,1,'2020-11-13 22:40:31.852851','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-13 22:40:33.021100',NULL),(12,'pbkdf2_sha256$216000$u2cOA2fO7XW6$UpPSpGt2D9L44H8o3p11zyE8OqD4anlhu7TVMJKzkTo=',NULL,0,'aldair','Aldair','Monsilla','amonsilla@nickname.com',0,1,'2020-11-13 22:58:35.703774','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-13 22:58:36.793539',NULL),(14,'pbkdf2_sha256$216000$6k1XtvXSe89r$xKWf3dvBh7OujVNELEHJ6icOBAdRHIr4jdb+L16Jyro=',NULL,0,'carlos','Carlos','Méndez','cmendez@numentec.net',0,1,'2020-11-14 02:47:37.534765','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-14 02:47:38.728989',NULL),(16,'pbkdf2_sha256$216000$1mkX8gczpptj$lW9dTX71ZqKuu7h5T+qi/8uoilsUs5otAP/4du1W/gs=',NULL,0,'leog','Leonardo','González','lgonzalez@numentec.net',0,1,'2020-11-14 02:52:27.242965','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-14 02:52:28.325848',NULL),(18,'pbkdf2_sha256$216000$woykpe18qsvX$STnZ+2iqgHa9GaVDFyX10FBW/264K712L8THbHn5DlU=',NULL,0,'canneo','Canneo','Batista','canneobatista@gmail.com',0,1,'2020-11-14 03:07:17.981136','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-14 03:07:19.061252',NULL),(20,'pbkdf2_sha256$216000$du0NSoxmb0kJ$Zlt1vkneuzHyBVdEY8Ag3OrmXP0OneUIGgh5fLft9gc=',NULL,0,'diana','Diana','Galván','dianag@gmail.com',0,1,'2020-11-14 03:11:40.006674','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-14 03:11:41.166141',NULL),(22,'pbkdf2_sha256$216000$N4xvt0KBaCUE$vKuyKkt5CbU/bB019/fCNgaw5EBAzcMUfRTbeTpYArw=',NULL,0,'greg','Gregorio','Aldana','greg@numentec.net',0,1,'2020-11-14 03:48:24.049600','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-14 03:48:24.620418',NULL),(23,'pbkdf2_sha256$216000$owSZdmKqNspn$Y2OMu2PX3ls+HmlxIi/z8rC7mPYQomuVjEmtQDr/3rs=',NULL,0,'claudia','Claudia','Diaz','cdiaz@hotmail.com',0,1,'2020-11-14 03:50:58.514640','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-14 03:50:59.101083',NULL),(24,'pbkdf2_sha256$216000$6omFmv9Bedh8$xmqIS/T9cxmiInu0sx2d/tMBuxSS5aYvkQkazOdglDU=',NULL,0,'jonathan','Jonathan','Moreno','jmoreno@numentec.net',0,1,'2020-11-14 16:44:59.444939','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-14 16:45:00.096205',NULL),(25,'pbkdf2_sha256$216000$WYUmW7oUS0Uy$r/nQiE6vOzOT+uRqrRl8XgzfK7Mx5/lmXROTePNSi6A=',NULL,0,'badu','Badabum','Valdéz','badu@numentec.net',0,1,'2020-11-14 20:31:26.569173','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-14 20:31:27.144074',NULL),(26,'pbkdf2_sha256$216000$NHabiLEk4PBC$PDudteWwXoRu0KcTFdZSAWIYQ234yejYYYvKlqToSSk=',NULL,0,'arda','Arda','Martinez','arda@gmail.com',0,1,'2020-11-15 02:26:08.808687','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-15 02:26:09.481135',NULL),(27,'pbkdf2_sha256$216000$mUR3E6O2gb1o$IlPumfsUQHAsdMCOAJliJNokkfNOaN304cLy5hd7PE4=',NULL,0,'victor','Victor','Pineda','vitin@numentec.net',0,1,'2020-11-15 22:42:30.265984','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-15 22:42:30.926054',NULL),(28,'pbkdf2_sha256$216000$qyVlHUFVaPf1$tQqM9CzMVBhZulpfEjWdTk81hwM8yu8dQdf0EjFZ/b8=',NULL,0,'nekelda','Nekelda','Ulianov','neke@gmail.com',0,1,'2020-11-15 22:59:06.018916','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-15 22:59:06.664262',NULL),(29,'pbkdf2_sha256$216000$1nUnbEYzeMGp$ki0v04sTiu5PWuSIgFsrr1ackO565HWUMmzIFcmmx3I=',NULL,0,'lina','Marialina','Niño','marialinanino@gmail.com',0,1,'2020-11-16 00:23:43.195139','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-16 02:21:16.597949',NULL),(30,'pbkdf2_sha256$216000$2896H37kfzz4$EFBuAQFthOosou/hMZeT2sWE5GXov6aczE18ZtGkdVo=',NULL,0,'ricardo','Ricardo','Villareal','rvillareal@numentec.net',0,1,'2020-11-16 00:33:09.159099','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-16 00:33:09.983352',NULL),(31,'pbkdf2_sha256$216000$rG39unarsxXb$9UgMWNF2CTKaH4LXx67dmNmCTyIduyryEBOQGIFG/xQ=',NULL,0,'david','David','Becerra','dbecerra@hotmail.com',0,1,'2020-11-16 00:35:59.090993','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-16 00:35:59.748034',NULL),(32,'pbkdf2_sha256$216000$FSRN07zbyWnX$rkdYOphmexvGKqzKICnVIBe3wWfekUNMdVpwW0mNO5Y=',NULL,0,'laura','Laura','Galván','laura@gmail.com',0,1,'2020-11-16 03:41:40.698986','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-16 03:41:41.278713',NULL),(33,'pbkdf2_sha256$216000$ThoxaFT10Fs2$Pf/JGZaobqicdHxjmHtSUn8eV4SeVrEmES8HanIuGi4=',NULL,0,'chila','Valiera','Chila','vchila@numentec.net',0,1,'2020-11-16 03:47:46.245521','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-16 03:47:46.871091',NULL),(34,'pbkdf2_sha256$216000$XZjSgbuUaZDk$w+BJoGVihiWWPgErZJz2dcx1XfqASpPPym7k4RFlOGY=',NULL,0,'hania','Hania','Trujillo','haniat@hotmail.com',0,1,'2020-11-16 03:58:50.968202','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-16 03:58:51.558115',NULL),(35,'pbkdf2_sha256$216000$xv54XSW5Kxjx$9TtsyLMmuqkmtCpqjlbwCUQJnsoCEmEYfSNhiiUftwE=',NULL,0,'Valkiria','Valkiria','Salas','valkiria@numentec.net',0,1,'2020-11-16 15:22:39.468298','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-16 15:22:40.117911',NULL),(36,'kjfrt2020',NULL,0,'teo','Teodolinda','Rodriguez','teorod@numentec.net',0,1,'2020-11-16 15:33:41.413234','','','','','','','es_PA','images/profiles/no_image_user.png',NULL,NULL,'','','2020-11-16 15:33:41.415062',NULL);

/*Table structure for table `core_user_groups` */

CREATE TABLE `core_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

/*Data for the table `core_user_groups` */

insert  into `core_user_groups`(`id`,`user_id`,`group_id`) values (1,2,1),(24,3,2),(25,4,1),(2,28,1),(3,28,3),(11,29,1),(4,29,2),(12,29,3),(5,29,4),(6,30,1),(7,30,3),(8,30,5),(9,31,4),(10,31,5),(13,32,1),(14,32,3),(15,33,2),(16,33,3),(17,34,1),(18,34,4),(19,35,1),(20,35,5),(21,36,2),(22,36,4),(23,36,5);

/*Table structure for table `core_user_user_permissions` */

CREATE TABLE `core_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `core_user_user_permissions` */

/*Table structure for table `django_admin_log` */

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_core_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;

/*Data for the table `django_admin_log` */

insert  into `django_admin_log`(`id`,`action_time`,`object_id`,`object_repr`,`action_flag`,`change_message`,`content_type_id`,`user_id`) values (1,'2020-10-16 01:21:04.038407','1','Cia de Prueba Uno',1,'[{\"added\": {}}]',6,1),(2,'2020-10-16 01:22:24.672824','2','Cia de Prueba Dos',1,'[{\"added\": {}}]',6,1),(3,'2020-10-16 20:49:48.670398','2','venta01',1,'[{\"added\": {}}]',7,1),(4,'2020-10-16 20:59:02.423313','2','venta01',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',7,1),(5,'2020-10-16 23:54:28.840862','2','venta01',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',7,1),(6,'2020-11-03 23:46:54.082875','1','ventas',1,'[{\"added\": {}}]',3,1),(7,'2020-11-03 23:47:09.472287','2','venta01',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',7,1),(8,'2020-11-12 23:59:17.193803','1','ventas',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(9,'2020-11-13 04:29:36.300722','1','root',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',7,1),(10,'2020-11-13 04:31:41.542439','2','venta01',2,'[{\"changed\": {\"fields\": [\"Last name\"]}}]',7,1),(11,'2020-11-14 21:40:36.620694','2','Ventas Admin',1,'[{\"added\": {}}]',3,1),(12,'2020-11-14 21:40:50.831373','3','Bodega',1,'[{\"added\": {}}]',3,1),(13,'2020-11-14 21:41:03.911923','4','Gerencia',1,'[{\"added\": {}}]',3,1),(14,'2020-11-14 21:41:11.613326','5','Contabilidad',1,'[{\"added\": {}}]',3,1),(15,'2020-11-14 21:41:26.704664','1','Ventas',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',3,1),(16,'2020-11-16 02:21:16.613858','29','lina',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',7,1),(17,'2020-12-01 02:19:43.525573','1','Ventas',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(18,'2020-12-01 02:55:29.343903','3','ventadmin',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',7,1),(19,'2020-12-01 02:55:38.386365','4','venta02',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',7,1),(20,'2020-12-01 03:06:36.446209','1','Ventas',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(21,'2020-12-01 03:08:33.027296','1','Ventas',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(22,'2020-12-01 04:12:36.893436','1','Ventas',2,'[]',3,1),(23,'2020-12-01 23:59:28.524587','1','CR1',1,'[{\"added\": {}}]',11,1),(24,'2020-12-01 23:59:33.225287','1','HOPSA, S.A. (X000000001)',1,'[{\"added\": {}}]',12,1),(25,'2020-12-02 00:01:01.438663','2','ANIBAL DELGADO (X000000002)',1,'[{\"added\": {}}]',12,1),(26,'2020-12-02 00:02:21.140659','3','ANAIS DELGADO (X000000003)',1,'[{\"added\": {}}]',12,1),(27,'2020-12-02 00:03:55.763739','4','ABOLU, S.A. (X000000004)',1,'[{\"added\": {}}]',12,1),(28,'2020-12-02 00:05:30.698653','5','PINTURAS OMAR, S.A. (X000000005)',1,'[{\"added\": {}}]',12,1),(29,'2020-12-02 00:06:33.670290','6','BANCO GENERAL (X000000006)',1,'[{\"added\": {}}]',12,1),(30,'2020-12-02 00:07:52.931399','7','RAMON JAQUEZ (X000000007)',1,'[{\"added\": {}}]',12,1);

/*Table structure for table `django_content_type` */

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(8,'authtoken','token'),(9,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(6,'core','cia'),(10,'core','gensequence'),(12,'core','stakeholder'),(11,'core','tipogenerico'),(7,'core','user'),(5,'sessions','session');

/*Table structure for table `django_migrations` */

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values (1,'contenttypes','0001_initial','2020-10-16 01:03:33.813856'),(2,'contenttypes','0002_remove_content_type_name','2020-10-16 01:03:33.896750'),(3,'auth','0001_initial','2020-10-16 01:03:34.035987'),(4,'auth','0002_alter_permission_name_max_length','2020-10-16 01:03:34.300122'),(5,'auth','0003_alter_user_email_max_length','2020-10-16 01:03:34.335115'),(6,'auth','0004_alter_user_username_opts','2020-10-16 01:03:34.361996'),(7,'auth','0005_alter_user_last_login_null','2020-10-16 01:03:34.389323'),(8,'auth','0006_require_contenttypes_0002','2020-10-16 01:03:34.394216'),(9,'auth','0007_alter_validators_add_error_messages','2020-10-16 01:03:34.418403'),(10,'auth','0008_alter_user_username_max_length','2020-10-16 01:03:34.442209'),(11,'auth','0009_alter_user_last_name_max_length','2020-10-16 01:03:34.467820'),(12,'auth','0010_alter_group_name_max_length','2020-10-16 01:03:34.532877'),(13,'auth','0011_update_proxy_permissions','2020-10-16 01:03:34.572696'),(14,'auth','0012_alter_user_first_name_max_length','2020-10-16 01:03:34.598860'),(15,'core','0001_initial','2020-10-16 01:03:34.801804'),(16,'admin','0001_initial','2020-10-16 01:03:35.227582'),(17,'admin','0002_logentry_remove_auto_add','2020-10-16 01:03:35.396046'),(18,'admin','0003_logentry_add_action_flag_choices','2020-10-16 01:03:35.446474'),(19,'sessions','0001_initial','2020-10-16 01:03:35.473233'),(20,'core','0002_remove_user_created_at','2020-10-16 01:15:57.871185'),(21,'core','0003_auto_20201016_2052','2020-10-17 01:53:22.332008'),(22,'authtoken','0001_initial','2020-11-08 17:32:48.286245'),(23,'authtoken','0002_auto_20160226_1747','2020-11-08 17:32:48.464132'),(24,'authtoken','0003_tokenproxy','2020-11-08 17:32:48.471769'),(25,'core','0004_cia_padre','2020-11-30 23:44:13.062683'),(26,'core','0005_gensequence_tipogenerico','2020-12-01 02:07:32.666987'),(27,'core','0006_auto_20201130_2121','2020-12-01 02:22:11.166383'),(28,'core','0007_auto_20201130_2121','2020-12-01 02:22:11.344081'),(29,'core','0008_auto_20201130_2145','2020-12-01 02:45:51.187921');

/*Table structure for table `django_session` */

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `django_session` */

/*Table structure for table `lina_core_cia` */

CREATE TABLE `lina_core_cia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(5) NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `nombre_corto` varchar(30) NOT NULL,
  `ruc` varchar(30) NOT NULL,
  `dv` varchar(3) NOT NULL,
  `direccion` longtext NOT NULL,
  `email` varchar(100) NOT NULL,
  `website` varchar(200) NOT NULL,
  `tel1` varchar(15) NOT NULL,
  `tel2` varchar(15) NOT NULL,
  `fax` varchar(15) NOT NULL,
  `otros_tels` varchar(60) NOT NULL,
  `observacion` longtext NOT NULL,
  `logopath` varchar(100) NOT NULL,
  `logo_url` longtext DEFAULT NULL,
  `soporte_idcli` varchar(10) NOT NULL,
  `country` varchar(64) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `padre_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `lina_core_cia_padre_id_68528270_fk_lina_core_cia_id` (`padre_id`),
  CONSTRAINT `lina_core_cia_padre_id_68528270_fk_lina_core_cia_id` FOREIGN KEY (`padre_id`) REFERENCES `lina_core_cia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `lina_core_cia` */

insert  into `lina_core_cia`(`id`,`codigo`,`nombre`,`nombre_corto`,`ruc`,`dv`,`direccion`,`email`,`website`,`tel1`,`tel2`,`fax`,`otros_tels`,`observacion`,`logopath`,`logo_url`,`soporte_idcli`,`country`,`is_active`,`created_at`,`modified_at`,`padre_id`) values (1,'cia01','Cia de Prueba Uno','CiaUno','100000-10-000001','11','Margarita, Cristobal','cia01@numentec.net','http://cia01.numen.com','4412587','','','','','images/no_image.png','','numencli','PA',1,'2020-10-16 01:21:04.035555','2020-10-16 01:21:04.035596',NULL),(2,'cia02','Cia de Prueba Dos','CiaDos','200000-20-000002','02','Vía Brasil, Panamá','cia02@numentec.net','http://cia02.numen.com','67163581','','','','','images/no_image.png','','numencli02','PA',1,'2020-10-16 01:22:24.668436','2020-10-16 01:22:24.668530',NULL);

/*Table structure for table `lina_core_gensequence` */

CREATE TABLE `lina_core_gensequence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(15) NOT NULL,
  `conteo` int(11) NOT NULL,
  `obs` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `lina_core_gensequence` */

/*Table structure for table `lina_core_stakeholders` */

CREATE TABLE `lina_core_stakeholders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `codigo` varchar(10) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `ruc` varchar(30) NOT NULL,
  `dv` varchar(2) NOT NULL,
  `direccion` longtext NOT NULL,
  `tel1` varchar(15) NOT NULL,
  `tel2` varchar(15) NOT NULL,
  `tel3` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `tipo` varchar(1) NOT NULL,
  `cred` tinyint(1) NOT NULL,
  `exonerado` tinyint(1) NOT NULL,
  `ordencompra` tinyint(1) NOT NULL,
  `diascr` decimal(3,0) NOT NULL,
  `maxcr` decimal(12,2) NOT NULL,
  `contacto` varchar(50) DEFAULT NULL,
  `descauto` decimal(6,3) NOT NULL,
  `retencion` decimal(6,3) NOT NULL,
  `is_cli` tinyint(1) NOT NULL,
  `is_pro` tinyint(1) NOT NULL,
  `is_ban` tinyint(1) NOT NULL,
  `is_soc` tinyint(1) NOT NULL,
  `foto` varchar(100) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `locale` varchar(5) NOT NULL,
  `website` varchar(200) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `idgenerico_id` int(11) NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `lina_core_stakeholders_created_by_id_ea303824_fk_core_user_id` (`created_by_id`),
  KEY `lina_core_stakeholde_idgenerico_id_e8792b3e_fk_lina_core` (`idgenerico_id`),
  KEY `lina_core_stakeholders_modified_by_id_1a5a69af_fk_core_user_id` (`modified_by_id`),
  KEY `lina_core_stakeholders_nombre_3a5d4327` (`nombre`),
  CONSTRAINT `lina_core_stakeholde_idgenerico_id_e8792b3e_fk_lina_core` FOREIGN KEY (`idgenerico_id`) REFERENCES `lina_core_tipo_generico` (`id`),
  CONSTRAINT `lina_core_stakeholders_created_by_id_ea303824_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `lina_core_stakeholders_modified_by_id_1a5a69af_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `lina_core_stakeholders` */

insert  into `lina_core_stakeholders`(`id`,`is_active`,`created_at`,`modified_at`,`codigo`,`nombre`,`ruc`,`dv`,`direccion`,`tel1`,`tel2`,`tel3`,`email`,`tipo`,`cred`,`exonerado`,`ordencompra`,`diascr`,`maxcr`,`contacto`,`descauto`,`retencion`,`is_cli`,`is_pro`,`is_ban`,`is_soc`,`foto`,`birth_date`,`locale`,`website`,`created_by_id`,`idgenerico_id`,`modified_by_id`) values (1,1,'2020-12-01 23:59:33.222883','2020-12-01 23:59:33.222994','X000000001','HOPSA, S.A.','71414-1-45874','62','','442-8172','','','ventas@hopsa.com.pa','J',1,0,0,'30','5000.00','Damaris','0.000','0.000',1,1,0,0,'images/profiles/no_image_user.png',NULL,'es_PA',NULL,NULL,1,NULL),(2,1,'2020-12-02 00:01:01.429188','2020-12-02 00:01:01.429248','X000000002','ANIBAL DELGADO','3-85-2144','15','','66452682','','','','N',1,0,0,'30','1000.00',NULL,'0.000','0.000',1,0,0,0,'images/profiles/no_image_user.png',NULL,'es_PA',NULL,NULL,1,NULL),(3,1,'2020-12-02 00:02:21.138410','2020-12-02 00:02:21.138469','X000000003','ANAIS DELGADO','3-96-1473','00','','67169542','','','','N',1,0,0,'30','2000.00',NULL,'0.000','0.000',1,0,0,0,'images/profiles/no_image_user.png',NULL,'es_PA',NULL,NULL,1,NULL),(4,1,'2020-12-02 00:03:55.758316','2020-12-02 00:03:55.758398','X000000004','ABOLU, S.A.','7451-1-2545','13','','445-3233','','','','J',1,0,0,'30','3000.00','ANIBAL HERNANDEZ','0.000','0.000',0,1,0,0,'images/profiles/no_image_user.png',NULL,'es_PA',NULL,NULL,1,NULL),(5,1,'2020-12-02 00:05:30.696283','2020-12-02 00:05:30.696341','X000000005','PINTURAS OMAR, S.A.','74145-1-77452','26','','445-3244','445-4430','','ventas@pinturasomar.com','J',1,0,0,'30','0.00','TOMY','0.000','0.000',0,1,0,0,'images/profiles/no_image_user.png',NULL,'es_PA',NULL,NULL,1,NULL),(6,1,'2020-12-02 00:06:33.664151','2020-12-02 00:06:33.664209','X000000006','BANCO GENERAL','6542-3-1457','66','','230-2127','','','','N',0,0,0,'30','0.00','YASMIN','0.000','0.000',1,0,1,0,'images/profiles/no_image_user.png',NULL,'es_PA',NULL,NULL,1,NULL),(7,1,'2020-12-02 00:07:52.929082','2020-12-02 00:07:52.929141','X000000007','RAMON JAQUEZ','EP-102-4528','00','','6625-8115','','','','N',1,0,0,'30','1500.00',NULL,'0.000','0.000',1,0,0,1,'images/profiles/no_image_user.png',NULL,'es_PA',NULL,NULL,1,NULL);

/*Table structure for table `lina_core_tipo_generico` */

CREATE TABLE `lina_core_tipo_generico` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `idgenerico` varchar(3) NOT NULL,
  `descripcion` varchar(15) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idgenerico` (`idgenerico`),
  KEY `lina_core_tipo_generico_created_by_id_18cd8d27_fk_core_user_id` (`created_by_id`),
  KEY `lina_core_tipo_generico_modified_by_id_1ba7a362_fk_core_user_id` (`modified_by_id`),
  CONSTRAINT `lina_core_tipo_generico_created_by_id_18cd8d27_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `lina_core_tipo_generico_modified_by_id_1ba7a362_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `lina_core_tipo_generico` */

insert  into `lina_core_tipo_generico`(`id`,`is_active`,`created_at`,`modified_at`,`idgenerico`,`descripcion`,`created_by_id`,`modified_by_id`) values (1,1,'2020-12-01 23:59:28.519823','2020-12-01 23:59:28.519884','CR1','CREDITO TIPO1',NULL,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
