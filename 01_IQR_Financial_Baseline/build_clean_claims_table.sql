-- flagship project cleaning code

SELECT *
FROM claims_expanded
WHERE patient_id IS NULL
   OR claim_id IS NULL
   OR allowed_amount IS NULL
   OR billed_amount IS NULL
   OR cpt_code IS NULL
   OR icd10_code IS NULL
   OR service_date IS NULL;
   
-- checking for duplicates

SELECT claim_id, COUNT(*) AS dup_count
FROM claims_expanded
GROUP BY claim_id
HAVING COUNT(*) > 1;

-- CPT and ICD-10 code validation

SELECT *
FROM claims_expanded
WHERE cpt_code NOT REGEXP '^[0-9]{4,5}$';
 
 SELECT *
 FROM claims_expanded
 WHERE icd10_code NOT REGEXP '^[A-Z][0-9][0-9A-Z](\\.[0-9A-Z]+)?$';
 
 -- Date Validation
 
 SELECT *
 FROM claims_expanded
 WHERE service_date > CURDATE();
 
 SELECT *
FROM claims_expanded
WHERE service_date IS NULL;

-- Age Validation 
SELECT *
FROM claims_expanded
WHERE age < 0 OR age > 120;

-- Risk Score Validation
SELECT *
FROM claims_expanded
WHERE risk_score < 0.2 OR risk_score > 3.0;

-- LOS Validation
SELECT *
FROM claims_expanded
WHERE length_of_stay < 0 OR length_of_stay > 30;

-- Network and Field Normilizations

UPDATE claims_expanded
SET network_status = 'In-Network'
WHERE network_status IS NULL;

UPDATE claims_expanded
SET provider_specialty = 'Unknown'
WHERE provider_specialty IS NULL;

UPDATE claims_expanded
SET place_of_service = 'Unknown'
WHERE place_of_service IS NULL;

-- Creating the table

CREATE TABLE claims_expanded_clean AS
SELECT *
FROM claims_expanded;










 
 
 





