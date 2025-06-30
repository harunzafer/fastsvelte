FROM python:3.12

# Directory structure will be like:
# /code/
#   ├── requirements.txt
#   └── app/
#        ├── main.py

# Set the working directory. We are going to work in /code
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code into the container
COPY app ./app

# Expose the port that the app will run on
EXPOSE 3100

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3100", "--workers", "1"]