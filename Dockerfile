FROM python:3.8  
  
# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt  
  
# Switch working directory  
WORKDIR /app  
  
# Install the dependencies and packages in the requirements file  
RUN pip install --upgrade pip && pip install -r requirements.txt
  
# Copy every content from the local file to the image  
COPY . /app  
  
ENV GUEST_SERVICE_PORT=8080

EXPOSE $GUEST_SERVICE_PORT

# Set the main command to run with Gunicorn
CMD exec gunicorn main:app --bind 0.0.0.0:$GUEST_SERVICE_PORT --workers=$GUEST_SERVICE_WORKERS --log-level=$GUEST_SERVICE_LOG_LEVEL
