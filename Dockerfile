# Use an official Python runtime as a parent image
FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies
RUN pip install --no-cache-dir tensorflow \
                                opencv-python \
                                mediapipe \
                                scikit-learn \
                                matplotlib \
                                scikit-image \
                                numpy \
                                keyboard

# Run app.py when the container launches
CMD ["python", "main.py"]

#On terminal: docker build -t asltranslator .