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

- The Rust Toolchain: `rustup`, `clippy`, `rustfmt`
- Performance and Analysis: `criterion`, `flamegraph`
- Reading Documentation
    - `clap`
    - `rand`
    - `time` vs `chrono`
    - `anyhow` vs `thiserror`
- Libraries / Frameworks
    - `rayon`
    - `serde`


---


# **The Rust Toolchain**


---


# The Rust Toolchain

* A toolchain is defined as a set of software tools used to build and develop software within a specific ecosystem
* Rust has several toolchains, which you manage via `rustup`


---


# **`rustup`**


---


# `rustup`

`rustup` is a _toolchain multiplexer_.

* A _toolchain_ is a complete installation of the Rust compiler (rustc) and related tools (like `cargo`)
    * Defined by release channel / version, and the host platform triple
        * `stable-x86_64-pc-windows-msvc`, `beta-aarch64-unknown-linux-gnu`
* `rustup` consolidates them as a single set of tools installed in `~/.cargo/bin`
* Similar to Ruby's `rbenv`, Python's `pyenv`, or Node's `nvm`


---


# `rustup` Channels

* There are 3 different channels
    * Stable: `rustc` and `cargo` release every 6 weeks
    * Beta: the next stable release
    * Nightly: release made every night, based on the `master` branch


---



# Stability without Stagnation

* Rust cares _a lot_ about the stability of your code
* At the same time, we all want to experiment with new features
* You should _never_ need to worry about breaking your code after updating Rust
* But you should also be able to opt-in to newer "unstable" features!

<!--
https://doc.rust-lang.org/book/appendix-07-nightly-rust.html
-->


---


# The Rust Train

Here is a high-level diagram of Rust's release cycle.

```
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

* This is called the “train model”
* Every six weeks, a release “leaves the station”
* Still has to take a journey through the beta channel before it arrives as a stable release


---


# Unstable Features

We can use features under development by enabling _unstable features_.

* You can only use unstable features on nightly
* Allows you to access cool new things in Rust
    * Example: [`downgrade` on `RwLock`](https://doc.rust-lang.org/std/sync/struct.RwLockWriteGuard.html#method.downgrade) with `#![feature(rwlock_downgrade)]`

<!--
Connor's PR to Rust :D https://github.com/rust-lang/rust/pull/128219
-->


---


# `rustup` Usage

Here are some basic `rustup` commands to remember:

* `rustup update`
    * Updates your Rust toolchains to the latest versions
* `rustup default set <stable/beta/nightly>`
    * Sets the default rust toolchain
* `rustup override set <stable/beta/nightly>`
    * Overrides the toolchain for the specific directory


---


# **Clippy**


---


# Clippy

Clippy is a collection of lints that can catch common mistakes when writing Rust, improving the quality of your code.


---

# Clippy Lint Levels

Clippy offers many different lint levels.

*  `clippy::all`: all lints that are on by default
    * `clippy::correctness`: code that is outright wrong or useless
    * `clippy::suspicious`: code that is most likely wrong or useless
    * `clippy::style`: code that should be written in a more idiomatic way
    * `clippy::complexity`: code that does something simple in a complex way
    * `clippy::perf`: code that can be written to run faster
* And more...
* You can even make your own lints!


---

# `clippy` Usage

* Already installed if using `rustup` (default profile)
* To run all lints, run `cargo clippy`
    * To run a specific lint, run `cargo clippy::___`
* To automatically apply suggestions, run `cargo clippy --fix`
* To run lints on tests and other files, run `cargo clippy --all-targets`


---


# Clippy Source Code Usage

You can also configure lint levels directly in your source code.

```rust
fn main() {
    #[allow(unused_variables)]
    let not_used = 42;

    println!("Hello, World!");
}
```

<!--
This is a very basic example, look online for more information!
-->


---


# **`rustfmt`**


---


# `rustfmt`

`rustfmt` is a formatting tool that checks adherence to Rust's strict formatting standards.

* Already installed if using `rustup` (default profile)
* To format one file: `rustfmt file.rs`
* To format whole project: `cargo fmt`
* To only *check* format: `cargo fmt -- --check`

<!--
It's pretty rare that you would use `rustfmt` by itself, usually you are running `cargo fmt` for everything.
-->


---


# Configuring `rustfmt`

You can configure format options with a `rustfmt.toml` file

```
indent_style = "Block"
reorder_imports = false
```

* There are many configuration [options](https://rust-lang.github.io/rustfmt/?version=v1.8.0&search=) for `rustfmt`
* **You probably shouldn't create your own formatting style**


---


# Consistent Formatting

* The default Rust style is defined in the [Rust Style Guide](https://doc.rust-lang.org/style-guide/index.html)
    * It is **strongly recommended** that developers use this style
* Consistent formatting makes code more readable
    * Also makes it easier to collaborate with others

<!--
This is a subtle thing, but when jumping into an unknown codebase, having consistent formatting of code across every single Rust repository lowers the barrier to entry (much more than you probably think).

This is one of the reasons it is much easier to start contributing to a code base over something like a C or C++ codebase. When jumping into a C or C++ codebase, a significant fraction of the time there will be custom macros and/or templates that you have to learn before you can even understand the code. TLDR you are basically learning a new language every time you jump into a C/C++ codebase.
-->


---


# **Performance and Analysis**


---


# Performance Profiling

Suppose we want to see how fast or slow our code runs.

```rust
pub fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n-1) + fibonacci(n-2),
    }
}
```

* How do we test/profile the _performance_ of our code?


---


# Performance Profiling: Timer

A simple solution is to just use a timer!

```rust
use std::time::Instant;
use std::hint::black_box;

fn main() {
    let start_time = Instant::now();

    let _ = black_box(fibonacci(30));

    let elapsed = start_time.elapsed();
    println!("Elapsed: {:.2?}", elapsed);
}
```

```
Elapsed: 14.00ms
```


---


# Problem: Statistical Significance

When we run this code multiple times, we could get different results...

```
Elapsed: 14.30ms
Elapsed: 11.59ms
Elapsed: 8.48ms
Elapsed: 10.35ms
Elapsed: 20.95ms
```

* How do we control our environment?
    * Compiler optimizations can skew results, the OS scheduler and other noise can create performance variations
    * Seeing a number go up/down is one thing, whether it's statistically significant is another

<!--
This is an overexaggeration, we ran other things at the same time on the same computer to make these
numbers vary wildly.
-->


---


# **Criterion**


---


# Criterion

Criterion is a statistics-driven micro-benchmarking library written in Rust.

* Collects detailed statistics, providing strong confidence that changes to performance are real, not measurement noise
* Produces detailed charts, providing thorough understanding of your code’s performance behavior
* Make sure to read the (very well-written) [library docs](https://docs.rs/criterion/latest/criterion/) and [user guide](https://bheisler.github.io/criterion.rs/book/index.html)!


---


# `criterion`

Add `criterion` as a development dependency:

```toml
[dev-dependencies]
criterion = "0.5.1"

[[bench]]
name = "my_benchmark"
harness = false
```

* `name = "my_benchmark"` declares that there is a benchmark file located at `benches/my_benchmark.rs`


<!--
Don't worry too much about the `harness = false`.
-->


---


# Example: Simple `criterion` Benchmark

Create a benchmark file at `$PROJECT/benches/my_benchmark.rs`:

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use my_crate::fibonacci;
```

* Import `criterion` items
* Import the function we want to bench (in this case, `my_crate::fibonacci`)

<!--
Note we import the crate because we consider our crate an external crate when writing things like benchmarks and integration tests we're benchmarking as an external crate.
This is because Cargo compiles each benchmark under `/benches` as if each was a separate crate from the main crate
-->

---


# Example: Simple `criterion` Benchmark

Next, create a benchmark using the `Criterion` object:

```rust
pub fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
```

* The `criterion_group!` macro generates a benchmark group called `benches`, containing the `criterion_benchmark` function defined earlier
* The `criterion_main!` macro generates a `main` function which executes the `benches` group


---


# Example: Simple `criterion` Benchmark

```rust
pub fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}
```

* We define benchmark with `bench_function`, which takes two arguments:
    * Name of the benchmark, `"fib 20"`
    * A closure that gets run for that benchmark
* `black_box` stops the compiler from optimizing away our whole function
    * Otherwise, the compiler may replace `fibonacci(20)` with a constant


---


# `criterion`

Run the benchmark with `cargo bench`:

```
$ cargo bench

Benchmarking fib 20: Warming up for 3.0000 s
Benchmarking fib 20: Collecting 100 samples in estimated 5.0329 s (475k iterations)
Benchmarking fib 20: Analyzing

fib 20                  time:   [10.404 µs 10.413 µs 10.422 µs]
Found 10 outliers among 100 measurements (10.00%)
  10 (10.00%) high mild
```

<!--
Some details omitted.
-->


---


# Fibonacci Improvements

Our Fibonacci could definitely be improved...

```rust
pub fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n-1) + fibonacci(n-2),
    }
}
```

* What's the complexity of the algorithm?
    * Exponential!


---


# Fibonacci Improvements

Let's write a second version for comparison:

```rust
pub fn fibonacci(n: usize) -> usize {
    fn fib_helper(from: (usize, usize), n: usize) -> usize {
        if n == 0 {
            from.0
        } else {
            fib_helper((from.1, from.0 + from.1), n - 1)
        }
    }
    fib_helper((0, 1), n)
}
```


---


# Fibonacci Improvements

Upon rerunning `cargo bench`, `criterion` compares it with our previous run:

```
$ cargo bench

Benchmarking fib 20: Warming up for 3.0000 s
Benchmarking fib 20: Collecting 100 samples in estimated 5.0000 s (2.2B iterations)
Benchmarking fib 20: Analyzing

fib 20                  time:   [2.2469 ns 2.2633 ns 2.2841 ns]
                        change: [-99.978% -99.978% -99.978%] (p = 0.00 < 0.05)
                        Performance has improved.
```

* `change: [-99.978% -99.978% -99.978%] (p = 0.00 < 0.05)`
    * This is a statistically significant improvement!


---


# **Flamegraphs**


---


# Flamegraphs

Suppose you want to know _where_ your program is spending time.

* We want to know which functions take the most time
* We could add timers for every single function call
    * Manually adding timers is error-prone, misses deeper call stacks
* That's why we have `flamegraph`s!


---


# Example: Concatenating Strings

Suppose we have the following function, and we want to know where most of the time is spent:

```rust
fn build_string(n: usize) -> String {
    let mut s = String::new();
    for i in 0..n {
        s += &format!("{}", i);
    }
    s
}

build_string(5); // produces "01234"
build_string(15); // produces "01234567891011121314"
```


---


# Flamegraph

We can generate flamegraphs for our code with `cargo flamegraph`:

![](../images/week13/flamegraph-format.svg)


---


# Flamegraph Analysis


![](../images/week13/flamegraph-format.svg)

* Flamegraphs are generated by _sampling_ the call stack many times
* Flamgegraphs display the call stack from bottom to top
    * Width of block is the relative time spent in that function


---


# Flamegraph Usage

It's more informative to have a side-by-side comparison:

```rust
fn build_string_format(n: usize) -> String {
    let mut s = String::new();
    for i in 0..n {
        s += &format!("{}", i);
    }
    s
}

fn build_string_pushstr(n: usize) -> String {
    let mut s = String::with_capacity(n * 2);
    for i in 0..n {
        s.push_str(&i.to_string());
    }
    s
}
```


---


# Flamegraph

Here is the flamegraph for `build_string_format`:

![](../images/week13/flamegraph-format.svg)


<!--
Note that these were generated with `cargo flamegraph --skip-after my_crate::main --min-width 5`.
This basically chops off a bunch of stuff below `main` and tidies up the graph.
Also, the function was called 1000000 times to get better readings. If you only run it once, it is
likely that the sampling doesn't get enough information.
-->


---


# Flamegraph

And here is the flamegraph for `build_string_pushstr`:

![](../images/week13/flamegraph-pushstr.svg)


<!--
KEY OBSERVATIONS:
- format! approach has wider + more blocks dedicated to memory allocation and string formatting operations
    `alloc::raw_vec::RawVecInner`, `alloc::string::String`, `core::fmt`
    - markedly taller call chain than push_str, more time spent in overhead functions than main algorithm
- push_str shows fewer allocations and less time spent in string manipulation operations
    - narrower sections for memory operations because pre-allocation
        reduces the number of reallocations needed
    - more time in the main algorithm, as opposed to overhead functions
-->


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

Usually, you use `rustdoc` via `cargo doc`. Here are some useful commands:

* `cargo doc --open`: Generates docs and opens it in a browser
* `cargo doc --document-private-items`: Generates documentation for private items like modules and functions
* `cargo doc --no-deps`: Does not generate docs for any dependencies
* `cargo doc --test`: Runs documentation tests



---


# Rust Documentation

All Rust library documentation has the same structure!

* By making documentation consistent, it shortens the time needed to get familiar with a library
    * This is more important than it might seem
* Because Rust has _excellent_ first-party tooling for generating documentation, Rust library writers tend to invest in writing _excellent_ documentation, guides, and tutorials


---


# **`rand`**


---


# `rand`

Let's look at an example of a popular third-party crate, `rand`.

* Rust does not have a random module in the standard library (unlike Python)
* Instead, the de-facto crate for dealing with randomness in Rust is `rand`!
* Use `rand` for:
  * Generating / sampling random numbers
  * Creating probability distributions
  * Providing random algorithms (like vector shuffling)

<!--
Why do we not have a random module in the standard library?

https://www.reddit.com/r/rust/comments/rgueuz/why/

Also, if you scroll down the comments, you'll find an example of randomness using the random state from the HashMap collection
-->


---


# `rand`?

* How do we use `rand`?
* We should really be asking "how do we learn how to use `rand`"?
* Google is our friend!
    * Search "Rust rand"

<!--
Maybe google isn't actually your friend, but you get the point. Choose whatever search engine you would like!
-->


---


# Docs.rs

![bg right:50% 100%](../images/week13/google-rand.png)

* Docs.rs has documentation for essentially every third-party Rust library
* When publishing your own crate, the documentation gets pushed to Docs.rs


---


![bg 75%](../images/week13/rand-docs.png)


---


# Anatomy of `rustdoc`

![bg right:50% 95%](../images/week13/hints.png)

* Navigation Bar (on the left)
* Search Bar (at the top)
    * Press "s" to search
* Settings (at the top right)
* Help menu (at the top right)
    * Press "?" for pop-up
    * Lots of cool tricks!


---


# `rand`: Quick Start

```rust
// The prelude import enables methods we use below...
use rand::prelude::*;

// Get an RNG:
let mut rng = rand::rng();

println!("char: '{}'", rng.random::<char>());
println!("alpha: '{}'", rng.sample(rand::distr::Alphanumeric) as char);

// Generate and shuffle a sequence:
let mut nums: Vec<i32> = (1..100).collect();
nums.shuffle(&mut rng);
// And take a random pick (yes, we didn't need to shuffle first!):
let _ = nums.choose(&mut rng);
```

<!--
Some comments omitted.
Source: https://docs.rs/rand/latest/rand/
 -->


---


# The Rust Rand Book

If we click on the link under the Quick Start, we are taken to [The Rust Rand Book](https://rust-random.github.io/book/).

![](../images/week13/rand-book.png)


---


# Aside: mdBook

* **mdBook** is a command line tool to create books with Markdown
* Used to make the official Rust Book
* Commonly used to make higher-level tutorials
    * Rust documentation structure can't cover everything


---


# The Rust Rand Book

The Rust Rand Book covers the higher-level concepts that might not be easily understandable in the `rustdoc` format.

- Core concepts of randomness
- Kinds of RNGs
- Seeding strategies
- Cryptographic vs non-cryptographic randomness
- Performance considerations
- Understanding the design and architecture of `rand`


---


# `rand` Lower-level Documentation

If we want to know the lower-level specific details about `rand`, then we need to read through the actual documentation.

* Specific RNG implementations and their guarantees
    - `ThreadRng`, `StdRng`, `SmallRng`, etc.
    - Security properties
    - Performance characteristics
* Detailed distribution implementations
    - `Uniform`, `Bernoulli`, `Alphanumeric`
    - Parameter configurations / constructors
    - Sampling methods


---


# Normal Distribution?

`rand` provides some basic probability distributions for us.

* `Uniform`, `Bernoulli`, `Alphanumeric`
* Where are the others?
* What about a Normal / Gaussian distribution?


---


# Google is your friend!


TODO image of google search

<!--
Again, you are free to use whatever search engine you prefer.
-->


---


# `rand_distr` crate

```rust
use rand::prelude::*;
use rand_distr::StandardNormal;

let val: f64 = rand::rng().sample(StandardNormal);
println!("{}", val);
```

- See how 3rd-party crates complement each other! Anyone can make their own `Distribution` if it implements that trait from rand

---

# LLMs: good and bad for writing Rust code

- Good because Rust has many guardrails for writing code (if it compiles, it is probably correct)
- Bad because the type of problems Rust is trying to solve are usually very complex systems code
  - LLMs fall over
- But generally quite good at filling in patterns

---


# **Rust Time**

* Time for Rust!


---


# Time?

How do we keep time in Rust?

* `std::time`
* `time`
* `chrono`

---

# How do you choose which `time` to use?

- `std::time`: Simple timing and benchmarking (built-in)
- `time`: Modern, safe date/time operations
- `chrono`: Full-featured with timezone support (legacy)

---

# Google is your friend!

---

# Answer: it depends, and you should go read through the documentation of each to figure out which is the best for you

- `std::time`: https://doc.rust-lang.org/std/time
- `time`: https://docs.rs/time/latest/time/
- `chrono`: https://docs.rs/chrono/latest/chrono/


<!-- Look up the documentation of each of these crates -->

---

# Error Handling

- `anyhow`
- `thiserror`
- `snafu`

---

# How to choose between the 3 error handling libraries?

- `anyhow`: "I don't want to care about error types"

- `thiserror`: "I want to easily define errors for my library"

- `snafu`: "I want BOTH!"

---

# `anyhow`: Type erasure

- Remember how painful it was to define a proper error type?

```rust
use anyhow::Result;

fn get_cluster_info() -> Result<ClusterMap> {
    let config = std::fs::read_to_string("cluster.json")?;
    let map: ClusterMap = serde_json::from_str(&config)?;
    Ok(map)
}
```

---

# `anyhow`: Attach context

- `with_context` is a macro that attaches a context to the error

```rust
use anyhow::{Context, Result};

fn main() -> Result<()> {
    let content = std::fs::read(path)
        .with_context(|| format!("Failed to read instrs from {}", path))?;
}
```

```text
Error: Failed to read instrs from ./path/to/instrs.json
Caused by:
    No such file or directory (os error 2)
```

---

# Summary

- `anyhow` is good for type erasure in binaries
- `anyhow` is also good for attaching context to errors

---


# `thiserror`: Define errors for your library

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DataStoreError {
    #[error("data store disconnected")]
    Disconnect(#[from] io::Error),
    #[error("the data for key `{0}` is not available")]
    Redaction(String),
    #[error("invalid header (expected {expected:?}, found {found:?})")]
    InvalidHeader {
        expected: String,
        found: String,
    },
    #[error("unknown data store error")]
    Unknown,
}
```

---


# Summary: `thiserror` is good for libraries with many kinds of errors


---


# `snafu` is like a combo of both

* (Google it if you want to know more)

<!-- don't go through docs -->


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

Threads don't sit idle:
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


`serde`


---


`