# html-mutation

## Requirement

Before installing the pyenv environment make sure the following are installed on your machine:

```sh
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```

Then make sure you have the following to be able to build:

- pyenv
- poetry

## Prepare the project
0. (optional if Python 3.10.1 is already present) ```pyenv install 3.10.1```
1. ```pyenv local 3.10.1```
2. ```git clone git@github.com:serval-uni-lu/html-mutation.git```
3. ```cd html-mutation```
4. ```potery env use python```
5. ```poetry install```

## Run tests

```poetry run pytest```

And to use them with coverage report

```poetry run pytest --cov=tests```
