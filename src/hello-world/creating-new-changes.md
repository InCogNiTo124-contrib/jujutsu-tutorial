# Using `jj new` to create new changes

We're done with our first commit, and we're ready to do more work. Let's start
that work by using `jj new`:

```console
$ (~/bak) jj new
Working copy now at: upvquvzp 493054a9 (empty) (no description set)
Parent commit      : mqxqrzlm 69e3b8b0 bak version 1
```

It's that easy!

We now have a new change, `upvquvzp`, that's empty and has no description. But its parent is our previous change, `mqxqrzlm`. Let's check out `jj st`:

```console
$ (~/bak) jj st
The working copy is clean
Working copy : upvquvzp 493054a9 (empty) (no description set)
Parent commit: mqxqrzlm 69e3b8b0 bak version 1
```

Nice, a clean working directory: all of our changes were made in `mqxqrzlm`, and
we're starting this change fresh.

We now technically have a very primitive, but near-complete, workflow. That's
_really_ all you need to know to get started. To practice, let's make another
change. This time, I'm going to describe things first, before I make any changes:

```console
$ (~/bak) jj describe -m "it's important to comment our code"
Working copy now at: upvquvzp 232e1d84 (empty) it's important to comment our code
Parent commit      : mqxqrzlm 69e3b8b0 bak version 1
```

Just what we expected, still an empty change, but with a description, and our
commit ID has updated while the change ID stays the same.

Let's modify `bak.py`:

```python
import sys

def main():
    print('bat - a simple backup tool')
    # show help if no args
    if len(sys.argv) == 1:
        print('Usage: bat [file]')
        sys.exit(1)
    filename = sys.argv[1]

    # figure out the name of the backup
    backup_filename = filename + '.bak'
    
    # write the content byte-for-byte
    with open(backup_filename, 'w') as file_write:
        with open(filename, 'r') as file_read:
            file_write.write(file_read.read())
    return

if __name__ == "__main__":
    main()
```

We can double check that `jj` has noticed our change:

```console
$ (~/bak) jj st
Working copy changes:
M bak.py
Working copy : upvquvzp 886439f9 it's important to comment our code
Parent commit: mqxqrzlm 69e3b8b0 bak version 1
```

Excellent, `bak.py` has been `M`odified, we have a new commit hash. Since
we're done with this change, let's start a new one:

```console
$ (~/bak) jj new
Working copy now at: mmxtwkxv 3e0ff705 (empty) (no description set)
Parent commit      : upvquvzp 886439f9 it's important to comment our code
```

Wonderful.

Just seeing the parent change is very restrictive, though. It would be nice
if we could look at all of the work we've done. Let's tackle that next.
