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

# Parallelism


---


# Parallelism vs. Concurrency

<div class="columns">
<div>

## Concurrency

**Problem** of handling many tasks at once


## Parallelism

**Solution** of working on multiple tasks at the same time

* **Key difference:** Parallelism utilizes **multiple** workers

---


# Workers

Parallelism divides tasks among workers.

* In hardwareland, we call these workers **processors** and **cores**.

* In softwareland, <!-- "we give these workers a different name" -->
  * "Processors" => Processes
  * "Cores" => Threads

* **Key difference:** Parallelism utilizes **multiple** processors/cores
  * Some concurrency models don't!


<!-- Note:
Students coming from 122 may be unfamiliar with processors/cores,
so I added this for clarification.

Alternate suggestion is to remove mention of hardware,
so that this slide is shortened to
  "Examples of workers: 
      * Processes
      * Threads"
-->


---


# Parallelism vs. Concurrency


<img src="img/concvspar.jpg" style="width: 85%; margin-left: auto; margin-right: auto;">


---


# Parallelism vs. Concurrency: Examples
<div class="columns">
<div>

## Parallelism

* 8 cores, 8 threads
* 4 threads load the webpage, 4 threads update the progress bar

</div>
<div>

## Alternate Concurrency Model

* 1 core, 1 thread
* When blocked on loading the webpage, update the progress bar


</div>
</div>


---


# Designing Parallel Solutions

Two big questions to ask:
* Division of Work
  * Who are the workers and how do we divide the work?
* Inter-thread / Inter-process Communication (IPC)
  * What needs to be shared and how?
  * Approach 1: Shared Memory
  * Approach 2: Message Passing


---


# Multithreading

For this lecture only...
* Our workers are threads
* **Thread:** "stream of instructions"

<!--Speaker note:
Same principles can be applied to multiprocessing
Emphasize that "thread" is overloaded term
-->


---


# Example: Creating a Thread
Threads can be created ("spawned") using `thread::spawn`.
```rust
let handle = thread::spawn(|| {
    for i in 1..10 {
        println!("hi number {} from the spawned thread!", i);
        thread::sleep(Duration::from_millis(1));
    }
});
```
* `thread::spawn` takes a function as argument
  * This is the function that the thread runs
* We can spawn multiple of these, to run multiple functions at once


---


# Multithreading

Suppose we're painting an image to the screen, and we have eight threads.

* How should we divide the work?
  * Divide image into eight regions
  * Assign each thread to paint one region
* Easy! "Embarassingly parallel"
  * Threads don't need to keep tabs on each other

<!--Speaker note:
"Embarassingly parallel" refers to problems where
we can easily utilize our hardware in full,
usually because tasks are super independent

Each thread retires to their cave
  to paint all day,
  not too different from modern artists
-->

---


# The Case for Communication

What if our image is more complex?

* We're painting semi-transparent circles
* Circles overlap and are constantly moving
* The _order_ we paint circles affects the color mixing

![bg right 100%](../images/week12/circle-order-A-then-B.png)

![bg right 100%](../images/week12/circle-order-B-then-A.png)

<!--
This is also known as the painter's algorithm
-->


---


# The Case for Communication

Now our threads need to talk to each other!

* For each pixel
  * How many circles have been drawn?
  * Do _not_ paint this pixel until previous circles are done


---


# Motivating Communication

**Problem:** How do threads communicate?

**Solutions:** We'll discuss two approaches...
* Approach 1: Shared Memory
* Approach 2: Message Passing

<!--Speaker note:
  Now our threads must talk to each other
-->


---


# Approach 1: Shared Memory

For each pixel, create a shared variable `x`:

```c
static int x = 0; // One per pixel
```

* When a thread touches a pixel, increment the pixel's associated `x`
* Now each thread knows how many layers of paint on that pixel


---


# Shared Memory: Data Races

Are we done?

Not quite...

* Shared memory is an ingredient for **data races**
* Let's illustrate

<!--Speaker note:
We'll walk through the other ingredients
-->


---


# Shared Memory: Data Races

Suppose we have a shared variable `x`.

```c
// Note this is C pseudocode
static int x = 0;
```

<!-- Speaker note:
(1) This is pseudocode; we'll explain Rust's interface in second half
(2) `static` => shared
-->


---


# Shared Memory: Data Races

First ingredient: `x` is in shared memory, and `x` must satisfy some property to be correct.

```c
// x is # of times *any* thread has called `update_x`
static int x = 0;
```


---


# Shared Memory: Data Races

Second ingredient: `x` becomes incorrect mid-update.

```c
// x is # of times *any* thread has called `update_x`
static int x = 0;

static void update_x(void) {
  int temp = x; // <- x is INCORRECT
  temp += 1;    // <- x is INCORRECT
  x = temp;     // <- x is CORRECT
}
```

* We don't actually write code like this
  * This is how it gets compiled to machine instructions

---


# Shared Memory: Data Races

Third ingredient: when multiple threads update at once...

```c
// x is # of times *any* thread has called `update_x`
static int x = 0;

static void update_x(void) {
  int temp = x; // <- x is INCORRECT
  temp += 1;    // <- x is INCORRECT
  x = temp;     // <- x is CORRECT
}
// <!-- snip -->
for (int i = 0; i < 20; ++i) {
  create_thread(update_x);
}
```


---


# Shared Memory: Data Races

Third ingredient: when multiple threads update at once...they interleave!


| Thread 1      |   Thread 2    |
|---------------|---------------|
| temp = x      |               |
|               | temp = x      |
| temp += 1     |               |
|               | temp += 1     |
| x = temp      |               |
|               | x = temp      |


<!--
Q: Can someone tell me the outcome of this sequence?
A: Next slide
-->


---


# Shared Memory: Data Races

We want `x = 2`, but we get `x = 1`!


| Thread 1      |   Thread 2    |
|---------------|---------------|
| Read temp = 0 |               |
|               | Read temp = 0 |
| Set temp = 1  |               |
|               | Set temp = 1  |
| Set x = 1     |               |
|               | Set x = 1     |


---


# Shared Memory: Data Races

We want the read-set operations to be **atomic**.

<style>
    .container {
        display: flex;
        gap: 16px;
    }
    .col {
        flex: 1;
    }
</style>
<div class = "container">

<div class = "col">

**Not Atomic**

| Thread 1      |   Thread 2    |
|---------------|---------------|
| temp = x  |               |
|               | temp = x      |
| temp += 1 |               |
|               | temp += 1     |
| x = temp      |               |
|               | x = temp      |

</div>
<div class = "col">

**Atomic**

| Thread 1      |   Thread 2    |
|---------------|---------------|
| temp = x  |               |
| temp += 1 |               |
| x = temp  |               |
|               | temp = x      |
|               | temp += 1     |
|               | x = temp      |

</div>
</div>

<!--Speaker Note:
That is, while Thread 1 is executing these instructions,
  Thread 2 cannot cut in.
-->

---


# Fixing a Data Race

We must eliminate one of the following:
1. `x` is shared memory
2. `x` becomes incorrect mid-update
3. Unsynchronized updates (parties can "cut in" mid-update)


---


# Approach 1: Mutual Exclusion


Take turns! No "cutting in" mid-update.

1. `x` is shared memory
2. `x` becomes incorrect mid-update
3. ~~Unsynchronized updates (parties can "cut in" mid-update)~~


---


# Approach 1: Mutual Exclusion

We need to establish *mutual exclusion*, so that threads don't interfere with each other.
* Mutual exclusion means "Only one thread can do something at a time"
* A common tool for this is a mutex lock


<!-- Explain what mutual exclusion is, what a mutex is, high level, verbally -->
---


# Approach 1: Mutual Exclusion

```c
static int x = 0;
static mtx_t x_lock;

static void thread(void) {
  mtx_lock(&x_lock);
  int temp = x;
  temp += 1;
  x = temp;
  mtx_unlock(&x_lock);
}
// <!-- snip -->
```
- Only one thread can hold the mutex lock at a time

- This provides *mutual exclusion*--only one thread may access `x` at the same time.


---


# Approach 2: Atomics


One airtight update! Cannot be "incorrect" mid-update.

1. `x` is shared memory
2. ~~`x` becomes incorrect mid-update~~
3. Unsynchronized updates (parties can "cut in" mid-update)


---


# Approach 2: Atomics

The compiler usually translates the following operation...

```c
x += 1;
```

...into the machine instruction equivalent of this:

```c
int temp = x;
temp += 1;
x = temp;
```


---


# Approach 2: Atomics

However, we can use an atomic operation like this:

```c
__sync_fetch_and_add(&x, 1); // syntax depends on library
```

...which is implemented in hardware with just one instruction:

```c
x += 1;
```

* `fetch_and_add`: performs the operation suggested by the name, and returns the value that was previously in memory
  * Also `fetch_and_sub`, `fetch_and_or`, `fetch_and_and`, ...

---

# Atomics

Other common atomic is `compare_and_swap`
* If the current value matches some old value, then write new value into memory
  * Depending on variant, returns a boolean for whether new value was written into memory
* "Lock-free" programming:
  * No locks! Just `compare_and_swap` until we successfully write new value
  * Not necessarily more performant than lock-based solutions
    * Contention is bottleneck, not presence of locks
  
<!-- Speaker note:
Rule of thumb: conventional wisdom is that locking code is perceived as slower than lockless code

This does NOT mean that lock-free solutions are more performant than lock-based solutions.

Lock-based solutions are slow due to _contention_ for locks, not _presence_ of locks
If multiple threads are contending for same memory location, i.e. stuck in a `compare_and_swap` loop, that can be equally slow
This is why benchmarking is importnat, because we can't crystal-ball the performance of our solutions!
-->


---


# Atomics

Rust provides atomic primitive types, like `AtomicBool`, `AtomicI8`, `AtomicIsize`, etc.
* Provides a way to access values atomically from any thread
  * Safe to share between threads implementing `Sync`
* We won't cover it further in this course, but the API is largely 1:1 with the C++20 atomics
  * If interested in pitfalls, read up on *memory ordering* in computer systems


---


# Fixing a Data Race

**Approach 3: No Shared Memory**

If we eliminate shared memory...

1. ~~`x` is shared memory~~
2. `x` becomes incorrect mid-update
3. Unsynchronized updates


---


# Fixing a Data Race

**Approach 3: No Shared Memory**

If we eliminate shared memory... race is trivially gone.

1. ~~`x` is shared~~
2. ~~`x` becomes incorrect mid-update~~
3. ~~Unsynchronized updates~~


---


# Message Passing

Now we talk about the second approach to inter-thread communication:

- Approach 1: Shared Memory
* Approach 2: Message Passing
  * Eliminates shared memory


---


# Approach 2: Message Passing

Previously, our shared memory solution was

* For each pixel...
  * Create shared variable `x`
  * Increment `x` when thread touches pixel


---



# Approach 2: Message Passing

In our **message passing** solution, we do *not* share `x`, but create a thread-local copy.

- For each pixel...
  - Create a local variable `x` for each thread (not shared!)
  - Increment `x` when thread touches pixel


---


# Approach 2: Message Passing

When threads update their local copy, they notify other threads via **message passing**.

- For each pixel...
  - Create a local variable `x` for each thread (not shared!)
  - Increment `x` when thread touches pixel
    - Send message to other threads, so they update their copies of `x`
* Left as an exercise:
  * There's another way to divide the work with less communication costs
  * Ferris (and Clarabelle) will be proud of you if you find it


---


# Message Passing

* Threads communicate via channels
* Golang famously uses this approach


---



# Message Passing Example

```rust
let (tx, rx) = mpsc::channel();
```
* Channels have two halves, a transmitter and a receiver
* Connor writes "Review the ZFOD PR" on a rubber duck and it floats down the river (transmitter)
  * Ben finds the duck downstream, and reads the message (receiver)
* Note that communication is one-way here
* Note also that each channel can only transmit/receive one type
  * e.g. `Sender<String>`, `Receiver<String>` can't transmit integers

---


# Message Passing Example

```rust
let (tx, rx) = mpsc::channel();

thread::spawn(move || { // Take ownership of `tx`
    let val = String::from("review the ZFOD PR!");
    tx.send(val).unwrap(); // Send val through the transmitter
});

let received = rx.recv().unwrap(); // receive val through the receiver
println!("I am too busy to {}!", received);
```
* Note that, after we send `val`, we no longer have ownership of it!

---

# Message Passing in Rust
We can also use receivers as iterators!

```rust
let (tx, rx) = mpsc::channel();

thread::spawn(move || { // Take ownership of `tx`
    let val = String::from("review the ZFOD PR!");
    tx.send(val).unwrap(); // Send val through the transmitter
    tx.send("buy Connor lunch".into()).unwrap();
});

for msg in rx {
  println!("I am too busy to {}!", msg);
}
```
* Wait, what does `mpsc` stand for?


---


# `mpsc` ⟹ Multiple Producer, Single Consumer

This means we can `clone` the transmitter end of the channel, and have *multiple producers*.

```rust
let (tx, rx) = mpsc::channel();

let tx1 = tx.clone();
thread::spawn(move || { // owns tx1
      tx1.send("yo".into()).unwrap();
      thread::sleep(Duration::from_secs(1));
});

thread::spawn(move || { // owns tx
      tx.send("hello".into()).unwrap();
      thread::sleep(Duration::from_secs(1));
});

for received in rx {
    println!("Got: {}", received);
}
```

---


# Recap

When tackling a parallelism problem, think:

* What are my workers and how many do I have?
* How to divide the work among workers
* Do I need to share data between workers?
  * Shared Memory vs Message Passing


---

# Threads in Rust

Now that we have an framework for parallelism problems, let's dive into the Rust specifics!

---

# Threads in Rust
* Rust's typechecker guarantees an absence of *data races*
  * (Unless you use unsafe)
* General race conditions are not prevented
* Deadlocks are still allowed

<!-- In my opinion, this is the single best reason to use this language -->

---

# Creating Threads
Threads can be created/spawned using `thread::spawn`.
```rust
let handle = thread::spawn(|| {
    for i in 1..10 {
        println!("hi number {} from the spawned thread!", i);
        thread::sleep(Duration::from_millis(1));
    }
});
```
* `thread::spawn` takes in a function, implementing the `FnOnce` and `Send` traits.
  * Closures are often used to allow capturing values, but functions work as well
  * More on the `Send` trait later...
* Returns a `JoinHandle` type


---

# Joining Threads
To wait for a thread to complete, we *join* on it.
```rust
let handle = thread::spawn(|| {
    for i in 1..10 {
        println!("hi number {} from the spawned thread!", i);
        thread::sleep(Duration::from_millis(1));
    }
});

handle.join().unwrap();
```
* Execution of the main thread is halted until the spawned thread finishes


---

![bg right:20% 75%](../images/ferris_does_not_compile.svg)

# Capturing Values in Threads
We often want to use things outside of the the closure, but borrowing them can be problematic.
```rust
let v = vec![1, 2, 3];

let handle = thread::spawn(|| {
    println!("Here's a vector: {:?}", v);
});
```
```
error[E0373]: closure may outlive the current function,
but it borrows `v`, which is owned by the current function
```
* In other words, what if `v` goes out of scope while the thread is still running?

---

# Capturing Values in Threads
To solve this problem, we can take ownership of values, *moving* them into the closure.
```rust
let v = vec![1, 2, 3];

let handle = thread::spawn(move || {
    println!("Here's a vector: {:?}", v);
});
```
* `v` is no longer accessible in the main thread
* You could clone `v` to solve this problem
  * But, what if we *wanted* to share `v`?

---

# Multiple Owners

Recall `Rc<T>` from last lecture.
* `Rc<T>` works like `Box<T>`, providing a (spiritually) heap-allocated value.
* The difference is, `Rc<T>` has an internal reference count, and the heap allocated value will only be dropped when the reference count reaches zero.
* The only problem is, `Rc<T>` is not thread safe...

<!-- Make sure people know about reference counts -->

---

# `Arc<T>`

"Arc" stands for "Atomically Reference Counted". This means, it is thread-safe, at the cost of slightly slower operations.
* General advice: default to using `Rc<T>`, and switch to `Arc<T>` if you need to share ownership across threads
  * The compiler will not let you use `Rc` across threads

---

# Sharing Resources in Rust
We can give the vector multiple owners by using an `Arc`.
```rust
let v = Arc::new(vec![1, 2, 3]);

let v_copy = v.clone();
let handle = thread::spawn(move || {
    println!("Here's a vector: {:?}", v_copy);
});

println!("Here's a vector: {:?}", v);

handle.join().unwrap();
```
* `v` and `v_copy` both point to the same value
* When both  are dropped, only then will the underlying vector be dropped
* Is this a data race?
  * No, because we are only performing reads

---

![bg right:20% 75%](../images/ferris_does_not_compile.svg)

# Sharing Mutable Resources in Rust
If we attempt to mutate the vector, we will indeed encounter an error
```rust
let v = Arc::new(vec![1, 2, 3]);

let v_copy = v.clone();
let handle = thread::spawn(move || {
    v_copy.push(4);
    println!("Here's a vector: {:?}", v_copy);
});

v.push(5);
println!("Here's a vector: {:?}", v);

handle.join().unwrap();
```
* This prevents a data race
  * If we allowed this, it would violate one of the rules—only one mutable reference at a time

---

![bg right:20% 75%](../images/ferris_does_not_compile.svg)

# Sharing Mutable Resources in Rust
```rust
let v = Arc::new(vec![1, 2, 3]);

let v_copy = v.clone();
let handle = thread::spawn(move || {
    v_copy.push(4);
    println!("Here's a vector: {:?}", v_copy);
});

v.push(5);
println!("Here's a vector: {:?}", v);

handle.join().unwrap();
```

```
cannot borrow data in an Arc as mutable
<!-- snip -->
help: trait DerefMut is required to modify through a dereference,
but it is not implemented for Arc<Vec<i32>>
```

---


# Sharing Mutable Resources in Rust
The solution to this is actually the same as in C—we introduce a mutex.

---

# Mutexes in Rust

Unlike in C, mutexes in Rust actually *wrap* values.

```rust
let x = Mutex::new(0);
let x_data = x.lock().unwrap();
```
* This allows the typechecker to verify that the lock is acquired before accessing a value (and eliminates a class of bugs)
  * If we know this, our multiple mutable references rule is not broken!
* `x_data` is a `MutexGuard` type.
  * It has deref coercion, so one can operate on it just like it was the actual data
* When `x_data` is dropped, the mutex will be unlocked.
* `lock` may return an error if another thread panics

---

# Sharing Mutable Resources in Rust
```rust
let v = Arc::new(Mutex::new(vec![1, 2, 3]));

let v_copy = v.clone();
let handle = thread::spawn(move || {
    v_copy.lock().unwrap().push(4);
    println!("Here's a vector: {:?}", v_copy);
});

v.lock().unwrap().push(5);
println!("Here's a vector: {:?}", v);

handle.join().unwrap();
```
* The other thread cannot access the mutex until it is dropped (unlocked)
* This prevents multiple mutable references, and the data race, by providing mutual exclusion!

---

# C to Rust Example

---

# C to Rust Example

![bg right:20% 75%](../images/ferris_does_not_compile.svg)

Here's the C code from before, turned into Rust directly.

```rust
let mut x = 0;

for _ in 0..20 {
    thread::spawn(|| {
        x += 1;
    });
}
```
* A sea of errors ensues of course, but the key idea is that this violates one of our rules.
  * We can't have multiple mutable references at the same time!


---

# C to Rust Example (with Mutexes)

![bg right:20% 75%](../images/ferris_does_not_compile.svg)

Here's our code from before, with mutexes incorporated

```rust
let x = Mutex::new(0);

for _ in 0..20 {
    thread::spawn(|| {
        let mut data = x.lock().unwrap();
        *data += 1;
    });
}
```
* What is wrong now?
  * What if the main function ends? It owns `x`, so the thread references to `x` will be invalid...
* How can we have multiple owners?

---

# C to Rust Example (with Multiple Ownership)

```rust
let x = Arc::new(Mutex::new(0));

for _ in 0..20 {
    let x_clone = Arc::clone(&x);
    thread::spawn(move || {
        let mut data = x_clone.lock().unwrap();
        *data += 1;
    });
}
```
* Notice that we `move` each clone of `x` into each thread, taking ownership of it
* Each thread has a pointer to the mutex
  * The mutex is not deallocated until all of the `Arc`s pointing to it are dropped (and the reference count is zero)


<!--
Q: Why not give mutex an internal Arc?
A: What if we want to have a mutex around only some values in a struct, while others are atomic?
-->
---

# The Good Slide

```rust
let x = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..20 {
    let x_clone = Arc::clone(&x);
    handles.push(thread::spawn(move || {
        let mut data = x_clone.lock().unwrap();
        *data += 1;
    }));
}

for handle in handles { handle.join().unwrap(); } // Wait for all threads
println!("Final value of x: {}", *x.lock().unwrap());
```
* `x` is 20, *every time*.
  * And it is illegal for it to be anything else in safe Rust.


---

# `Send` and `Sync`

---

# `Send` and `Sync`

Everything we have gone over so far is a *standard library* feature. The language itself provides two marker traits to enforce safety when dealing with multiple threads, `Send` and `Sync`.


<!-- Marker trait == no implementation, signal to the compiler -->

---

# `Send` vs. `Sync`


## `Send`

* Indicates that the type is safe to *send* between threads.
* `Rc<T>` does not implement this trait, because it is not thread safe.


## `Sync`

* Indicates that the type implementing `Send` can be referenced from multiple threads
* For example, `RefCell<T>` from last lecture implements `Send` but not `Sync`
* `Rc<T>` does not implement `Sync` either

<!-- MutexGuard implements Sync, but not Send, actually! -->


---

# Using `Send` and `Sync`
* It is generally rare that you would implement these traits yourself
  * Structs containing all `Send`/`Sync` types automatically derive `Send`/`Sync`
  * Explicitly implementing either one requires using `unsafe`
* This would be an example of a trait you might want to *unimplement*
  * e.g. If you are doing something with `unsafe` that is not thread-safe
  * `impl !Send for CoolType<T> {}`

<!-- Notice this negative impl is not unsafe-->

---

# More Shared State Primitives

---

# `RwLock<T>` (Reader-Writer Lock)

A reader-writer lock is like a mutex, except it allows concurrent access between readers (not writers).
* We can acquire a read lock (or shared lock)
  * Can be held by multiple readers at once
  * No writers can hold the lock
* We can acquire a write lock (or exclusive lock),
  * Can be held by only one writer
  * No readers can hold the lock

---

# `RwLock<T>` Example

```rust
let shared_data = Arc::new(RwLock::new(Vec::<i32>::new()));

// All of the readers can hold the read lock simultaneously
for _ in 0..5 {
    let shared_data_clone = Arc::clone(&shared_data);
    thread::spawn(move || {
        let data = shared_data_clone.read().unwrap();
        println!("Reader: {:?}", *data);
    });
}

// The writer has to be the only one with the lock
let shared_data_clone = Arc::clone(&shared_data);
thread::spawn(move || {
    let mut data = shared_data_clone.write().unwrap();
    data.push(42);
    println!("Writer: {:?}", *data);
});
```

---

# Even More  Primitives

* `CondVar<T>`—release a mutex and atomically wait to be signaled to re-acquire it
* `Barrier`—Memory barrier, allows multiple threads to wait at a certain point, until all relevant threads reach that point
* `Weak<T>`—downgraded version of `Rc` or `Arc` that holds a pointer, but does not count as an owner.
  * Retrieving the value can fail, if it has been deallocated already.

---


# Review: "Fearless Concurrency"

What we have gone over today is referred to as "fearless concurrency" in the rust community.
* By leveraging the ownership system, we can move entire classes of concurrency bugs to compile-time
* Rather than choosing a restrictive "dogmatic" approach to concurrency, Rust supports many approaches, *safely*
* Subjectively, this may be the single best reason to use this language
* Both parallelism and concurrency, as introduced in this lecture, benefit from these guarantees

---

# Next Lecture: Concurrency

![bg right:30% 80%](../images/ferris_happy.svg)

Thanks for coming!

<br>

_Slides created by:_
Connor Tsui, Benjamin Owad, David Rudo,
Jessica Ruan, Fiona Fisher, Terrance Chen
