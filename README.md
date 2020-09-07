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

To start the vagrant virtual machine by running:
```bash
$ vagrant up --provision
```

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

The end to end tests require you have the firefox browser installed and that you download the corresponding version of the Geckodriver (check version compatability [`here`](https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html)):
* Download and install firefox from [`here`](https://www.mozilla.org/en-US/firefox/download/)
* Download Geckodriver from [`here`](https://github.com/mozilla/geckodriver/releases) and add the executable file to the root of the project.

Once the test setup requirments are completed, execute the tests by running:
```bash
$ poetry run pytest
```
