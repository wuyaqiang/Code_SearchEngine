# import os
#
# from .configure import COMPILER_GROUP_GID
# from .exceptions import JudgeClientError
#
#
# class InitSubmissionEnv:
#     def __init__(self, judger_workspace, submission_id):
#         self.path = os.path.join(judger_workspace, submission_id)
#
#     def __enter__(self):
#         try:
#             os.mkdir(self.path)
#             os.chown(self.path, 0, COMPILER_GROUP_GID)
#             os.chmod(self.path, 0o771)
#         except Exception as e:
#             raise JudgeClientError("failed to create runtime dir")
#         return self.path
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         # try:
#         #     shutil.rmtree(self.path)
#         # except Exception as e:
#         #     raise JudgeClientError("failed to clean runtime dir")
#         pass
#
#
# # def write_code_file(env_folder, usercode, language):
# #     """
# #     :param env_folder: folder used to put code file and executable
# #     :param usercode: user uploaded code
# #     :param language: user selected language
# #     """
# #     try:
# #         file_path = os.path.join(env_folder, LANGUAGE_FILENAMES[language])
# #         with open(file_path, "w", encoding="utf-8") as f:
# #             f.write(usercode)
# #         return file_path
# #     except Exception as e:
# #         raise JudgeClientError("write user code to file error")
#
#
# def get_compile_config(config, language):
#     return config[language]["compile"]
#
#
# def get_run_config(config, language):
#     return config[language]["run"]
#
#
# def get_testcase_path(folder):
#     """
#     :param folder: the testcase folder name
#     :return: list of absolute path for each testcase pairs
#     """
#     # return os.path.join(TESTCASE_DIR, testcase_folder)
#     result = []
#     inputs = []
#     outputs = []
#
#     cases = os.listdir(folder)
#     for item in cases:
#         if item.endswith("in"):
#             inputs.append(item)
#         else:
#             outputs.append(item)
#     inputs.sort()
#     outputs.sort()
#     return list(zip(inputs, outputs))
#
#
# # def judge_one(submission_folder, run_config):
