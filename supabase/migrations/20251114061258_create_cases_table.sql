/*
  # Create Project Canary Cases Database (BigQuery Version)

  ## Overview
  This migration creates the core database structure for the Project Canary dashboard in Google BigQuery.

  ## New Tables
  
  ### `cases`
  Main table storing all customer support cases with the following columns:
  - `id` (STRING, primary key) - Unique identifier for each case
  - `case_id` (STRING, unique) - Human-readable case ID (e.g., "CASE-00001")
  - `customer_name` (STRING) - Name of the customer who submitted the case
  - `description` (STRING) - Detailed description of the issue
  - `priority` (STRING) - Priority level: Low, Medium, High, Critical
  - `type` (STRING) - Case type: Inquiry, Incident, Jira, Bug, Feature Request
  - `product` (STRING) - Product name related to the case
  - `status` (STRING) - Current status: Open, In Progress, Resolved, Closed
  - `module` (STRING) - Primary module classification
  - `sub_module` (STRING) - Sub-module classification
  - `category` (STRING) - Category classification
  - `created_date` (TIMESTAMP) - Timestamp when case was created
  - `updated_date` (TIMESTAMP) - Timestamp when case was last updated
  - `geography` (STRING) - Geographic region of the customer

  ### `case_similarity`
  Table for storing pre-computed case similarity relationships:
  - `id` (STRING, primary key) - Unique identifier
  - `case_id` (STRING, foreign key) - Reference to the main case
  - `related_case_id` (STRING, foreign key) - Reference to the related case
  - `similarity_score` (NUMERIC) - Similarity score (0-1)
  - `created_date` (TIMESTAMP) - When the similarity was computed

  ## Security
  - BigQuery does not support row-level security or custom policies in DDL. Use IAM for access control.

  ## Indexes
  - Use clustering for fast filtering and sorting.
*/

CREATE TABLE IF NOT EXISTS cases (
  id STRING NOT NULL,
  case_id STRING NOT NULL,
  customer_name STRING NOT NULL,
  description STRING NOT NULL,
  priority STRING NOT NULL,
  type STRING NOT NULL,
  product STRING NOT NULL,
  status STRING NOT NULL,
  module STRING,
  sub_module STRING,
  category STRING,
  geography STRING,
  created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  CONSTRAINT pk_cases PRIMARY KEY(id),
  CONSTRAINT uq_cases_case_id UNIQUE(case_id)
)
CLUSTER BY case_id, priority, status, type, created_date, customer_name, product;

CREATE TABLE IF NOT EXISTS case_similarity (
  id STRING NOT NULL,
  case_id STRING NOT NULL,
  related_case_id STRING NOT NULL,
  similarity_score NUMERIC NOT NULL,
  created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  CONSTRAINT pk_case_similarity PRIMARY KEY(id),
  CONSTRAINT uq_case_similarity UNIQUE(case_id, related_case_id)
)
CLUSTER BY case_id, similarity_score;

-- Note: Foreign key constraints are not enforced in BigQuery, but you can document them.
-- Security policies and row-level security must be handled via BigQuery IAM, not DDL.
