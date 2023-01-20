FROM vtvit/iquser:slim-buster

#clonning repo 
RUN git clone https://github.com/vtvit/iquser /root/iquser
#working directory 
WORKDIR /root/iquser

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/iquser/bin:$PATH"

CMD ["python3","-m","iquser"]
