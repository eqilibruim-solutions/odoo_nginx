-- Create table

DROP TABLE IF EXISTS productos_wms;
CREATE TABLE IF NOT EXISTS productos_wms
(
    id integer,
    referencia character varying(150),
    barcode character varying(250),
    name character varying(250),
    category character varying(150),
    price character varying(100),
    cost character varying(100),
    unidad character varying(150),
    peso character varying(50),
    volumen character varying(50),
    iva character varying(50),
    lote character varying(50) 
);

DROP TABLE IF EXISTS categorias_wms;
CREATE TABLE IF NOT EXISTS categorias_wms
(
    id integer,
    name_category character varying(150)
);

DROP TABLE IF EXISTS clientes_wms;
CREATE TABLE IF NOT EXISTS clientes_wms
(
    id integer,
    vat character varying(150) NOT NULL,
    l10n_latam_identification_type_id character varying(100),
    customer_rank character varying(20),
    name character varying(255),
    email character varying(255),
    phone character varying(100),
    mobile character varying(50),
    street character varying(250),
    zip character varying(50),
    city character varying(150),
    state_id character varying(255),
    country_id character varying(50)
);

DROP TABLE IF EXISTS unidad_medida;
CREATE TABLE IF NOT EXISTS unidad_medida
(
    id integer NOT NULL,
    name character varying(150),
    CONSTRAINT unidad_medida_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS t_iva;
CREATE TABLE IF NOT EXISTS t_iva
(
    id integer NOT NULL,
    iva character varying(50),
    CONSTRAINT t_iva_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS proveedores_wms;
CREATE TABLE IF NOT EXISTS proveedores_wms
(
    id integer NOT NULL,
    vat integer NOT NULL,
    l10n_latam_identification_type_id character varying(100),
    customer_rank character varying(20),
    name character varying(255),
    email character varying(255),
    phone character varying(100),
    mobile character varying(50),
    street character varying(250),
    zip character varying(50),
    city character varying(150),
    state_id character varying(50),
    country_id character varying(50)
);


-- Base de datos Integraciones global --
-- CREATE DATABASE db_maestra_integradora
-- Tablas de integracion

CREATE TABLE IF NOT EXISTS tipos_conexion(
    id SERIAL PRIMARY KEY,
    nombre_tipo character varying(150)
);

CREATE TABLE IF NOT EXISTS maestra_integradora(
    id SERIAL PRIMARY KEY,
    nombre_compania character varying(150),
    wms_bd_principal character varying(150),
    wms_bd_integracion character varying(150),
    wms_username_api character varying(150),
    wms_token_api character varying(150),
    wms_endpoint_db character varying(150),
    ruta_archivos character varying(150),
    api_endpoint character varying(150),
    api_username character varying(150),
    api_token character varying(150),
    wms_tipo_integracion integer references tipos_conexion(id)
);
