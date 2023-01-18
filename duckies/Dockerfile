# Start image
FROM python:3.9.13

# Define starting directory
WORKDIR /src

# Copy requirements for python
COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copies all files to our image
COPY ./src/Excel_Solver.py /src/Excel_Solver.py
COPY ./src/historical_sales_data.xls /src/historical_sales_data.xls
COPY ./src/bathing_friends_unlimited.xls /src/bathing_friends_unlimited.xls

# Specify starting command
CMD [ "python", "Excel_Solver.py"]