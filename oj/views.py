# import hashlib
# import uuid
#
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from rest_framework import serializers
# import json
# from .utils import InitSubmissionEnv, get_compile_config, get_run_config, get_testcase_path
# from .language import LANGUAGE_CONFIGS
# from .configure import SUBMISSION_DIR, JUDGER_RUN_LOG_PATH, TESTCASE_DIR, JUDGER_WORKSPACE_BASE
# import os
# import _judger
# from .compiler import Compiler
# from search.models import Problem, Label
#
# class LabelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Label
#         fields = ('id', 'label_name', 'father_id')
#
#
# def question_bank(request):
#     print("oj question_bank called.")
#     data = LabelSerializer(Label.objects.all(), many=True).data
#     check_box_list = ['']
#     problem_label = []
#     diffi = 'No'
#     if request.method == "POST":
#         check_box_list = request.POST.getlist('select_check')
#         diffi = request.POST.get('select_difficulty')
#
#     if len(check_box_list[0]) == 0:
#         if diffi == 'No':
#             problem_detail = Problem.objects.all()[:7]
#         else:
#             problem_detail = Problem.objects.filter(difficult=int(diffi))[:7]
#
#         for problem_d in problem_detail:
#             problem_label_str = ','.join(
#                 [i[0] for i in Label.objects.filter(problem__id=problem_d.id).values_list('label_name')])
#             problem_label.append(problem_label_str)
#     else:
#         type_list = check_box_list[0].split(',')
#         if diffi == 'No':
#             problem_detail = Problem.objects.filter()
#         else:
#             problem_detail = Problem.objects.filter(difficult=int(diffi))
#         for label_i in type_list:
#             problem_detail = problem_detail.filter(label__id=int(label_i))
#             if len(problem_detail) == 0:
#                 break
#         for problem_d in problem_detail:
#             problem_label_str = ','.join(
#                 [i[0] for i in Label.objects.filter(problem__id=problem_d.id).values_list('label_name')])
#             problem_label.append(problem_label_str)
#
#     return render(request, 'oj/question_bank.html',
#                   {"data": json.dumps(data), 'problem': zip(problem_detail, problem_label),
#                    'problem_label': problem_label, 'problem_id': [i for i in range(len(problem_label))]})
#
#
# def question_detail(request, question_id):
#     problem = get_object_or_404(Problem, pk=question_id)
#     return render(request, "oj/problem_detail.html", {"problem": problem})
#
#
# def question_result(request, question_id):
#     if request.method == "POST":
#         usercode = request.POST.get("user_code")
#         selected_language = request.POST.get("selected_language")
#
#         compile_config = get_compile_config(LANGUAGE_CONFIGS, selected_language)
#         submission_id = uuid.uuid4().hex
#
#         with InitSubmissionEnv(SUBMISSION_DIR, str(submission_id)) as submission_dir:
#             if compile_config:
#                 src_path = os.path.join(submission_dir, compile_config['src_name'])
#                 with open(src_path, "w", encoding="utf-8") as f:
#                     f.write(usercode)
#                 exe_path = Compiler().compile(compile_config, src_path, submission_dir)
#
#                 # run testcase
#                 problem = Problem.objects.get(pk=question_id)
#                 time_limit = problem.time_limit
#                 memory_limit = problem.memory_limit
#
#                 run_config = get_run_config(LANGUAGE_CONFIGS, selected_language)
#                 command = run_config["command"]
#
#                 # TODO temporarily set max_memory=int(0/1024)
#                 command = command.format(exe_path=exe_path, exe_dir=os.path.dirname(exe_path),
#                                          max_memory=int(0 / 1024)).split(" ")
#                 env = ["PATH=" + os.environ.get("PATH", "")] + run_config.get("env", [])
#
#                 testcase_folder = problem.testcase_folder
#                 if not testcase_folder:
#                     testcase_folder = "testcase_" + str(problem.id)
#                 testcase_folder = os.path.join(TESTCASE_DIR, problem.testcase_folder)
#
#                 testcase_pairs = get_testcase_path(testcase_folder)
#
#                 if time_limit is None:
#                     max_cpu_time = -1
#                     max_real_time = -1
#                 else:
#                     max_cpu_time = time_limit
#                     max_real_time = max_cpu_time * 3
#
#                 if memory_limit is None:
#                     max_memory_limit = -1
#                 else:
#                     max_memory_limit = memory_limit * 1024
#
#                 mem_check = run_config.get("memory_limit_check_only", 0)
#                 print("memory check only {}".format(mem_check))
#
#                 user_output_md5 = []
#                 correct_output_md5 = []
#                 for i, o in testcase_pairs:
#                     id = i.split(".")[0]
#                     in_file = os.path.join(testcase_folder, i)
#                     out_file = os.path.join(testcase_folder, o)
#                     user_output_file = os.path.join(submission_dir, "user" + id + ".out")
#
#                     run_result = _judger.run(max_cpu_time=max_cpu_time,
#                                              max_real_time=max_real_time,
#                                              max_memory=max_memory_limit,
#                                              max_stack=128 * 1024 * 1024,
#                                              max_output_size=-1,
#                                              max_process_number=_judger.UNLIMITED,
#                                              exe_path=command[0],
#                                              input_path=in_file,
#                                              output_path=user_output_file,
#                                              error_path=user_output_file,
#                                              args=command[1::],
#                                              env=env,
#                                              log_path=JUDGER_RUN_LOG_PATH,
#                                              seccomp_rule_name=run_config["seccomp_rule"],
#                                              uid=0,
#                                              gid=0,
#                                              # uid=RUN_USER_UID,
#                                              # gid=RUN_GROUP_GID,
#                                              memory_limit_check_only=mem_check)
#                     if run_result["result"] == _judger.RESULT_CPU_TIME_LIMIT_EXCEEDED:
#                         return HttpResponse("cpu time exceeded.")
#                     elif run_result["result"] == _judger.RESULT_REAL_TIME_LIMIT_EXCEEDED:
#                         return HttpResponse("Real time exceeded.")
#                     elif run_result["result"] == _judger.RESULT_MEMORY_LIMIT_EXCEEDED:
#                         return HttpResponse("Memory limit exceeded")
#                     elif run_result["result"] == _judger.RESULT_RUNTIME_ERROR:
#                         return HttpResponse("runtime error happend.")
#                     elif run_result["result"] == _judger.RESULT_SYSTEM_ERROR:
#                         return HttpResponse("system error happend.")
#                     else:
#                         with open(user_output_file, "r", encoding="utf-8") as f:
#                             content = f.read()
#                             print("current user output is {}".format(content))
#                         user_md5 = hashlib.md5(content.rstrip().encode("utf-8")).hexdigest()
#                         with open(out_file, "r", encoding="utf-8") as f:
#                             content = f.read()
#                             print("current correct output is {}".format(content))
#                         correct_md5 = hashlib.md5(content.rstrip().encode("utf-8")).hexdigest()
#                         user_output_md5.append(user_md5)
#                         correct_output_md5.append(correct_md5)
#                 for i in range(len(user_output_md5)):
#                     if user_output_md5[i] != correct_output_md5[i]:
#                         return HttpResponse("Wrong Answer, the {}th testcase failed.".format(i + 1))
#             return HttpResponse("All correct")
#
#     return HttpResponse("THis is the result page for question {}".format(question_id))