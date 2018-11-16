# Creating your first Docker service
Originally presented at Mintel's Chicago office accompanied by these [slides](https://docs.google.com/presentation/d/1rK9y6Qs6qcrbK3--qUYeeacr3z2BSVE48WI-DfX6gJM).

### Prerequisites

* [docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [docker-compose](https://docs.docker.com/compose/install/)
* *optional* [pyenv](https://github.com/pyenv/pyenv-installer) with python 3.6, pip, pipenv
* *optional* [ctop](https://ctop.sh/) - "Top-like interface for container metrics"



Test everything is working

```bash
docker --version
docker-compose --version

docker run -it --rm --name nyancat 06kellyjac/nyancat
```



What's the difference between docker and a virtual machine?

- It works on my machine, but not in production!"
- Build once, deploy everywhere







ps. its a meme, but test that docker is installed and working before we start
docker run -it --rm --name nyancat 06kellyjac/nyancat

https://docs.docker.com/install/linux/docker-ce/ubuntu/

https://docs.docker.com/compose/install/

https://www.youtube.com/watch?v=JprTjTViaEA

https://www.youtube.com/watch?v=wxxigbHwDGM

https://www.youtube.com/watch?v=JBtWxj9l7zM

https://medium.freecodecamp.org/docker-quick-start-video-tutorials-1dfc575522a0

https://docker-curriculum.com