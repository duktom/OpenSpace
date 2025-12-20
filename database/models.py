from sqlalchemy import (
    Column,
    MetaData,
    String,
    Integer,
    Boolean,
    DateTime,
    Date,
    ForeignKey,
    PrimaryKeyConstraint,
    and_,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base, foreign, remote

metadata = MetaData()
Base = declarative_base(metadata=metadata)


# ======================
# ACCOUNT & APPLICANT
# ======================

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # e.g. "applicant", "recruiter", "admin"
    type = Column(String(50), nullable=True)

    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    exp_date = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(50), nullable=True)

    # relationships
    applicant = relationship(
        "Applicant",
        back_populates="account",
        uselist=False,
        cascade="all, delete-orphan",
    )
    recruiters = relationship(
        "Recruiter",
        back_populates="account",
        cascade="all, delete-orphan",
    )
    company_admin_links = relationship(
        "CompanyAdmin",
        back_populates="account",
        cascade="all, delete-orphan",
    )


class Applicant(Base):
    __tablename__ = "applicant"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"), unique=True, nullable=False)

    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=True)
    description = Column(String(255), nullable=True)

    account = relationship("Account", back_populates="applicant")

    work_experiences = relationship(
        "WorkExperience",
        back_populates="applicant",
        cascade="all, delete-orphan",
    )
    educations = relationship(
        "Education",
        back_populates="applicant",
        cascade="all, delete-orphan",
    )
    skills = relationship(
        "ApplicantSkill",
        back_populates="applicant",
        cascade="all, delete-orphan",
    )
    job_applications = relationship(
        "JobApplicant",
        back_populates="applicant",
        cascade="all, delete-orphan",
    )
    favorites = relationship(
        "Favorites",
        back_populates="applicant",
        cascade="all, delete-orphan",
    )


# ======================
# EXPERIENCE & EDUCATION
# ======================

class WorkExperience(Base):
    __tablename__ = "work_experience"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicant.id"), nullable=False)

    job_title = Column(String(100), nullable=False)
    company_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(String(255), nullable=True)

    applicant = relationship("Applicant", back_populates="work_experiences")


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicant.id"), nullable=False)

    school_name = Column(String(100), nullable=False)
    degree = Column(String(100), nullable=True)
    field_of_study = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(String(255), nullable=True)

    applicant = relationship("Applicant", back_populates="educations")


# ======================
# COMPANY / ADMIN / RECRUITER
# ======================

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    nip = Column(String(10), unique=True, nullable=False)

    admins = relationship(
        "CompanyAdmin",
        back_populates="company",
        cascade="all, delete-orphan",
    )
    recruiters = relationship(
        "Recruiter",
        back_populates="company",
        cascade="all, delete-orphan",
    )
    jobs = relationship(
        "Job",
        back_populates="company",
        cascade="all, delete-orphan",
    )
    favorites_by_applicants = relationship(
        "Favorites",
        back_populates="company",
        cascade="all, delete-orphan",
    )


class CompanyAdmin(Base):
    __tablename__ = "company_admin"

    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("account_id", "company_id", name="pk_company_admin"),
    )

    account = relationship("Account", back_populates="company_admin_links")
    company = relationship("Company", back_populates="admins")


class Recruiter(Base):
    __tablename__ = "recruiter"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)

    recruiter_name = Column(String(50), nullable=False)
    recruiter_surname = Column(String(50), nullable=False)
    join_date = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="recruiters")
    company = relationship("Company", back_populates="recruiters")

    jobs_posted = relationship(
        "Job",
        back_populates="poster",
        cascade="all, delete-orphan",
        foreign_keys="Job.poster_id",
    )


# ======================
# JOBS & APPLICATIONS
# ======================

class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    poster_id = Column(Integer, ForeignKey("recruiter.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    posting_date = Column(DateTime(timezone=True), server_default=func.now())
    expiry_date = Column(DateTime, nullable=True)

    company = relationship("Company", back_populates="jobs")
    poster = relationship("Recruiter", back_populates="jobs_posted")

    applicants = relationship(
        "JobApplicant",
        back_populates="job",
        cascade="all, delete-orphan",
    )

    entity_tags = relationship(
        "EntityTag",
        primaryjoin=lambda: and_(
            foreign(EntityTag.entity_id) == remote(Job.id),
            EntityTag.entity_type == "job",
        ),
        viewonly=True,
    )


class JobApplicant(Base):
    __tablename__ = "job_applicant"

    applicant_id = Column(Integer, ForeignKey("applicant.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job.id"), nullable=False)
    application_date = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint("applicant_id", "job_id", name="pk_job_applicant"),
    )

    applicant = relationship("Applicant", back_populates="job_applications")
    job = relationship("Job", back_populates="applicants")


class Favorites(Base):
    __tablename__ = "favorites"

    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    applicant_id = Column(Integer, ForeignKey("applicant.id"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("company_id", "applicant_id", name="pk_favorites"),
    )

    company = relationship("Company", back_populates="favorites_by_applicants")
    applicant = relationship("Applicant", back_populates="favorites")


# ======================
# TAGS & SKILLS
# ======================

class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String, nullable=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    applicant_skills = relationship(
        "ApplicantSkill",
        back_populates="tag",
        cascade="all, delete-orphan",
    )
    entity_tags = relationship(
        "EntityTag",
        back_populates="tag",
        cascade="all, delete-orphan",
    )


class ApplicantSkill(Base):
    __tablename__ = "applicant_skill"

    applicant_id = Column(Integer, ForeignKey("applicant.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tag.id"), nullable=False)

    name = Column(String(100), nullable=False)
    desc = Column(String(255), nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    where_learned_or_used_id = Column(Integer, nullable=True)
    proficiency = Column(Integer, nullable=True)  # e.g. 1–5

    __table_args__ = (
        PrimaryKeyConstraint("applicant_id", "tag_id", name="pk_applicant_skill"),
    )

    applicant = relationship("Applicant", back_populates="skills")
    tag = relationship("Tag", back_populates="applicant_skills")


class EntityTag(Base):
    """
    Generic tag assignment: can connect a tag to a job, company, applicant, etc.
    entity_type holds values like: 'job', 'company', 'applicant'
    """
    __tablename__ = "entity_tag"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, nullable=False)
    entity_type = Column(String(50), nullable=False)
    tag_id = Column(Integer, ForeignKey("tag.id"), nullable=False)

    tag = relationship("Tag", back_populates="entity_tags")

    job = relationship(
        "Job",
        primaryjoin=lambda: and_(
            foreign(EntityTag.entity_id) == remote(Job.id),
            EntityTag.entity_type == "job",
        ),
        viewonly=True,
    )
