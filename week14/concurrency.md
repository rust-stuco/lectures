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

# Concurrency: Async/Await


---


# Recap: Parallelism vs. Concurrency

<div class="columns">
<div>

## Parallelism

- Do work on multiple tasks at the same time (in parallel)
- Utilize multiple processors

</div>
<div>

## Concurrency

- Manage multiple tasks, but only do one thing at a time
- Better utilizes a single processor

</div>
</div>

<br>
<br>

<center>

These terms tend to be used (_and abused_) interchangeably

</center>


---


![bg 100%](../images/week12/conc-vs-par.jpg)


---


# Concurrency

Today, we'll be talking about concurrency in Rust.

* When we say something is **asynchronous**, we generally also mean it is **concurrent**
* Rust approaches concurrency differently than other languages
* Rust provides keywords `async` and `.await` to help write asynchronous code


---


# Concurrency is Complicated

* Asynchronous execution in _any_ language is complicated
* Asynchronicity and parallelism are not mutually exclusive
    * This makes reasoning about concurrency **even harder**!
    * _You can have both in Rust, and we'll see an example of this_


---


# Rust's Concurrency is Even More Complicated!

Due to the high complexity of Rust's rules and features, `async` is _even harder_ to use in Rust compared to other languages.

* Asynchronous execution is still evolving both as a feature in Rust and as a programming paradigm in general
* The Rust team has [prioritized](https://blog.rust-lang.org/2025/04/08/Project-Goals-2025-March-Update/) bringing the Async Rust experience closer to parity with synchronous Rust
    * _Lots of exciting work incoming soon!_


---


# Today

* It would be quite challenging to teach you what you need to know about `async`/`.await` in Rust in one lecture
* Instead, we will use `tokio` as a practical medium to learn how to use `async`
* There are **many** online resources dedicated to Async Rust (_see website_)
* We will give a sneak peek of `async`, and hopefully in the future you will be able to teach yourself how to use it!

<!--
The rust book has a new chapter about async and await and it is quite well writte:
https://doc.rust-lang.org/book/ch17-00-async-await.html

This should probably be the first thing you read if you want to learn more about this.

Then there is the tokio tutorial that this lecture is based on: https://tokio.rs/tokio/tutorial

And then there is Jon Gjengset's livestream on async/await: https://www.youtube.com/watch?v=ThjvMReOXYM

There's a lot more still if you want more! Reach out to us for more recommendations.
-->


---


# **Tokio**


---


# What is Tokio?

What is Tokio?

> Tokio is an asynchronous runtime for the Rust programming language. It provides the building blocks needed for writing network applications. It gives the flexibility to target a wide range of systems, from large servers with dozens of cores to small embedded devices.

<!--
Taken directly from https://tokio.rs/
-->


---


# What is Tokio?

At a high level, Tokio provides a few major components:

* A **multi-threaded runtime** for **executing** asynchronous code
* An **asynchronous** version of the standard library
* A **large ecosystem** of libraries

<!--
Taken directly from https://tokio.rs/tokio/tutorial

Bolded words are interesting words that people _shouldn't_ understand yet.

A lot of words to break down! Hopefully by the end of this lecture everyone will understand what each of the words mean.
-->


---


# Why do we need Tokio?

* Making your program asynchronous allows it to scale much better
    * Reduces the cost of doing many things at the same time
* However, asynchronous Rust code does not run on its own
    * You must choose a runtime to execute it
* The Tokio library is the most widely used runtime

<!--
Remember that the definition of concurrency is literally "doing many things at the same time"

"most widely used" might be a bit of an understatement, it surpasses all other runtimes in usage combined
-->


---


# Tokio and the Rust Ecosystem

Tokio is arguably one of the most important libraries in the Rust ecosystem.

* Many _major_ Rust libraries built on top of Tokio
* There are large companies relying on Tokio in production

<!--
See https://github.com/tokio-rs for all crates under the Tokio umbrella

Many major libraries on top of it, MUCH more minor/smaller libraries as well!

See the landing page on https://tokio.rs/ for some of the companies who use Tokio (includes AWS, Azure, Facebook, Discord)
-->


---


# When not to use Tokio

Tokio is useful for many projects, but there are some cases where this isn't true.

* Tokio is designed for IO-bound applications, not CPU-bound
* Reading many files is the same as a synchronous thread pool
    * Operating systems do not provide [stable](https://unixism.net/loti/index.html) asynchronous file APIs
* Sequential applications / low-concurrency programs
* It is important to note that Tokio is **NOT** the only asynchronous runtime
    * Remember that today we are talking about Tokio idioms, which are not necessarily the same as Rust Async idioms

<!--
"not stable" is somewhat of an oversimplification of io_uring. TLDR a very powerful idea in theory, but in practice lots of security vulnerabilities, unstable APIs, and generally a lot more work needed before it becomes production ready
-->


---


# Mini-Redis

We are going to create a miniature [Redis](https://redis.io/) client and server.

* Start with the basics of asynchronous programming in Rust
* Implement a subset of Redis commands
* Take a comprehensive tour of Tokio
* If you want to do the actual tutorial, follow along [here](https://tokio.rs/tokio/tutorial)


---


# Starter Code

Set up a new crate called `my-redis` and add some dependencies.

```sh
$ cargo new my-redis
$ cd my-redis
```

<br>

###### `Cargo.toml`
```
[dependencies]
tokio = { version = "1", features = ["full"] }
mini-redis = "0.4
```


---


# Starter Code

###### `src/main.rs`
```rust
use mini_redis::{client, Result};

#[tokio::main]
async fn main() -> Result<()> {
    // Open a connection to the mini-redis address.
    let mut client = client::connect("127.0.0.1:9808").await?;

    // Set the key "hello" with value "world"
    client.set("hello", "world".into()).await?;

    // Get key "hello"
    let result = client.get("hello").await?;

    println!("got value from the server; result={:?}", result);
    Ok(())
}
```


---


# Running our Client

Start the server:

```sh
$ cargo install mini-redis

# Run the mini server
$ mini-redis-server
```

Run the client:

```sh
$ cargo run
got value from the server; result=Some(b"world")
```


---


# Lecture Done!

![bg right:30% 80%](../images/ferris_panics.svg)

Thanks for coming!

<br>

_Slides created by:_
Connor Tsui, Benjamin Owad, David Rudo,
Jessica Ruan, Fiona Fisher, Terrance Chen


---


# Breaking it down

Okay, let's actually break this down. There isn't much code, but a lot is happening.

```rust
use mini_redis::{client, Result};

#[tokio::main]
async fn main() -> Result<()> {
    let mut client = client::connect("127.0.0.1:9808").await?;

    client.set("hello", "world".into()).await?;

    let result = client.get("hello").await?;

    println!("got value from the server; result={:?}", result);

    Ok(())
}
```

<!--
Comments omitted for slide real estate
-->


---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---


# Title




---

