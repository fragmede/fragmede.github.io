---
layout: post
title:  "Ubuntu Kernel PPA"
date:   2015-11-07 11:54:00
categories: ubuntu kernel ppa trim
---

Notes on what I had to do as a kernel person in order to get this [TRIM disabling PPA][trim-disable-ppa] working.

Creating the PPA itself was pretty easy to point and click at launchpad.net, and getting the gpg key configured and setup wasn't too hard.

However, even though I know git relatively well, how git interacts with the debian packaging scripts, and the PPA system was a mystery, so here are my notes on what I had to do in order to get a relatively simple patch uploaded to that PPA.

First I checked out the tag I wanted to build on top of and started a branch:

> git checkout -b option-disable-trim Ubuntu-4.2.0-16.19

Next I cherry picked the previous prepared commit:

> git cherry-pick 73267d3b226d

Now for the packaging/PPA bits. First we reset everything.

> fakeroot debian/rules clean

The next command fires up $EDITOR with some prepared text that we need to edit. Edit the version number to include ~branch-slug and change UNRELEASED to your Ubuntu codename (in this case, wily). I don't know about the urgency field, so I set it to 'low'. After the asterisk, put a short description of the changes.

> dch 

Next, build the source package, substituting in your key. (Use `gpg --list-secret-keys | head -3 | tail -1 | sed 's/^[^/]*\/\([^ ]*\) .*$/\1/'` to get it.) This assumes you have already setup your GPG key for launchpad.

> dpkg-buildpackage -S -nc -sa -kXXXXXXXX --force-sign -I.git -I.gitignore -i '\\.git.\*'

After that finishes, in the *parent* directory (../), you'll have a couple files. This is a bit weird, and doesn't work with symlinks, but that's how debian packaging has always (mis)worked, AFAIK.

The last two steps are to configure the dput config file with the correct incoming and login, and to run the dput. If there are issues after the upload related to your dput configuration, you can add `-f` to dput to force it to re-upload.

> cd ..
> dput -f ppa:samson-uo/trim-disable-kernel linux_4.2.0-16.19~option-trim-disable_source.changes 

Assuming that completes successfully, Launchpad will email if there are errors, or if there are none, that your upload has been accepted. Eventaully the build should complete, but I'm writing this while waiting for the compile to finish, but assumedly I have a PPA with installable packages.

(Also, if you have a system with hardware that reports it has TRIM but sending TRIM causes it to blow up, then you can try out this one-off PPA build.)

[trim-disable-ppa]: https://launchpad.net/~samson-uo/+archive/ubuntu/trim-disable-kernel
