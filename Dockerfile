# The Dockerfile defines the image's environment
# Import Python runtime and set up working directory
FROM python:3.7-alpine

# Install any necessary dependencies
RUN pip install jsonify
RUN pip install flask_restful
RUN pip install requests
RUN pip install Flask
RUN pip install Flask-Session
RUN pip install redis

# Open port 80 for serving the webpage
EXPOSE 80

# Run app.py when the container launches
CMD ["flask", "run"]