ALTER TABLE job DROP CONSTRAINT IF EXISTS job_recruiter_id_fkey;
ALTER TABLE job DROP COLUMN recruiter_id;

DROP TABLE IF EXISTS company_admin;
DROP TABLE IF EXISTS recruiter;
