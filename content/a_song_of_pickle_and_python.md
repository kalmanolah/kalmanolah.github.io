Title: A Song of Pickle and Python
Date: 2014-06-17T23:41:56+02:00
Category: Programming
Tags: Horrible, Python

So here's the setting: you're a handsome, extremely charismatic
all-rounder tech-type person. Apparently you're also a bit of a
narcissist. On a warm and cosy evening you're sitting in front
of your fireplace in your leather armchair sipping on a fine
alcoholic beverage of your choice. As the individual hairs that
make up your beard are swaying in the breeze that
managed to find its way in through your open window, you are struck
by inspiration! Opening `$EDITOR` (which is **clearly** the
greatest of all text editors) after rushing your way to your
battlestation, you are greeted by this Python3 (because you
don't live in the past, y'know) module:

```python
"""This is the Thing module."""


class Thing:

    """This class represents a Thing."""

    @property
    def a_prop(self):
        """Return a prop."""
        return self._a_prop

    @a_prop.setter
    def a_prop(self, value):
        """Set a prop."""
        self._a_prop = value

    def __init__(self):
        """Instantiate Thing."""
        self.a_prop = 'value'
```

_"Damn, that's some nice pep8/pep257 conformity,"_ you think to
yourself. "I really am the best." Cursing yourself for letting
your mind wander, you hurriedly open the file you were looking
for. After a bit of buffering that you're not really aware of,
you are presented with yet another module, this time containing
two functions:

```python
"""This module handles Thing storage and loading."""
import pickle
import storage


def store_thing(thing):
    """Store an instance of Thing in $BACKEND_STORE."""
    serialized_thing = pickle.dumps(thing)
    storage.store(serialized_thing)


def load_things_from_store:
    """Load and return all instances of Thing in $BACKEND_STORE."""
    serialized_things = storage.load_all()
    things = []

    for serialized_thing in serialized_thing:
        thing = pickle.loads(serialized_thing)
        things.append(thing)

    return things
```

You instantly recognize these functions. You wrote them, after all.
You remember `store_thing` takes an instance of `Thing` as a parameter
and stores it in `$BACKEND_STORE`. `load_things_from_store` fetches all
instances of `Thing` you've previously stored in `$BACKEND_STORE` and
returns them.

Glossing over the code, your eyes stop on that familiar word: _pickle_.
`pickle` is the library you use for serializing `Thing` instances in
order to be able to save them and recreate them later.
"Ah _pickle_, bane of my existence, why must you torment me so?" you
lament. "Were it not for your ease of use and hilarious name, I would
have never had to suffer so!" A few days ago, you decided to add the
property `a_prop` to your `Thing` class. At the time you didn't know
your change would completely break the unpickling of your saved
`Thing` instances that were being loaded from `$BACKEND_STORE`. "But,
that all ends today!"

You decide that you're going to solve your pickling issues by invoking
two of the darkest magicks in your arsenal: inheritance and functions.
Recalling that Drupal - a PHP CMS/Framework - seems to be alive and
well despite the fact that its users don't know what anything *but*
functions are, you reckon you should be fine if you take this approach.

Deciding not to procrastinate too much, you manage to quickly add two
methods to your `Thing` class, making the improved version look like this:

```python
"""This is the Thing module."""


class Thing:

    """This class represents a Thing."""

    @property
    def a_prop(self):
        """Return a prop."""
        return self._a_prop

    @a_prop.setter
    def a_prop(self, value):
        """Set a prop."""
        self._a_prop = value

    def dump(self):
        """Turn this instance of Thing into plain data."""
        return self.__dict__

    @classmethod
    def load(cls, data):
        """Recreate and populate a Thing from existing data."""
        # Create a new Thing without calling __init__
        instance = cls.__new__(cls)

        # Populate Thing with data
        for key, value in data.items():
            setattr(instance, key, value)

        return instance

    def __init__(self):
        """Instantiate Thing."""
        self.a_prop = 'value'
```

You wipe away the tears that had appeared in the corner of your eye.
Looking toward Dropbox HQ, you solemnly perform a salute and thank
Guido van Rossum for creating such a beautiful work of art.
After contemplating what a world without Python would look like for a moment,
you turn to look at the masterpiece you've written.

The `dump` method will return a dict containing all of the attributes
of a `Thing` instance. The `load` class method can be called without
instantiating a new `Thing` manually, and will populate a new `Thing`
instance with existing data without incurring overhead by triggering
the constructor. Furthermore, if you move `load` and `dump` into a
class of their own, you can have `Thing` inherit that class and then
override the methods if needed. This would be useful in the case of
classes where attributes tend to disappear and appear randomly. For
instance, you could implement versioning logic in the `load` method
based on a `version` attribute.

At this point, you make a mental note to never use pickle for versioned
objects again.

It's getting late now. You're someone who finishes what they've
started though, so you decide you should see this through until the end.

You decide to update the functions that manage storage of `Thing`
instances in `$BACKEND_STORE`. After adding the correct method
calls and replacing pickle with the superior [msgpack][1], your fingers
finally relax as you save your module.

```python
"""This module handles Thing storage and loading."""
import msgpack
import storage
import thing


def store_thing(thing):
    """Store an instance of Thing in $BACKEND_STORE."""
    serialized_thing = msgpack.dumps(thing.dump())
    storage.store(serialized_thing)


def load_things_from_store:
    """Load and return all instances of Thing in $BACKEND_STORE."""
    serialized_things = storage.load_all()
    things = []

    for serialized_thing in serialized_thing:
        thing = Thing.load(msgpack.loads(serialized_thing))
        things.append(thing)

    return things
```

You retire to your chambers for the night, after you quickly write
a completely over the top blog post on the completely trivial and
boring thing you just did.

[1]: http://msgpack.org/
