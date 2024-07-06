# Introduction - Marijan Smetko

In this codelab I'll introduce a new VCS called [jj](https://github.com/martinvonz/jj).
This codelab is written by Marijan Smetko, a.k.a. `InCogNiTo124`.

This tutorial came to be because, just like Steve, I like to write little notes and tutorials for, and by, myself when learning. I'm a big proponent of project-based learning, and I just happened to have a small project aside on which I would teach myself `jj` VCS and write about it. When I finished my independently created tutorial, I was surprised by just how __similar__ my and Steve's tutorials were -- while the topics would, naturally, going to be mostly same, I actually wrote some eeringly similar sentences sounding just like Steve, even some similar jokes! The sole difference was that I have a concrete project. After asking Steve privately if it was OK[^accept], I decided to merge my tutorial to his.

Unlike Steve, though, I have a deep dislike of `git`. My VCS background to my sadness consists solely of `git` - while I __have__ heard about other VCSs (`hg`, `pijul`, `svn` etc), I've never had an opportunity to work with them extensively[^google]. I understand `git`'s model and theory (it's just DAG's all the way down, right?), but I am fed up with `git`'s CLI and magical incantations. Splitting individual commits, reordering the parent and children, merging multiple commits, undoing the operations... those should all be easy operations. Yet, in `git`'s case, they really aren't.

I discovered that `jj` turned out to solve _all_ of the forementioned problems I had with `git`. I did not have to remember exactly which command to invoke, they came to me naturally. I could easily go back in time, fix stuff and later changes would rebase automatically. If I made a mistake, `jj undo` was always there.

There was a second subtle effect - using `jj` made me care about what goes into the changes I'm making. Before, with `git`, I did not care much what was a part of the commit. Commit cleanliness wasn't much enforced with my previous employers, let alone during Uni days, and editing the staging area to split a chage or commit partiall was always a PITA. Now, it's brainless for me to make a new commit or clean up an old one, so much that now that that friction is gone I started caring more about what goes into every change.

[^accept]: And an affirmative reply, ofc.
[^google]: Until I started at Google, that is - they use `hg`.
[^git]: This isn't _strictly_ necessary, as `jj` can create a git repository on its own. But this is written from a perspective of a user that wishes to adopt a `jj` on an existing project.
