# Create external volume only once
docker volume create fastsvelte-data

# Start the container
docker-compose up -d
