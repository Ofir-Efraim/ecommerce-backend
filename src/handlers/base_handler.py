from src.zechem_db_utils.zechem_db_utils import ZechemDBUtils
from src.utils.s3_utils import S3Utils


class BaseHandler:

    def __init__(self):
        self.db = ZechemDBUtils()
        self.s3 = S3Utils()
