# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies for PyODBC and Microsoft ODBC Driver 17 for SQL Server
RUN apt-get update && apt-get install -y gnupg2 wget \
    && wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && wget -qO- https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get install -y unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
