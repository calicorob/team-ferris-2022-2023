FROM jupyter/datascience-notebook:latest
RUN pip install czapi==0.2
RUN pip install pg8000
RUN pip install sqlalchemy_utils
