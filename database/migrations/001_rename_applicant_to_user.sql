ALTER TABLE applicant RENAME TO "User";

ALTER TABLE work_experience
  RENAME COLUMN applicant_id TO user_id;

ALTER TABLE education
  RENAME COLUMN applicant_id TO user_id;

ALTER TABLE job_applicant
  RENAME COLUMN applicant_id TO user_id;

ALTER TABLE favorites
  RENAME COLUMN applicant_id TO user_id;

ALTER TABLE applicant_skill
  RENAME COLUMN applicant_id TO user_id;
