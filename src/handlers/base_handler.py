from src.zechem_db_utils.zechem_db_utils import ZechemDBUtils
from src.utils.s3_utils import S3Utils
from src.utils.email_utils import EmailSender


class BaseHandler:

    def __init__(self):
        self.db = ZechemDBUtils()
        self.s3 = S3Utils()
        self.email_sender = EmailSender()
