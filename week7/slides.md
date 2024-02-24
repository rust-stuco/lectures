---
marp: true
theme: default
class: invert
paginate: true
---

# Intro to Rust Lang

# **Crates, Closures, and Iterators**
*Oh my!*
<br>

Benjamin Owad, David Rudo, and Connor Tsui

![bg right:35% 65%](../images/ferris.svg)


---

## Week 7: Crates, Closures, and Iterators
- Crate Highlights
- Closures
- Iterators
- Loops vs. Iterators

### After Dark
- More Essential Rust Crates
    - `rayon`, `serde`, `criterion`

---

# **Crate Highlights**

---

# Rand
The standard library includes many things but a random number generator isn't one of them*

* Rand is the defacto crate for:
    * Generate random numbers
    * Create distributions
    * Provides randomness related algorithms (like vector shuffling)

```Rust
use rand::prelude::*;

let mut rng = rand::thread_rng();
let y: f64 = rng.gen(); // generates a float between 0 and 1

let mut nums: Vec<i32> = (1..100).collect();
nums.shuffle(&mut rng);
```

---

# Clap
A very popular (but not the only!) argument parser used in Rust programs.

```Rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    name: String, // Name of the person to greet

    #[arg(short, long, default_value_t = 1)]
    count: u8, // Number of times to greet
}

fn main() {
    let args = Args::parse(); //get-opt could never
    for _ in 0..args.count {
        println!("Hello {}!", args.name)
    }
}
```

---

# Anyhow
Have code that can throw multiple error types that you wish was one? Use this!
```Rust
use anyhow::Result;

fn get_cluster_info() -> Result<ClusterMap> {
    let config = std::fs::read_to_string("cluster.json")?;
    let map: ClusterMap = serde_json::from_str(&config)?;
    Ok(map)
}
```
* Makes error more dynamic
* Allows for:
    * Downcasting to original error types
    * Attaching custom context/error messages
    * Custom errors

---

# Tracing
Framework for instrumenting Rust programs 
* Collects structured, event-based diagnostic information
* First class support for async programs
* Manages execution through periods of computation known as *spans*
* Provides distinction of program events in terms of severity and custom messages
* Extremely flexible for reformatting/changing

---

# Flamegraph
![bg right:50% 90%](../images/example_flame.png)
Rust powered flamegraph generator with Cargo support!
* Can support non-Rust projects too
* Relies on perf/dtrace

---

# **Closures**

---

# What Is A Closure?
* Known as lambdas in "lesser languages"
* Anonymous functions you can save in a variable or pass as an argument to other functions

**Unlike functions**: Closures can capture values from the scope in which they're defined

---

# Closure Syntax
```Rust
let annotated_closure = |num : u32| -> u32 {
    num
};
```
This looks very similar to functions, but Rust is smarter than this. Rust can derive closure type annotations from context!

---

# Closures Simplified
```Rust
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ; 
```
Note that for v4, we can remove the `{}` since the body is only one line.
This simplification is similar in style to how we don't annotate `let v = Vec::new()`.

---

# How about this?
![bg right:25% 75%](../images/ferris_does_not_compile.svg)

```Rust
let example_closure = |x| x;

let s = example_closure(String::from("hello"));
let n = example_closure(5);
```

---

# Annotations Are Still Important
```
$ cargo run
   Compiling closure-example v0.1.0 (file:///projects/closure-example)
error[E0308]: mismatched types
 --> src/main.rs:5:29
  |
5 |     let n = example_closure(5);
  |             --------------- ^- help: try using a conversion method: `.to_string()`
  |             |               |
  |             |               expected struct `String`, found integer
  |             arguments to this function are incorrect
  |
note: closure parameter defined here
 --> src/main.rs:2:28
  |
2 |     let example_closure = |x| x;
  |                            ^

For more information about this error, try `rustc --explain E0308`.
error: could not compile `closure-example` due to previous error
```

---

# So What Happened Here?
* The first time we called `example_closure` with a `String` 
* Rust inferred the type of `x` and the return type 
* Those types are now bound to the closure 
    * Causing `example_closure(5)` to fail

---

# Capturing References
Closures can capture values from their environment in three ways:
* Borrowing immutably
* Borrowing mutably
* Taking ownership 
    * i.e. _moving_ the value to the closure

---

# Immutable Borrowing in Closures

```rust
let list = vec![1, 2, 3];
println!("Before defining closure: {:?}", list);

let only_borrows = || println!("From closure: {:?}", list);

println!("Before calling closure: {:?}", list);
only_borrows();
println!("After calling closure: {:?}", list);
```
- Note how once a closure is defined, it's invoked in the same manner as a function.
- Because we can have many immutable borrows, Rust allows us to to print, even with the closure holding a reference.

---

![bg right:25% 75%](../images/ferris_does_not_compile.svg)
# Mutable Borrowing in Closures
```rust
let mut list = vec![1, 2, 3];
println!("Before defining closure: {:?}", list);

let borrows_mutably = || list.push(7);

borrows_mutably();
println!("After calling closure: {:?}", list);
```
* This seems like it would work...

---

# Mutable Borrowing in Closures

```
error[E0596]: cannot borrow `borrows_mutably` as mutable, as it is not declared as mutable
 --> src/main.rs:7:5
  |
5 |     let borrows_mutably = || list.push(7);
  |                              ---- calling `borrows_mutably` requires mutable 
  |                                    binding due to mutable borrow of `list`
6 |
7 |     borrows_mutably();
  |     ^^^^^^^^^^^^^^^ cannot borrow as mutable
  |
help: consider changing this to be mutable
  |
5 |     let mut borrows_mutably = || list.push(7);
  |         +++
```
* Mutability must always be explicitly stated
* Note that Rust only considers the **invocation** a borrow, not the definition

---

# Mutable Borrowing in Closures

```rust
let mut list = vec![1, 2, 3];
println!("Before defining closure: {:?}", list);

let mut borrows_mutably = || list.push(7);

borrows_mutably();
println!("After calling closure: {:?}", list);
```

```
Before defining closure: [1, 2, 3]
After calling closure: [1, 2, 3, 7]
```
* Note how we can't have a `println!` before invoking `borrows_mutably` like before.
* `borrows_mutably` isn't called again, so Rust knows the borrowing has ended.
  * This is why we can call `println!` after.

---

# Giving Closures Ownership
![bg right:25% 75%](../images/ferris_does_not_compile.svg)
```rust
let mystery = {
    let x = rand::random::<u32>();
    |y: u32| -> u32 { x + y }
};

println!("Mystery value is {}", mystery(5));
```
```
error[E0373]: closure may outlive the current block, but it borrows `x`,
 which is owned by the current block
 --> src/main.rs:6:9
  |
6 |         |y: u32| -> u32 { x + y }
  |         ^^^^^^^^^^^^^^^   - `x` is borrowed here
  |         |
  |         may outlive borrowed value `x`
  |
  |
4 |     let mystery = {
  |         ^^^^^^^
help: to force the closure to take ownership of `x`, use the `move` keyword
  |
6 |         move |y: u32| -> u32 { x + y }
  |         ++++
```

---

# Giving Closures Ownership
![bg right:25% 75%](../images/ferris_happy.svg)
```rust
let mystery = {
    let x = rand::random::<u32>();
    move |y: u32| -> u32 { x + y }
};

println!("Mystery value is {}", mystery(5));
```

* We can tell a closure to own a value using the `move` keyword
* This is important for threads in Rust (to be discussed later)

---

#  Closures After Capturing
- A closure body can now do any of the following:
  - Move a captured value out of the closure
  - Mutate a captured value
  - Neither of the above
  - Capture nothing to begin with!
- Depending on which of these properties a closure has determines its trait
  - Closure traits is how functions/structs specify what _kind_ of closure is wanted

---

# FnOnce

* Trait applied to closure that can be called once
* All closures implement this trait (obviously)
* A closure that moves captured values **out** of its body will _only_ implement this trait
  * Because it can only be called once (can't move something out twice)

```rust
let my_str = String::from("x");
let consume_and_return = move || my_str;
```
* Rust won't implicitly copy `my_str`
  * This closure consumes `my_str` by giving ownership back to the caller 

---

# FnMut

* Trait applies to closures that: 
  * Don't move captured values out of their body
  * Might mutate captured values
* Can be called more than once

```rust
let mut x: usize = 1;
let add_two_to_x = || x += 2;
```
* Note this compiles until `add_two_to_x()` then `mut` is needed for the borrow
  * `mut` signals that we are mutating our closure's environment

---

# Fn
* Trait applies to closures that:
  * Don't move captured values out of their body
  * Don't mutate captured values
  * Or don't capture anything from their environment
* Can be called more than once without mutating environment

```rust
let double = |x| x * 2;
```

---

# Closure Traits Summarized
* `Fn`, `FnMut`, `FnOnce` describe different groups of closures
  * You don't `impl` them, they apply to a closure automatically if appropriate
  * A single closure can implement one or multiple of these traits
* `Fn` - call multiple times, environment doesn't change
* `FnMut` - call multiple times, environment may change
* `FnOnce` - call at least once, environment may be consumed

---

# Closure Traits Picturized
![bg right:65% 100%](../images/closure_traits.svg)

---

# Passing Closures to Functions
```rust
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T // we could replace FnOnce with Fn and still compile!
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```
* We simply use trait bounds!
* `F` is a generic for any closure that implements `FnOnce`
  * Every closure implements `FnOnce` at minimum making this function flexible
  * ` F: FnOnce() -> T` - `F` must take no args and return `T`

---

# Passing Mutable Closures to Functions
```rust
fn do_twice<F>(mut func: F)
    where F: FnMut()
{
    func();
    func();
}
```
* In this example we need the `mut` keyword
  * We now require mutable borrowing the environment
  * Similar to the requirements of defining and using a `FnMut` shown before

---

# Passing Specific Closures to Functions
```rust
fn reduce<F, T>(reducer: F, data: &[T]) -> Option<T>
where
    F: Fn(T, T) -> T,
{
    // -- snip --
}
```
* We can specify the arguments and return types
* While this example is generic we could've replaced `T` with a concrete type

---

# Hate Functional Programming? No Problem!
```rust
fn add_one(x: i32) -> i32 {
    x + 1
}

fn do_twice(f: fn(i32) -> i32, arg: i32) -> i32 {
    f(arg) + f(arg)
}

fn main() {
    let answer = do_twice(add_one, 5);
}
```
* Rust has function pointers, notated by `fn` (**not** `Fn`)
* `fn` is a **type** that implements `Fn`, `FnMut`, and `FnOnce`

---

# **Iterators**
Sorry functional haters

---

# What is an Iterator?
* Iterators allow you to perform some task on a sequence of elements
* Iterators manage iterating over each item and determining termination
* Rust iterators are *lazy*
  * This means we don't pay a cost until we consume the iterator

---

# Iterator Trait
All iterators must implement the `Iterator` trait:
```rust
pub trait Iterator {
  type Item;

  fn next(&mut self) -> Option<Self::Item>;

  // methods with default implementations elided
}
```
* What's going on with `Item`?
  * This is an *associated type*
  * Interpret as: to define `Iterator` you must define the type, `Item`, you're iterating over

---

# Custom Iterator Example
```rust
struct Fibonacci {
  curr: u32,
  next: u32,
}
```
* I want to implement an iterator that contains the fibonacci sequence.
* First need to declare the struct that can implement `Iterator`

---
 
# Custom Iterator Example

```rust
impl Iterator for Fibonacci {
    type Item = u32;

    // We use Self::Item in the return type, so we can change
    // the type without having to update the function signatures.
    fn next(&mut self) -> Option<Self::Item> {
        let current = self.curr;

        self.curr = self.next;
        self.next = current + self.next;

        // No endpoint to a Fibonacci sequence - `Some` is always returned.
        Some(current)
    }
}
```
* Notice `Self::Item` is aliased to `u32`
* When the `Iterator` is finished, `None` is returned, else `Some`

---

# Iterators from Vectors
```rust
let v1 = vec![1, 2, 3];

let v1_iter = v1.iter();

for val in v1_iter {
    println!("Got: {}", val);
}
```
* We saw this code before in lecture 4
  * Except now we explicitly create the iterator that Rust did for us

---

# Iterating Explicitly

```rust
let v1 = vec![1, 2, 3];

let mut v1_iter = v1.iter();

assert_eq!(v1_iter.next(), Some(&1));
assert_eq!(v1_iter.next(), Some(&2));
assert_eq!(v1_iter.next(), Some(&3));
assert_eq!(v1_iter.next(), None);
    
```
* Here we see how the required `next` function operates
* Notice how `v1_iter` is mutable
  * When we call `next()` we've **consumed** that iterator element
  * The iterators internal state has changed
  * Note that `iter()` provides immutable borrows to `v1`'s elements

---

# Iterators and Mutable Borrows
```rust
let mut vec = vec![1, 2, 3]; // Note we need vec to be mutable
let mut mutable_iter = vec.iter_mut();

while let Some(val) = mutable_iter.next() {
    *val += 1;
}

println!("{:?}", vec);
```
```
[2, 3, 4]
```
* Before we saw that `v1.iter()` gave us references to elements
* We can use `iter_mut()` for `&mut`

---

# Iterators and Ownership
```rust
let mut vec = vec![1, 2, 3];
let owned_iter = vec.into_iter(); // vec is consumed
for val in owned_iter {
    println!("{}", val);
}
// owned_iter is consumed
```
* To make an iterator that owns its values we have `into_iter()`
* This is what consuming for loops do under the hood

---

# 