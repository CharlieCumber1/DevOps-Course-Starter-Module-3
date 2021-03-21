docker build --target production --tag todo-app .
docker image tag todo-app "${DOCKER_USERNAME}/todo-app:latest"
docker image tag todo-app "${DOCKER_USERNAME}/todo-app:${TRAVIS_COMMIT}"
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push "${DOCKER_USERNAME}/todo-app:latest"
docker push "${DOCKER_USERNAME}/todo-app:${TRAVIS_COMMIT}"
docker tag "${DOCKER_USERNAME}/todo-app:latest" registry.heroku.com/todo-cc/web
echo "$HEROKU_API_KEY" | docker login --username=_ --password-stdin registry.heroku.com
docker push registry.heroku.com/todo-cc/web
heroku container:release web -a todo-cc
