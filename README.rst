patch_env - Patch os.environ dynamically without changing code
==============================================================

``patch_env`` lets you change Python's ``os.environ`` (the system environment
variables dictionary) early during the interpreter's lifecycle, using the output
of a command you specify.

This means you can inject a dynamic set of environment variables into the Python
interpreter without changing the environment of the process that starts the
interpreter, or the command line arguments used to start it.  Integrated
development environments (IDEs) often make it inconvenient or difficult to use
dynamic values in those things, so ``patch_env`` can help there.

How it Works
------------

``patch_env`` works when you put a symbolic link named for a module you know
your program will load into a directory that's in ``PYTHONPATH``.  When Python
tries to import that module, it finds your symbolic link and actually imports
``patch_env``, which runs a command to update ``os.environ``, removes itself
from ``sys.path``, and then imports the actual module. The program continues
running with the updated environment.

Since ``patch_env`` removes itself from ``sys.path`` before it completes, you
can only patch one module per program.  This isn't a problem, though. Just
choose the module that gets imported earliest.

You can put multiple symbolic links in that directory, all pointing to
``patch_env.py`` of course, when you need to patch multiple programs.  You only
need to delete symbolic links if they're causing patching to happen too soon
(this is rarely a problem).

You can try using a symbolic link named after a Python system module to get
patching to happen very early, but this may cause problems because ``patch_env``
uses some of those modules itself.

Platform Support
----------------

``patch_env`` should work on any platform that supports symbolic links.  I
haven't tested it on Windows.

Example: PyCharm/IntelliJ IDEA debugging with aws-vault
-------------------------------------------------------

You're developing a program that uses the `boto3 <https://github.com/boto/boto3>` library to access Amazon Web Services (AWS).
Your organization prohibits storing unencrypted access keys on disk, so you use
`aws-vault <https://github.com/99designs/aws-vault>` to manage them securely.
This works great when you're running your program from the command line, but
there isn't an easy way to get your IDE to feed the output of ``aws-vault`` into
the environment before it starts the Python interpreter.

Here's how you can use ``patch_env`` with an IDE like PyCharm to inject
``aws-vault``'s output into the Python interpreter you're debugging with:

1.  Create an empty directory to contain your patch links (you can use any name)::

        mkdir /home/myself/patch_env_links

2.  Create a symbolic link for ``botocore``, the module we want to patch the
    environment before importing, that points to wherever ``patch_env.py`` is
    installed:

        ln -s /usr/local/bin/patch_env.py /home/myself/patch_env_links/botocore.py

3.  Edit your PyCharm debug configuration and set the following two environment
    variables, adjusting the ``PATCH_ENV_COMMAND`` value as needed to call
    ``aws-vault`` the right way for your profile:

        PYTHONPATH=/home/myself/patch_env_links

        PATCH_ENV_COMMAND=aws-vault exec myself-profile -- sh -c "env | grep ^AWS_"

Now run the debugger.  ``patch_env`` prints the variables it injects as it
injects them, so you can look for those in the PyCharm console.

Limitations
===========

If ``aws-vault`` doesn't already have valid credentials when you start
debugging, it may need to read things like your MFA token from standard input.
This will fail since ``patch_env`` doesn't feed any input to its
``PATCH_ENV_COMMAND``.

As a work-around, open a new terminal and run ``aws-vault exec`` for the profile
you use for debugging, and enter the credentials there, and then re-launch the
debugger.  ``aws-vault`` stores its session tokens in your system's keystore,
and they'll be available to other instances of ``aws-vault`` until they expire.
