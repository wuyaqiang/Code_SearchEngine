from __future__ import unicode_literals


default_env = ["LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"]


c_lang_config = {
    "compile": {
        "src_name": "main.c",
        "exe_name": "main",
        "max_cpu_time": 3000,
        "max_real_time": 5000,
        "max_memory": 128 * 1024 * 1024,
        "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c99 {src_path} -lm -o {exe_path}",
    },
    "run": {
        "command": "{exe_path}",
        "seccomp_rule": "c_cpp",
        "env": default_env
    }
}

cpp_lang_config = {
    "compile": {
        "src_name": "main.cpp",
        "exe_name": "main",
        "max_cpu_time": 3000,
        "max_real_time": 5000,
        "max_memory": 128 * 1024 * 1024,
        "compile_command": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++11 {src_path} -lm -o {exe_path}",
    },
    "run": {
        "command": "{exe_path}",
        "seccomp_rule": "c_cpp",
        "env": default_env
    }
}

py2_lang_config = {
    "compile": {
        "src_name": "solution.py",
        "exe_name": "solution.pyc",
        "max_cpu_time": 3000,
        "max_real_time": 5000,
        "max_memory": 128 * 1024 * 1024,
        "compile_command": "/usr/bin/python -m py_compile {src_path}",
    },
    "run": {
        "command": "/usr/bin/python {exe_path}",
        "seccomp_rule": "general",
        "env": default_env
    }
}

py3_lang_config = {
    "compile": {
        "src_name": "solution.py",
        "exe_name": "__pycache__/solution.cpython-35.pyc",
        "max_cpu_time": 3000,
        "max_real_time": 5000,
        "max_memory": 128 * 1024 * 1024,
        "compile_command": "/usr/bin/python3 -m py_compile {src_path}",
    },
    "run": {
        "command": "/usr/bin/python3 {exe_path}",
        "seccomp_rule": "general",
        "env": ["PYTHONIOENCODING=UTF-8"] + default_env
    }
}

java_lang_config = {
    "name": "java",
    "compile": {
        "src_name": "Main.java",
        "exe_name": "Main",
        "max_cpu_time": 3000,
        "max_real_time": 5000,
        "max_memory": -1,
        "compile_command": "/usr/bin/javac {src_path} -d {exe_dir} -encoding UTF8"
    },
    "run": {
        "command": "/usr/bin/java -cp {exe_dir} -XX:MaxRAM={max_memory}k -Djava.security.manager -Dfile.encoding=UTF-8 -Djava.security.policy==/etc/java_policy -Djava.awt.headless=true Main",
        "seccomp_rule": None,
        "env": default_env,
        "memory_limit_check_only": 1
    }
}

LANGUAGE_CONFIGS = {"C": c_lang_config,
                    "C++": cpp_lang_config,
                    "python2": py2_lang_config,
                    "python3": py3_lang_config,
                    "Java": java_lang_config}


LANGUAGE_FILENAMES = {"C": "main.c",
                      "C++": "main.cpp",
                      "python2": "main.py",
                      "python3": "main.py",
                      "Java": "Main.java"
                      }