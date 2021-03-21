# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses vagrant to create an isolated application environment within a virtual machine. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install vagrant by following the [instructions here]('https://learn.hashicorp.com/tutorials/vagrant/getting-started-install). Addtitionaly you will need a provider such as [VirtualBox]('https://www.virtualbox.org/) or [Hyper-V]('https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v) installed.


## Configuration

You need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.


## Running the App

### Option 1: Docker

Docker compose configurations are provided for both production and development modes. The production configuration uses Gunicorn, while the development configuration uses Flask development server which has the additional benifit of hot reloading.

To start the application within a docker container, firstly ensure you have docker desktop installed and running, then you can run either command from your terminal:

```bash
# Production Mode
$ docker-compose up
```
```bash
# Development Mode
$ docker-compose -f docker-compose.development.yml up
```


### Option 2: Vagrant

To start the application in a vagrant virtual machine by running:
```bash
$ vagrant up
```


### Option 3: Poetry 
Alternatively you can start the app on your own machine with poetry by running:
```bash
$ poetry install
$ poetry run flask run
``` 


### Accessing the application:

After the project dependancies are installed, you should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Testing

### Option 1: Poetry
The end to end tests require you have the Chrome browser installed and that you download the corresponding version of the ChromeDriver:
* Download and install Chrome from [`here`](https://www.google.co.uk/chrome/)
* Download ChromeDriver from [`here`](https://sites.google.com/a/chromium.org/chromedriver/downloads) and add the executable file to the root of the project.

Once the test setup requirments are completed, execute the tests by running:
```bash
$ poetry run pytest
```

### Option 2: Docker
To build the docker image by running:
```bash
$ docker build --target test --tag todo-app:test .
```
To execute the unit and integration tests by running:
```bash
$ docker run todo-app:test tests
```
To execute the E2E tests by running:
```bash
$ docker run --env-file .env todo-app:test e2e_tests
```
