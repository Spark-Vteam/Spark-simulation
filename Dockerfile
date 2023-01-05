# syntax=docker/dockerfile:1.4

# Specify the base image for the first stage of the build, and also
# specify that this stage should be named "builder"
FROM --platform=$BUILDPLATFORM python:3.8-slim


# RUN apk update
# RUN apk add make automake gcc g++ subversion python3-dev
# Set the working directory for the rest of the build to the /app directory
WORKDIR /app

# Copy the requirements.txt file from the current directory to the /app directory
# inside the image
COPY requirements.txt /app

# Install the Python packages listed in the requirements.txt file, using a cache
# of the pip package manager's cache directory to speed up the process
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

# Copy all files and directories in the current directory to the /app directory
# inside the image
COPY . /app

# Specify the default command that will be run when the container is started
ENTRYPOINT ["python3"]

# Specify the default arguments that will be passed to the ENTRYPOINT command
CMD ["app.py"]
