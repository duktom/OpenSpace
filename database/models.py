from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    type = Column(Boolean)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    expiry_date = Column(DateTime)
    is_email_verified = Column(Boolean, default=False)

    applicant = relationship("Applicant", back_populates="account")
    company_account = relationship("CompanyAccount", back_populates="account")


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    desc = Column(String(255))
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="company")
    favourites = relationship("Favourites", back_populates="company")
    company_tag = relationship("CompanyTag", back_populates="company")
    company_account = relationship("CompanyAccount", back_populates="company")
    company_applicant = relationship("CompanyApplicant", back_populates="company")


class CompanyAccount(Base):
    __tablename__ = "company_account"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    company_id = Column(Integer, ForeignKey("company.id"))
    recruter_name = Column(String(50))
    recruter_surname = Column(String(50))
    recruter_desc = Column(String(255))

    account = relationship("Account", back_populates="company_account")
    company = relationship("Company", back_populates="company_account")


class CompanyApplicant(Base):
    __tablename__ = "company_applicant"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicant.id"))
    company_id = Column(Integer, ForeignKey("company.id"))
    job_id = Column(Integer, ForeignKey("job.id"))
    result = Column(Boolean)
    registration_date = Column(DateTime)
    contents = Column(String)
    direction = Column(String)

    job = relationship("Job", back_populates="company_applicant")
    company = relationship("Company", back_populates="company_applicant")
    applicant = relationship("Applicant", back_populates="company_applicant")


class Applicant(Base):
    __tablename__ = "applicant"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    name = Column(String(50))
    surname = Column(String(50))
    birth_date = Column(DateTime)
    desc = Column(String(255))

    account = relationship("Account", back_populates="applicant")
    favourites = relationship("Favourites", back_populates="applicant")
    applicant_tag = relationship("ApplicantTag", back_populates="applicant")
    company_applicant = relationship("CompanyApplicant", back_populates="applicant")


class Favourites(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicant.id"))
    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", back_populates="favourites")
    applicant = relationship("Applicant", back_populates="favourites")


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    desc = Column(String)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    company_id = Column(Integer, ForeignKey("company.id"))
    exp_date = Column(DateTime)

    job_tag = relationship("JobTag", back_populates="job")
    company = relationship("Company", back_populates="job")
    company_applicant = relationship("CompanyApplicant", back_populates="job")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80))
    desc = Column(String)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    job_tag = relationship("JobTag", back_populates="tag")
    company_tag = relationship("CompanyTag", back_populates="tag")
    applicant_tag = relationship("ApplicantTag", back_populates="tag")


class JobTag(Base):
    __tablename__ = "job_tag"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))

    tag = relationship("Tag", back_populates="job_tag")
    job = relationship("Job", back_populates="job_tag")


class CompanyTag(Base):
    __tablename__ = "company_tag"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))
    creation_time = Column(DateTime(timezone=True), server_default=func.now())

    tag = relationship("Tag", back_populates="company_tag")
    company = relationship("Company", back_populates="company_tag")


class ApplicantTag(Base):
    __tablename__ = "applicant_tag"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicant.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    tag = relationship("Tag", back_populates="applicant_tag")
    applicant = relationship("Applicant", back_populates="applicant_tag")
