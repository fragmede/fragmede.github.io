---
layout: post
title:  "Hotspot on Nexus 5x"
date:   2015-12-28 09:32:00
categories: android hotspot root 
---

Not going to get into Why carriers continue to charge extra for this, but to
enable the built-in hotspot feature on Android Marshmallow (6.0), I had to root
the phone, then add `net.tethering.noprovisioning=true` to the end of
`/system/build.prop` (and reboot). `settings put global tether_dun_required`
into a shell is the way to enable it for phones running KitKat, but that didn't
seem to do anything.
