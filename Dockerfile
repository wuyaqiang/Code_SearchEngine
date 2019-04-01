FROM registry.docker-cn.com/library/ubuntu:16.04

COPY build/java_policy /etc

COPY . /code

WORKDIR /code

RUN apt-get update && apt-get install -y apt-transport-https && mv ./sources.list /etc/apt/ && \
    mv ./.pip /root

RUN buildDeps='software-properties-common git libtool cmake python-dev python3-pip python-pip libseccomp-dev' && \
    apt-get update && apt-get install -y python python3.5 python-pkg-resources python3-pkg-resources gcc g++ clang $buildDeps && \
    add-apt-repository ppa:openjdk-r/ppa && apt-get update && apt-get install -y openjdk-8-jdk && \
    apt-get install -y libssl-dev libffi-dev && \
    apt-get install -y libmysqlclient-dev && \
    cd /code && pip3 install --no-cache-dir -r requirements.txt && \
    cd /tmp && git clone -b newnew  --depth 1 https://github.com/QingdaoU/Judger && cd Judger && \ 
    mkdir build && cd build && cmake .. && make && make install && cd ../bindings/Python && python3 setup.py install && \
    apt-get purge -y --auto-remove $buildDeps && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -r compiler && useradd -r code

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]