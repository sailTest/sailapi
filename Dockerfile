FROM python:3.11.6
ADD dependencies.txt /
RUN pip install -r dependencies.txt
ADD githubQuery.py /
ADD sendComms.py /
ADD setUpVariables.py /
CMD [ "python3", "./githubQuery.py" ]