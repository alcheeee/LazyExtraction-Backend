from UserDataManager import user_data_manager
from Corporations.CorporationManager import corporation_manager
from Jobs.GeneralJobs import Job, all_jobs
from Jobs.PoliceForce import PoliceForce, police_ranks
from db import create_db_and_tables
import random


DO_ADD_USERS_TEST, users_to_add = 0, 10
DO_USER_STAT_TEST = 0
DO_CORP_TEST = 0
DO_JOB_TEST = 1

def Add_Users_tests(amount_tests):
    for i in range(1, amount_tests+1):
        user_data_manager.create_user(f'Dev{random.randint(100, 10000)}', '123',
                                      f'dev{random.randint(100, 10000)}@dev.com')

def Adjust_User_Stat_tests():
    user_data_manager.update_stat(user_id=8, stat_name='health', new_value=300)
    user_data_manager.adjust_energy(user_id=6, energy_delta=-1)

def Corporation_tests():
    corporation_manager.create_corporation(corp_name='Dev Team Inc', corp_type='Crime', user_id=6) #Create Corporation
    corporation_manager.add_user_to_corporation(user_id=5, corporation_id=1) #Add user to Corporation
    corporation_manager.is_user_in_corporation(user_id=5, corporation_id=1) #Is user in Corporation
    corporation_manager.remove_user_from_corporation(user_id=6, corporation_id=1) #Remove user from Corporation
    corporation_manager.is_user_in_corporation(user_id=6, corporation_id=1) #Is user in Corporation

def Jobs_tests():
    #store_bagger = all_jobs['Store Bagger']
    #user_data_manager.update_user_job(user_id=3, job_name=store_bagger.job_name)

    user_job_get = all_jobs[user_data_manager.get_user_info(user_id=3).job]

    user_job_get.apply_stat_changes(user_id=3)

def main():
    create_db_and_tables()

    #Tests, Temporary
    if DO_ADD_USERS_TEST:
        Add_Users_tests(users_to_add)
    if DO_USER_STAT_TEST:
        Adjust_User_Stat_tests()
    if DO_CORP_TEST:
        Corporation_tests()
    if DO_JOB_TEST:
        Jobs_tests()


if __name__ == "__main__":
    main()