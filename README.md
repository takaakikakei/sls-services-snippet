# template-sls

Serverless Framework のテンプレート

# 主な設定内容

- ディレクトリとファイルの骨組み

```
.
├── .github
│   └── PULL_REQUEST_TEMPLATE.md
├── .gitignore
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── includes
│   └── state-machines.yml
├── node_modules
├── package-lock.json
├── package.json
├── serverless.yml
└── src
    ├── __init__.py
    ├── exception.py
    ├── handlers
    │   ├── __init__.py
    │   └── handler.py
    ├── services
    │   └── __init__.py
    └── use_cases
        └── __init__.py
```

- パッケージやライブラリのインストール

```
$ serverless create --template aws-python3
$ npm init
$ sls plugin install -n serverless-step-functions
$ sls plugin install -n serverless-python-requirements
$ sls plugin install -n serverless-prune-plugin
$ pipenv install boto3 requests
$ pipenv install -dev isort flake8
```

- 下記ファイルの編集

```
serverless.yml
includes/state-machines.yml
.gitignore
```
