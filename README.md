# Creating your first Docker service
Originally presented at Mintel's Chicago office accompanied by these [slides](https://docs.google.com/presentation/d/1rK9y6Qs6qcrbK3--qUYeeacr3z2BSVE48WI-DfX6gJM).

## § Prerequisites

* [docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [docker-compose](https://docs.docker.com/compose/install/)
* *optional* [pyenv](https://github.com/pyenv/pyenv-installer) with python 3.6, pip, pipenv
* *optional* [ctop](https://ctop.sh/) - "Top-like interface for container metrics"

Test everything is working.

```bash
docker --version
docker-compose --version

docker run -it --rm --name nyancat 06kellyjac/nyancat
```
