import logging
from fastapi import HTTPException, UploadFile, File
from sqlalchemy.sql import exists
from database import db_session_scope
from core.services.file_service.file_config import OBJECT_CONFIG
from cloudinary.uploader import upload
from cloudinary.uploader import destroy

logger = logging.getLogger(__name__)


class ImageService:

    def __init__(self, model):
        self.model = model
        self.config = self._resolve_config()

    def _resolve_config(self):
        config = next(
            (
                cfg for cfg in OBJECT_CONFIG.values()
                if cfg["model"] == self.model.__name__
            ),
            None
        )

        if not config:
            raise HTTPException(
                status_code=500,
                detail="Invalid object type provided"
            )

        return config

    def record_exists(self, model, object_id: int) -> bool:
        with db_session_scope(commit=False) as session:
            return session.query(
                exists().where(model.id == object_id)
            ).scalar()

    def upload_object_image(
                self,
                object_id: int,
                file: UploadFile = File(...)
            ):

        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=500,
                detail="Only image files are allowed on this endpoint"
            )

        if self.record_exists(self.model, object_id):

            try:
                result = upload(
                    file.file,
                    folder=self.config["folder"],
                    resource_type="image"
                )

                with db_session_scope(commit=True) as session:
                    column = getattr(self.model, self.config["column"])
                    column_id = getattr(self.model, self.config["img_id"])

                    session.query(self.model).filter(
                        self.model.id == object_id
                    ).update(
                        {column: result["secure_url"],
                         column_id: result["public_id"]}
                    )

                return {
                    "url": result["secure_url"]
                }

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Image upload failed: {str(e)}"
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="No record found based on data provided!")

    def get_object_image(self, object_id: int):

        mapped_column = self.config["column"]

        with db_session_scope(commit=False) as session:
            obj = session.query(self.model).filter(
                self.model.id == object_id
            ).first()

        if not obj:
            raise HTTPException(
                status_code=404,
                detail="Record not found"
            )

        return getattr(obj, mapped_column)

    def delete_from_cloudinary(self, public_id: str):
        result = destroy(public_id)

        if result.get("result") != "ok":
            raise RuntimeError("Failed to delete image from Cloudinary")

    def delete_object_image(self, object_id: int):

        with db_session_scope(commit=True) as session:
            obj = session.query(self.model).filter(
                self.model.id == object_id
            ).first()

            if not obj:
                raise HTTPException(
                    status_code=404,
                    detail="Record not found"
                )

            public_id = getattr(obj, self.config["img_id"])

            if not public_id:
                return {"message": "No image to delete"}

            self.delete_from_cloudinary(public_id)

            setattr(obj, self.config["column"], None)
            setattr(obj, self.config["img_id"], None)

            return {"message": "Image deleted successfully"}
