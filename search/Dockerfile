FROM python:3.7
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./app.py /
COPY ./model/model_knn.sav /
RUN mkdir -p -v /templates
COPY ./templates/base.html /templates/base.html
COPY ./templates/index.html /templates/index.html
COPY ./templates/filter.html /templates/filter.html
EXPOSE 5000
CMD ["python", "/app.py"]