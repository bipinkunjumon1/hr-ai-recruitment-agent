import json
import os

from agents.jd_agent import JDAgent
from utils.document_parser import (
    DocumentParser
)


class JDService:

    def __init__(self):

        self.agent = JDAgent()

    async def upload_and_process(
        self,
        file
    ):

        upload_dir = "uploads/jd"

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

        jd_text = (
    DocumentParser.extract_text(
        file_path
    )
)

        result = self.agent.process(
            jd_text
        )

        with open(
            "uploads/jd/jd.json",
            "w"
        ) as f:

            json.dump(
                result,
                f,
                indent=4
            )

        return {

            "status": "success",

            "jd_data": result
        }