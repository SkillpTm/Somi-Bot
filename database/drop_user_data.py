from database.database_keywords import delete_all_user_keywords
from database.database_reminders import delete_all_user_reminders

###reminder#add###########################################################

def drop_user_data_in_database(member):
    deleted_keywords = delete_all_user_keywords(member.id)
    deleted_reminders = delete_all_user_reminders(member.id)