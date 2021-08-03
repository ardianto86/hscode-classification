FROM python:3.7
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./app.py /
COPY ./model_knn.sav /
EXPOSE 5000
CMD ["python", "/app.py"]