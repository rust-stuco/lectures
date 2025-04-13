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

`rustup` is a _toolchain multiplexer_
* Installs and manages many Rust toolchains 
* Consolidates them as a single set of tools installed in `~/.cargo/bin`
* Analogous to Ruby's _rbenv_, Python's _pyenv_, or Node's _nvm_


---

# `rustup` Basic Usage

* To update Rust: `rustup update`
* To install a specific version: `rustup install __`
* To set default global version: `rustup default set ___`
* To override default for a specific project: `rustup override set ___`


---


# `rustup` Channels

* Rust has three different "channels" of releases
* **Stable** channel: releases made every six weeks
* **Beta** channel: the next stable release
* **Nightly** channel: releases made every night
    * Has experimental features and may fail to build

---


# `rustup` Channels

* Stable is the default channel used with `rustup` commands
* To use the beta channel...
    * Install: `rustup install beta`
    * Set default: `rustup default beta`
* To use the nightly channel...
    * Install: `rustup toolchain install nightly`
    * Set default: `rustup default nightly`


---


# Clippy

Clippy is a collection of lints that can catch common mistakes when writing Rust, improving the quality of your code.


---

# Clippy Lint Levels
Clippy offers many levels of lints, based on your needs
*  `clippy::all`: all lints that are on by default
    * `clippy::correctness`: code that is outright wrong or useless
    * `clippy::suspicious`: code that is most likely wrong or useless
    * `clippy::style`: code that should be written in a more idiomatic way
    * `clippy::complexity`: code that does something simple in a complex way
    * `clippy::perf`: code that can be written to run faster
* And more...
* You can even make your own lints!


---

# Clippy CLI Usage
* Likely already installed if using `rustup`
    * Otherwise: `rustup component add clippy [--toolchain=<name>]`
* Run all lints: `cargo clippy`
    * Run specific lint: `cargo clippy::__`
* Automatically apply suggestions: `cargo clippy --fix`


---


# Clippy Source Code Usage
You can also configure lint levels in your source code
```rust
#![allow(clippy::style)]

#[warn(clippy::box_default)]
fn main() {
    let _ = Box::<String>::new(Default::default());
    // ^ warning: `Box::new(_)` of default value
}
```


---



# `rustfmt`
`rustfmt` is a formatting tool that checks adhearance to formatting standards
* To install: `rustup component add rustfmt`
* To format one file: `rustfmt file.rs`
* To format whole project: `cargo fmt`
* To only *check* format: `cargo fmt -- --check`



---


# Configuring `rustfmt`


You can configure format options with a `rustfmt.toml` file
```
indent_style = "Block"
reorder_imports = false
```
* There are many configuration [options](https://rust-lang.github.io/rustfmt/?version=v1.8.0&search=) for `rustfmt`


---


# Consistent Formatting
* The default Rust style is defined in the Rust Style Guide
    * Recommended that developers use this style
* Consistent formatting makes code more readable
    * Also makes it easier to collaborate with others


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

Write parallel code as easily as sequential code

---


# `rayon`: The Problem

Your sequential code:

```rust
let data = (1..1_000_000).collect::<Vec<i32>>();
let sum: i32 = data.iter().sum();
```

* Say we want to parallelize this
    * "Divide the vector into eight regions, spawn eight threads, give each thread a region, and combine their results..."


---


# `rayon`: The Problem

Question: do we really want to type all of this?

```rust
// ... some logic to divide the vector ...
let handle1 = thread::spawn(|| { /* work */ });
...
let handle8 = thread::spawn(|| { /* work */ });
handle1.join().unwrap();
...
handle8.join().unwrap();
// ... then we have to combine results...
```

* "Gee, `data.iter().sum()` was so clean!"
    * "If only we could type the equivalent of `data.iter().sum()`, and it'd be parallelized for us..."
    * We can!

---

# `rayon`: The Solution

Add `rayon`:

```toml
[dependencies]
rayon = "1.10"
```

---


# `rayon`: The Solution

Then change `iter().sum()`...

```rust
let data = (1..1_000_000).collect::<Vec<i32>>();
let sum: i32 = data.iter().sum();
```

---


# `rayon`: The Solution

...to `par_iter().sum()`!

```rust
let data = (1..1_000_000).collect::<Vec<i32>>();
let sum: i32 = data.par_iter().sum(); // done!
```

* No threading needed
* Automatically parallelized


---


# `rayon`: Chained Operations

Recall that we can chain operations for iterators:

```rust
let result = numbers.iter()
    .filter(|&&x| x % 2 == 0)
    .map(|x| x * x)
    .collect();
```

* We can parallelize these operations as well!

---


# `rayon`: Chained Operations

When we use `par_iter()`, subsequent operations are automatically parallelized:

```rust
let result = numbers.par_iter()
    .filter(|&&x| x % 2 == 0)
    .map(|x| x * x)
    .collect();
```

* `filter`, `map`, and `collect` are now parallelized via Rayon's implementation
* Yet it still reads like sequential code!


---


# `rayon`: Parallelized Sort

Need to sort a massive collection?

```rust
let mut data = (1..1_000_000).collect::<Vec<i32>>();
data.sort();
```

---


# `rayon`: Parallelized Sort

`rayon` to the rescue:

```rust
let mut data = (1..1_000_000).collect::<Vec<i32>>();
data.par_sort();
```

* Just change `sort()` to `par_sort()`


---

# How `rayon` Works

* Suspiciously simple
    * All we have to do is add `par_`?
* How does Rayon work its magic?

---


# How `rayon` Works: Thread Pool Basics

Rayon creates a global thread pool:
* One pool per program, initialized on first use
* Number of threads matches your CPU cores (e.g., 8)
* Threads are ready, waiting for work


---


# How `rayon` Works: Splitting the Work

When you call `par_iter()`:
* Data (e.g., vector of `numbers`) is split into chunks
* Each thread grabs a chunk to process (e.g., filter, map)
* No manual division needed!


---


# How `rayon` Works: Work-Stealing

Threads don’t sit idle:
* If a thread finishes early, it _steals_ work from others
    * Balances load dynamically


---


# `rayon`: Key Idea

Rayon creates the illusion that you are writing sequential code
* Divides the labor and monitors utilization rates so you don't have to
* _Dynamically_ manages the load balancing for high efficiency


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
