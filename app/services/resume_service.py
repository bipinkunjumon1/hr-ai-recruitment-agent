import json
import os

from agents.resume_agent import ResumeAgent
from utils.document_parser import (
    DocumentParser
)


class ResumeService:

    def __init__(self):

        self.agent = ResumeAgent()

    async def upload_and_process(
        self,
        file
    ):

        upload_dir = "uploads/resumes"

        os.makedirs(
            upload_dir,
            exist_ok=True
        )

        file_path = os.path.join(
            upload_dir,
            file.filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                await file.read()
            )

            resume_text = (
    DocumentParser.extract_text(
        file_path
    )
)
        result = self.agent.process(
            resume_text
        )

        json_path = (
            file_path
            .replace(".pdf", ".json")
        )

        with open(
            json_path,
            "w"
        ) as f:

            json.dump(
                result,
                f,
                indent=4
            )

        return {

            "status": "success",

            "resume_data": result
        }