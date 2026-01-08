import os
import cloudinary

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

OBJECT_CONFIG = {
    "applicant": {
        "model": "Applicant",
        "folder": "applicant_prof_img",
        "column": "profile_img_link",
        "img_id": "profile_img_id"
    },
    "company": {
        "model": "Company",
        "folder": "company_prof_img",
        "column": "profile_img_link",
        "img_id": "profile_img_id"
    },
    "job": {
        "model": "Job",
        "folder": "job_posting_img",
        "column": "posting_img_link",
        "img_id": "posting_img_id"
    },
}
