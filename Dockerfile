#docker build . -t nyc-navigation1 -f Dockerfile
#docker run --name nyc-challenge1 -v $PWD/website/route.py:/app/website/route.py -it nyc-navigation1 bash

# Get base image
FROM python:3.8
# Create directories
RUN mkdir /app
# Copy local files to the app folder
COPY . /app/.
# Select the working directory
WORKDIR /app
# Install required packages
RUN pip install -r requirements.txt
# Run the model.py file
CMD ["python", "website/route.py"]