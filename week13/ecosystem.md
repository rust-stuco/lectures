---
marp: true
paginate: true
theme: rust
class: invert
---


<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Mono:wght@100..900&family=Noto+Sans:ital,wght@0,100..900;1,100..900&display=swap');
section {
    font-family: "Noto Sans";
}
code {
    font-family: "Noto Sans Mono";
}
</style>

<!-- _class: communism invert  -->

## Intro to Rust Lang

# The Rust Ecosystem


---


# Today: The Rust Ecosystem

TODO


---


# **The Rust Toolchain**


---


# The Rust Toolchain

* A toolchain is defined as a set of software tools used to build and develop software within a specific ecosystem
* Rust has several toolchains, which you manage via `rustup`


---


# `rustup`

`rustup` is a _toolchain multiplexer_.

TODO: https://rust-lang.github.io/rustup/concepts/index.html


---


`rustup`

Talk about stable channel


---


`rustup`

Talk about beta and nightly


---


`rustup`

Talk about basic usage of `rustup`

- `rustup update`
- `rustup default set ___`
- `rustup override set ___`


---


# Clippy

Clippy is a collection of lints that can catch common mistakes when writing Rust, improving the quality of your code.

TODO: https://doc.rust-lang.org/clippy/


---


Clippy


---


Clippy


---


Clippy


---


# `rustfmt`

Talk about `cargo fmt` options?

TODO: https://rust-lang.github.io/rustfmt/?version=v1.8.0&search=


---


Talk briefly about how consistent formatting across all Rust projects is super important


---


# Criterion?

Maybe talk about criterion before talking about flamegraphs

TODO: https://bheisler.github.io/criterion.rs/book/


---


Criterion

Basic Usage code


---


Criterion

More basic usage code


---


Criterion

Basic usage CLI


---


# Flamegraphs

Explain what a flamgraph is


---


High-quality high-resolution image of a flamegraph (is it possible to use the same svg?)


---


Flamegraph

Things you can do with it (how to go about optimizing code?)


---


Flamegraph


---


Flamegraph


---


Flamegraph


---


Padding


---


Padding


---


Padding



---


Padding


---


Padding


---


# **Reading Rust Documentation**


---


# Reading Rust Documentation

Reading the documentation of third-party libraries is super important!

* When we are unfamiliar with a tool, the first thing we need to do is read through documentation
* Rust's `rustdoc` tool provides a way for developers to write documentation consistently between packages
    * _All of our homework writeups were generated with `rustdoc`!_


---


# `rustdoc`

TODO cleanup slide

Useful `cargo doc` commands
- `cargo doc --open`
- `cargo doc --document-private-items`
- `cargo doc --no-deps`
- `cargo doc --test`


---


# `mdbook`

Mention mdbook as a popular alternative to just generating rust docs.


---


# `clap`

Show screenshot of clap crate-level docs

https://docs.rs/clap/latest/clap/


---

Show screenshot of the Example


---


# `clap` Example

```rust
use clap::Parser;

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    /// Name of the person to greet
    #[arg(short, long)]
    name: String,

    /// Number of times to greet
    #[arg(short, long, default_value_t = 1)]
    count: u8,
}
```

<!--
This example is split across two slides
-->


---


# `clap` Example

```rust
fn main() {
    let args = Args::parse();

    for _ in 0..args.count {
        println!("Hello {}!", args.name);
    }
}
```


---


# `clap` Example

```rust
$ demo --help
A simple to use, efficient, and full-featured Command Line Argument Parser

Usage: demo[EXE] [OPTIONS] --name <NAME>

Options:
  -n, --name <NAME>    Name of the person to greet
  -c, --count <COUNT>  Number of times to greet [default: 1]
  -h, --help           Print help
  -V, --version        Print version

$ demo --name Me
Hello Me!
```


---


Derive tutorial: https://docs.rs/clap/latest/clap/_derive/_tutorial/index.html


---


# `rand`

* Rust does not* have a random module in the standard library
* Instead, the de-facto crate for dealing with randomness in Rust is `rand`!
* Use `rand` for
    * Generating / sampling random numbers
    * Creating probability distributions
    * Providing random algorithms (like vector shuffling)

<!--
Why do we not have a random module in the standard library?

https://www.reddit.com/r/rust/comments/rgueuz/why/

Also, if you scroll down the comments, you'll find an example of randomness using the random state from the HashMap collection
-->


---


`rand` Example


---


Do a google search and find "The Rust Rand Book" (mbdook)

https://rust-random.github.io/book/intro.html


---


The mdbook is a high-level tutorial


---


Have to actual go to the rand docs for more specific things


---


How do you create a normal probability distribution? Google is your friend!


---


rand_distr crate


---


Maybe a note about LLMs? Both good and bad for writing Rust code

- Good because Rust has many guardrails for writing code (if it compiles, it is probably correct)
- Bad because the type of problems Rust is trying to solve are usually very complex systems code
    - LLMs fall over
- But generally quite good at filling in patterns


---


# Time?

How do we keep time in Rust?

- std::time
- time
- chrono


---


How do you choose which `time` to use?


---


Google is your friend!


---


Answer: it depends, and you should go read through the documentation of each to figure out which is the best for you


---


# Error Handling

* `anyhow`
* `thiserror`
* `snafu`


---


How do you choose between the 3 error handling libraries?


---


Briefly go through docs of anyhow


---


Summary: anyhow is good for type erasure in binaries


---


Briefly go through docs of thiserror


---


Summary: thiserror is good for libraries with many kinds of errors


---


Aside about snafu and how it is like a combo of both (don't go through docs)


---


# Other Useful Crates

TBD slide for each of these?

* `derive_more`
* `regex`
* `itertools`


---


Padding


---


Padding


---


Padding


---


Padding


---


Padding


---


Padding


---


Padding


---


# **Libraries and Frameworks**


---


# Libraries and Frameworks

Libraries can come in all different shapes and sizes, but there are several libraries that are so integral to the Rust that they are basically their own sub-ecosystems.

- **`rayon`**
- **`serde`**
- `tokio`
- `reqwest`
- `tracing`

<!--
Listed in no particular order. Well also only talk about the first 2
-->


---


# `rayon`


---


`rayon`


---


`rayon`


---


`rayon`


---


`rayon`


---


`rayon`


---


`rayon`


---


`rayon`


---


# `serde`


---


`serde`


---


`serde`


---


`serde`


---


`serde`


---


`serde`


---


`serde`


---


`serde`


---


`serde`


---


`serde`


---


# Next Lecture: Concurrency

![bg right:30% 80%](../images/ferris_happy.svg)

Thanks for coming!

<br>

_Slides created by:_
Connor Tsui, Benjamin Owad, David Rudo,
Jessica Ruan, Fiona Fisher, Terrance Chen
