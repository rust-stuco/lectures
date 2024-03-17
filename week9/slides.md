---
marp: true
theme: rust
class: invert
paginate: true
---

<!-- _class: communism invert  -->

## Intro to Rust Lang
# Box<T> and Trait Objects

<br>

Benjamin Owad, David Rudo, and Connor Tsui

<!-- ![bg right:35% 65%](../images/ferris.svg) -->


---

# Today: Box<T> and Trait Objects

- `Box<T>`
- The `Deref` and `Drop` trait
- Trait Objects
- Object Safety

---


# **Motivation for `Box<T>`**


---


# Let's Make a List

![bg right:30% 80%](../images/ferris_does_not_compile.svg)
Let's say we wanted to make recursive-style list
```rust
enum List {
  Cons(i32, List),
  Nil,
}

fn main() {
  // List of 1,2,3
  let list = Cons(1, Cons(2, Cons(3, Nil)));
}
```


---


# Cargo's Suggestion

```
error[E0072]: recursive type `List` has infinite size
 --> src/main.rs:1:1
  |
1 | enum List {
  | ^^^^^^^^^
2 |     Cons(i32, List),
  |               ---- recursive without indirection
  |
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```
- Rust is upset because we've defined a type with infinite size
- The suggestion provided is to use a `Box<List>`


---


# Indirection with `Box<T>`

* In the suggestion "indirection" means we store a *pointer* to a list rather than a list directly
  * Because a pointer has a fixed size our enum is no longer infinite!
* We create a `Box` with the `new` function
```rust
let singleton = Cons(1, Box::new(Nil));
let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
```


---


# Cost of `Box<T>`

* `Box<T>` is a simple smart pointer, it just allocates on the heap**
* Boxes don’t have performance overhead, other than storing their data on the heap
* They provide no other "special" capabilities


---


# When to use `Box<T>`

* When you have a type of unknown size **at compile time** and you need it's exact size
  * `List` from before

* When you have a large amount of data and want to transfer ownership and ensure no data is copied
  * Copying a pointer is faster than copying a large chunk of data

* When you want to own a value and you care only that it’s a type that implements a particular trait rather than being of a specific type
  * We'll get to this *soon*


---


# Using Values in the `Box`

```rust
fn main() {
    let x = 5;
    let y = Box::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```
* Just like reference we can derefernce a `Box<T>` to get `T`
* `Box<T>` implements the `Deref` trait which customizes the behavior of `*`


---


# `Deref` Trait

The deref trait is defined as follows:
```rust
pub trait Deref {
    type Target: ?Sized;

    // Required method
    fn deref(&self) -> &Self::Target;
}
```
* Behind the scenes `*y` is actually `*(y.deref())`
* Note this does not recurse infinitely
* We are now able to treat smart pointers just like regular pointers!


---


# Deref Coercion
* Convert a reference to a type that implements the Deref trait into a reference to another type
  * Example: deref coercion can convert `&String` to `&str` because `String` implements the Deref trait such that it returns `&str`

```rust
fn hello(name: &str) {
    println!("Hello, {name}!");
}

fn main() {
    let m = Box::new(String::from("Rust"));
    hello(&m);
}
```
* Here we see `Box<String>` deref coerces to `&str`


---


# Deref Coercion Rules

* From `&T` to `&U` when `T: Deref<Target=U>`
* From `&mut T` to `&mut U` when `T: DerefMut<Target=U>`
* From `&mut T` to `&U` when `T: Deref<Target=U>`

Note Rust will coerce mutable to immutable but not the reverse


---


# &mut T to &mut U Example
```rust
fn foo(s: &mut [i32]) {
    // Borrow a slice for a second.
}

// Vec<T> implements Deref<Target=[T]>.
let mut owned = vec![1, 2, 3];

foo(&mut owned);
```


---


# &mut T to &U Example

```rust
fn foo(s: &[i32]) {
    // Borrow a slice for a second.
}

// Vec<T> implements Deref<Target=[T]>.
let mut owned = vec![1, 2, 3];

foo(&mut owned);
```

---


# The Drop Trait
* Determines what happens when value goes out of scope (dropped)
* You can provide an implementation of `Drop` on any type
* This is how Rust doesn't need you to carefully clean up memory


---


# Drop Trait Example

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}
```


---


# Drop Trait In
```rust
fn main() {
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };
    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    };
    println!("CustomSmartPointers created.");
}
```
```
CustomSmartPointers created.
Dropping CustomSmartPointer with data `other stuff`!
Dropping CustomSmartPointer with data `my stuff`!
```
* Items are dropped in reverse order of creation


---


# Dropping Manually

![bg right:30% 80%](../images/ferris_does_not_compile.svg)
```rust
fn main() {
  let c = CustomSmartPointer {
      data: String::from("some data"),
  };
  println!("CustomSmartPointer created.");
  c.drop();
  println!("CustomSmartPointer dropped before the end of main.");
}
```

```
error[E0040]: explicit use of destructor method
  --> src/main.rs:16:7
   |
16 |     c.drop();
   |     --^^^^--
   |     | |
   |     | explicit destructor calls not allowed
   |     help: consider using `drop` function: `drop(c)`
```
* Rust won't let you explicitly call the drop function to avoid double drops


---


# Dropping Manually
```rust
fn main() {
  let c = CustomSmartPointer {
      data: String::from("some data"),
  };
  println!("CustomSmartPointer created.");
  drop(c);
  println!("CustomSmartPointer dropped before the end of main.");
}
```
* This code works since we use `std::mem::drop` instead
  * This is different that calling `c.drop()`
* You can think of this as `drop` taking ownership of `c` and dropping it
  * Actual source code: `pub fn drop<T>(_x: T) {}`


---


# **Object-Oriented Features of Rust**


---


# Disclaimer
* Rust's classifaction as an OOP language is debated
  * Both by definers of OOP and (probably) the instructors
* This section is not an endorsement of OOP
* We will discuss **real** polymorphism (You're welcome type nerds)


---





---


# Next Lecture: ISD

*Instructors still debating*

![bg right:30% 80%](../images/ferris_happy.svg)

* Thanks for coming!
