ALTER TABLE job_applicant RENAME TO job_application;

-- Rename PK constraint if it exists as a constraint (most likely)
ALTER TABLE job_application
  RENAME CONSTRAINT pk_job_applicant TO pk_job_application;
