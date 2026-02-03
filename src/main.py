from Data_Scraping.last_ar_of_fx import scrap
from Batch_Handling.duplicate_checking import hashing , check_duplication
from helper.config import get_setting
from Batch_Handling.write_on import write_on_minio , write_on_postgreSQL

setting = get_setting()

connect_str = f"dbname={setting.postgres_dbname} user={setting.postgres_user} password={setting.postgres_passward} host={setting.postgres_host} port={setting.postgres_port}"

# 1- scraping
docs = scrap()

# 2-cheking the data
hashing(docs)
check_duplication(connect_str, docs)

# 3- uploading on db's
write_on_minio(docs)
write_on_postgreSQL(docs, connect_str)