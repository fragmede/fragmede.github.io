---
layout: post
title: "Are Compilers Deterministic?"
date: 2026-02-21 16:02:21 PST
categories: 
---

Betteridge says "no," and for normal developer experience that answer is mostly right. (Also, you’re absolutely right! and here’s an em—dash so that you know that I used ChatGPT to help me write this.)

Here’s my take. There's a computer science answer and an engineering answer. The computer science answer: a compiler is deterministic as a function of its full input state. Engineering answer: most real builds do not control the full input state, so outputs drift.

I worked at Ksplice back in the 2000s, where we patched running Linux kernels in RAM so you could take security updates without rebooting. Reading `objdump` output of crashy kernels was not daily routine, but I had to do it often enough that "compiler output versus source intent" stopped being theoretical.

Formally:

```
artifact = F(
  source,
  flags,
  compiler binary,
  linker + assembler,
  libc + runtime,
  env vars,
  filesystem view,
  locale + timezone,
  clock,
  kernel behavior,
  hardware/concurrency schedule
)
```

Most teams hold only `source` and maybe `flags` constant, then call everything else "noise." That "noise" is where non-reproducibility lives.

I learned this hard at Ksplice in the 2000s. We generated rebootless Linux kernel updates by diffing old vs new compiled output and stitching hot patches into live kernel memory. Most diffs mapped cleanly to changed C. Sometimes they exploded for reasons that were not semantic source changes: register allocation differences, altered pass behavior, section/layout changes. Same intent, different machine code.

If you want a concrete historical artifact, GCC bug 18574 has a [gcc-bugs thread](https://gcc.gnu.org/pipermail/gcc-bugs/2004-November/139548.html) calling out pointer-hash instability affecting traversal order and [SSA coalescing](https://gcc.gnu.org/wiki/SSA%20Pressure%20Reduction).

That distinction matters:

- deterministic compiler: same complete input tuple -> same output
- reproducible build: two independent builders recreate bit-identical output
- reliable toolchain: differences rarely matter functionally

Related concepts, not equivalent guarantees.

## Where Entropy Comes From

- `__DATE__`, `__TIME__`, `__TIMESTAMP__`
- embedded absolute paths in DWARF/debug info
- build path leakage (for example `/home/fragmede/projects/foo`)
- locale-sensitive sort behavior (`LC_ALL`)
- filesystem iteration order
- parallel build and link race ordering
- archive member order and metadata (`ar`, `ranlib`)
- build IDs, UUIDs, random seeds
- network fetches during build
- toolchain version skew
- host kernel/c library differences
- historical compiler internals depending on unstable pointer/hash traversal order

ASLR note: ASLR does not directly randomize the emitted binary. It randomizes process memory layout. But if a compiler pass behavior depends on pointer identity/order, ASLR can indirectly perturb outcomes.

So "compilers are deterministic" is often true in a theorem sense and false in an operational sense.
And even with reproducible artifacts, Ken Thompson's [Reflections on Trusting Trust](https://aeb.win.tue.nl/linux/hh/thompson/trust.html) still applies.

## Reproducible Builds: Deliberate Engineering

Debian and the broader reproducible-builds effort (around 2013 onward) pushed this mainstream: same source + same build instructions should produce bit-for-bit identical artifacts.

The practical playbook:

- freeze toolchains and dependencies
- stable environment (`TZ=UTC`, `LC_ALL=C`)
- set `SOURCE_DATE_EPOCH`
- normalize/strip volatile metadata
- canonicalize path prefixes (`-ffile-prefix-map`, `-fdebug-prefix-map`)
- deterministic archives (`ar -D`)
- remove network from the build graph
- build in hermetic containers/sandboxes
- continuously diff artifacts across builders in CI

That gets you:

- Repeatable
- Reproducible
- Verifiable
- Hermetic
- Deterministic

Do we have this now? In many ecosystems, mostly yes. But it took years of very intentional work across compilers, linkers, packaging, and build systems.
We got here by grinding through weird edge cases, not by waving our hands and declaring purity.

## Why This Matters For LLMs

This comes up now as "is vibecoding sane if LLMs are nondeterministic?"
Again: do you want the CS answer, or the engineering answer?

We have, and have not, solved the halting problem with LLMs.
We have not remotely solved the halting problem in the formal sense
But for practical purposes, if I write a `for`loop and mess up the condition, an LLM can look at my code, tell me I'm being dumb, and then it can go fix it for me.

Engineering has never depended on perfectly deterministic intelligence. It depends on controlled interfaces, test oracles, reproducible pipelines, and observability.
I'm AI-pilled enough to daily-drive [comma.ai](https://comma.ai), and I still want deterministic verification gates around generated code.
My girlfriend prefers when I let it drive because it's smoother and less erratic than I am, which is a useful reminder that "probabilistic system" and "operationally better result" can coexist.

Same pattern for LLM-assisted coding:

- constrain inputs
- make outputs testable
- gate with deterministic CI
- require reproducible artifacts
- treat stochastic generation as upstream, not deploy-time truth

Computer science answer: nondeterminism is scary.
Engineering answer: control boundary conditions, verify outputs, ship.

And yes, part of this argument is existential: most of us are still in the rent-paying business, not the philosophy business. So we use the tools that move work forward, then build the guardrails we need.
