import json
import tenacity
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


class AttachmentsHandler:
    def __init__(self):
        self.allowed_attachments = None
        self.attachments = None


    async def add_attachment(self, attachment_name: str, session: AsyncSession):
        attachments_list = json.loads(self.attachments) if self.attachments else []
        if attachment_name in json.loads(self.allowed_attachments) and attachment_name not in attachments_list:
            attachments_list.append(attachment_name)
            self.attachments = json.dumps(attachments_list)
            session.add(self)
            await session.commit()


    async def remove_attachment(self, attachment_name: str, session: AsyncSession):
        attachments_list = json.loads(self.attachments) if self.attachments else []
        if attachment_name in attachments_list:
            attachments_list.remove(attachment_name)
            self.attachments = json.dumps(attachments_list)
            session.add(self)
            await session.commit()


    def get_attachments(self) -> List[str]:
        return json.loads(self.attachments) if self.attachments else []

