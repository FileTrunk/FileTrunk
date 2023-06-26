docker-compose stop
docker-compose rm
env > .env
env > ./backend/.env
env > ./frontend/.env
docker-compose up --build -d
