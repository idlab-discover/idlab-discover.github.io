---
layout: post
title: Trusting your containers - introduction
date: 2023-10-25
hero_height: is-large
hero_darken: true
tags: containers
author: Michiel Van Kenhove
---

Have you ever wondered if you should blindly run that Docker container image you found in some tutorial or guide? Can you trust every container image you find on the internet? What if that image you just pulled contains some malicious code? In this post, I will be going over the risks of blindly running any container image you find on the internet and why you may want to think twice when running that container image you just found.

## How do containers work?

Before we dive into the risks of running random container images, let's first take a look at how containers work.

Before containers existed, the cloud was using Virtual Machines (VM) to run workloads in the cloud. A virtual machine can be looked at as a virtual computer on physical hardware, and the same physical machine (host) can run multiple virtual machines. This is accomplished by virtualizing hardware, and most of the times a complete operating system (OS) runs inside the VM. The software running inside the VM (guest) sees the virtual hardware and it behaves as if it were running on physical hardware. Because each VM has its own virtual hardware, a good isolation between different workloads is accomplished. A (major) downside of VMs is the significant amount of overhead: they have slow boot times and consume a lot of resources, like CPU and RAM.

When the cloud became more popular, with higher and a more dynamic loads, it became clear that using VMs was not going to cut it anymore. When the load on an application suddenly increases, new VMs need to start. However, starting a VM can take a couple of minutes in the worst case. Due to the large overhead, a new solution needed to be found. This is the moment when containers were introduced!

Containers offer a lot less overhead compared to VMs. The time to start a container can be as little as a couple of seconds, having almost native performance of the physical hardware. Compared to a VM, a container uses software based isolation techniques, instead of creating virtual hardware. Multiple containers share the same underlying kernel (and sometimes also libraries) of the host-OS.

In the figure below, you can see the architectural difference between VMs and containers. As you can see, each VM has its own complete operating system which adds overhead. Containers on the other hand, run directly on the host operating system and share its kernel using a container runtime.
![Container vs virtual machine architecture](/img/trusting-your-containers/container_vs_vm_arch.png)

To run a container, you will first need a container image. A container image consists of all the software and dependencies needed to be able to run the bundled application. These bundles typically follow an industry standard, developed by the [Open Container Initiative (OCI)](https://opencontainers.org/). This image is used to start a container and a container image can run on multiple OCI-compliant runtimes without the need to recompile. If a container runtime is OCI-compliant, it should be able to run OCI-compliant container images. A container runtime is responsible for everything needed to run containers.

## The problem with traditional container runtimes

As mentioned above, traditional container runtimes share the underlying operating system kernel and hardware. There is no hardware isolation. If an application running inside a container has malicious behavior, it could escape the container through a vulnerability (e.g., [CVE-2019-5736](https://nvd.nist.gov/vuln/detail/CVE-2019-5736), [CVE-2022-0185](https://nvd.nist.gov/vuln/detail/CVE-2022-0185) and [CVE-2022-0811](https://nvd.nist.gov/vuln/detail/CVE-2022-0811)) and access the underlying host operating system, other containers, confidential data, etc. This malicious behavior is shown in the figure below.

![Evil application escapes container](/img/trusting-your-containers/container_evil_app.png)

When running a container image you downloaded from the internet, you don't always know its internal behavior. The image may contain malicious code. Another possibility is that the image does not contain any malicious code at the time you first downloaded the image, but a future update may introduce malicious behavior without you realizing. Therefore, you should always double check if you trust the publisher of a container image as a first precaution. It is also possible that a container image itself does intend any malicious behavior, but a malicious actor may find a way to attack a publicly accessible container and use privilege escalation techniques to escape the container.

## Solution: secure containers

Next to being extra precautious with which images you run, sometimes it is necessary for certain security sensitive environments to have a guarantee that a container image cannot do any harm due to malicious behavior. This is easier said than done, because this requires better isolation between the container, the host and other running containers, which in turn causes extra overhead.

Secure containers try to solve this with minimal overhead. They achieve better isolation while still offering the benefits of traditional containers, e.g., good boot times, portability, etc. A secure container does this by encapsulating each container in its own lightweight VM, appropriately named as microVM, as shown in the figure below. A microVM is a slimmed down version of a normal VM, where a lightweight and optimized guest-OS is utilized instead of a fully-fledged OS. A microVM reduces the overhead, e.g., booting times, CPU usage, memory usage, etc., that a traditional VM comes with. Using virtual hardware better isolates the workloads as shown in the figure below: when an attacker successfully escapes the container, they are still stuck in the microVM isolated environment. Ideally, secure container runtimes should also be OCI-compliant such that they can be used as a drop-in replacement for current container runtimes. A microVM-based secure container has the benefits of both worlds: the versatility of containers and the security of VMs.

![Evil application stuck in isolated microVM container](/img/trusting-your-containers/microvm_container_isolation.png)

## Conclusion

After reading this article, I hope you understand the risks of running "untrusted" container images and to be extra cautious when you don't recognize or trust the publisher of the image. We have discussed the potential for malicious code in container images and a solution to reduce the damage caused by malicious containers. Utilizing secure containers can significantly improve the security of your deployment without too much overhead. In a next post, I will be going more into detail about what a secure container runtime is and how it works. I will also analyse the overhead caused by using a secure container runtime, so you can determine if the (minimal) overhead is acceptable in your use-case to improve the security of your environment.


