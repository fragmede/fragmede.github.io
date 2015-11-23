---
layout: post
title:  "Ubuntu Kernel PPA"
date:   2015-11-07 11:54:00
categories: ubuntu kernel ppa trim
---

To preface, I'm fluent in git, and kernel stuff. I've been using Debian since before Ubuntu came around, and have made a .deb or two, but haven't really explored the Ubuntu kernel build process. The kernel has special packagine needs because multiple versions of the kernel want to exist on disk, in case the new version fails to boot. In order to accomodate this, there's a debian/ subdir and a debian.master/ subdir. I haven't really explored the ramifications of this past the bare minimum required to get it to work.

These are my notes on what I had to do as a kernel person in order to take a simple patch that I wrote and end up with an Ubuntu PPA hosting a kernel with that patch. (The patch in question force disables TRIM, in case the hardware (an SSD) reports TRIM support but doesn't actually support it for some reason or other. [TRIM disabling PPA][trim-disable-ppa])

Creating the PPA itself was pretty easy to point and click at launchpad.net, and getting the gpg key configured and setup wasn't too hard.

However, even though I know git relatively well, how git interacts with the debian packaging scripts, and the PPA system was a mystery, so here are my notes on what I had to do in order to get a relatively simple patch uploaded to that PPA.aaaa

First I checked out the tag I wanted to build on top of and started a branch:

    git checkout -b option-disable-trim Ubuntu-4.2.0-16.19

Next I cherry picked the previous prepared commit:

    git cherry-pick 73267d3b226d

Now for the packaging/PPA bits. First we reset everything.

    fakeroot debian/rules clean

The next command fires up $EDITOR with some prepared text that we need to edit. The kernel, being the kernel, has a hack so the version number actually part of package name: linux-image-4.2.0-16-generic is the actual package name, with a version number of '4.2.0-16.19'. In order to be compatible with this hack, our custom version has to comply with debian package naming convention. Theres a bunch of bogus ABI check stuff (it doesn't *really* check the ABI) that I got tired of trying to work around, so for now just reuse the same version number.

Edit the version number to be the same, and change 'UNRELEASED' to your Ubuntu codename (in this case, wily). urgency doesn't do much so I set it to 'low' (has a minor effect on the PPA build priority). After the asterisk, put a short description of the changes.

    dch 

Then, because the kernel is special, we copy the changelog:

    cp debian/changelog debian.master/changelog

You want the two changelog files to match, but the tools aren't polished enough to assert that they're the same. If they don't match, then you'll only find out hours later when some aspect of the PPA process fails relating to package versions. (I didn't try making it a sym/hard link, so that might work.)

Next, build the source package, substituting in your key. (Use `gpg --list-secret-keys | head -3 | tail -1 | sed 's/^[^/]*\/\([^ ]*\) .*$/\1/'` to get it.) This assumes you have already setup your GPG key for launchpad.

    dpkg-buildpackage -S -nc -sa -kXXXXXXXX --force-sign -I.git -I.gitignore -i'\.git.*'

After that finishes, in the *parent* directory (../), you'll have a couple files. This is a bit weird, and doesn't work with symlinks, but that's how debian packaging has always (mis)worked, AFAIK.

The last two steps are to configure the dput config file with the correct incoming and login, and to run the dput. If there are issues after the upload related to your dput configuration, you can add `-f` to dput to force it to re-upload.

    cd ..
    dput -f ppa:samson-uo/trim-disable-kernel linux_4.2.0-16.19~option-trim-disable_source.changes 

Assuming that completes successfully, Launchpad will email if there are errors, or if there are none, that your upload has been accepted. Eventaully the build should complete, but I'm writing this while waiting for the compile to finish, but assumedly I have a PPA with installable packages.

(Also, if you have a system with hardware that reports it has TRIM but sending TRIM causes it to blow up, then you can try out this one-off PPA build.)

[trim-disable-ppa]: https://launchpad.net/~samson-uo/+archive/ubuntu/trim-disable-kernel
