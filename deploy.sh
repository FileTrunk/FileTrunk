docker-compose stop
docker-compose rm
env > .env
env > ./backend/.env
docker-compose up --build -d
