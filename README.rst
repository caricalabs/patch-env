patch_env - Patch os.environ with dynamic values when the interpreter starts
============================================================================

``patch_env`` lets you update Python's ``os.environ`` (the system environment
variables dictionary) early during the interpreter's lifecycle, using the output
of a command you specify.

This means you can inject a dynamic set of environment variables into the Python
interpreter without changing the environment of the process that starts the
interpreter or the command line arguments used to start it.  Integrated
development environments (IDEs) often make it inconvenient or difficult to
inject dynamic values in those configuration elements, so ``patch_env`` can help
there.

How it Works
------------

``patch_env`` installs a `Python site-specific configuration hook
<https://docs.python.org/3/library/site.html>` that causes it to run very early
when the interpreter starts.  When it runs, if the ``PATCH_ENV_COMMAND``
environment variable is set, its value is executed as a shell command and the
output of that command is used to update ``os.environ``.

So basically, set ``PATCH_ENV_COMMAND`` when you want ``patch_env`` to patch
things up for you, and don't set it when you don't.

Your command's output should contain one environment variable per line, in the
format ``KEY=value``::

    FOO=bar
    AWS_SESSION_TOKEN=FwoGZXIvY...
    HINT=values can have spaces and "special chars", but not newlines

Example: PyCharm/IntelliJ IDEA debugging with aws-vault
-------------------------------------------------------

You're developing a program that uses the `boto3
<https://github.com/boto/boto3>` library to access Amazon Web Services (AWS).
Your organization prohibits storing unencrypted access keys on disk, so you use
`aws-vault <https://github.com/99designs/aws-vault>` to manage them securely.
This works great when you're running your program from the command line, but
there isn't an easy way to get your IDE to feed the output of ``aws-vault`` into
the environment before it starts the Python interpreter.

Here's how you can use ``patch_env`` with an IDE like PyCharm to inject
``aws-vault``'s output into the Python interpreter you're debugging with:

1.  Install ``patch_env`` using pip.

2.  Edit your PyCharm debug configuration and set the ``PATCH_ENV_COMMAND``
    environment variable::

        PATCH_ENV_COMMAND=aws-vault exec my-profile -- sh -c "env | grep ^AWS_"

    Adjust the ``aws-vault`` command line as needed for your profile, session
    duration, etc.  The important part is that we make ``aws-vault`` execute a
    shell process that pipes all its environment variables through `grep` so we
    select only the AWS credential variables.

Now run the debugger.  ``patch_env`` logs the variables it parses from your
command at the ``DEBUG`` level, so you can configure Python logging at that
level if you need to verify that they're being parsed correctly.

Limitations
===========

If ``aws-vault`` doesn't already have valid credentials when you start
debugging, it may need to read things like your MFA token from standard input.
This will fail since ``patch_env`` doesn't feed any input to its
``PATCH_ENV_COMMAND``.

As a work-around, open a new terminal and run ``aws-vault exec`` for the profile
you use for debugging, enter the credentials there, and then re-launch the
debugger.  ``aws-vault`` stores its session tokens in your system's keystore, so
they'll be available to other instances of ``aws-vault`` until they expire.
