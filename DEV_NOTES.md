## Database Notes / Migrations

### Company NIP column

On **2025-12-19**, a new column was added manually to the `company` table:

- Column name: `nip`
- Type: `VARCHAR(10)`
- Purpose: Polish company tax identifier (NIP)

This change was applied **manually** in the local development database and is
**not yet covered by an automated migration**.

⚠️ If you are setting up the project on a new database, you must add this column
manually or create/apply a migration before running the backend.

A proper migration (e.g. Alembic) should be added later.
