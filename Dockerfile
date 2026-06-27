FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Set up a new user named "user" with user ID 1000 for cloud security
RUN useradd -m -u 1000 user
USER user

# Set home directory and path
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy project files and assign ownership to the user
COPY --chown=user . $HOME/app

# Expose port 7860 (Hugging Face Spaces Cloud Standard)
EXPOSE 7860

# Run Streamlit on port 7860
CMD ["streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]