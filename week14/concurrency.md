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
    let mut client = client::connect("127.0.0.1:6379").await?;

    // Set the key "hello" with value "world"
    client.set("hello", "world".into()).await?;

    // Get key "hello"
    let result = client.get("hello").await?;

    println!("got value from the server; result={:?}", result);
    Ok(())
}
```

<!--
Note that 6379 is the actual dedicated redis port: https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
-->


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
    let mut client = client::connect("127.0.0.1:6379").await?;

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


# What's the Difference?

What's going on here?

```rust
let mut client = client::connect("127.0.0.1:6379").await?;
```

* The `client::connect` function is provided by the `mini-redis` crate
* Establishes a TCP connection with the remote address and returns a handle
* The only indication that this is asynchronous is the `.await` operator

<!--
Notice how this looks basically the same as synchronous Rust code...
-->


---


# What is Synchronous Programming?

* Most programs are executed in the same order in which they are written
    * Execute first line of code, then second line, etc.
* We call this _synchronous_ programming
* When a program encounters an operation that cannot be completed immediately, it will _block_ until the operation completes
    * For example, establishing a TCP connection over the network

<!--
TCP connection requires an exchange with a peer over the network, so if the peer is on the other side of the world,
the speed of light becomes a bottleneck and it could take time for the connection to be established.
In synchronous programming, the thread that executes this blocks / waits for it to finish.
-->


---


# What is Asynchronous Programming?

* In asynchronous programming, operations that cannot complete immediately are _suspended_
* The thread executing is not blocked and can instead run other things
* When the operation completes, it becomes _unsuspended_ and the thread continues processing it where it left off


---


# Asynchronous Programming in Practice

* In our example, we only have one task (a single `client::connect`)
* Usually, asynchronous programs have _many_ tasks running at the same time
* This results in much more complicated programs
    * Track all of the state necessary to suspend/resume work

<!--
This is essentially what the operating system is doing with synchronous threads, but at the kernel level. Asynchronous programs have to do this at the user level, which is significantly harder.

Also note that we are using the word "task" here instead of "thread". This is intentional, and we'll explain this more in depth later.
-->


---


# `async`

Functions that perform asynchronous operations are labeled with the `async` keyword.

```rust
use mini_redis::Result;
use mini_redis::client::Client;
use tokio::net::ToSocketAddrs;

//  vvvvv
pub async fn connect<T: ToSocketAddrs>(addr: T) -> Result<Client> {
    // <-- snip -->
}
```


---


# `async`

```rust
//  vvvvv
pub async fn connect<T: ToSocketAddrs>(addr: T) -> Result<Client> {}
```

* The `async fn` definition looks like a regular synchronous function!
* The compiler transforms the `async fn` at **compile-time** into a routine
    * You can think of this routine as a low-level state machine


---


# `.await`

```rust
let mut client = client::connect("127.0.0.1:6379").await?;
```

* When we call `.await` on an `async fn`, we _yield_ control back to the thread
* The executing thread is then allowed to go work on other tasks as the current `connect` task is processed in the background
* Once the connection has been established in `connect`, the thread can resume working on this task

<!--
You might wonder how exactly the thread knows that it can "come back" and resume working on this task.

There is a very specific mechanism that is WAY beyond the scope of this lecture in which the underlying state machine is able to signal the executor that the current task can be waken up.
See https://docs.rs/futures/latest/futures/task/struct.Waker.html
-->


---


# Calling `async` Functions

Async functions are similar to normal Rust functions. However, calling these functions does not result in the function body executing.

```rust
/// An asynchronous function that prints "world".
async fn say_world() {
    println!("world");
}

#[tokio::main]
async fn main() {
    let op = say_world();

    println!("hello");

    op.await;
}
```

<!--
Can you guess what the behavior of this program is?
-->


---


# Calling `async` Functions

```rust
async fn say_world() { println!("world"); }

#[tokio::main]
async fn main() {
    // Calling `say_world()` does not execute the body of `say_world()`.
    let op = say_world();

    // This println! comes first.
    println!("hello");

    // Calling `.await` on `op` starts executing `say_world`.
    op.await;
}
```

```
hello
world
```


---


# `async` is Lazy

* Other languages implement `async/await` (notably JavaScript and C#)
* However, Rust async operators are **lazy**
* This results in dramatically different runtime semantics


---


# Asynchronous `main` Function

You may have noticed something different about our `main` function.

```rust
#[tokio::main]
async fn main() { ... }
```

* It is labeled `async fn`
* It is annotated with `#[tokio::main]`


---


# Asynchronous Runtimes

Asynchronous functions (`async fn`) must be **executed** by a **runtime**.

* A runtime provides many components needed for running asynchronous programs
    - Task scheduler
    - I/O event handlers
    - Timers
* A runtime must be started by a real `main` function


---


# `#[tokio::main]`

The `#[tokio::main]` function is a macro that transforms the `async fn main()` into a synchronous `fn main()`.

```rust
#[tokio::main]
async fn main() {
    println!("hello");
}

/// The above gets transformed into:
fn main() {
    let mut rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        println!("hello");
    })
}
```


---


# Back to the Server

Let's go back to implementing a Redis server. We want to:

* Accept inbound TCP sockets in a loop
* Process each socket
    * Read the command
    * Print to `stdout`
    * For now, respond with an "unimplemented" error


---


# Accept TCP Connections

```rust
use tokio::net::{TcpListener, TcpStream};
use mini_redis::{Connection, Frame};

#[tokio::main]
async fn main() {
    // Bind the listener to the address.
    let listener = TcpListener::bind("127.0.0.1:6379").await.unwrap();

    loop {
        // The second item contains the IP and port of the new connection.
        let (socket, _) = listener.accept().await.unwrap();
        process(socket).await;
    }
}
```


---


# Process Sockets

```rust
async fn process(socket: TcpStream) {
    // The `Connection` lets us read/write redis **frames** instead of
    // byte streams. The `Connection` type is defined by mini-redis.
    let mut connection = Connection::new(socket);

    if let Some(frame) = connection.read_frame().await.unwrap() {
        println!("GOT: {:?}", frame);

        // Respond with an error
        let response = Frame::Error("unimplemented".to_string());
        connection.write_frame(&response).await.unwrap();
    }
}
```


---


# Server and Client

If we run both the server and client programs:

Server (example request):

```
GOT: Array([Bulk(b"set"), Bulk(b"hello"), Bulk(b"world")])
```

Client:

```
Error: "unimplemented"
```


---


# Server Problem

Our server has a small problem...

```rust
#[tokio::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:6379").await.unwrap();

    loop {
        let (socket, _) = listener.accept().await.unwrap();
        process(socket).await;
    }
}
```

* _Other than the fact that it only returns "unimplemented" errors_
* Sockets are processed one at a time!


---


# Limited Concurrency

```rust
loop {
    let (socket, _) = listener.accept().await.unwrap();
    process(socket).await;
}
```

* When a connection is accepted:
    * The server `process`es the `socket` until completion
    * Goes back to listening
* Ideally, we want to process many requests concurrently


---


# More Concurrency

If we want to process connections concurrently, we will need to `spawn` new tasks.

* We can spawn a new concurrent task for each socket
* This allows the executor to process each connection concurrently!


---


# `tokio::spawn`

`tokio::spawn` spawns a new task on the `tokio` runtime.

```rust
loop {
    let (socket, _) = listener.accept().await.unwrap();

    // A new task is spawned for each inbound socket. The socket is
    // moved to the new task and processed there.
    tokio::spawn(async move {
        process(socket).await;
    });
}
```

* Now our server can accept many concurrent requests!


---


# Tasks

You may have noticed we have been using the word "Task".

* A Tokio task is an asynchronous _green thread_
* We create Tokio tasks by passing an `async` block / scope to `tokio::spawn`
* Tokio tasks are _very_ lightweight
    * Can spawn millions of tasks without much overhead!

<!--
A single tokio task requires only a single allocation an 64 bytes of memory
-->


---


# Tasks vs Threads

* When we talk about Tokio, **tasks** lightweight units of execution managed by the Tokio scheduler
* On the other hand, **threads** are heavyweight units of execution managed by the operating system's scheduler
    * You _cannot_ spawn millions of threads without any overhead
* The tokio runtime (which manages tasks) run on top of OS threads


---


# Tasks and Threads

Recall that Tokio is a **multi-threaded runtime** for **executing** asynchronous code.

* When tasks are spawned, the Tokio scheduler will ensure that the task executes once it has work to do (when it needs to resume)
* The scheduler might decide to execute the task on a different thread than the one it was originally spawned on
* **Important: Not all asynchronous runtimes do this!**

<!--
More on the implications of this later in the lecture
-->


---


# `std::thread::spawn`

![bg right:30% 75%](../images/ferris_does_not_compile.svg)

Recall that we often had to `move` things into `std::thread::spawn`.


```rust
let v = vec![1, 2, 3];

thread::spawn(|| {
    println!("Here's a vector: {:?}", v);
});
```

```
note: function requires argument type to outlive `'static`
 --> src/main.rs:6:5
  |
6 | /     thread::spawn(|| {
7 | |         println!("Here's a vector: {:?}", v);
8 | |     });
  | |______^
```


---


# `'static` Bound

* The closure that we pass to `thread::spawn` needs a `'static` bound
* This is a more precise way of saying the closure cannot contain references to data owned elsewhere
* Tasks require the exact same `'static` bound for the same reason


---


# `'static` Bound

![bg right:30% 75%](../images/ferris_does_not_compile.svg)

```rust
#[tokio::main]
async fn main() {
    let v = vec![1, 2, 3];

    tokio::task::spawn(async {
        println!("Here's a vec: {:?}", v);
    });
}
```


---


```
error[E0373]: async block may outlive the current function, but it borrows `v`, which is owned by the current function
 --> src/main.rs:7:23
  |
7 |       task::spawn(async {
  |  _______________________^
8 | |         println!("Here's a vec: {:?}", v);
  | |                                        - `v` is borrowed here
9 | |     });
  | |_____^ may outlive borrowed value `v`
  |

note: function requires argument type to outlive `'static`
 --> src/main.rs:7:17
  |
7 |       task::spawn(async {
  |  _________________^
8 | |         println!("Here's a vector: {:?}", v);
9 | |     });
  | |_____^

help: to force the async block to take ownership of `v` (and any other
      referenced variables), use the `move` keyword
  |
7 |     task::spawn(async move {
8 |         println!("Here's a vec: {:?}", v);
9 |     });
  |
```


---


# `async move`

The solution is similar to the synchronous `thread::spawn` example.

```rust
#[tokio::main]
async fn main() {
    let v = vec![1, 2, 3];

    //                       vvvv
    tokio::task::spawn(async move {
        println!("Here's a vec: {:?}", v);
    });
}
```

* Note that this is _not_ an asynchronous closure
* `async` closures were stabilized in the Rust 2024 Edition (_2/20/2025_)!


---


# `Send` Bound

Since Tokio is a multi-threaded runtime, it also requires a `Send` bound.

* Because tasks can execute on multiple threads, the runtime needs to be able to `Send` the task between threads
* This is a huge (and almost controversial) topic that we won't get into


---


# The `Send` Bound Problem

If you see this error (or something similar):

```
error: future cannot be sent between threads safely
   --> src/main.rs:6:5
    |
6   |     tokio::spawn(async {
    |     ^^^^^^^^^^^^ future created by async block is not `Send`
    |
```

* RUN!!!
* If you can't run, then that is a good time to dive deeper into how `async` and `Future`s work under the hood

<!--
TODO: Write down why we're not going to talk about this
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

