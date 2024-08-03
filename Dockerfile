FROM python:3.10
ENV HOME /root
WORKDIR /root
COPY . .
# Download dependancies
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD python3 -u server.py