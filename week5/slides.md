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


# Today: Error Handling and Traits

* Const generic types
* Rust's error handling mechanisms
    * `Result<V,E>`
    * `panic!`
* The never type
* Traits
    * Trait bounds
    * `Copy` vs `Clone`
    * Super traits


---

# Const Generics

```rust
struct ArrayPair<T, const N: usize> {
    left: [T; N],
    right: [T; N],
}
```
Const generics are arguments that generic over constant values, rather than types.


---


# Const Generics Rules

Currently, const parameters may only be instantiated by const arguments of the following forms:

* A standalone const parameter
* A literal (i.e. an integer, bool, or character)
* A concrete constant expression (enclosed by {}), involving no generic parameters


---


# A Const Parameter

Currently, const parameters may only be instantiated by const arguments of the following forms:

1. A standalone const parameter
2. A literal (i.e. an integer, bool, or character)
3. A concrete constant expression (enclosed by {}), involving no generic parameters


---


# Standalone Const Parameter
```rust
fn foo<const N: usize>() {}

fn bar<T, const M: usize>() {
    foo::<M>(); // Okay: `M` is a const parameter
    let _: [u8; M]; // Okay: `M` is a const parameter
}
```


---


# A Literal
```rust
fn foo<const N: usize>() {}

fn bar<T, const M: usize>() {
    foo::<2021>(); // Okay: `2021` is a literal
}

```


---


# A Concrete Constant Expression
```rust
fn foo<const N: usize>() {}

fn bar<T, const M: usize>() {
    foo::<{20 * 100 + 20 * 10 + 1}>(); // Okay: const expression
                                       // contains no generic parameters

    foo::<{ M + 1 }>(); // Error: const expression
                        // contains the generic parameter `M`

    foo::<{ std::mem::size_of::<T>() }>(); // Error: const expression
                                           //contains the generic parameter `T`

    let _: [u8; std::mem::size_of::<T>()]; // Error: const expression
                                           // contains the generic parameter `T`
}

```


---


# Advantages of Const Generics

* Generalize behavior for larger set of types
* Let us avoid some runtime checks (less overhead)
```rust
pub struct MinSlice<T, const N: usize> {
    /// The bounded region of memory. Exactly `N` `T`s.
    pub head: [T; N],
    /// Zero or more remaining `T`s after the `N`
    pub tail: [T],
}

fn main() {
    let slice: &[u8] = b"Hello, world";
    // Length check is performed when we construct a MinSlice,
    // and it's known at compile time to be of length 12.
    // If the `unwrap()` succeeds, no more checks are needed
    let minslice = MinSlice::<u8, 12>::from_slice(slice).unwrap();
    let value: u8 = minslice.head[6];
    assert_eq!(value, b' ')
}
```


---


# Const Generic Designs

Const generics can be used to create multiple versions of the same function with slightly different behavior. One popular way of doing this is letting const generics represent "option flags" for a function.

```rust
fn git_commit<const FORCE : bool, const NO_MESSAGE : bool>() {
    ...
    if FORCE {...}
}
```

This design pattern will become more useful when we discuss closures and function pointers.


---


# **Error Handling**


---


# What `type_of` Error?

In Rust there are two main types of errors we care about: recoverable and unrecoverable errors (panics).
* `Result<V, E>` - A return type for recoverable errors
* `panic!` - A macro (*notice the `!`*) to invoke unrecoverable errors

![bg right:25% 75%](../images/ferris_panics.svg)


---


# The Result Type
This is how Rust represents "success" and "failure" states in code.
```rust
enum Result<V, E> {
    Ok(V),
    Err(E),
}
```


---


## Example Representing Errors
```rust
fn integer_divide(a: i32, b: i32) -> Result<i32, String> {
    Err("Divide by zero") if b == 0 else Ok(a/b)
}
```

```rust
enum ArithError { // Dedicated Error enums is a common practice
    DivideByZero,
    IllegalShift(i32)
}

fn shift_and_divide(x: i32, div: i32, shift: i32) -> Result<i32, ArithError> {
    if shift <= 0 {
        Err(IllegalShift(shift))
    } else if div == 0 {
        Err(DivideByZero)
    } else {
        (x << shift)/div
    }
}
```


---


# The ? Operator

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


# The ? Operator Example 
```rust
use std::num::ParseIntError;

fn multiply(first_number_str: &str, second_number_str: &str) -> Result<i32, ParseIntError> {
    let first_number = first_number_str.parse::<i32>()?;
    let second_number = second_number_str.parse::<i32>()?;

    Ok(first_number * second_number)
}

fn print(result: Result<i32, ParseIntError>) {
    match result {
        Ok(n)  => println!("n is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    print(multiply("10", "2"));
    print(multiply("ten", "2"));
}
```


---


# The ? Operator

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


# Panics

Panics in Rust are unrecoverable errors. They can happen in many different ways:
* Out of bounds slice indexing
* Integer overflow (debug)
* `.unwrap()` on a `None` or `Err`
* Calls to the `panic!` macro


---


# More Panics

- `assert!`, `assert_eq!`, `assert_ne!` conditionally panic

There also some more uncommon, but useful macros that panic:
- `unimplemented!` / `todo!` - self documented
- `unreachable!` - Lets the compiler optimize a code segment away


---


# Using `expect()` w/ Panics

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


# Using `expect()` w/ Panics

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


# Functions that never return

Consider the following code, what should the type of `x` be?
```rust
let x = loop { println!("forever"); };
```


---


# The "Never" Type - `!`

It isn't clear, right? That's why Rust has a special type called `!` for this exact reason.
Another example:
```rust
fn bar() -> ! {
    loop {}
}
```


---


# What's the point?

Why have a type that never has a value? Consider the following
```rust
let guess: u32 = match guess.trim().parse() {
    Ok(num) => num,
    Err(_) => continue,
};
```
Recall match statements can only return 1 type. So what's happening here? Well, `continue` has the `!` type. And so Rust knows this can't be value and allows
`guess: u32`.


---


# What else uses `!`?

Recall that `()` is a value! So `print!` and `assert!` don't use `!`.

* `panic!`
* `break`
* `continue`
* Everything that doesn't return a value -- typically control flow related.


---


# Pop Quiz

What should the type of `x` be?
```rust
let x = {
    return 123
};
```


---


# Answer

`return` is also type `!`. So Rust views it as  `let x : ! = ...`.

Think of it like this because `return` returns from the **entire function**, `x` can be given type `!`


---


# **Traits**


---


# Trait Overview

A `trait` is a collection of methods defined for an unknown type: `Self`. They can access other methods declared in the same trait.

Traits are defined with the `trait` keyword:
```rust
trait Shape {
    // Associated function signature; `Self` refers to the implementor type.
    fn new_unit() -> Self;

    // Method signature to be implemented by a struct.
    fn area(&self) -> f32;

    fn name(&self) -> String;
```


---


# Trait Overview
Traits can also provide a default implementation of functions. They can be overriden for any given `impl Shape for MyStruct`
```rust
    // Default method implementation -- can be overriden
    fn print(&self) {
        println!("{} has an area of {}", self.name(), self.area());
    }
} // end Trait Shape
```


---


# Trait Overview

So how do we use traits? We `impl`ement them `for` a `struct`
```rust
struct Rectangle {
    height: f32,
    width: f32
}

impl Shape for Rectangle {
    // Notice how 'Self' is now 'Rectangle' since it's the implementor
    fn new_unit() -> Rectangle {
        Rectangle { height: 1.0, width: 1.0 }
    }

```


---


# Trait Overview
We can simply override functions as such:
```rust
    fn print(&self) {
        println!("I am a rectangle! :)");
    }
}
```


---


# Traits in Action

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

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


---


# Traits in Action

![bg right:25% 80%](../images/ferris_happy.svg)

```rust
let rec: Rectangle = Shape::new_unit();
```
Traits, even those that define their functions, cannot be constructed directly. To use the `Shape` trait, Rust must know who is implementing it.

Similar in style to:
- Interfaces
- Abstract/virtual classes

---


# Type Aliases

Rust gives us a way to declare a type alias i.e. give a name to an already existing type.
```rust
type Kilometers = i32;

let x: i32 = 5;
let y: Kilometers = 5;

println!("x + y = {}", x + y); // Rust knows the types are really the same
```


---


# Advanced Traits

We'll look at the common `Iterator` trait which uses an *associated type* `Item`.
```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;
}
```


---


# Advanced Traits

Here we see the associated type `Item` being defined for a particular instance. This means the `Iterator` trait can be defined for any `Item` depending on the collection.
```rust
impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        // --snip--
```


---


# Why Not Use Generics?

Some of you may be wondering why the Rust std library doesn't define the `Iterator` trait like this:
```rust
pub trait Iterator<T> {
    fn next(&mut self) -> Option<T>;
}
```
There's nothing technically wrong with this -- it will compile.

Here's the issue, it would be possible to implement both `Iterator<i64> for Counter` **and** `Iterator<u32> for Counter` !


---


# Why Is This Bad?

When we use the `next()` method on `Counter`, we would have to provide type annotations to indicate which implementation of `Iterator` we want to use.

By using an associated type, we only implement `Iterator` once -- Note that we can define `Item` to be a generic type instead.

Associated types also become part of the trait’s contract: implementors of the trait must provide a type to stand in for the associated type placeholder. Associated types often have a name that describes how the type will be used, and documenting the associated type in the API documentation is good practice.


---


# Derive Traits

The compiler is capable of providing basic implementations for some traits via the
`#[derive]` attribute. These traits can still be manually implemented if a more complex behavior is required.

Here's a list
- Comparison traits: `Eq`, `PartialEq`, `Ord`, `PartialOrd`.
- `Clone`, to create `T` from `&T` via a copy.
- `Copy`, to give a type 'copy semantics' instead of 'move semantics'.
- `Hash`, to compute a hash from `&T`.
- `Default`, to create an empty instance of a data type.
- `Debug`, to format a value using the `{:?}` formatter.


---


# Copy

Recall `copy` only applies to:
- All integer types: `u8`, `i32`, etc
- `bool`
- All floating point types: `f32`, `f64`, etc
- `char` type

It is a differentiator in whether or not move semantics are applied to a function. (aka pass by reference vs value)


---


# Clone

* Means the type can be duplicated
* Creates a new value with the same information as the original.
* The new value is independent of the original value and can be modified without affecting the original value.
```rust
let mut foo = vec![1, 2, 3];
let mut foo2 = foo.clone(); // explicit duplication of an object

foo.push(4); // foo = [1,2,3,4]
let y = foo2.pop(); // y=3, foo2 = [1, 2]
```

---


# Clone vs Copy

Although their end result may feel the same they are different:

Copy
* Copies happen implicitely ex: `x = y`
* Copy cannot be overloaded it is always a simple bitwise copy

Clone
* Cloning is an explicit action `x.clone()`
* `Clone` can provide any type-specific behavior necessary to duplicate values safely.
    * An example of this is for `String`, `Clone` would need to copy not just the pointer but the data on the heap.

---


# So How Do You `#[derive]` Clone?

Any type made out of types that implement `Clone` can use the `#[derive]` -- This is a general rule for derivation.

Example:
```rust
#[derive(Clone)]
pub struct Cat {
    age: u32,
    name: String
}
```
Note how in this example `Cat` can't implement `Copy` since a `String` can't be copied.


---


# A Brief Break w/ Super Traits

Rust doesn't have "inheritence", but you can define a trait as being a superset of another trait.

```rust
trait Person {
    fn name(&self) -> String;
}

trait Student: Person {
    fn university(&self) -> String;
}
```
`Person` is a supertrait of Student. This means implementing `Student` requires you to also `impl Person`.


---


# Even Superer Traits

```rust
trait Programmer {
    fn fav_language(&self) -> String;
}

// CompSciStudent is a subtrait of both Programmer
// and Student.
trait CompSciStudent: Programmer + Student {
    fn git_username(&self) -> String;
}
```
We can make a trait a subtrait of multiple traits with the `+` operator. Implementing CompSciStudent will now require you to `impl` both supertraits.


---


# What Can `#[derive]` Copy?

Any type made out of types that implement Copy or a it holds a shared reference `&T`.

**Clone is a supertrait of Copy**
So if we want to derive one, we have to derive the other.

```rust
#[derive(Clone, Copy)]
pub struct Cat {
    age: u32,
    name: &'static str // reference to a string literal
}
```


---


# When `#[derive]` Fails

Sometimes we can't derive a trait, or need a more complex behavior than what the
`#[derive]` will provide.
1. Look at the standard library documentation for the trait
2. Find out what the required functions are and `impl` them like any trait


---


# Example: `Default`

`std::default::Default`
```rust
pub trait Default: Sized {
    // Required method
    fn default() -> Self;
}

struct SomeOptions {
    foo: i32,
    bar: f32,
}
```


---


# Example: `Default`

```rust
impl Default for SomeOptions {
    fn default() -> Self {
        SomeOptions {
            foo: 12,
            bar: 20.0,
        }
    }
}
```


---


# The Orphan Rule

Rust has a rule that you cannot provide implementations of a trait for a struct unless:
-  You are the crate that defines the struct
- You are the crate that defines the trait.

What does this mean? Well it means we can't apply traits like `Clone` on a stdlib type since we neither define `Clone` nor the stdlib type (such as `String` or `Box`)


---


# Trait Mix Ups

Consider the following
```rust
trait Pilot {
    fn fly(&self);
}

trait Wizard {
    fn fly(&self);
}

struct Human;
```


---


# Trait Mix Ups

```rust
impl Pilot for Human {
    fn fly(&self) {
        println!("This is your captain speaking.");
    }
}

impl Wizard for Human {
    fn fly(&self) {
        println!("Up!");
    }
}

impl Human {
    fn fly(&self) {
        println!("*waving arms furiously*");
    }
}
```


---


# Trait Mix Ups

What happens here?
```rust
fn main() {
    let person = Human;
    person.fly();
}
```


---


# Trait Mix Ups

```rust
fn main() {
    let person = Human;
    person.fly();
}
```
`*waving arms furiously*` - Rust used `.fly()` from `Human`.


How do we call every version of `.fly()`?
```rust
fn main() {
    let person = Human;
    Pilot::fly(&person); // fly takes &self as a parameter
    Wizard::fly(&person);
    person.fly();
}
```


---


# Even Worse Trait Mix Ups

Last time we got lucky because `fly` took `&self` as a parameter. What would we do if that wasn't the case?

```rust
fn main() {
    let person = Human;
    <person as Pilot>::fly();
    <person as Wizard>::fly();
    person.fly();
}
```

This is considered the *fully qualified syntax* of a trait.


---


# Trait Bounds

If your function is generic over a trait but you don't mind the specific type, you can simplify the function declaration using `impl Trait` as the type of the argument.

Instead of
```rust
fn get_csv_lines<R: std::io::BufRead>(src: R) -> u32
```
We can write:
```rust
fn get_csv_lines(src: impl std::io::BufRead) -> u32
```


---


# Trait Bounds

If your function returns a type that implements `MyTrait`, you can write its return type as `-> impl MyTrait`. This can help simplify your type signatures a lot!

```rust
fn combine_vecs(
    v: Vec<i32>,
    u: Vec<i32>,
) -> impl Iterator<Item=i32>
```


---


# `where` Clauses

Trait bounds are awesome, but sometimes too many can be a problem.

```rust
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```
This can be cumbersome to write up so we have `where` clauses!
```rust
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{
```
Now we don't need ultrawide monitors to code in Rust!


---


# Conditionally Implement Methods

Say we have a struct `Pair`.
```rust
use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Self { x, y }
    }
}
```


---


# Conditionally Implement Methods

```rust
impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("The largest member is x = {}", self.x);
        } else {
            println!("The largest member is y = {}", self.y);
        }
    }
}
```
For `cmp_display()` to work, `T` must implement `Display` to be printed and `PartialOrd` to be compared. So `cmp_display` will exist for a `Pair<i32>` but not for `Pair<T: !PartialOrd>`


---


# **Next Lecture: Cargo, Testing, Modules, and Crates**

![bg right:30% 80%](../images/ferris_happy.svg)

Thanks for coming!
