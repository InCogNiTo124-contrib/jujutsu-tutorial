# Creating a repository with `jj git init`

Let's make a new `jj` repository!

To create a new repository run the following command:

```console
$ (~/bak) jj git init
Initialized repo in "."
```

Now, you may be wondering, "why not just something along the lines of `jj init`?" The deal is this: there exists
a native repository format, but it is still a work in progress. So we're creating a
repository that's backed by a `git` repository underneath, because in practice, this
early in `jj`'s life, that's the right thing to do.

To check what just happened, run a `ls`:
```console
$ (~/bak) ls -lh
total 0
drwxr-xr-x  4 codelab codelab  80 Jun 22 21:08 .jj
```

`.jj` folder serves the same purpose as `.git` folder - it stores the code history in a sort of a file-system database.
