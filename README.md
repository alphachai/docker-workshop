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

## § Introduction

Have you ever heard an anguished developer shout out, "it works on my machine, but not in production!" You're not alone.

#### What is Docker?

Docker is a software container platform.[^1] 

* **Developers** use Docker to eliminate "works on my machine" problems when collaborating.
* **Operators** use Docker to make the best use possible of the available hardware.
* **Enterprises** use Docker to build agile pipelines which produce faster, more secure applications.

The key thing Docker does, "build once, deploy everywhere."

####  Terminology

##### Images

##### Containers

##### Volumes

##### Networks


## § Docker vs virtual machines

To understand why Docker is the new shiny, we must first understand how Docker differs from the Virtual Machines we've used in the past.

![VM Stack](media/vm_stack.svg)

The layers in a VM stack are:

1. **Infrastructure**: This is the hardware you're running on.
2. **Host operating system**: Usually a variation of Linux. On your laptop, this is probably ubuntu or fedora.
3. **Hypervisor**: You can think of a virtual machine as a complete, self-contained, simulated computer packaged into a file. Something needs to run that file, and that's where the hypervisor comes in.
   * Type 1: Direct link to infrastructure's hardware. Examples include Hyper-V on Windows, Hyperkit on macOS, and KVM on Linux.
   * Type 2: Runs an application on your host operating system. Examples include VirtualBox or VMWare.
   * Type 1 is usually far more efficient.
4. **Guest OS**
   * Each guest OS uses provisioned CPU, RAM, and disk space
   * In each OS, you must install your required dependencies (for example: python, postgres, redis)
   * Finally, you add your application.

![Docker Stack](media/docker_stack.svg)

1. Docker also requires a **infrastructure** and a **host operating system**. However, docker only runs on Linux. Most major versions are supported.
   * You can also develop on windows (pls no) or macOS
2. **Docker Daemon**:
   * Communicates directly with the host operating system and knows how to ration out resources for the running containers.
   * It's also an expert at ensuring each container is isolated from the host OS and other containers.
3. We still need **dependencies** to make our application work, but instead of requiring a host OS, we can bundle them up into a "docker image."
4. Our **application** code (if interpreted) or compiled application also lives in the compiled image.

---

In the past, we've used virtual machines to isolate applications. Containerization does this better!

A good analogy I've found[^2]  describes virtual machines as houses each with their own resources, while Docker containers are apartments, residing in a building where resources are shared more efficiently.

| Virtual Machines  | Docker                                                       |
| ----------------- | ------------------------------------------------------------ |
| Isolates systems  | Isolates applications                                        |
| Starts in minutes | Starts in milliseconds                                       |
| Full OS           | *Can* be a full OS, but ideally a single process (microservice) |

Other pros of using Docker:

* Generally faster
  * Lower system overhead
  * Shared kernel and libraries
* The program you tested while developing is identical to what will run in production
* Never ask infra to install a package on an app VM ever again!

## § References

[^1]: https://github.com/jonnylangefeld/learning/tree/master/Docker
[^2]: https://www.youtube.com/watch?v=pGYAg7TMmp0 "What is Docker & Docker Containers, Images, etc?"