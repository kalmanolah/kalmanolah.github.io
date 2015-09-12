Title: Getting fail2ban to work with Symfony2 the proper(?) way
Date: 2014-06-21T17:24:25+02:00
Category: Web development
Tags: PHP, Symfony2, Security, fail2ban

_NOTE: This is a repost of an old article. I noticed that it was generating
a bunch of 404s for some people, so I figured I'd dig it up._

Described as "a script kiddie's worst nightmare", [fail2ban][1] is a tool that
reads log files, tries to match lines to predefined rules or filters, extracts
an IP address from those lines and "bans" the host that IP address belongs to,
in a certain way.

It is extremely customizable, can send email notifications and do even more cool
stuff. If you want to learn more about fail2ban, you can visit its homepage
[here][2].

This blog post will be focusing on making this wonderful tool work properly with
Symfony2, so you can automatically ban anyone trying to gain access to your
application in a harmful manner for a certain period.

## Creating the Authentication Failure Handler

Fail2ban needs a host or IP address so it can ban any offenders. This makes a
lot of sense, since generally it'll be creating temporary iptables rules that
drop packets coming from the offending IP address on ports 80 and 443.

Symfony however does not log the offender's IP address when authentication
fails, so we'll have to add that functionality ourselves by extending the
Default Authentication Failure Handler.

The only functionality we'll add is the logging of IP addresses when
authentication fails, in order to be able to extra data from our logs (stored in
app/logs/) using fail2ban.

```php
<?php

# src/Your/ExampleBundle/EventHandler/AuthenticationFailureHandler.php
namespace Your\ExampleBundle\EventHandler;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Security\Core\Exception\AuthenticationException;
use Symfony\Component\Security\Http\Authentication\DefaultAuthenticationFailureHandler;

class AuthenticationFailureHandler extends DefaultAuthenticationFailureHandler
{
    public function onAuthenticationFailure(Request $request, AuthenticationException $exception)
    {
        if (null !== $this->logger && null !== $request->getClientIp()) {
            $this->logger->error(sprintf('Authentication failure for IP: %s', $request->getClientIp()));
        }

        return parent::onAuthenticationFailure($request, $exception);
    }
}
```

As you can see, the only real functionality we've added is the logging. Now for
the matching service definition:

```yaml
# src/Your/ExampleBundle/Resources/config/services.yml
services:
    your.examplebundle.authenticationfailurehandler:
        class: Your\ExampleBundle\EventHandler\AuthenticationFailureHandler
        arguments: ["@http_kernel", "@security.http_utils", {}, "@logger"]
        tags:
            - { name: 'monolog.logger', channel: 'security' }
```

You'll also need to tell Symfony to use your handler by specifying a
failure_handler in your security.yml, like so:

```yaml
# app/config/security.yml
    firewalls:
        main:
            pattern: ^/
            form_login:
                provider: fos_userbundle
                csrf_provider: form.csrf_provider
                failure_handler: your.examplebundle.authenticationfailurehandler
            logout:       true
            anonymous:    true
```

Alright, that's it for the Symfony part. You should be seeing the IP address of
any offenders in your `app/logs/%kernel.environment%.log` file, like so:

```
[2013-11-03 23:24:55] security.INFO: Authentication request failed: Bad credentials [] []
[2013-11-03 23:24:55] security.ERROR: Authentication failure for IP: 127.0.0.1 [] []
```

Next up: the fail2ban filter!

## Creating a custom fail2ban filter for Symfony2

To create a new filter for fail2ban, we'll create a file in
`/etc/fail2ban/filter.d/symfony.conf` with the following contents:

```ini
[Definition]
failregex = Authentication\sfailure\sfor\sIP:\s<HOST>\s
```

That was easy, right? We should create a jail in `/etc/fail2ban/jail.local`
which uses our new filter. The definition for this jail will depend on your
configuration, but a basic one could look like this:

```ini
[symfony]
enabled   = true
filter    = symfony
logpath   = /var/www/my-project/app/logs/prod.log
port      = http,https
bantime   = 600
banaction = iptables-multiport
maxretry  = 3
```

Now all that remains is to execute `service fail2ban reload` and to test your
new setup.

[1]: http://en.wikipedia.org/wiki/Fail2ban
[2]: http://www.fail2ban.org
