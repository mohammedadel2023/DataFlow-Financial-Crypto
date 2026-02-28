from Data_Scraping.last_ar_of_fx import scrap
from Batch_Handling.duplicate_checking import hashing , check_duplication
from helper.config import get_setting
from Batch_Handling.write_on import write_on_minio , write_on_postgreSQL
import logging


setting = get_setting()

logging.basicConfig(
    level=setting.Log_level.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True
)

logger = logging.getLogger(__name__)
connect_str = f"dbname={setting.postgres_dbname} user={setting.postgres_user} password={setting.postgres_passward} host={setting.postgres_host} port={setting.postgres_port}"

logger.debug("start the program and enter the scrap() function")
# 1- scraping
docs = scrap()

logger.debug(" finish scrap() and enter the hashing() function")
# 2-cheking the data
hashing(docs)
check_duplication(connect_str, docs)

logger.debug(" finish hashing() and check_duplication() and enter the write_on_minio() function")
# 3- uploading on db's
write_on_minio(docs)

logger.debug(" finish write_on_minio() and enter the write_on_postgreSQL() function")
write_on_postgreSQL(docs, connect_str)

logger.debug(" finish write_on_postgreSQL() and exit the program")