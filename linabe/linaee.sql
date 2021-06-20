-- MariaDB dump 10.17  Distrib 10.4.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: linaee
-- ------------------------------------------------------
-- Server version	10.4.14-MariaDB-1:10.4.14+maria~bionic

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'contabilidad'),(1,'gerencia'),(5,'trafico'),(3,'ventadmin'),(4,'ventas');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,16),(2,1,17),(3,1,18),(4,1,19),(5,1,20),(6,1,25),(7,1,26),(8,1,27),(9,1,28),(10,1,29),(11,1,30),(12,1,31),(13,1,32),(14,1,33),(15,1,38),(16,1,39),(17,1,40),(18,1,41),(19,1,42),(20,1,46),(21,1,54),(22,1,58),(23,1,59),(24,1,60),(25,1,61),(26,1,62),(27,1,63),(28,1,64),(29,1,65),(30,1,66),(31,1,67),(32,1,68),(33,1,69),(34,1,70),(35,1,71),(36,1,72),(37,1,73),(38,1,74),(39,1,75),(40,1,76),(41,1,77),(42,1,78),(43,1,79),(44,1,80),(45,1,85),(46,1,86),(47,1,87),(48,1,88),(49,1,89),(50,1,90),(51,1,91),(52,1,92),(53,1,93),(54,1,94),(55,1,95),(56,1,96),(63,2,25),(64,2,30),(57,2,32),(58,2,38),(59,2,39),(60,2,40),(61,2,41),(62,2,42),(65,3,16),(66,3,20),(67,3,25),(68,3,26),(69,3,27),(70,3,28),(71,3,32),(72,3,38),(73,3,39),(74,3,58),(75,3,59),(76,3,60),(77,3,62),(78,3,63),(79,3,64),(80,3,65),(81,3,66),(82,3,67),(83,3,68),(84,3,69),(85,3,80),(86,3,88),(87,3,92),(88,3,96),(96,4,20),(98,4,25),(99,4,26),(89,4,32),(93,4,38),(94,4,39),(92,4,58),(101,4,62),(102,4,63),(91,4,67),(95,4,80),(97,4,88),(100,4,92),(90,4,96),(110,5,20),(112,5,25),(114,5,28),(116,5,31),(103,5,32),(105,5,38),(107,5,39),(113,5,58),(115,5,62),(106,5,71),(109,5,80),(111,5,88),(108,5,92),(104,5,96);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add content type',3,'add_contenttype'),(10,'Can change content type',3,'change_contenttype'),(11,'Can delete content type',3,'delete_contenttype'),(12,'Can view content type',3,'view_contenttype'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add Secuencia',5,'add_gensequence'),(18,'Can change Secuencia',5,'change_gensequence'),(19,'Can delete Secuencia',5,'delete_gensequence'),(20,'Can view Secuencia',5,'view_gensequence'),(21,'Can add Módulo',6,'add_modulo'),(22,'Can change Módulo',6,'change_modulo'),(23,'Can delete Módulo',6,'delete_modulo'),(24,'Can view Módulo',6,'view_modulo'),(25,'Access to CRM Module',6,'acc_crm'),(26,'Access to Sales Module',6,'acc_sales'),(27,'Access to Purchase Module',6,'acc_purchase'),(28,'Access to Inventory Module',6,'acc_inv'),(29,'Access to HR Module',6,'acc_hr'),(30,'Access to Accounting Module',6,'acc_accounting'),(31,'Access to Logistics Module',6,'acc_logistics'),(32,'Access to BI Module',6,'acc_linabi'),(33,'Access to Configuration Module',6,'acc_config'),(34,'Can add Vista',7,'add_vista'),(35,'Can change Vista',7,'change_vista'),(36,'Can delete Vista',7,'delete_vista'),(37,'Can view Vista',7,'view_vista'),(38,'Access to LinaBI Catalog view',7,'acc_linabi_catalog'),(39,'Access to LinaBI Sale Docs Master view',7,'acc_linabi_saledocs_master'),(40,'Access to LinaBI Sale Docs Detail view',7,'acc_linabi_saledocs_datail'),(41,'Access to LinaBI  Sales Detail view',7,'acc_linabi_sales_detail'),(42,'Access to LinaBI  Reports view',7,'acc_linabi_reports'),(43,'Can add Configuración por Vista',8,'add_vistaconfig'),(44,'Can change Configuración por Vista',8,'change_vistaconfig'),(45,'Can delete Configuración por Vista',8,'delete_vistaconfig'),(46,'Can view Configuración por Vista',8,'view_vistaconfig'),(47,'Can add Configuración por Vista y Usuario',9,'add_vistaconfiguser'),(48,'Can change Configuración por Vista y Usuario',9,'change_vistaconfiguser'),(49,'Can delete Configuración por Vista y Usuario',9,'delete_vistaconfiguser'),(50,'Can view Configuración por Vista y Usuario',9,'view_vistaconfiguser'),(51,'Can add Acceso a conf',10,'add_vistaconfigacc'),(52,'Can change Acceso a conf',10,'change_vistaconfigacc'),(53,'Can delete Acceso a conf',10,'delete_vistaconfigacc'),(54,'Can view Acceso a conf',10,'view_vistaconfigacc'),(55,'Can add Tipo Generico',11,'add_tipogenerico'),(56,'Can change Tipo Generico',11,'change_tipogenerico'),(57,'Can delete Tipo Generico',11,'delete_tipogenerico'),(58,'Can view Tipo Generico',11,'view_tipogenerico'),(59,'Can add Stakeholder',12,'add_stakeholder'),(60,'Can change Stakeholder',12,'change_stakeholder'),(61,'Can delete Stakeholder',12,'delete_stakeholder'),(62,'Can view Stakeholder',12,'view_stakeholder'),(63,'View customers details or list',12,'view_cliente'),(64,'Create customer',12,'create_cliente'),(65,'Update customer',12,'update_cliente'),(66,'Edit customer credit',12,'change_cliente_cr'),(67,'View supplier details or list',12,'view_proveedor'),(68,'Create supplier',12,'create_proveedor'),(69,'Update supplier',12,'update_proveedor'),(70,'Edit supplier credit',12,'change_proveedor_cr'),(71,'View bank details or list',12,'view_banco'),(72,'Create bank',12,'create_banco'),(73,'Update bank',12,'update_banco'),(74,'View partner details or list',12,'view_socio'),(75,'Create partner',12,'create_socio'),(76,'Update partner',12,'update_socio'),(77,'Can add Compañía',13,'add_cia'),(78,'Can change Compañía',13,'change_cia'),(79,'Can delete Compañía',13,'delete_cia'),(80,'Can view Compañía',13,'view_cia'),(81,'Can add bi catalog',14,'add_bicatalog'),(82,'Can change bi catalog',14,'change_bicatalog'),(83,'Can delete bi catalog',14,'delete_bicatalog'),(84,'Can view bi catalog',14,'view_bicatalog'),(85,'Can add Plantilla xlsx',15,'add_bixlsxtemplate'),(86,'Can change Plantilla xlsx',15,'change_bixlsxtemplate'),(87,'Can delete Plantilla xlsx',15,'delete_bixlsxtemplate'),(88,'Can view Plantilla xlsx',15,'view_bixlsxtemplate'),(89,'Can add Columna',16,'add_bixlsxtemplatecol'),(90,'Can change Columna',16,'change_bixlsxtemplatecol'),(91,'Can delete Columna',16,'delete_bixlsxtemplatecol'),(92,'Can view Columna',16,'view_bixlsxtemplatecol'),(93,'Can add Favorito',17,'add_bifavorito'),(94,'Can change Favorito',17,'change_bifavorito'),(95,'Can delete Favorito',17,'delete_bifavorito'),(96,'Can view Favorito',17,'view_bifavorito'),(97,'Can add log entry',18,'add_logentry'),(98,'Can change log entry',18,'change_logentry'),(99,'Can delete log entry',18,'delete_logentry'),(100,'Can view log entry',18,'view_logentry'),(101,'Can add session',19,'add_session'),(102,'Can change session',19,'change_session'),(103,'Can delete session',19,'delete_session'),(104,'Can view session',19,'view_session'),(105,'Can add Token',20,'add_token'),(106,'Can change Token',20,'change_token'),(107,'Can delete Token',20,'delete_token'),(108,'Can view Token',20,'view_token'),(109,'Can add token',21,'add_tokenproxy'),(110,'Can change token',21,'change_tokenproxy'),(111,'Can delete token',21,'delete_tokenproxy'),(112,'Can view token',21,'view_tokenproxy');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('21b6d8edc9cdc3f97a3765bf93a5d34c80baf151','2021-06-20 19:10:46.913465',1);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_cia`
--

DROP TABLE IF EXISTS `core_cia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_cia` (
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
  KEY `core_cia_padre_id_9ee0ab1a_fk_core_cia_id` (`padre_id`),
  CONSTRAINT `core_cia_padre_id_9ee0ab1a_fk_core_cia_id` FOREIGN KEY (`padre_id`) REFERENCES `core_cia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_cia`
--

LOCK TABLES `core_cia` WRITE;
/*!40000 ALTER TABLE `core_cia` DISABLE KEYS */;
INSERT INTO `core_cia` VALUES (1,'cia01','Cia de Prueba Uno','CiaUno','100000-10-000001','11','Margarita, Cristobal','cia01@numentec.net','http://cia01.numen.com','4412587','','','','','images/no_image.png','','numencli','PA',1,'2020-10-16 01:21:04.035555','2020-10-16 01:21:04.035596',NULL);
/*!40000 ALTER TABLE `core_cia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_gensequence`
--

DROP TABLE IF EXISTS `core_gensequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_gensequence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(15) NOT NULL,
  `conteo` int(11) NOT NULL,
  `obs` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_gensequence`
--

LOCK TABLES `core_gensequence` WRITE;
/*!40000 ALTER TABLE `core_gensequence` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_gensequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_modulos`
--

DROP TABLE IF EXISTS `core_modulos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_modulos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) NOT NULL,
  `descrip` varchar(50) NOT NULL,
  `tipo` int(10) unsigned NOT NULL CHECK (`tipo` >= 0),
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_modulos`
--

LOCK TABLES `core_modulos` WRITE;
/*!40000 ALTER TABLE `core_modulos` DISABLE KEYS */;
INSERT INTO `core_modulos` VALUES (1,'core','Módulo base del sistema. Núcleo.',1,0),(2,'inv','Inventario',2,0),(3,'linabi','Lina Business Intelligence',2,1),(4,'crm','Lina CRM',2,1),(5,'ventas','Lina Ventas',2,0),(6,'compras','Lina Compras',2,0),(7,'rrhh','Lina Recursos Humanos',2,1),(8,'conta','Lina Contabilidad',2,0),(9,'logistica','Lina Logística',2,0),(10,'config','Lina Configuración',1,1);
/*!40000 ALTER TABLE `core_modulos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_stakeholders`
--

DROP TABLE IF EXISTS `core_stakeholders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_stakeholders` (
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
  KEY `core_stakeholders_created_by_id_dfd4a653_fk_core_user_id` (`created_by_id`),
  KEY `core_stakeholders_idgenerico_id_612e4023_fk_core_tipo` (`idgenerico_id`),
  KEY `core_stakeholders_modified_by_id_40320095_fk_core_user_id` (`modified_by_id`),
  KEY `core_stakeholders_nombre_9f080303` (`nombre`),
  CONSTRAINT `core_stakeholders_created_by_id_dfd4a653_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_stakeholders_idgenerico_id_612e4023_fk_core_tipo` FOREIGN KEY (`idgenerico_id`) REFERENCES `core_tipo_generico` (`id`),
  CONSTRAINT `core_stakeholders_modified_by_id_40320095_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_stakeholders`
--

LOCK TABLES `core_stakeholders` WRITE;
/*!40000 ALTER TABLE `core_stakeholders` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_stakeholders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_tipo_generico`
--

DROP TABLE IF EXISTS `core_tipo_generico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_tipo_generico` (
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
  KEY `core_tipo_generico_created_by_id_26045c6b_fk_core_user_id` (`created_by_id`),
  KEY `core_tipo_generico_modified_by_id_16501f73_fk_core_user_id` (`modified_by_id`),
  CONSTRAINT `core_tipo_generico_created_by_id_26045c6b_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_tipo_generico_modified_by_id_16501f73_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_tipo_generico`
--

LOCK TABLES `core_tipo_generico` WRITE;
/*!40000 ALTER TABLE `core_tipo_generico` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_tipo_generico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user`
--

DROP TABLE IF EXISTS `core_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
  `foto` varchar(100) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `bio` longtext DEFAULT NULL,
  `city` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `cia_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `core_user_cia_id_8ae75a28_fk_core_cia_id` (`cia_id`),
  CONSTRAINT `core_user_cia_id_8ae75a28_fk_core_cia_id` FOREIGN KEY (`cia_id`) REFERENCES `core_cia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user`
--

LOCK TABLES `core_user` WRITE;
/*!40000 ALTER TABLE `core_user` DISABLE KEYS */;
INSERT INTO `core_user` VALUES (1,'pbkdf2_sha256$216000$GfvF754as5aj$B2k7sKk9qzfZ0rdg33r5NKELLuCcVrTsgSMSLWy4K4o=','2021-06-20 19:16:49.560556',1,'root','Moisés','Galván Niño','soporte@numentec.net',1,1,'2021-06-20 19:10:46.378083','3-92-952','Margarita','66128172','','','root','es_PA','images/profiles/2012-09-01_12.41.47.jpg','1967-10-18','Main developer senior','Colón','Panamá','2021-06-20 19:10:46.907314',1);
/*!40000 ALTER TABLE `core_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_groups`
--

DROP TABLE IF EXISTS `core_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_groups`
--

LOCK TABLES `core_user_groups` WRITE;
/*!40000 ALTER TABLE `core_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_user_permissions`
--

DROP TABLE IF EXISTS `core_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_user_permissions`
--

LOCK TABLES `core_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `core_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_vistaconfacc`
--

DROP TABLE IF EXISTS `core_vistaconfacc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_vistaconfacc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `acceso` tinyint(1) NOT NULL,
  `group_id` int(11) NOT NULL,
  `vistaconf_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_vistaconfacc_group_id_a4573541_fk_auth_group_id` (`group_id`),
  KEY `core_vistaconfacc_vistaconf_id_8f66add3_fk_core_vistaconfig_id` (`vistaconf_id`),
  CONSTRAINT `core_vistaconfacc_group_id_a4573541_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_vistaconfacc_vistaconf_id_8f66add3_fk_core_vistaconfig_id` FOREIGN KEY (`vistaconf_id`) REFERENCES `core_vistaconfig` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_vistaconfacc`
--

LOCK TABLES `core_vistaconfacc` WRITE;
/*!40000 ALTER TABLE `core_vistaconfacc` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_vistaconfacc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_vistaconfig`
--

DROP TABLE IF EXISTS `core_vistaconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_vistaconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `configkey` varchar(20) NOT NULL,
  `ordinal` int(11) NOT NULL,
  `configval1` varchar(20) NOT NULL,
  `configval2` varchar(20) NOT NULL,
  `configval3` varchar(20) NOT NULL,
  `configval4` varchar(20) NOT NULL,
  `configval5` varchar(20) NOT NULL,
  `configval6` varchar(20) NOT NULL,
  `configval7` varchar(20) NOT NULL,
  `configval8` varchar(20) NOT NULL,
  `configval9` varchar(20) NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `vista_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_vistaconfig_created_by_id_0c7f760f_fk_core_user_id` (`created_by_id`),
  KEY `core_vistaconfig_modified_by_id_cba74a68_fk_core_user_id` (`modified_by_id`),
  KEY `core_vistaconfig_vista_id_ab619a17_fk_core_vistas_id` (`vista_id`),
  CONSTRAINT `core_vistaconfig_created_by_id_0c7f760f_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_vistaconfig_modified_by_id_cba74a68_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_vistaconfig_vista_id_ab619a17_fk_core_vistas_id` FOREIGN KEY (`vista_id`) REFERENCES `core_vistas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_vistaconfig`
--

LOCK TABLES `core_vistaconfig` WRITE;
/*!40000 ALTER TABLE `core_vistaconfig` DISABLE KEYS */;
INSERT INTO `core_vistaconfig` VALUES (1,1,'2021-03-13 02:04:35.326000','2021-03-13 02:14:16.533505','filter01',1,'1','SKU','0','0','0','','','','','filter',1,1,14),(2,1,'2021-03-13 02:05:21.486691','2021-03-13 02:14:26.540104','filter02',2,'1','Descripción','0','0','0','','','','','filter',1,1,14),(3,1,'2021-03-13 02:05:30.863345','2021-04-12 01:42:13.019930','filter03',3,'1','Marca','1','getListMar','','','','','','filter',1,1,14),(4,1,'2021-03-13 02:05:56.952594','2021-04-12 02:26:52.314079','filter04',4,'1','Categoría','1','getListCla1','','','','','','filter',1,1,14),(5,1,'2021-03-13 02:06:08.078888','2021-04-12 02:34:40.070695','filter05',5,'1','Sub Linea','1','getListCla2','','','','','','filter',1,1,14),(6,1,'2021-03-13 02:06:16.817308','2021-04-12 02:35:05.576510','filter06',6,'1','Tipo','1','getListCla3','','','','','','filter',1,1,14),(7,1,'2021-03-13 02:07:01.602097','2021-04-12 02:36:40.250304','filter07',7,'1','CLA1-IPO','1','getListClx1','','','','','','filter',1,1,14),(8,1,'2021-03-13 02:07:12.555030','2021-04-12 02:37:00.567150','filter08',8,'1','CLA2-IPO','1','getListClx2','','','','','','filter',1,1,14),(9,1,'2021-03-13 02:07:23.281977','2021-04-12 02:37:24.297824','filter09',9,'1','CLA3-IPO','1','getListClx3','','','','','','filter',1,1,14),(10,1,'2021-03-13 02:07:56.733198','2021-03-13 02:07:56.733253','filter10',10,'1','N° de Entrada','0','0','0','','','','','filter',1,1,14),(11,1,'2021-03-13 02:09:08.750636','2021-03-13 22:43:02.528855','filter11',11,'1','Incluir Periodo','0','0','0','','','','','filter',1,1,14),(12,1,'2021-03-13 02:09:35.967313','2021-03-13 02:09:35.967368','filter12',12,'1','Inicio','0','0','0','','','','','filter',1,1,14),(13,1,'2021-03-13 02:09:45.068531','2021-03-13 02:09:45.068586','filter13',13,'1','Fin','0','0','0','','','','','filter',1,1,14),(14,1,'2021-03-13 02:12:00.283387','2021-04-02 14:26:31.556843','filter14',14,'1','Opciones','1','','','','','','','filter',1,1,14),(15,1,'2021-03-13 02:12:33.504789','2021-03-21 22:32:14.088216','filter15',15,'0','Reservado','0','0','0','','','','','filter',1,1,14),(16,1,'2021-03-13 03:17:46.375422','2021-03-14 03:37:17.290194','FOTO',16,'1','Foto','1','','','','0','','','col-build',1,1,14),(17,1,'2021-03-13 03:18:42.103856','2021-05-30 18:35:47.839511','SKU',17,'1','SKU','1','','','','0','count','','col',1,1,14),(18,1,'2021-03-13 03:19:16.435378','2021-03-14 03:37:45.189176','DESCRIP',18,'1','Descripción','1','','','','0','','','col',1,1,14),(19,1,'2021-03-13 03:19:49.008196','2021-03-14 03:37:54.724961','UMEDIDA',19,'1','UM','1','','','','1','','','col',1,1,14),(20,1,'2021-03-13 18:49:01.236951','2021-03-14 03:38:05.042101','TALLA',20,'1','Talla','0','','','','0','','','col',1,1,14),(21,1,'2021-03-13 18:50:18.705854','2021-03-14 03:38:15.049616','PRECIO',21,'1','Precio','1','number','currency','right','0','','','col',1,1,14),(22,1,'2021-03-13 18:50:51.956992','2021-05-23 02:52:45.004740','FISICO',22,'1','Físico','0','','','','0','','sortIntFrac','col',1,1,14),(23,1,'2021-03-13 18:51:30.758336','2021-05-23 02:52:34.620594','RESERVA_BODEGA',23,'1','Reserva','0','','','','0','','sortIntFrac','col',1,1,14),(24,1,'2021-03-13 18:51:59.490446','2021-05-23 02:52:24.062631','DISPONIBLE_REAL',24,'1','Disponible','1','','','','0','','sortIntFrac','col',1,1,14),(25,1,'2021-03-13 18:52:19.501403','2021-03-14 03:38:49.961711','BODEGA',25,'1','Bodega','0','','','','1','','','col',1,1,14),(26,1,'2021-03-13 18:54:11.222650','2021-03-14 03:39:03.210710','TRANSITO',26,'1','En Tránsito','0','','','','0','','','col',1,1,14),(27,1,'2021-03-13 18:54:38.728171','2021-04-06 03:08:44.870453','AFUTURO',27,'1','A Futuro','0','','','','0','','','col',1,1,14),(28,1,'2021-03-13 18:54:57.124665','2021-05-22 21:07:04.451589','EMPAQUE',28,'1','Empaque','1','number','','','0','','','col',1,1,14),(29,1,'2021-03-13 18:55:14.297782','2021-04-07 01:40:15.346325','PESO',29,'1','Peso','1','number','','','','','','col',1,1,14),(30,1,'2021-03-13 18:55:53.725536','2021-04-07 01:40:04.439114','CUBICAJE',30,'1','Cubicaje','0','number','','','','','','col',1,1,14),(31,1,'2021-03-13 18:56:15.587380','2021-03-14 03:39:55.525781','MARCA',31,'1','Marca','1','','','','1','','','col',1,1,14),(32,1,'2021-03-13 18:56:33.312759','2021-03-14 03:40:05.925622','COLORES',32,'1','Colores','0','','','','0','','','col',1,1,14),(33,1,'2021-03-13 18:57:09.343633','2021-03-14 03:40:14.577680','NO_ENTRADA',33,'1','Nº Entrada','0','','','','1','','','col',1,1,14),(34,1,'2021-03-13 18:57:36.159633','2021-03-14 03:40:22.339929','DISTRIBUCION',34,'1','Distribución','0','','','','0','','','col',1,1,14),(35,1,'2021-03-13 18:57:52.213917','2021-03-14 03:40:30.225117','BARCODE',35,'1','Barcode','0','','','','0','','','col',1,1,14),(36,1,'2021-03-13 18:58:09.376255','2021-03-14 03:40:40.183686','PAISORIGEN',36,'1','País','0','','','','1','','','col',1,1,14),(37,1,'2021-03-13 18:58:36.923100','2021-03-14 03:40:49.179794','DESCRIP_EN',37,'1','Description','0','','','','0','','','col',1,1,14),(38,1,'2021-03-13 18:58:59.748843','2021-03-14 03:41:03.854268','PRECIOPUBLICO',38,'1','PVP','0','number','currency','right','0','','','col',1,1,14),(39,1,'2021-03-13 18:59:43.739239','2021-03-14 03:41:13.406127','TEXTURA_NOM',39,'1','Textura','0','','','','1','','','col',1,1,14),(40,1,'2021-03-13 19:00:09.818009','2021-05-23 02:52:12.008287','PREVENTA',40,'1','Preventa','0','','','','0','','sortIntFrac','col',1,1,14),(41,1,'2021-03-13 19:00:40.757487','2021-03-14 03:41:33.573593','PROPIEDADES',41,'1','Propiedades','0','','','','0','','','col',1,1,14),(42,1,'2021-03-13 19:00:55.458124','2021-03-14 03:41:42.404629','DEPARTAMENTO',42,'1','Departamento','0','','','','1','','','col',1,1,14),(43,1,'2021-03-13 19:01:29.037702','2021-03-14 03:41:58.702539','SUBCATEGORIA',43,'1','SubCat','1','','','','1','','','col',1,1,14),(44,1,'2021-03-13 19:01:48.833460','2021-03-14 03:36:59.075451','CLASI6_NOM',44,'1','CLASI6','1','','','','1','','','col',1,1,14),(45,1,'2021-03-13 03:18:13.136063','2021-04-27 22:27:28.625245','FECHA_ULT_VENTA',45,'1','FUV','0','date','date','','0','','','col',1,1,14),(46,1,'2021-03-21 16:32:59.228203','2021-04-02 14:55:52.881331','filter11',11,'1','Incluir Periodo','1','','','','','','','filter',1,1,16),(47,1,'2021-03-21 16:34:41.745809','2021-03-21 19:52:35.383115','filter12',12,'1','Inicio','2021-01-01','','','','','','','filter',1,1,16),(48,1,'2021-03-21 16:35:04.897659','2021-03-21 19:52:22.031119','filter13',13,'1','Fin','2021-01-31','','','','','','','filter',1,1,16),(49,1,'2021-03-21 16:35:54.508712','2021-03-21 19:52:02.044225','filter01',1,'1','Nº Documentos','','','','','','','','filter',1,1,16),(50,1,'2021-03-21 16:37:32.426973','2021-03-21 19:50:08.556747','filter15',15,'1','Tipo de Documento','COT','','','','','','','filter',1,1,16),(51,1,'2021-03-21 16:38:01.063158','2021-04-12 22:06:36.112779','filter02',2,'1','Cliente','1','getListCli','','','','','','filter',1,1,16),(52,1,'2021-03-21 16:38:31.938461','2021-04-12 22:07:10.642636','filter03',3,'1','Vendedor','1','getListVen','','','','','','filter',1,1,16),(53,1,'2021-03-21 17:02:00.647881','2021-04-20 01:38:34.588190','NUMDOC',16,'1','Nº Doc','1','number','','','0','count','','col',1,1,16),(54,1,'2021-03-21 17:02:21.646145','2021-03-21 17:26:47.062890','TIPODOC',17,'1','Tipo Doc','1','','','','0','','','col',1,1,16),(55,1,'2021-03-21 17:02:58.030852','2021-04-06 02:56:01.795641','FECHADOC',18,'1','Fecha','1','date','date','','1','','','col',1,1,16),(56,1,'2021-03-21 17:03:16.540192','2021-03-22 02:43:55.724510','NOMCLI',19,'1','Cliente','1','','','','1','','','col',1,1,16),(57,1,'2021-03-21 17:03:34.723316','2021-04-20 01:38:58.491762','MONTO',20,'1','Monto','1','number','currency','right','0','sum','','col',1,1,16),(58,1,'2021-03-21 17:03:51.469672','2021-03-21 17:25:33.584030','ESTADO',21,'1','Estado','1','','','','1','','','col',1,1,16),(59,1,'2021-03-21 17:04:32.691049','2021-04-13 14:04:42.375733','VENDEDOR',22,'1','Vendedor','0','','','','1','','','col',1,1,16),(60,1,'2021-03-21 21:52:40.826642','2021-03-21 21:52:40.826712','filter04',4,'0','Reservado','','','','','','','','filter',1,1,16),(61,1,'2021-03-21 21:52:53.098156','2021-03-21 21:52:53.098240','filter05',5,'0','Reservado','','','','','','','','filter',1,1,16),(62,1,'2021-03-21 21:53:01.011933','2021-03-21 21:53:01.011993','filter06',6,'0','Reservado','','','','','','','','filter',1,1,16),(63,1,'2021-03-21 21:53:09.772528','2021-03-21 21:53:09.772611','filter07',7,'0','Reservado','','','','','','','','filter',1,1,16),(64,1,'2021-03-21 21:53:18.894990','2021-04-13 14:05:35.720102','OBSERVACION',23,'1','Observación','0','','','','0','','','col',1,1,16),(65,1,'2021-03-23 02:12:22.451299','2021-03-23 02:12:22.451356','filter01',1,'1','Nº Documentos','0','','','','','','','filter',1,1,17),(66,1,'2021-03-23 02:16:13.335888','2021-03-23 02:19:03.498370','filter02',2,'1','SKUs','','','','','','','','filter',1,1,17),(67,1,'2021-03-23 02:16:42.633778','2021-03-23 02:19:19.629276','filter03',3,'1','Marca','','','','','','','','filter',1,1,17),(68,1,'2021-03-23 02:18:14.814089','2021-03-23 02:20:08.925888','filter04',4,'0','Categoría','','','','','','','','filter',1,1,17),(69,1,'2021-03-23 02:21:46.749662','2021-03-23 02:21:46.749721','filter11',11,'1','Incluir Periodo','0','','','','','','','filter',1,1,17),(70,1,'2021-03-23 02:22:35.395340','2021-03-23 02:22:35.395398','filter12',12,'1','Inicio','2021-01-01','date','','','','','','filter',1,1,17),(71,1,'2021-03-23 02:22:51.042928','2021-03-23 02:22:51.042995','filter13',13,'1','Fin','2021-01-31','date','','','','','','filter',1,1,17),(72,1,'2021-03-23 03:42:52.313545','2021-03-23 03:42:52.313882','ID',16,'1','ID','0','number','','','0','','','col',1,1,17),(73,1,'2021-03-23 03:44:06.880999','2021-04-20 02:59:09.037093','NUMDOC',17,'1','Nº Doc','1','number','','','0','count','','col',1,1,17),(74,1,'2021-03-23 03:44:51.009148','2021-03-23 03:44:51.009232','TIPODOC',18,'1','Tipo Doc','0','','','','1','','','col',1,1,17),(75,1,'2021-03-23 03:47:12.872266','2021-04-20 03:08:22.889527','SKU',19,'1','SKU','1','','','','1','','','col',1,1,17),(76,1,'2021-03-23 03:50:10.476473','2021-03-23 03:50:10.476529','DESCRIP',20,'1','Descripción','1','','','','0','','','col',1,1,17),(77,1,'2021-03-23 03:50:42.916982','2021-03-23 03:50:42.917074','UMEDIDA',21,'1','UM','1','','','','0','','','col',1,1,17),(78,1,'2021-03-23 03:51:13.652092','2021-03-23 03:51:13.652151','CANTIDAD',22,'1','Cantidad','1','','','','0','','','col',1,1,17),(79,1,'2021-03-23 03:51:46.528169','2021-03-23 03:51:46.528259','NO_LINEA',23,'1','Nº Linea','0','','','','0','','','col',1,1,17),(80,1,'2021-03-23 03:52:46.093588','2021-04-20 02:59:35.129999','BULTOS',24,'1','Bultos','0','','','','0','sum','','col',1,1,17),(81,1,'2021-03-23 03:53:16.067008','2021-04-20 03:00:10.288414','PESO_BULTOS',25,'1','Peso Bultos','0','','','','0','sum','','col',1,1,17),(82,1,'2021-03-23 03:53:38.442867','2021-04-20 03:00:26.191527','EMPAQUE',26,'1','Empaque','0','','','','0','sum','','col',1,1,17),(83,1,'2021-03-23 03:54:07.571782','2021-03-23 03:54:07.571854','PESO_LINEA',27,'0','Peso Linea','0','','','','0','','','col',1,1,17),(84,1,'2021-03-23 03:54:30.474608','2021-03-23 03:54:30.474667','CUBICAJE_LINEA',28,'0','Cubicaje Linea','0','','','','0','','','col',1,1,17),(85,1,'2021-03-23 03:54:49.898670','2021-04-20 03:02:33.643335','PESO',29,'1','Peso','0','','','','0','','','col',1,1,17),(86,1,'2021-03-23 03:55:06.503986','2021-03-23 03:55:06.504065','CUBICAJE',30,'1','Cubicaje','0','','','','0','','','col',1,1,17),(87,1,'2021-03-23 03:55:27.828027','2021-03-23 03:55:27.828084','MARCA',31,'1','Marca','0','','','','1','','','col',1,1,17),(88,1,'2021-03-23 03:55:43.873714','2021-03-23 03:55:43.873772','TALLA',32,'1','Talla','0','','','','1','','','col',1,1,17),(89,1,'2021-03-23 03:56:59.379842','2021-03-23 03:56:59.379965','SALIDA',34,'0','Salida','0','','','','0','','','col',1,1,17),(90,1,'2021-03-23 03:57:26.205154','2021-03-23 03:57:26.205212','CLA1',35,'1','CLA1','0','','','','1','','','col',1,1,17),(91,1,'2021-03-23 03:57:50.708829','2021-03-23 03:57:50.708886','DISTRIBUCION',36,'1','Distribución','0','','','','0','','','col',1,1,17),(92,1,'2021-03-23 03:58:08.828041','2021-03-23 03:58:08.828099','COLORES',37,'1','Colores','0','','','','0','','','col',1,1,17),(93,1,'2021-03-23 03:58:28.703927','2021-03-23 03:58:28.703999','BARCODE',38,'1','Barcode','0','','','','0','','','col',1,1,17),(94,1,'2021-03-23 03:58:53.129775','2021-03-23 03:58:53.129895','PAISORIGEN',39,'1','País','0','','','','1','','','col',1,1,17),(95,1,'2021-03-23 03:59:16.882014','2021-03-23 04:05:15.566349','PRECIO',40,'1','Precio','1','number','currency','','0','','','col',1,1,17),(96,1,'2021-03-23 03:59:39.707652','2021-03-23 04:03:56.742322','PRECIOPUBLICO',41,'1','PVA','0','number','currency','','0','','','col',1,1,17),(97,1,'2021-03-23 03:59:54.727670','2021-03-23 03:59:54.727751','OBSERVACION',42,'1','Observación','0','','','','0','','','col',1,1,17),(98,1,'2021-03-23 04:00:20.651618','2021-04-20 03:03:47.892382','DESCUENTO',43,'1','Descuento','0','number','currency','','0','sum','','col',1,1,17),(99,1,'2021-03-23 04:01:00.729972','2021-04-20 03:03:59.909571','TOTAL',44,'1','Total','0','number','currency','','0','sum','','col',1,1,17),(100,1,'2021-03-23 04:01:38.297187','2021-03-23 21:03:01.392692','TEXTURA_NOM',33,'1','Textura','0','','','','0','','','col',1,1,17),(101,1,'2021-03-23 21:02:40.855803','2021-03-23 21:03:50.947131','filter15',15,'1','Tipo de Documento','','','','','','','','filter',1,1,17),(102,1,'2021-03-29 02:42:47.362790','2021-03-29 02:44:18.258758','filter01',1,'1','SKUs','','','','','','','','filter',1,1,18),(103,1,'2021-03-29 02:45:20.496690','2021-04-19 04:00:37.785815','filter02',2,'1','Marca','1','getListMar','','','','','','filter',1,1,18),(104,1,'2021-03-29 02:45:39.120975','2021-04-19 04:01:06.167300','filter03',3,'1','Categoría','1','getListCla1','','','','','','filter',1,1,18),(105,1,'2021-03-30 00:56:03.891032','2021-03-30 00:56:03.891129','ID',16,'1','ID','0','number','','','0','','','col',1,1,18),(106,1,'2021-03-30 00:56:59.882900','2021-05-09 20:21:45.061586','NUMDOC',17,'1','Nº Doc','0','number','','','1','','','col',1,1,18),(107,1,'2021-03-30 00:57:38.112169','2021-03-30 00:57:38.112230','TIPODOC',18,'1','Tipo Doc','0','','','','0','','','col',1,1,18),(108,1,'2021-03-30 00:58:27.236565','2021-03-30 15:34:34.837293','FECHADOC',19,'1','Fecha','0','date','','','1','','','col',1,1,18),(109,1,'2021-03-30 00:58:58.907733','2021-05-09 20:21:58.826358','SKU',20,'1','SKU','1','','','','1','count','','col',1,1,18),(110,1,'2021-03-30 00:59:22.018875','2021-03-30 00:59:22.018950','BARCODE',21,'1','Barcode','0','','','','0','','','col',1,1,18),(111,1,'2021-03-30 00:59:50.419860','2021-03-30 00:59:50.419929','DESCRIP',22,'1','Descripción','1','','','','0','','','col',1,1,18),(112,1,'2021-03-30 01:00:22.404836','2021-03-30 01:00:22.404894','DESCRIPTION',23,'1','Description','0','','','','0','','','col',1,1,18),(113,1,'2021-03-30 01:00:41.110569','2021-03-30 01:00:41.110779','UM',24,'1','UM','0','','','','0','','','col',1,1,18),(114,1,'2021-03-30 01:01:01.391340','2021-03-30 01:01:01.391433','CANTIDAD',25,'1','Cantidad','0','','','','0','','','col',1,1,18),(115,1,'2021-03-30 01:02:14.791370','2021-04-20 03:23:00.948561','QTY_INT',26,'1','Entero','1','number','','','0','sum','','col',1,1,18),(116,1,'2021-03-30 01:02:42.421062','2021-04-20 03:23:14.910606','QTY_FRAC',27,'1','Fracción','1','number','','','0','sum','','col',1,1,18),(117,1,'2021-03-30 01:03:14.300837','2021-03-30 01:03:14.300899','PRECIO',28,'1','Precio','1','number','currency','','0','','','col',1,1,18),(118,1,'2021-03-30 01:03:40.293846','2021-04-20 03:23:29.886383','COSTO',29,'1','Costo','0','number','currency','','0','sum','','col',1,1,18),(119,1,'2021-03-30 01:05:32.262394','2021-03-30 01:07:04.718682','PVP',30,'1','PVP','0','number','currency','','0','','','col',1,1,18),(120,1,'2021-03-30 01:08:06.260840','2021-04-20 03:23:48.612997','TOTAL',31,'1','Total','1','number','currency','','0','sum','','col',1,1,18),(121,1,'2021-03-30 01:08:36.243887','2021-03-30 01:08:36.243963','MARCA',32,'1','Marca','0','','','','1','','','col',1,1,18),(122,1,'2021-03-30 01:09:23.789335','2021-03-30 01:09:23.789405','PAISORIGEN',33,'1','País','0','','','','1','','','col',1,1,18),(123,1,'2021-03-30 01:09:50.036099','2021-03-30 01:09:50.036168','TEXTURA',34,'1','Textura','0','','','','0','','','col',1,1,18),(124,1,'2021-03-30 01:10:45.587839','2021-03-30 01:10:45.587898','NO_LINEA',35,'1','Nº Linea','0','','','','0','','','col',1,1,18),(125,1,'2021-03-30 01:11:03.013965','2021-03-30 01:11:03.014068','BULTOS',36,'1','Bultos','0','','','','0','','','col',1,1,18),(126,1,'2021-03-30 01:11:24.124478','2021-03-30 01:11:24.124558','PESO_BULTOS',37,'1','Peso Bultos','0','','','','0','','','col',1,1,18),(127,1,'2021-03-30 01:11:40.057658','2021-03-30 01:11:40.057738','EMPAQUE',38,'1','Empaque','0','','','','0','','','col',1,1,18),(128,1,'2021-03-30 01:11:58.626713','2021-03-30 01:11:58.626802','PESO_LINEA',39,'1','Peso Linea','0','','','','0','','','col',1,1,18),(129,1,'2021-03-30 01:12:24.057876','2021-03-30 01:12:24.058016','CUBICAJE',40,'1','Cubicaje','0','number','','','0','','','col',1,1,18),(130,1,'2021-03-30 01:12:47.924262','2021-03-30 01:12:47.924323','DISTRIBUCION',41,'1','Distribución','0','','','','0','','','col',1,1,18),(131,1,'2021-03-30 01:13:04.841980','2021-03-30 01:13:04.842093','TALLA',42,'1','Talla','0','','','','0','','','col',1,1,18),(132,1,'2021-03-30 01:13:22.454145','2021-03-30 01:13:22.454204','COLORES',43,'1','Colores','0','','','','0','','','col',1,1,18),(133,1,'2021-03-30 01:14:08.020027','2021-03-30 01:14:08.020108','CLA1',44,'1','Categoría','0','','','','1','','','col',1,1,18),(134,1,'2021-03-30 01:14:32.753832','2021-03-30 01:14:32.753890','CLA2',45,'0','SubCat1','0','','','','1','','','col',1,1,18),(135,1,'2021-03-30 01:14:43.776597','2021-03-30 01:14:43.776685','CLA3',46,'0','SubCat2','0','','','','1','','','col',1,1,18),(136,1,'2021-03-30 01:15:25.232438','2021-03-30 01:15:25.232496','ESTADO',47,'1','Estado','0','','','','1','','','col',1,1,18),(137,1,'2021-03-30 01:16:23.678807','2021-03-30 15:34:47.341277','RECEPCION',48,'1','Recepción','0','date','','','1','','','col',1,1,18),(138,1,'2021-03-30 01:16:48.732832','2021-03-30 01:16:48.732892','CLIENTE',49,'1','Cliente','0','','','','1','','','col',1,1,18),(139,1,'2021-03-30 01:17:33.238964','2021-03-30 01:17:33.239087','OBSERVACION',50,'1','Observación','0','','','','0','','','col',1,1,18),(140,1,'2021-03-30 14:16:19.002637','2021-03-30 14:17:14.472487','filter11',11,'1','Incluir Periodo','1','','','','','','','filter',1,1,18),(141,1,'2021-03-30 14:16:44.718426','2021-03-30 15:52:46.607124','filter12',12,'1','Inicio','2021-01-01','','','','','','','filter',1,1,18),(142,1,'2021-03-30 14:16:58.600956','2021-03-30 15:52:55.133845','filter13',13,'1','Fin','2021-01-31','','','','','','','filter',1,1,18),(143,1,'2021-03-30 14:31:12.823741','2021-03-30 15:52:06.603625','filter15',15,'1','Tipo de Documento','FAC','','','','','','','filter',1,1,18);
/*!40000 ALTER TABLE `core_vistaconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_vistaconfiguser`
--

DROP TABLE IF EXISTS `core_vistaconfiguser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_vistaconfiguser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `configkey` varchar(20) NOT NULL,
  `configval1` varchar(20) NOT NULL,
  `configval2` varchar(20) NOT NULL,
  `configval3` varchar(20) NOT NULL,
  `configval4` varchar(20) NOT NULL,
  `configval5` varchar(20) NOT NULL,
  `configval6` varchar(20) NOT NULL,
  `configval7` varchar(20) NOT NULL,
  `configval8` varchar(20) NOT NULL,
  `configval9` varchar(20) NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `vista_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_vistaconfiguser_created_by_id_52b0c1b8_fk_core_user_id` (`created_by_id`),
  KEY `core_vistaconfiguser_modified_by_id_ba430ffd_fk_core_user_id` (`modified_by_id`),
  KEY `core_vistaconfiguser_user_id_3b52977a_fk_core_user_id` (`user_id`),
  KEY `core_vistaconfiguser_vista_id_ba0c2848_fk_core_vistas_id` (`vista_id`),
  CONSTRAINT `core_vistaconfiguser_created_by_id_52b0c1b8_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_vistaconfiguser_modified_by_id_ba430ffd_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_vistaconfiguser_user_id_3b52977a_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_vistaconfiguser_vista_id_ba0c2848_fk_core_vistas_id` FOREIGN KEY (`vista_id`) REFERENCES `core_vistas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_vistaconfiguser`
--

LOCK TABLES `core_vistaconfiguser` WRITE;
/*!40000 ALTER TABLE `core_vistaconfiguser` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_vistaconfiguser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_vistas`
--

DROP TABLE IF EXISTS `core_vistas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_vistas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `nombre` varchar(25) NOT NULL,
  `descrip` varchar(50) NOT NULL,
  `link` varchar(100) NOT NULL,
  `tipo` int(10) unsigned NOT NULL CHECK (`tipo` >= 0),
  `checkelperms` tinyint(1) NOT NULL,
  `disponible` tinyint(1) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `modulo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `core_vistas_created_by_id_42b90746_fk_core_user_id` (`created_by_id`),
  KEY `core_vistas_modified_by_id_77fdc58f_fk_core_user_id` (`modified_by_id`),
  KEY `core_vistas_modulo_id_c84dccb7_fk_core_modulos_id` (`modulo_id`),
  CONSTRAINT `core_vistas_created_by_id_42b90746_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_vistas_modified_by_id_77fdc58f_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_vistas_modulo_id_c84dccb7_fk_core_modulos_id` FOREIGN KEY (`modulo_id`) REFERENCES `core_modulos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_vistas`
--

LOCK TABLES `core_vistas` WRITE;
/*!40000 ALTER TABLE `core_vistas` DISABLE KEYS */;
INSERT INTO `core_vistas` VALUES (1,1,'2021-06-17 01:50:15.761387','2021-06-17 01:50:15.761488','LinaAuthToken','Autenticación por Token','login/',1,1,1,1,1,1),(2,1,'2021-06-17 01:51:13.415624','2021-06-17 01:51:13.415682','CiaViewSet','CRUD de compañías','cias/',1,1,1,1,1,1),(3,1,'2021-06-17 01:53:05.045113','2021-06-17 01:53:05.045256','StakeHolderViewSet','CRUD de stakeholders','stakeholders/',1,1,1,1,1,1),(4,1,'2021-06-17 02:09:57.501125','2021-06-17 02:09:57.501204','UserList','Listado de usuarios','users/<username>/',1,1,1,1,1,1),(5,1,'2021-06-17 02:10:23.988022','2021-06-17 02:10:23.988079','UserDetail','Detalle de un usuario','users/<pk>/',1,1,1,1,1,1),(6,1,'2021-06-17 02:10:51.306131','2021-06-17 02:10:51.306205','UserPermsDetail','Detalle de un usuario con sus permisos','user_perms/<pk>/',1,1,1,1,1,1),(7,1,'2021-06-17 02:11:19.024115','2021-06-17 02:11:19.024218','UserRegister','Registro básico de usuario','user_register/',1,1,1,1,1,1),(8,1,'2021-06-17 02:11:48.426310','2021-06-17 02:11:48.426369','GroupsList','Listado de grupos de usuarios','groups/',1,1,1,1,1,1),(9,1,'2021-06-17 02:12:09.473533','2021-06-17 02:12:09.473610','ModuloViewSet','CRUD de Módulos del sistema','modulos/',1,1,1,1,1,1),(10,1,'2021-06-17 02:12:33.669348','2021-06-17 02:12:33.669415','VistaViewSet','CRUD de Vistas por cada módulo del sistema','vistas/',1,1,1,1,1,1),(11,1,'2021-06-17 02:12:55.322573','2021-06-17 02:12:55.322650','VistaConfigViewSet','CRUD de configuración por cada vista','vistas-conf/',1,1,1,1,1,1),(12,1,'2021-06-17 02:13:23.462560','2021-06-17 02:13:23.462617','VistaConfigUserViewSet','CRUD de configuración por cada vista por usuario','vistas-conf-usr/',1,1,1,1,1,1),(13,1,'2021-06-17 02:13:57.262337','2021-06-17 02:13:57.262395','CatalogModelViewSet','Catálogo basado en modelo','model-catalog/',1,1,1,1,1,3),(14,1,'2021-06-17 02:14:19.833766','2021-06-20 15:53:40.000416','CatalogAPIView','Catálogo basado en APIView','catalog/',1,0,1,1,1,3),(15,1,'2021-06-17 02:14:46.491537','2021-06-17 02:14:46.491631','FavoritoModelViewset','CRUD de favoritos','favoritos/',1,1,1,1,1,3),(16,1,'2021-06-17 02:15:08.182205','2021-06-19 22:07:41.156709','SaleDocsMAPIView','Maestro de documentos de ventas','saledocsm/',1,1,1,1,1,3),(17,1,'2021-06-17 02:15:31.273487','2021-06-17 02:15:31.273615','SaleDocsDAPIView','Detalle de documentos de ventas','saledocsd/',1,1,1,1,1,3),(18,1,'2021-06-17 02:16:17.761009','2021-06-17 02:16:17.761091','SalesDetailAPIView','Detalle de ventas','salesdetail/',1,1,1,1,1,3);
/*!40000 ALTER TABLE `core_vistas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-06-20 19:20:21.426975','1','gerencia',1,'[{\"added\": {}}]',2,1),(2,'2021-06-20 19:21:33.511251','2','contabilidad',1,'[{\"added\": {}}]',2,1),(3,'2021-06-20 19:24:19.168548','3','ventadmin',1,'[{\"added\": {}}]',2,1),(4,'2021-06-20 19:26:31.376771','4','ventas',1,'[{\"added\": {}}]',2,1),(5,'2021-06-20 19:28:10.461060','5','trafico',1,'[{\"added\": {}}]',2,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (18,'admin','logentry'),(2,'auth','group'),(1,'auth','permission'),(20,'authtoken','token'),(21,'authtoken','tokenproxy'),(3,'contenttypes','contenttype'),(13,'core','cia'),(5,'core','gensequence'),(6,'core','modulo'),(12,'core','stakeholder'),(11,'core','tipogenerico'),(4,'core','user'),(7,'core','vista'),(8,'core','vistaconfig'),(10,'core','vistaconfigacc'),(9,'core','vistaconfiguser'),(14,'linabi','bicatalog'),(17,'linabi','bifavorito'),(15,'linabi','bixlsxtemplate'),(16,'linabi','bixlsxtemplatecol'),(19,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-06-20 19:09:29.421587'),(2,'contenttypes','0002_remove_content_type_name','2021-06-20 19:09:29.499273'),(3,'auth','0001_initial','2021-06-20 19:09:29.629463'),(4,'auth','0002_alter_permission_name_max_length','2021-06-20 19:09:29.836320'),(5,'auth','0003_alter_user_email_max_length','2021-06-20 19:09:29.857698'),(6,'auth','0004_alter_user_username_opts','2021-06-20 19:09:29.893403'),(7,'auth','0005_alter_user_last_login_null','2021-06-20 19:09:29.928750'),(8,'auth','0006_require_contenttypes_0002','2021-06-20 19:09:29.934141'),(9,'auth','0007_alter_validators_add_error_messages','2021-06-20 19:09:29.991908'),(10,'auth','0008_alter_user_username_max_length','2021-06-20 19:09:30.018636'),(11,'auth','0009_alter_user_last_name_max_length','2021-06-20 19:09:30.047575'),(12,'auth','0010_alter_group_name_max_length','2021-06-20 19:09:30.160304'),(13,'auth','0011_update_proxy_permissions','2021-06-20 19:09:30.252803'),(14,'auth','0012_alter_user_first_name_max_length','2021-06-20 19:09:30.292778'),(15,'core','0001_initial','2021-06-20 19:09:30.976277'),(16,'linabi','0001_initial','2021-06-20 19:09:40.495035'),(17,'admin','0001_initial','2021-06-20 19:09:56.393572'),(18,'admin','0002_logentry_remove_auto_add','2021-06-20 19:09:56.556678'),(19,'admin','0003_logentry_add_action_flag_choices','2021-06-20 19:09:56.660376'),(20,'authtoken','0001_initial','2021-06-20 19:09:56.788416'),(21,'authtoken','0002_auto_20160226_1747','2021-06-20 19:09:57.128783'),(22,'authtoken','0003_tokenproxy','2021-06-20 19:09:57.137465'),(23,'sessions','0001_initial','2021-06-20 19:09:57.208403');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `linabi_favorito`
--

DROP TABLE IF EXISTS `linabi_favorito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linabi_favorito` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `name` varchar(25) NOT NULL,
  `link` varchar(200) NOT NULL,
  `descrip` longtext NOT NULL,
  `todos` tinyint(1) NOT NULL,
  `vuextore` varchar(50) NOT NULL,
  `image` varchar(100) NOT NULL,
  `perm` varchar(50) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `link` (`link`),
  KEY `linabi_favorito_created_by_id_16725e8c_fk_core_user_id` (`created_by_id`),
  KEY `linabi_favorito_modified_by_id_8c9a453c_fk_core_user_id` (`modified_by_id`),
  CONSTRAINT `linabi_favorito_created_by_id_16725e8c_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `linabi_favorito_modified_by_id_8c9a453c_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `linabi_favorito`
--

LOCK TABLES `linabi_favorito` WRITE;
/*!40000 ALTER TABLE `linabi_favorito` DISABLE KEYS */;
INSERT INTO `linabi_favorito` VALUES (1,1,'2021-02-20 20:13:02.914132','2021-06-19 20:17:10.672632','Catálogo','/linabi/catalogo','Lista de productos. Confección de catálogos. Exportación a PDF, csv y Excel',1,'linabi/catalogo','images/bifavoritos/prev3.gif','core.acc_linabi_catalog',1,1),(2,1,'2021-02-21 04:47:06.823709','2021-06-19 20:16:45.365918','Documentos de Venta','/linabi/saledocs','Listado de documentos de venta: Cotizaciones, pedidos, pedidos confirmados y facturas.\r\nSoporta filtrar por cliente y exportación a Excel, csv y PDF.',1,'linabi/saledocsm','images/bifavoritos/prev1.jpg','core.acc_linabi_saledocs_master',1,1),(3,1,'2021-02-22 04:07:34.099767','2021-06-19 20:16:56.440494','Detalle de Ventas','/linabi/salesdetail','Análisis de el detalle de ventas: Cotizaciones, pedidos, pedidos confirmados y facturas.\r\nBrinda consulta de ventas por producto, por marca o categoría dentro de un periodo. Con exportación Excel, csv y PDF.',1,'linabi/salesdetail','images/bifavoritos/prev2.png','core.acc_linabi_sales_detail',1,1),(4,1,'2021-03-24 01:03:28.516783','2021-06-19 20:17:03.482363','Procesar Marcaciones','/linabi/reportes','Asistente para procesar marcaciones de asistencia de los colaboradores. Actualiza las entradas desde el reloj. Hace el analisis para depurar y resumir las marcaciones. Aplica excepciones así como horas extra, ausencias o tardanzas. Exporta a csv compatible con planilla de DMC. Se puede exportar a Excel.',0,'linabi/marcaciones','images/bifavoritos/rpt01.jpeg','core.acc_linabi_reports',1,1);
/*!40000 ALTER TABLE `linabi_favorito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `linabi_xlsxtemplate`
--

DROP TABLE IF EXISTS `linabi_xlsxtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linabi_xlsxtemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `name` varchar(10) NOT NULL,
  `descrip` longtext NOT NULL,
  `row` int(11) NOT NULL,
  `col` int(11) NOT NULL,
  `archivo` varchar(100) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `linabi_xlsxtemplate_created_by_id_bb641fe4_fk_core_user_id` (`created_by_id`),
  KEY `linabi_xlsxtemplate_modified_by_id_c5782395_fk_core_user_id` (`modified_by_id`),
  CONSTRAINT `linabi_xlsxtemplate_created_by_id_bb641fe4_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `linabi_xlsxtemplate_modified_by_id_c5782395_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `linabi_xlsxtemplate`
--

LOCK TABLES `linabi_xlsxtemplate` WRITE;
/*!40000 ALTER TABLE `linabi_xlsxtemplate` DISABLE KEYS */;
INSERT INTO `linabi_xlsxtemplate` VALUES (1,1,'2021-05-29 20:27:24.889861','2021-05-29 20:27:24.889925','Tova','Grupo TOVA. Hoja de pedido para proveedor',12,2,'xlsxtemplates/tova.xlsx',1,1);
/*!40000 ALTER TABLE `linabi_xlsxtemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `linabi_xlsxtemplatecol`
--

DROP TABLE IF EXISTS `linabi_xlsxtemplatecol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linabi_xlsxtemplatecol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `name` varchar(20) NOT NULL,
  `descrip` longtext NOT NULL,
  `ordinal` int(11) NOT NULL,
  `posicion` int(11) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `plantilla_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `linabi_xlsxtemplatecol_created_by_id_1c00f03d_fk_core_user_id` (`created_by_id`),
  KEY `linabi_xlsxtemplatecol_modified_by_id_e50c2bd9_fk_core_user_id` (`modified_by_id`),
  KEY `linabi_xlsxtemplatec_plantilla_id_3c8d06d9_fk_linabi_xl` (`plantilla_id`),
  CONSTRAINT `linabi_xlsxtemplatec_plantilla_id_3c8d06d9_fk_linabi_xl` FOREIGN KEY (`plantilla_id`) REFERENCES `linabi_xlsxtemplate` (`id`),
  CONSTRAINT `linabi_xlsxtemplatecol_created_by_id_1c00f03d_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `linabi_xlsxtemplatecol_modified_by_id_e50c2bd9_fk_core_user_id` FOREIGN KEY (`modified_by_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `linabi_xlsxtemplatecol`
--

LOCK TABLES `linabi_xlsxtemplatecol` WRITE;
/*!40000 ALTER TABLE `linabi_xlsxtemplatecol` DISABLE KEYS */;
INSERT INTO `linabi_xlsxtemplatecol` VALUES (1,1,'2021-05-30 02:04:00.562416','2021-05-30 02:04:00.562476','MARCA','',0,1,1,1,1),(2,1,'2021-05-30 02:04:12.134037','2021-05-30 02:04:12.134092','SKU','',1,2,1,1,1),(3,1,'2021-05-30 02:04:25.821940','2021-05-30 02:04:25.822096','BARCODE','',2,3,1,1,1),(4,1,'2021-05-30 02:04:37.712649','2021-05-30 02:04:37.712704','COLORES','',3,4,1,1,1),(5,1,'2021-05-30 02:04:48.725350','2021-05-30 02:04:48.725443','TALLA','',4,5,1,1,1),(6,1,'2021-05-30 02:05:03.907070','2021-05-30 18:41:56.592994','TEXTURA_NOM','',5,6,1,1,1),(7,1,'2021-05-30 02:05:17.804257','2021-05-30 02:05:17.804316','DESCRIP','',6,7,1,1,1),(8,1,'2021-05-30 02:05:42.829713','2021-05-30 18:39:55.276669','UMEDIDA','',7,8,1,1,1),(9,1,'2021-05-30 02:05:55.740579','2021-05-30 02:05:55.740652','PRECIO','',8,9,1,1,1),(10,1,'2021-05-30 02:06:30.758851','2021-05-31 01:45:10.057384','EMPAQUE','',9,10,1,1,1),(11,1,'2021-05-30 02:06:56.422139','2021-05-31 01:44:56.470085','BULTOS','',10,11,1,1,1);
/*!40000 ALTER TABLE `linabi_xlsxtemplatecol` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-20 16:07:37
