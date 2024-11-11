# Intermezzo: `jj undo`.

`jj` has undo. This alone should delight you. It means that whatever you do to a
repo, there's a way out, unlike `git`.

Before trying the other workflow, where we'll implement exactly the same
functionality, we'll reset the repo to the state that was before our previous
changes.

## Undoing the changes

Let's try it right away:

```console
$ (~/bak) jj undo
Working copy now at: xspnypvt d88b6910 (no description set)
Parent commit      : vnzlqxlw 79784b78 Add support for arguments
```

My last change was a `jj describe`, and now it is undone. Let's try to undo one
more change:

```console
$ (~/bak) jj undo
Working copy now at: xspnypvt d026f4aa Add missing filesystem checks
Parent commit      : vnzlqxlw 79784b78 Add support for arguments
```

[_\*record screech\*_](https://youtu.be/sy_Aje0hnac?t=6) Uhm, why is the
description back?? Well, it turns out that there's an ever-so-slight gotcha with
`jj undo` ...

## Explanation: the log of ops

Every operation which updates the state of the repo (snapshotting while running
`jj log`, creating new commits, describing them, ...[^more]) is an operation
that gets logged in a log of operations, or informally, the `op log`. Every
operation is invertible, and this is what `jj undo` does - it peeks for the
topmost operation, creates an inverse op, and pushes it to the oplog stack. You
might already see where this is going.

To see the oplog for the current repo, run `jj op log`:

```console
$ (~/bak) jj op log
jj op log
@  fb3452e557e6 codelab@CODELAB 17 minutes ago, lasted less than a microsecond
│  undo operation 92b31b1aad08230d675e3f2be1f0ca74a601edaf1b5f96efa3cfafb4de293c3265fd85fbe09d9705d6127c2bb58b34481d31d5b25b97e0de271b5a879bd17eb1
│  args: jj undo
○  92b31b1aad08 codelab@CODELAB 19 minutes ago, lasted 1 millisecond
│  undo operation 7279764147e3b9098cbafb0ed1e3cbf54c21e7ae30d55aabe1b551a5828971f67bb365036b991578d5843245e5791b11e53bc1f1609e7536ac65184eb9860182
│  args: jj undo
○  7279764147e3 codelab@CODELAB 19 minutes ago, lasted less than a microsecond
│  describe commit d88b6910777df8f915cea61bf756ac2aeea253dc
│  args: jj describe -m 'Add missing filesystem checks'
○  537d0c86740a codelab@CODELAB 19 minutes ago, lasted 8 milliseconds
│  snapshot working copy
│  args: jj describe -m 'Add missing filesystem checks'
○  22b8c929078f codelab@CODELAB 19 minutes ago, lasted 4 milliseconds
│  new empty commit
│  args: jj new -B vounrmkw
○  fd9d4fd580a8 codelab@CODELAB 19 minutes ago, lasted 1 millisecond
│  describe commit 6775ea6e9869d4f6ca3c5e4777ae7ae12172a795
│  args: jj describe -m 'Refactor the code'
...
```

So what happened was that the second `jj undo` undid the first undo (_de facto_
a redo), bringing us back to the first place. 🔄.[^surprise]

Not all is lost, though - there's a way to return the repo to the previous state
stored in the oplog with one more command

## Restoring the previous state

Since, in the next chapter, we'll try to create exactly the same features but
with another workflow, we'll try to reset the repo to the state before our 3
commits:

```console
$ (~/bak) jj op log
...
○  954d42960f59 codelab@CODELAB 58 minutes ago, lasted 1 millisecond
│  describe commit 8ea1bb797546b7c844d549d7757ebd8a80f7c4cc
│  args: jj describe -m 'Add support for arguments'
○  d68ee7e203f5 codelab@CODELAB 58 minutes ago, lasted 5 milliseconds
│  snapshot working copy
│  args: jj describe -m 'Add support for arguments'
○  d22a86c1e48d codelab@CODELAB 58 minutes ago, lasted 8 milliseconds
│  new empty commit
│  args: jj new
○  fa336f46446e codelab@CODELAB 58 minutes ago, lasted 15 milliseconds
│  snapshot working copy
│  args: jj st
○  f90062d6cf64 codelab@CODELAB 58 minutes ago, lasted 4 milliseconds
│  describe commit a20c735c5c33f7a4abd726945e93ac5c234defed
│  args: jj describe -m 'it\'s important to comment our code'
...
```

In my repo, the operation which creates a new change after adding comments to
the code, but before adding support for the arguments is `d22a86c1e48d`. In
order to reset the repo to this point, simply write:

```console
$ (~/bak) jj op restore d22a86c1e48d
Working copy now at: vnzlqxlw c19e02a3 (empty) (no description set)
Parent commit      : vlxslxsq 90872cc0 it's important to comment our code
Added 0 files, modified 1 files, removed 0 files
$ (~/bak) jj log
@  vnzlqxlw codelab@example.com 2024-11-11 20:22:22 c19e02a3
│  (empty) (no description set)
○  vlxslxsq codelab@example.com 2024-11-11 20:22:22 90872cc0
│  it's important to comment our code
○  ozmllltk codelab@example.com 2024-11-11 20:22:22 8ff37d45
│  bak version 1
◆  zzzzzzzz root() 00000000
```

Perfect!

Don't worry if you make a mistake - there's always `jj undo` :)

## Summary

Running `jj undo` once will undo the last operation. This will create a new
operation on the opstack.

Running `jj undo` again will, also, undo the latest operation. However, at this
point the latest operation will be the operation that undoes the previous -
effectively redoing an op.

In order to restore the history to a particular point, we use `jj op restore`.

<hr/>

[^more]:
    further down the road we'll see merging commits, splitting, and other kinds
    of ops

[^surprise]:
    Surprised? Take a look at the following discussion
    [martinvonz/jujutsu#3700](https://github.com/martinvonz/jj/issues/3700)
