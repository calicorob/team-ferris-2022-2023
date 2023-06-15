FROM jupyter/datascience-notebook:latest
RUN pip install czapi 
RUN pip install pg8000