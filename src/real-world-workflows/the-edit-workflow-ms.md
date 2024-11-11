# The Edit Workflow

The first workflow we're gonna look at is The Edit Workflow™️. This workflow is
a simple extension of the previous commands and features a new command
(`jj edit`), as well as a new flag to `jj new`. Lots to learn!

The workflow goes like this:

1. We create a new change to work on our feature.
2. If we end up doing exactly what we wanted to do, we're done. This is what we
   know.
3. If we realize we want to break this up into smaller changes, we do it by
   splitting the change, or making a new change before the current one, swapping
   to it, and making that change.
4. We then go back to the main change.

Let's see how to use `jj` this way.

## Setup

Let's create support for providing multiple files through CLI arguments. We'll
also do some refactoring along the way.

### Commit 1:

First we'll loop over the args list and back the files up sequentially:

<details>
<summary>Solution👇</summary>

```python
import sys

def main():
    print("bat - a simple backup tool")

    # show help if no args
    if len(sys.argv) == 1:
        print("Usage: bat [file]")
        sys.exit(1)
    filenames = sys.argv[1:]  # <-- this is new

    for filename in filenames:
        # figure out the backup filename
        backup_filename = filename + ".bak"

        # write the content byte-for-byte
        with open(backup_filename, "w") as file_write:
            with open(filename, "r") as file_read:
                return file_write.write(file_read.read())


    return


if __name__ == "__main__":
    main()
```

</details>

We've changed about half of our lines, but most of it is indendation. Remember,
the changes we've done are already "commited", in a `git` sense. Describe the
changes appropriately with `jj describe` (and don't forget to create a new
change).

### Commit 2: Refactor the backup

So far so good, and not that much different from before. Let's make another
change which will prepare us for the core of the edit workflow. This time, we'll
refactor backup into a function. Pretty straightforward:

<details>
<summary>Solution👇</summary>

```python
import sys

def backup(filename, backup_filename):

    # write the content byte-for-byte
    with open(backup_filename, "w") as file_write:
        with open(filename, "r") as file_read:
            return file_write.write(file_read.read())

def main():
    print("bat - a simple backup tool")

    # show help if no args
    if len(sys.argv) == 1:
        print("Usage: bat [file]")
        sys.exit(1)
    filenames = sys.argv[1:]

    for filename in filenames:
        # figure out the backup filename
        backup_filename = filename + ".bak"

        backup(filename, backup_filename)

    return


if __name__ == "__main__":
    main()
```

</details>

Give a nice description to this change, too.

### Commit 3: filesystem checks we forgot to add

It's been pretty straightforward for now, but now we're getting to the crux of
The Edit Workflow. Imagine that at this point you remembered you wanted to add
checks that the files exist when you added the support for the arguments. The
commit history looks like this now:

TODO output

```console
$ (~/bak) jj log
@  yttplkun codelab@example.com 2024-10-20 21:33:55 54ea73e4
│  Refactor
○  pwvspqpu codelab@example.com 2024-10-20 21:33:25 78119b26
│  Add support for multiple files
○  toopzvqo codelab@example.com 2024-10-20 21:31:20 72cbddae
│  it's important to comment our code
○  pztxxzlr msmetko@msmetko.xyz 2024-10-20 21:31:19 cc487119
│  bak version 1
◆  zzzzzzzz root() 00000000
```

Let's try adding a new change between Commits 1 and 2:

TODO output

```console
$ (~/bak) jj new -B y
Rebased 1 descendant commit
Working copy now at: lwylrkpv 12375c1c (empty) (no description set)
Parent commit      : pwvspqpu 78119b26 Add support for multiple files
Added 0 files, modified 1 files, removed 0 files
```

<!--
```
$ (~/bak) jj log
○  yttplkun codelab@example.com 2024-10-20 22:43:41 427e2e37
│  Refactor
@  lwylrkpv codelab@example.com 2024-10-20 22:43:41 12375c1c
│  (empty) (no description set)
○  pwvspqpu codelab@example.com 2024-10-20 21:33:25 78119b26
│  Add support for multiple files
○  toopzvqo codelab@example.com 2024-10-20 21:31:20 72cbddae
│  it's important to comment our code
○  pztxxzlr msmetko@msmetko.xyz 2024-10-20 21:31:19 cc487119
│  bak version 1
◆  zzzzzzzz root() 00000000
```
-->

The very first line of the output shows the power of The Edit Workflow, and `jj`
in general. We inserted a new change in between two commits _with a single
command_[^git] and the child commit, `y`, got rebased auto-magically.

That's right: editing change history chain in the middle is no problem for `jj`
because the later commits simply get rebased so you can just continue working.
To illustrate this rebasing behaviour, let's just implement the checks in the
current working copy by adding the following changes, and see what happens:

<details>
<summary>Solution👇</summary>

```python
import sys
import os  # <-- this is new

def main():
    print("bat - a simple backup tool")

    # show help if no args
    if len(sys.argv) == 1:
        print("Usage: bat [file]")
        sys.exit(1)
    filenames = sys.argv[1:]

    assert all(os.path.isfile(p) for p in filenames), "Not all file paths exist!"  # <-- this is new

    for filename in filenames:
        # figure out the backup filename
        backup_filename = filename + ".bak"

        # write the content byte-for-byte
        with open(backup_filename, "w") as file_write:
            with open(filename, "r") as file_read:
                return file_write.write(file_read.read())


    return


if __name__ == "__main__":
    main()
```

</details>

If you save this, nothing will happen immediately. For the changes to be picked
up by `jj`, you ned to run a command, i.e. running `jj st`[^jj] to see the
status yields the following info:

```console
$ (~/bak) jj st
Rebased 1 descendant commits onto updated working copy
Working copy changes:
M bak.py
Working copy : lwylrkpv d7ce5a7c (no description set)
Parent commit: pwvspqpu 78119b26 Add support for multiple files
```

Again, by pure magic, and some math, commit containg the refactor got rebased
just like that ✨

To show this, switch back to the refactor commit and see the contents of the
`bak.py`:

```console
$ (~/bak) jj next --edit
$ (~/bak) cat bak.py
import sys
import os

def backup(filename, backup_filename):
    # write the content byte-for-byte
    with open(backup_filename, "w") as file_write:
        with open(filename, "r") as file_read:
            file_write.write(file_read.read())
    return


def main():
    print("bat - a simple backup tool")

    # show help if no args
    if len(sys.argv) == 1:
        print("Usage: bat [file]")
        sys.exit(1)

    filenames = sys.argv[1:]
    assert all(os.path.isfile(p) for p in filenames), "Not all file paths
exist!"

    for filename in filenames:
        # figure out the backup filename
        backup_filename = filename + ".bak"

        backup(filename, backup_filename)
    return


if __name__ == "__main__":
    main()
```

Those are all our changes at once! `jj` did an excellent job of staying out of
our way.

This is **extremelly powerful** and it eases lifes of many a developer.

## Conflicts?

You may be wondering, what if there were conflicts? Conflicts will be handled in
a different chapter. For now, know that a) rebasing always succeeds, even with
conflicts b) information about conflicts are stored as a part of the change, and
c) conflicts can be always be resolved manually or with more rebases.

## Summary

??

<hr/>

[^git]:
    to the best of my knowledge, this is impossible with `git`:
    https://stackoverflow.com/q/32315156

[^jj]: this could've been any other command, e.g. `jj log`
