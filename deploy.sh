docker build --target production --tag todo-app .
docker image tag todo-app "${DOCKER_USERNAME}/todo-app:latest"
docker image tag todo-app "${DOCKER_USERNAME}/todo-app:${TRAVIS_COMMIT}"
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push "${DOCKER_USERNAME}/todo-app:latest"
docker push "${DOCKER_USERNAME}/todo-app:${TRAVIS_COMMIT}"
curl -dH -X POST "$DEPLOY_WEBHOOK"
