# docker-healthchecksio

[![Docker Build](https://github.com/Arcanexus/docker-healthchecksio/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Arcanexus/docker-healthchecksio/actions/workflows/docker-publish.yml)

## Purpose

This repo creates a Docker image that performs HTTP tests on services and update [healthchecks.io](https://healthchecks.io) checks accordingly.

Services are described in yaml config files.

## Configuration format
The expected configuration is the following :
```yaml
services:
  - name: "Google"
    service_url: "https://www.google.com/"
    healthchecks_io_monitoring_url: "https://hc-ping.com/12345678-9abc-defg-hijk-lmnopqrstuv"
  - name: "Test"
    service_url: "https://test.company.com/api/45/metrics/ping"
    healthchecks_io_monitoring_url: "https://hc-ping.com/12345678-9abc-defg-hijk-zzzzzzzzzzz"

```
Each service is defined by :
|   |   |
|---|---|
|name                             |Name of the service (for logging purpose)                    |
|service_url                      |URL of the service to check                                  |
|healthchecks_io_monitoring_url   |URL of the healthchecks.io check associated to the service ([documentation](https://healthchecks.io/docs/http_api/#success-uuid))  |

## Usage

:information_source: : DEBUG Mode can be activated using either :
- **-d, --debug** option in command line
- **DEBUG** environment variable set to `true`

### Using Docker
#### Use a single YAML config file
```bash
docker run -d --name docker-healthchecksio \
    -v /path/to/config.yml:/app/config/config.yml \
    ghcr.io/arcanexus/docker-healthchecksio:main
```

#### Use a directory containing multiple YAML config files
```bash
docker run -d --name docker-healthchecksio \
    -v /path/to/dir/containing/config/files/:/app/config/ \
    ghcr.io/arcanexus/docker-healthchecksio:main
```

### Using Helm chart (beta)
:construction: An example Helm chart is available in the helm directory. 

### Run Python directly

#### Prerequisites
- Python 3
- PIP

#### Available options
```bash
options:
  -h, --help                             show this help message and exit
  -c CONFIG, --config CONFIG             Path to the config file or directory
  -d, --debug                            Enable debug mode
```

#### Use a single YAML config file

```bash
pip install -U -r src/requirements.txt
python3 src/main.py -c /path/to/config.yml
```

#### Use a directory containing multiple YAML config files

```bash
pip install -U -r src/requirements.txt
python3 src/main.py -c /path/to/dir/containing/config/files/
```
