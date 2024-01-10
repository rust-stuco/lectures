---
marp: true
theme: default
class: invert
paginate: true
---

# Intro to Rust Lang

# **Error Handling and Traits**

<br>

Benjamin Owad, David Rudo, and Connor Tsui

![bg right:35% 65%](../images/ferris.svg)


---


# **What `type_of` Error?**
In Rust there are two main types of errors we care about: recoverable and unrecoverable errors (panics).
* `Result<V, E>` - A return type for recoverable errors
* `panic!` - A macro (*notice the `!`*) to invoke unrecoverable errors

![bg right:30% 80%](../images/ferris_panics.svg)

---


# **The Result Type**
This is how Rust represents "success" and "failure" states in code.
```rust 
enum Result<V, E> {
    Ok(V),
    Err(E),
}
```
## Example with error messages
```rust
fn integer_divide(a : i32, b : i32) -> Result<i32, String> {
    Err("Divide by zero") if b == 0 else Ok(a/b)
}
```

---


# **The ? Operator**
The `?` operator when applied to a result type, unwraps it on a `Ok` and propogates the error up one in the call stack otherwise.

For clarity:
```rust
let x = potential_fail()?;
```
de-sugars to
```rust
let x = match potential_fail() {
    Ok(v) => v
    Err(e) => return Err(e.into()), // Error is propogated up a level
}
```
Think of the `?` as quick way to see where a function short-circuit returns on failure

---
# **The ? Operator**
We can also chain multiple `?` together:
```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username = String::new();

    File::open("hello.txt")?.read_to_string(&mut username)?;

    Ok(username)
}
```

---

# **Panics**
Panics in Rust are unrecoverable errors. They can happen in many different ways:
* Out of bounds slice indexing
* Integer overflow (debug)
* `.unwrap()` on a `None` or `Err`
* Calls to the `panic!` macro
    - `assert!`, `assert_eq!`, `assert_ne!` conditionally panic

There also some more uncommon, but useful macros that panic:
- `unimplemented!` / `todo!`
- `unreachable!` - Lets the compiler optimize a code segment away
---

# **Using `expect()` w/ Panics**
Consider the following example from the Rust book:
```rust
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt").unwrap();
}
```
What happens if we don't have `"hello.txt"`?
```
thread 'main' panicked at 'called `Result::unwrap()` on an `Err` value: Os {
code: 2, kind: NotFound, message: "No such file or directory" }',
src/main.rs:4:49
```

---

# **Using `expect()` w/ Panics**
We can do better than this. If we *expect* this error and have a specific message in mind.
```rust
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt")
        .expect("hello.txt should be included in this project");
}
```
Now we get:
```
thread 'main' panicked at 'hello.txt should be included in this project: Os {
code: 2, kind: NotFound, message: "No such file or directory" }',
src/main.rs:5:10
```

---

# **Traits**

---

# **Trait Overview**
A `trait` is a collection of methods defined for an unknown type: `Self`. They can access other methods declared in the same trait.

Traits are defined with the `trait` keyword:
```rust
trait Shape {
    // Associated function signature; `Self` refers to the implementor type.
    fn new_unit() -> Self;

    // Method signature to be implemented by a struct.
    fn area(&self) -> f32;

    fn name(&self) -> String;

    // Default method implementation -- can be overriden
    fn print(&self) {
        println!("{} has an area of {}", self.name(), self.area());
    }
}
```

---
# **Trait Overview**
So how do we use traits? We `impl`ement them `for` a `struct`
```rust
struct Rectangle {
    height : f32,
    width : f32
}

impl Shape for Rectangle {
    // Notice how 'Self' is now 'Rectangle' since it's the implementor
    fn new_unit() -> Rectangle { 
        Rectangle { height : 1.0, width : 1.0 }
    }

    ...
    
    // We can override functions defined in the trait 
    fn print(&self) {
        println!("I am a rectangle! :)");
    }
}
```

---

# **Traits in Action**
What happens we try and construct a `Rectangle`?
```rust
let rec = Shape::new_unit();
```

```
error[E0790]: cannot call associated function on trait 
without specifying the corresponding `impl` type
  --> src/main.rs:43:15
   |
8  |     fn new_unit() -> Self;
   |     ---------------------- `Shape::new_unit` defined
```
![bg right:30% 80%](../images/ferris_does_not_compile.svg)

---

# **Traits in Action**
```rust
let rec : Rectangle = Shape::new_unit();
```
Traits, even those that define their functions, cannot be constructed directly. To use the `Shape` trait, Rust must know who is implementing it.

Similar in style to:
- Interfaces
- Abstract/virtual classes

---

# **Advanced Traits**
We'll look at the common `Iterator` trait which uses an *associated type* `Item`.
```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;
}
```

---

# **Advanced Traits**
Here we see the associated type `Item` being defined for a particular instance. This means the `Iterator` trait can be defined for any `Item` depending on the collection.
```rust
impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        // --snip--
```

---

# **Why Not Use Generics?**
Some of you may be wondering why the Rust std library doesn't define the `Iterator` trait like this:
```rust
pub trait Iterator<T> {
    fn next(&mut self) -> Option<T>;
}
```
There's nothing technically wrong with this -- it will compile. 

Here's the issue, it would be possible to implement both `Iterator<i64> for Counter` **and** `Iterator<u32> for Counter` !

---

# **Why Is This Bad?**
When we use the `next()` method on `Counter`, we would have to provide type annotations to indicate which implementation of `Iterator` we want to use.

By using an associated type, we only implement `Iterator` once -- Note that we can define `Item` to be a generic type instead.

Associated types also become part of the trait’s contract: implementors of the trait must provide a type to stand in for the associated type placeholder. Associated types often have a name that describes how the type will be used, and documenting the associated type in the API documentation is good practice.

---

# **Derive Traits**
The compiler is capable of providing basic implementations for some traits via the `#[derive]` attribute. These traits can still be manually implemented if a more complex behavior is required.

Here's a list
- Comparison traits: `Eq`, `PartialEq`, `Ord`, `PartialOrd`.
- `Clone`, to create `T` from `&T` via a copy.
- `Copy`, to give a type 'copy semantics' instead of 'move semantics'.
- `Hash`, to compute a hash from `&T`.
- `Default`, to create an empty instance of a data type.
- `Debug`, to format a value using the `{:?}` formatter.

---

# **Copy**
Recall `copy` only applies to:
- All integer types: `u8`, `i32`, etc
- `bool`
- All floating point types: `f32`, `f64`, etc
- `char` type

It is a differentiator in whether or not 

---

# **Next Lecture:**

![bg right:30% 80%](../images/ferris_happy.svg)

Thanks for coming!
