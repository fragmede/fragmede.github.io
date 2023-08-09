---
layout: post
title: Colo vs Cloud
date:   2023-08-04 01:33:00 PT
categories: 
---

what is the cheapest real actual server you can buy, new, with a support contract from a reputable vendor like HP/Dell/etc? (Assume we're running both the db and web-server on one server.) And what's the cost of sitting it in a reputable colo? And then multiply that by, let's say two, to get redundancy in a us-west and us-east region. Ideally, we'd want more regions to serve the entire world, but let's just go with two for now.

Let's say $10k for a server w/ support contract, x2, plus $400/mo for colo from Hurricane Electric (https://he.net/colocation.html) in us-west. It's a promo deal, and only in us-west, but let's just go with that price. $400*60 for 5 years (standard lifetime of computer equipment) = $24k. So $34k per server * 2 servers / 60 months ~= $1,130/month amortized. Thankfully, we're not in cloud, so that's the cost whether it's 1 request/second, or 1,000 requests/second.

A Raspberry Pi or old laptop in your basement with one consumer-grade ISP, and not factoring in the cost of electricity does not count here. Those are obviously going to be massively cheaper, but they're not remotely suitable for enterprise.

Meanwhile, Lambda gives you 1M requests and 3.2 million compute-seconds a month for free. This works out to be 0.4 rps (requests/second) or 22 requests / minute if spread out evenly. Which isn't, like, a lot, but you haven't paid a single cent to AWS for this yet. Let's say you want to get to 40 rps (to keep the math easy) or 100M requests over the month. According to the AWS calculator (https://calculator.aws/#/addService/Lambda), this'll run you $120/month, or $120*24 ~= $3k for 2 years.

But that doesn't count hosting for your static files with CloudFront, or does it count the RDS instance backing it, and we'd use AWS Cognito for user-auth since we've accepted AWS vendor lock-in. (Which isn't great, but that's the state of the industry.)

CloudFront: Free Tier 1TB, 10M requests/month. 10 TB/month will run you $1k/month https://calculator.aws/#/addService/CloudFront

RDS: This will vary greatly. A teeny tiny db.m6g.large instance w/ 2 CPUs and 8 GiB of RAM is going to run you $250/month, but a big one fat juicy db.r5d.24xlarge will run you closer to $20k/month. https://calculator.aws/#/addService/RDSMySQL

Cognito: With 1,000 active users, this'll be $50/month; 10,000 users is $500/mo, and 100,000 users is $5k/month.

Between Lambda, CloudFront, RDS, and Cognito you could easily blow past that $1,130/month estimate for a proper colo'd pair of servers, if your service gets at all popular. But if you stick within the free tier for Lambda and Cloudfront, then you're only looking at RDS and Cognito costs, which can vary greatly. Anywhere from $500/month to $26k/month, or more.

Except to get the same service in a colo as a $26k/month AWS bill, you'd need to spend way more and have much more than the single server in a rack that I started with. Thankfully, with something like Equinix Smart Hands, no one has to drive to the colo to futz with a server when it develops a bad hard drive.

Graph it out for your particular use case which one is better, but cloud infrastructure has the benefit of opex vs capex, as well as the opportunity cost of time. AWS Amplify will let you stand up a whole platform hacking on a Saturday before Dell can even quote you a price on a server or Equinix can answer the phone.

I also did reject a raspberry pi or old laptop server early on, but that's not to be underestimated. If I've already got some server running at home for my house, running a service on that, fronted by Cloudflare can take you quite far.

It depends on your use case. The big thing is that AWS/Cloud charges for egress, so if you're making a media distribution compnay, aka the Netflix model, you're better off building your own, but the cloud is actuallly cost competitive.

