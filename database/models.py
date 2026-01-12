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
    Text,
    and_,
    Float,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base, foreign, remote
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()
Base = declarative_base(metadata=metadata)


# ======================
# ACCOUNT & USER
# ======================

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    type = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    exp_date = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)

    # 1:1 Account -> user
    user = relationship(
        "User",
        back_populates="account",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    company_recruiters = relationship(
        "CompanyRecruiter",
        back_populates="account",
        cascade="all, delete-orphan",
    )

    admin_company = relationship(
        "Company",
        back_populates="admin_account",
        uselist=False,
    )


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"quote": True}  # ważne dla Postgresa (reserved keyword)

    id = Column(Integer, primary_key=True, index=True)

    # 1:1 user -> Account (FK + unique)
    account_id = Column(
        Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=True)
    description = Column(String(255), nullable=True)
    profile_img_id = Column(Text, nullable=True)
    profile_img_link = Column(Text, nullable=True)

    account = relationship("Account", back_populates="user")

    work_experiences = relationship(
        "WorkExperience",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    educations = relationship(
        "Education",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    skills = relationship(
        "UserSkill",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    job_applications = relationship(
        "JobApplication",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    favorites = relationship(
        "Favorites",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# ======================
# EXPERIENCE & EDUCATION
# ======================

class WorkExperience(Base):
    __tablename__ = "work_experience"

    id = Column(Integer, primary_key=True, index=True)

    # FK must reference quoted "user" table in Postgres
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    job_title = Column(String(100), nullable=False)
    company_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(String(255), nullable=True)

    user = relationship("User", back_populates="work_experiences")


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    school_name = Column(String(100), nullable=False)
    degree = Column(String(100), nullable=True)
    field_of_study = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(String(255), nullable=True)

    user = relationship("User", back_populates="educations")


# ======================
# COMPANY
# ======================

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    ein = Column(String(10), unique=True, nullable=False)
    address = Column(JSONB, default={}, nullable=False)
    description = Column(String(255), nullable=True)
    account_id = Column(
        Integer,
        ForeignKey("account.id", ondelete="RESTRICT"),
        nullable=True,
        unique=True,
        index=True,
    )
    # company timestamp column removed per requirements

    profile_img_id = Column(Text, nullable=True)
    profile_img_link = Column(Text, nullable=True)

    jobs = relationship(
        "Job",
        back_populates="company",
        cascade="all, delete-orphan",
    )
    favorites_by_users = relationship(
        "Favorites",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    admin_account = relationship(
        "Account",
        back_populates="admin_company",
        uselist=False,
    )

    recruiters = relationship(
        "CompanyRecruiter",
        back_populates="company",
        cascade="all, delete-orphan",
    )


class CompanyRecruiter(Base):
    __tablename__ = "company_recruiter"

    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    join_date = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint("account_id", "company_id", name="pk_company_recruiter"),
    )

    account = relationship("Account", back_populates="company_recruiters")
    company = relationship("Company", back_populates="recruiters")

# ======================
# JOBS & APPLICATIONS
# ======================

class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)

    # poster/owner reference removed (table removed per requirements)

    title = Column(String, nullable=False)
    payoff = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    posting_date = Column(DateTime(timezone=True), server_default=func.now())
    expiry_date = Column(DateTime, nullable=True)
    posting_img_id = Column(Text, nullable=True)
    posting_img_link = Column(Text, nullable=True)

    company = relationship("Company", back_populates="jobs")

    applications = relationship(
        "JobApplication",
        back_populates="job",
        cascade="all, delete-orphan",
    )

    entity_tags = relationship(
        "EntityTag",
        primaryjoin=lambda: and_(
            EntityTag.entity_id == Job.id,
            EntityTag.entity_type == "job",
        ),
        viewonly=True,
        foreign_keys=lambda: [EntityTag.entity_id],
    )


class JobApplication(Base):
    __tablename__ = "job_application"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job.id"), nullable=False)
    application_date = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "job_id", name="pk_job_application"),
    )

    user = relationship("User", back_populates="job_applications")
    job = relationship("Job", back_populates="applications")


class Favorites(Base):
    __tablename__ = "favorites"

    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("company_id", "user_id", name="pk_favorites"),
    )

    company = relationship("Company", back_populates="favorites_by_users")
    user = relationship("User", back_populates="favorites")


# ======================
# TAGS & SKILLS
# ======================

class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_skills = relationship(
        "UserSkill",
        back_populates="tag",
        cascade="all, delete-orphan",
    )
    entity_tags = relationship(
        "EntityTag",
        back_populates="tag",
        cascade="all, delete-orphan",
    )


class UserSkill(Base):
    __tablename__ = "user_skill"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tag.id"), nullable=False)

    name = Column(String(100), nullable=False)
    desc = Column(String(255), nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    where_learned_or_used_id = Column(Integer, nullable=True)
    proficiency = Column(Integer, nullable=True)  # e.g. 1–5

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "tag_id", name="pk_user_skill"),
    )

    user = relationship("User", back_populates="skills")
    tag = relationship("Tag", back_populates="user_skills")


class EntityTag(Base):
    """
    Generic tag assignment: can connect a tag to a job, company, user, etc.
    entity_type holds values like: 'job', 'company', 'user'
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
            EntityTag.entity_id == Job.id,
            EntityTag.entity_type == "job",
        ),
        viewonly=True,
        foreign_keys=lambda: [EntityTag.entity_id],
    )


