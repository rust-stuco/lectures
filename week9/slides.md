---
marp: true
theme: rust
class: invert
paginate: true
---

<!-- _class: communism communism2 invert  -->

## Intro to Rust Lang
# Smart Pointers and Trait Objects

<br>

#### Benjamin Owad, David Rudo, and Connor Tsui

<!-- ![bg right:35% 65%](../images/ferris.svg) -->


---


# Today: Smart Pointers and Trait Objects

- `Box<T>`
- The `Deref` and `Drop` trait
- Trait Objects
- Smart Pointers


---


# **Motivation for `Box<T>`**


---


# Let's Make a List

![bg right:30% 80%](../images/ferris_does_not_compile.svg)

Let's say we wanted to make recursive-style list:

```rust
enum List {
  Cons(i32, List),
  Nil,
}

fn main() {
  // List of [1, 2, 3]
  let list = Cons(1, Cons(2, Cons(3, Nil)));
}
```


---


# The Compiler's Suggestion

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
* Rust is upset because we've defined a type with _infinite size_
* The suggestion is to use a `Box<List>`


---


# Indirection with `Box<T>`

```rust
let singleton = Cons(1, Box::new(Nil));
let list = Cons(1, Box::new(Cons(2,
                     Box::new(Cons(3,
                       Box::new(Nil))))));
```

* In the suggestion, "indirection" means we store a _pointer_ to a `List` rather than an entire `List`
  * Pointers have fixed size, so our enum is no longer infinite!
* We create a `Box<List>` with the `Box::new` associated function


---


# More about `Box<T>`

* `Box<T>` is a simple "smart" pointer to memory allocated on the heap*
  * It is "smart" because it frees the memory when dropped
* Other than the cost of allocation and pointer indirection, `Box`es has no performance overhead
* `Box<T>` fully owns the data it points to (just like `Vec<T>`)


---


# When to use `Box<T>`

* When you have a type of unknown size **at compile time** (like `List`)
* When you have a large amount of data and want to transfer ownership
  * Copying a pointer is faster than copying a large chunk of data
  * Moving a `Box<T>` ensures no data is cloned
* Trait Objects
  * We'll get to this soon...


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
* Just like a reference we can dereference a `Box<T>` to get `T`
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
* We can treat anything that implements `Deref` like a pointer!


---


# Deref Coercion

Recall that we were able to coerce a `&String` into a `&str`. We can also coerce a `&Box<String>` into a `&str`!

```rust
fn hello(name: &str) {
    println!("Hello, {name}!");
}

fn main() {
    let m = Box::new(String::from("Rust"));
    hello(&m);
}
```

* Deref coercion converts a `&T` into `&U` if `Deref::Target = U`
* Example: Deref coercion can convert a `&String` into `&str`
  * `String` implements the `Deref` trait such that `Deref::Target = &str`



---


# Deref Coercion Rules

Note that Rust will coerce mutable to immutable but not the reverse.

* From `&T` to `&U` when `T: Deref<Target=U>`
* From `&mut T` to `&mut U` when `T: DerefMut<Target=U>`
* From `&mut T` to `&U` when `T: Deref<Target=U>`
* For more information, consult the [Rustonomicon](https://doc.rust-lang.org/nomicon/dot-operator.html)


---


# `&mut T` to `&mut U` Example

```rust
fn foo(s: &mut [i32]) {
    s[0] += 1;
}

// Vec<T> implements DerefMut<Target=[T]>.
let mut owned = vec![1, 2, 3];

foo(&mut owned);

println!("{:?}", owned);
```

```
[2, 2, 3]
```

* The immutable `Deref` would look similar, but with an immutable `&` reference


---


# The `Drop` Trait

We've talked about how things magically get freed when they go out of scope, but in reality, it is the work of the `Drop` trait.

```rust
pub trait Drop {
    fn drop(&mut self);
}
```

* Determines what happens when value goes out of scope (dropped)
* You can provide an implementation of `Drop` on any type you create
* With `Drop`, you never have to manually clean up your memory!


---


# `Drop` Trait Example

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping `CustomSmartPointer` with data `{}`!", self.data);
    }
}
```


---


# `Drop` Trait Example

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
* Notice how values are dropped in reverse order of creation


---


# Manual Drop

![bg right:30% 80%](../images/ferris_does_not_compile.svg)

What if we want to manually drop a value before the end of the scope?

```rust
let csm = CustomSmartPointer {
    data: String::from("some data"),
};
println!("CSM created.");

csm.drop();

println!("CSM dropped before the end of the scope");
```


---


# Manual Drop

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


# Manual Drop

```rust
let csm = CustomSmartPointer {
    data: String::from("some data"),
};
println!("CSM created.");

std::mem::drop(csm);

println!("CSM dropped before the end of the scope");
```

* This code works since we use `std::mem::drop` instead
  * This is different that calling `c.drop()`
* You can think of this as `drop` taking ownership of `c` and dropping it...


---


# `std::mem::drop`

Here is the actual source code of `std::mem::drop` in the standard library:

```rust
pub fn drop<T>(_x: T) {}
```

* https://doc.rust-lang.org/src/core/mem/mod.rs.html#942


---


# **Object Oriented Programming**

* oops!


---


# What We Know So Far...

```rust
pub struct AveragedCollection {
    list: Vec<i32>,
    average: f64,
}

impl AveragedCollection {
    pub fn add(&mut self, value: i32) {
        self.list.push(value);
        self.update_average();
    }

    <-- snip -->
}
```
* Encapsulation with `impl` blocks
* Public and private methods with crates and `pub`


---


# Inheritence?

* Rust structs cannot "inherit" the implementations of methods or data fields from another struct
* If we want to re-use code, we use traits
* If we want polymorphism...
  * Rust has something called "trait objects"


---


# Polymorphism

* Polymorphism != Inheritance
* Polymorphism == "Code that can work with multiple data types"
* For OOP languages, polymorphism is usually seen in the form of `Class`es
* Rust polymorphism includes generics and traits:
  * Generics are abstract over different possible monomorphized types
  * Trait bounds impose constraints on what behaviors types must have


---


# Trait Objects

Trait objects allow us to store objects that implement a trait.

```rust
pub trait Draw {
    fn draw(&self);
}

pub struct Screen {
    pub components: Vec<Box<dyn Draw>>,
}
```

* In this example, `Screen` holds a vector of `Draw`able objects
* We use the `dyn` keyword to describe any type that implements `Draw`
* We need to use a `Box` since Rust doesn't know the size of the type implementing `Draw`
* Note that converting a type into a trait object _erases_ the original type


---


# Trait Objects and Closures

Since closures implement the `Fn` traits, they can be represented as trait objects!

```rust
fn returns_closure() -> Box<dyn Fn(i32) -> i32> {
    Box::new(|x| x + 1)
}

fn main() {
    let closure = returns_closure();
    print!("{}", closure(5)); // prints 6
}
```

* We can use trait objects to return dynamic types
* Deref coercion happening in the background to keep ergonomics clean!


----


# Working With Trait Objects

```rust
impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

* Note that this is different than a struct that uses trait bounds
  * A generic parameter can only be substituted with one type at a time
* Trait objects allow for many types to fill in for the trait object **at runtime**


---


# Generic Version

```rust
pub struct Screen<T: Draw> {
    pub components: Vec<T>,
}

impl<T> Screen<T>
where
    T: Draw,
{
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```
* What's wrong with this version?
  * We can't draw a screen with different types of components on it


---


# Dynamically Sized Types

* Recall that we needed a `Box<dyn Draw>` before.
* `dyn Draw` is an example of a dynamically sized type (DST)
* Pointers to DSTs are double the size (wide pointers)
  * Stores both a pointer to memory and a **vtable** pointer
    * If you're interested in what this is, ask us after lecture!


---


# Next Lecture: ISD

*Instructors still debating*


![bg right:30% 80%](../images/ferris_happy.svg)

* Thanks for coming!
