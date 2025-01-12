# # Use an official Python runtime as the base image
# FROM python:3.9

# # Set the working directory
# WORKDIR /app

# # Copy application files
# COPY . /app
# COPY requirements.txt /app/

# # Update pip and setuptools
# RUN pip install --upgrade pip setuptools
# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose the port Streamlit runs on
# EXPOSE 8501

# # Start the Streamlit application
# CMD ["streamlit", "run", "chatbot.py", "--server.port=8501", "--server.enableCORS=false"]

# Use the official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt .

# Install required Python packages
RUN pip install -r requirements.txt --default-timeout=300 future

# Copy the rest of the application files to the container's working directory
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run your Streamlit application
CMD ["streamlit", "run", "chatbot.py", "--server.address=0.0.0.0"]