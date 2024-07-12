# docker-healthchecksio

[![Docker Build](https://github.com/Arcanexus/docker-healthchecksio/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Arcanexus/docker-healthchecksio/actions/workflows/docker-publish.yml) [![Automated Tests](https://github.com/Arcanexus/docker-healthchecksio/actions/workflows/tests.yml/badge.svg)](https://github.com/Arcanexus/docker-healthchecksio/actions/workflows/tests.yml)

## Purpose

This repo creates a Docker image that performs HTTP/TCP tests on services and update [healthchecks.io](https://healthchecks.io) checks accordingly.

Services are described in yaml config files.

## Configuration format
Each service is defined by :

|Parameter   |Mandatory|Value   |Default value|
|---|---|---|---|
|name |True|Name of the service (for logging purpose)||
|service_endpoint|True|Endpoint of the service to check                                  ||
|healthchecks_io_monitoring_url|True|URL of the healthchecks.io check associated to the service ([documentation](https://healthchecks.io/docs/http_api/#success-uuid))  ||
|check.type|False|- http<br>- tcp|http|
|check.ssl_check|False|true/false<br>(Only for check.type=http)|true|
|check.tcp_port|False|TCP port (Only for check.type=tcp)|80|
|check.tcp_timeout|False|TCP timeout (Only for check.type=tcp)|5|


Here is an configuration example :
```yaml
services:
  - name: "Google"
    check:
      type: http
      ssl_check: true
    service_endpoint: "https://www.google.com/"
    healthchecks_io_monitoring_url: "https://hc-ping.com/12345678-9abc-defg-hijk-lmnopqrstuv"
  - name: "Test"
    service_endpoint: "https://test.company.com/api/45/metrics/ping"
    healthchecks_io_monitoring_url: "https://hc-ping.com/12345678-9abc-defg-hijk-zzzzzzzzzzz"
  - name: TCPBin
    service_endpoint: tcpbin.com
    check:
      type: tcp
      tcp_port: 4242
      tcp_timeout: 30
    healthchecks_io_monitoring_url: "https://hc-ping.com/12345678-9abc-defg-hijk-zzzzzzzzzzz"
```

## Usage

:information_source: : DEBUG Mode can be activated using either :
- **-d, --debug** option in command line
- **DEBUG** environment variable set to `true`

### Using Docker
The image is build for the following architectures :
- linux/amd64
- linux/arm64
- linux/arm/v7

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
:construction: An example Helm chart is available in the `helm` directory. 

Customize the `values.yaml` file according to your needs.

:warning: The chart currently uses a NFS share to mount the config directory.

```bash
helm upgrade monitoring-healthckecksio ./helm/ -i
```

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
