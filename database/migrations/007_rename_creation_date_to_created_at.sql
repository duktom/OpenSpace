-- Rename Account.creation_date -> created_at (data-safe)
ALTER TABLE account RENAME COLUMN creation_date TO created_at;

-- Rename Tag.creation_date -> created_at (data-safe)
ALTER TABLE tag RENAME COLUMN creation_date TO created_at;

-- Company.creation_date removal should already be handled in 003_drop_company_creation_date.sql
