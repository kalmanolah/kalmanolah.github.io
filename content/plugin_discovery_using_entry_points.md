Title: Plugin Discovery Using Entry Points
Date: 2014-12-21T23:00:00+02:00
Category: Programming
Tags: Python

I'm of the belief that just about anyone should have the right to expand on the
functionality of a FLOSS tool, but I'm also really particular about code style,
so I'd rather not deal with a ton of pull requests. I'm a difficulty person.

With this in mind, a short while ago I was looking for ways to provide users
with the ability to create modules which my tool could then load in at runtime.

Luckily, it turned out `$deity` had provided us mortals with Python's
[setuptools library][1], which happened to contain the exact features I was
looking for in the form of [entry points][2].

Entry points are magical little things which allow library authors "plug in" to
your framework/utility, as long as they know your entry point group's name.

Here's a `setup.py` file for an imaginary `text-tool` module, which will plug
in to our `sweet-tool` utility:

```python
#!/usr/bin/env python3
"""Setup module."""
from setuptools import setup, find_packages

setup(
    name='text-tool',
    version='0.0.1',
    description='A tool which performs text transformations!',
    long_description='A tool which performs text transformations!',
    author='John Doe',
    author_email='john.doe@example.com',
    url='https://github.com/john.doe/text-tool',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(),
    entry_points={
        'sweet.modules': ['text = text_tool:TextTool']
    }
)
```

In the code above, we're defining our awesome text module, which can plug its
`TextTool` class from the `text_tool` module into the `sweet.modules` entry
point group, identified by the name `text`.

Frameworks or pluggable tools can then load these entry points by specifying an
entry point group name.

Here's some example code which will instantiate modules by iterating over a
list of entry points and loading the referenced classes:

```python
from pkg_resources import iter_entry_points


for entry_point in iter_entry_points(group='sweet.modules'):
    print('Loading entry point %s' % entry_point.name)

    module_class = entry_point.load()
    module_instance = module_class()
```

Though the code above is useful for illustrating the power of entry points,
it's useful to be able to disable/enable specific modules, as well as reload
them by removing old instances of the module from the python interpreter.

With that in mind, here's the module loader for our `sweet-tool`:

```python
"""Sweet tool module-loading module."""
from pkg_resources import iter_entry_points


class ModuleManager:

    """The ModuleManager manages the loading of modules."""

    @property
    def modules(self):
        """Return modules."""
        return self._modules

    @modules.setter
    def modules(self, value):
        """Set modules."""
        self._modules = value

    def load_single(self, identifier):
        """Load a module by its identifier."""
        for entry_point in iter_entry_points(group='sweet.modules', name=identifier):
            self.modules[identifier] = entry_point.load()()

    def unload_single(self, identifier):
        """Unload a module by its identifier."""
        # We need to remove the module from the python interpreter in
        # order for live codebase updates to work.
        sys.modules.pop(self.modules[identifier].__module__)

        del self.modules[identifier]
        self.modules.pop("", None)
        self.modules.pop(None, None)

    def load(self):
        """Load all modules."""
        for entry_point in iter_entry_points(group='sweet.modules'):
            self.load_single(entry_point.name)

    def unload(self):
        """Unload all modules."""
        # We need to copy the list of identifiers, because unloading a
        # module removes it from the modules dict
        identifiers = list(self.modules.keys())
        for identifier in identifiers:
            self.unload_single(identifier)

    def start_single(self, identifier):
        """Start a module by its identifier."""
        self.modules[identifier].start()

    def stop_single(self, identifier):
        """Stop a module by its identifier."""
        self.modules[identifier].stop()

    def start(self):
        """Start all modules."""
        self.load()

        for identifier in self.modules.keys():
            self.start_single(identifier)

    def stop(self):
        """Stop all modules."""
        for identifier in self.modules.keys():
            self.stop_single(identifier)

        self.unload()

    def __init__(self):
        """Constructor."""
        self.modules = {}
```

Using the loader above, we could load, unload, start, stop all or specific
modules using only a few lines of code. Furthermore, because we remove the
imported module from `sys.modules` while unloading a module, reloading module
code without restarting the parent program becomes possible.

Here's a sample:

```python
from sweet.modules import ModuleManager


modules = ModuleManager()

# Load and start all modules
modules.start()

# Stop and unload all modules
modules.stop()

# Load a specific module by identifier
modules.load_single('text')

# Unload a specific module by identifier
modules.unload_single('text')

# Reload a module without having to shut down the program
modules.stop_single('text')
modules.unload_single('text')
modules.load_single('text')
modules.start_single('text')
```

Conclusion: entry points are amazingly useful. I think the
[xkcd python comic][3] pretty much sums up how I felt after writing the code
above for the first time.

[1]: http://pythonhosted.org//setuptools/
[2]: https://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins
[3]: http://xkcd.com/353/
