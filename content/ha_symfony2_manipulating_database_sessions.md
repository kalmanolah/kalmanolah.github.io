Title: HA Symfony2: Manipulating Database Sessions
Date: 2014-05-27T22:51:42+02:00
Category: Web development
Tags: Symfony2, PHP

![user plus database][1]

During the ongoing quest for high performance and high availability for your
Symfony2 project, at some point you're going to want to stick your sessions
into your database. Why, you ask? Well, consider the following scenario:

- You make a webapp named *"thing"* and deploy it on machines A and B
- User Bob logs in and starts using *thing* on machine **A**
- Machine **A** goes *down* and the service IP switches to machine **B**
- User Bob **now has to log in again**

Storing sessions in the databases also scales better, and so on and so forth.

Luckily, Symfony2 has got you covered. Though sessions live somewhere in the
`app/cache/<env>/` directory by default, there's a short and comprehensive
[cookbook article][2] that explains how and why to stop abusing I/O.

Once you follow the steps in that article, your sessions will all live happily
ever after. In your database.


## Manipulating session data

You don't want a gazillion session records in your database. Though the next
generation will surely enjoy the fact that humans/bots were already accessing
and using your application in the year 2014, there really is no real need for
you to keep that many sessions. The solution here is to delete all of the
things... or most of 'em anyway.

Making a command that deletes old sessions from the database is pretty
straightforward.
Here's an example:

```php
<?php

// src/Your/Bundle/Command/SessionsPurgeCommand.php
namespace Your\Bundle\Command;

use Symfony\Bundle\FrameworkBundle\Command\ContainerAwareCommand;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class SessionsPurgeCommand extends ContainerAwareCommand
{
    protected function configure()
    {
        $this
          ->setName('sessions:purge')
          ->setDescription('Deletes old sessions from the database');
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $threshold = 86400; // Maximum seconds of inactivity (86400s = 1 day)
        $limit = time() - $threshold; // Time limit, we'll purge older sessions

        $em = $this->getContainer()->get('doctrine.orm.entity_manager');

        $dql = 'select s from YourBundle:Session s
                where s.sessionTime < ?1';
        $query = $em->createQuery($dql);
        $query->setParameter(1, $limit);
        $sessions = $query->getResult();

        foreach ($sessions as $session) {
            $em->remove($session);
        }

        $em->flush();
    }
}

```

There. Just throw that into a cron job somewhere, and you're good to go.

You can also decode, access and modify user session data easily, since it's now
stored in the database. This means you could get stats from logged in users,
queue notifications for users, check certain types of history.. stuff like that.

Here's an example command which prints out a list and count of users who have
been active in the last 10 minutes:

```php
<?php

// src/Your/Bundle/Command/SessionsCheckCommand.php
namespace Your\Bundle\Command;

use Symfony\Bundle\FrameworkBundle\Command\ContainerAwareCommand;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class SessionsCheckCommand extends ContainerAwareCommand
{
    protected function configure()
    {
        $this
          ->setName('sessions:check')
          ->setDescription('Checks user activity for the past couple of minutes and prints out some stats');
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $threshold = 600; // Maximum seconds for last activity
        $limit = time() - $threshold;

        $em = $this->getContainer()->get('doctrine.orm.entity_manager');

        $dql = 'select s from YourBundle:Session s
            where s.sessionTime >= ?1
            order by s.sessionTime desc';
        $query = $em->createQuery($dql);
        $query->setParameter(1, $limit);
        $sessions = $query->getResult();

        $active_users = array();                // Names of active users
        $total_active_count = count($sessions); // Total active users
        $total_active_auth_count = 0;           // Total active logged in users

        foreach ($sessions as $session) {
            $data = base64_decode($session->getSessionValue());
            $data = str_replace('_sf2_attributes|', '', $data);
            $data = unserialize($data);

            // If this is a session belonging to an anonymous user, do nothing
            if (!array_key_exists('_security_main', $data)) continue;

            // User is logged in, increment counter
            $total_active_auth_count++;

            // Grab security data
            $data = $data['_security_main'];
            $data = unserialize($data);

            // Add username to activity list
            $last_active_users[] = $data->getUser()->getUsername();
        }

        $output->writeln('The following users were active in the past few minutes:');
        $output->writeln(join(', ', $active_users));

        $output->writeln(sprintf(
            '%s user(s) were active, and %s of them was/were logged in.',
            $total_active_count,
            $total_active_auth_count
        ));
    }
}

```

---

I'm not entirely sure what I wanted to achieve by writing this piece of blog
padding, but at the very least I'll never lose my session purging code again.

If you've read this far, you might want to [**buy Bastion on steam since it's
a great game with a godly OST and you'll save 85% at the time of writing**][3].
Seriously, hurry.

[1]: {filename}/assets/img/user_plus_database.svg
[2]: http://symfony.com/doc/current/cookbook/configuration/pdo_session_storage.html
[3]: http://store.steampowered.com/app/107100/
