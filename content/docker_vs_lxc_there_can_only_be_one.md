Title: Docker vs. LXC: There Can Only Be One
Date: 2014-07-17T23:37:19+02:00
Tags: Docker, LXC, Horrible
Cover: /assets/img/docker_lxc.png

![docker vs lxc][99]

_My sincere apologies for the title._

We've all heard of the (not so) new kid on the block: [*Docker*][1]. This
application shipping tool has been garnering lots of attention for a while now,
resulting in quite the amazing community, as well as it being pretty much
directly responsible for breathing life into the "containerize all the
things"-movement once again.

Docker has an extensive, yet easy to use set of features: with a
user-friendliness level several times that of things like LXC, the amazing
layered filesystem/snapshotting functionality, hosted image repositories
and last but not least the promise that you'll be able ship the exact same
application you developed right to production without the modification of a
single file, it would be strange for people not to be all over Docker. The
CentOS devs seem to agree with me, since there are in fact [**official** CentOS
7 docker images][2] out there.

Yet, while Docker's awesome and all, I - and most likely you, the reader - don't
have a real use-case for it beyond running some tests with Jenkins CI. (or
Bamboo if you hate freedom)

## An OS is not an artifact

_The title for this section was provided by Kris Buytaert, an angry bearded man
much like myself. We work together, and he has actually written [a blog post
about Docker][3] before.The difference between me and him is that he actually
knows what he's talking about._

An interesting thing that was brought up by Kris is that a Docker image cannot
be considered to be an artifact of your application. Instead, it's an artifact
of a minimal ubuntu/whatever installation with your application deployed inside
of it. This musing of his was so cryptic that I barely managed to draw
meaning out of it.

Now why is this important, you may ask? Well, the way I see it it's because
artifacts are supposed to be consistent across your infrastructure. Thus,
the Docker approach essentially forces you to go stateless, which is just not
viable in most cases.

## Containerize all the.. *thing*?

The number one reason why I will most likely never be using Docker in production
is because a Docker container is not intended to be used as a cheap VM, but
rather a sort of executable magic package.

In a perfect world, a Docker container executes a single process, sends all of
its log output to stdout/stderr and all blobs (think DBs) are stored in separate
volumes. That would then be the extent of the container's state. Sadly, we don't
live in a world like that.

When I deploy an application, I want its logs to be rotated, perhaps even
shipped to logstash. I want to be able to log into the machine the application
is running on, just in case. I want to be able to run cron jobs, tweak iptables
rules, #puppetize and a lot more. Docker doesn't want me to do any of that.

## PID 1

In a [recent blog post][4] by a friend and (as of very recently) vocal Docker
supporter Kenny Rasschaert, he goes into detail on the various advantages of
using Docker to deploy single applications. He also mentions a workaround for
using a Docker container as a cheap VM instead of a package on steroids. But in
the end, that's all it is: a workaround.

As I mentioned before, Docker containers are intended to run a single
application and nothing more. Got logs? Use a volume. Got blobs? Use a volume.
Need ssh access? Use [nsenter][5]. Need cron jobs? Too bad.

The guys over at Phusion [seem to think otherwise][6].
Since you're supposed to run one process inside a Docker container, the Phusion
guys made it run `systemd`. Armed with a real init system (and ntp server,
log guzzler, and a bunch of other things), their Docker baseimage defies all
preconceptions of normality and grants you `sshd`, `crond` and more. With their
image you can then build you own container: one that's quite similar to an [LXC
container][7].

## Hail LXC

So now I'll ask you this: If you're going to cast aside Docker's original
purpose - that is, to provide a Platform for your application (think PaaS) - and
are going to treat it as if it were LXC by using workarounds, why not just use
LXC instead?

Much like Phusion's baseimage, LXC allows you to create containers which you can
treat as if they were VMs with nearly no overhead, abiding by the [JeOS][8]
principle. (I really hope I used that right) Furthermore, LXC containers can be
nested, its resources can be limited using `cgroups`, and more.

As long as you are using a somewhat recent version of the Linux kernel, you'll
be able to have those CentOS/Fedora/Debian/Arch containers up and running in
next to no time at all.

## Closing thoughts

I feel like I'd rather use a tool like LXC rather than having to abuse Docker to
achieve the same thing. Though Docker's [AuFS][9] functionality would be nice to
have, it's not something I **need**. As for LXC: though its community certainly
is smaller, that's not a deal-breaker for me by any stretch of the imagination.

For now I'll continue to power my personal infrastructure using LXC, and perhaps
I'll take another look at Docker in the near future.

To the people out there with contrasting viewpoints, or the people who wish to
point out inconsistencies in my reasoning (there are more holes in this article
than there are in swiss cheese): I look forward to hearing your thoughts.
&#9786;

[1]: https://www.docker.com/
[2]: http://seven.centos.org/2014/06/docker-image-for-centos-7qa-now-available/
[3]: http://www.krisbuytaert.be/blog/docker-vs-reality-0-1
[4]: http://blog.kennyrasschaert.be/blog/2014/07/10/docker-process-or-machine/
[5]: http://man7.org/linux/man-pages/man1/nsenter.1.html
[6]: http://phusion.github.io/baseimage-docker/
[7]: https://linuxcontainers.org/
[8]: http://en.wikipedia.org/wiki/Just_enough_operating_system
[9]: http://en.wikipedia.org/wiki/Aufs
[99]: {filename}/assets/img/docker_lxc.png
