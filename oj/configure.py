# import os
# import pwd
# import grp
# from ChildProgramming.settings import BASE_DIR
#
#
# # put all data into this place
# DATA_DIR = os.path.join(BASE_DIR, "data")
#
# # temporarily put folder for judge
# SUBMISSION_DIR = os.path.join(DATA_DIR, "submission")
#
# JUDGER_WORKSPACE_BASE = os.path.join(BASE_DIR, "judger/run")
#
# # put all testcase into this place
# TESTCASE_DIR = os.path.join(DATA_DIR, "testcase")
#
# # put log files
# LOG_BASE = os.path.join(DATA_DIR, "log")
#
# COMPILER_LOG_PATH = os.path.join(LOG_BASE, "compile.log")
# JUDGER_RUN_LOG_PATH = os.path.join(LOG_BASE, "judger.log")
#
#
# COMPILER_USER_UID = pwd.getpwnam("compiler").pw_uid
# COMPILER_GROUP_GID = grp.getgrnam("compiler").gr_gid
#
# RUN_USER_UID = pwd.getpwnam("code").pw_uid
# RUN_GROUP_GID = grp.getgrnam("code").gr_gid