FROM python
ADD ./bin/.bashrc /root/.bashrc
RUN apt update
RUN apt install wget
RUN apt install nano
ADD ./requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

CMD tail -f /dev/null