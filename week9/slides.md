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

Let's say we wanted to make a recursive-style list:

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
* The compiler is complaining because we've defined a type with _infinite size_
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
  * Pointers have fixed size, so our enum is no longer of infinite size!
* We create a `Box<List>` with the `Box::new` associated function


---


# More about `Box<T>`

* `Box<T>` is a simple "smart" pointer to memory allocated on the heap*
  * It is "smart" because it frees the memory when dropped
* Other than the cost of allocation and pointer indirection, `Box` has no performance overhead
* `Box<T>` fully owns the data it points to (just like `Vec<T>`)


---


# When to use `Box<T>`

* When you have a type of unknown size **at compile time** (like `List`)
* When you have a large amount of data and want to transfer ownership
  * Transferring ownership of a pointer is faster than a large chunk of data
* Trait Objects
  * We'll get to this soon...


<!--
The reasoning for why transferring ownership is faster is that data
won't need to be copied to another stack for example, just the pointer.
-->

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

Rust is able to coerce mutable to immutable but not the reverse.

* From `&T` to `&U` when `T: Deref<Target=U>`
* From `&mut T` to `&mut U` when `T: DerefMut<Target=U>`
* From `&mut T` to `&U` when `T: Deref<Target=U>`
* For more information, consult the [Rustonomicon](https://doc.rust-lang.org/nomicon/dot-operator.html)


---

# `&T` to `&U` Example

```rust
fn foo(s: &[i32]) {
    print(s[0])
}

// Vec<T> implements Deref<Target=[T]>.
let owned = vec![1, 2, 3];

// Here we coerce &Vec<T> to &[T]
foo(&owned);

println!("{:?}", owned);
```

```
[1]
[1, 2, 3]
```

---

# `&mut T` to `&mut U` Example

```rust
fn foo(s: &mut [i32]) {
    s[0] += 1;
}

// Vec<T> implements DerefMut<Target=[T]>.
let mut owned = vec![1, 2, 3];

// Here we coerce &mut Vec<T> to &mut [T]
foo(&mut owned);

println!("{:?}", owned);
```

```
[2, 2, 3]
```

* `DerefMut` also allows coercing to &[T]

<!--

-->

---


# The `Drop` Trait

```rust
pub trait Drop {
    fn drop(&mut self);
}
```

* Values are dropped when they go out of scope
* Dropping a value will recursively drop all its fields by default
    * This mechanism allows automatically freeing memory
* You can also provide a custom implementation of `Drop` on your types
    * Allows us to run user code when values are dropped

<!--
first bullet: RAII
your types -> specifically types declared in the crate per the orphan rule
-->

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

* This is a custom implementation that simply prints the data on drop
* The data will still be freed automatically
    * This method does not include automatic memory freeing logic


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
# `Drop` Trait Usage

`Drop` trait implementations are typically not needed unless:
- You are manually managing memory
    - This likely involves using `unsafe` under the hood
- You need to do something special before a value is dropped
    - Might involve managing OS resources
    - Might involve signalling other parts of your codebase



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

* Rust won't let you explicitly call the drop trait method to avoid double drops


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
* What's the difference?


---


# `std::mem::drop`

Here is the actual source code of `std::mem::drop` in the standard library:

```rust
pub fn drop<T>(_x: T) {}
```

* It takes ownership of `_x`, and then `_x` reaches the end of the scope and is dropped
    * Hence, calling this function drops it, on demand!

<!--
This is beautiful!!
https://doc.rust-lang.org/src/core/mem/mod.rs.html#942
-->



---


# **Object Oriented Programming**

* Well...
    * Not quite...


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
* Encapsulation within `impl` blocks and crates
* Public and private functions and methods with `pub`


---


# Inheritence?
Rust structs cannot "inherit" the implementations of methods or data fields from another struct...
* If we want to wrap another struct's functionality, we can use composition
* If we want to define interfaces, we can use traits
* If we want polymorphism...
    * Rust has something called "trait objects"

<!--
Composition is usually preferred in other languages nowadays too
--->

---


# Polymorphism

* Polymorphism != Inheritance
* Polymorphism == "Code that can work with multiple data types"
* In object oriented languages, polymorphism is usually expressed with classes
* Rust expresses polymorphism with generics and traits:
  * Generics are abstract over different possible types
  * Traits impose constraints on what behaviors types must have


---


# Trait Objects

Trait objects allow us to store objects that implement a trait.

```rust
pub trait Window {
    fn draw(&self);
}

pub struct LaptopScreen {
    pub windows: Vec<Box<dyn Window>>,
}
```

* In this example, `LaptopScreen` holds a vector of `Window` objects
* We use the `dyn` keyword to describe any type that implements `Window`
    * In a `Box`, since objects implementing `Window` could be of any size at runtime


<!--
key: Not size at compile time
Note that converting a type into a trait object _erases_ the original type
-->

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


---


# Working With Trait Objects

```rust
struct Chrome {
    width: u32,
    height: u32,
    evil_tracking: bool
}

struct QBittorrent {
    width: u32,
    height: u32,
    color: String,
}

impl Window for Button { fn draw(&self) { ... } }
impl Window for SelectBox { fn draw(&self) { .. } }
```

* Say we have **multiple** types that implement `Window`


---


# Working With Trait Objects: Dynamic Dispatch

```rust
impl LaptopScreen {
    pub fn run(&self) {
        // `windows` is of type Vec<Box<dyn Window>>
        for window in self.windows.iter() {
            window.draw();
        }
    }
}
```

* This is different than if `windows` was `Vec<Chrome>`
  * The generic parameter (in `Vec`) is known at compile time.
* Trait objects allow for types to fill in for the trait object **at runtime**


---


# Generic Version

What about a version implemented with generics?

```rust
pub struct LaptopScreen<T: Window> {
    pub windows: Vec<T>,
}

impl<T> LaptopScreen<T>
where
    T: Window,
{
    pub fn run(&self) {
        for window in self.windows.iter() {
            window.draw();
        }
    }
}
```
* What is wrong with this version?
  * We can't create a `LaptopScreen` with two different types of windows in it

---

# Trait Objects: Mixing Objects

```rust
fn main() {
    let screen = LaptopScreen {
        windows: vec![
            Box::new(Chrome {
                width: 1280,
                width: 720,
                evil_tracking: true,
            }),
            Box::new(QBitTorrent {
                <-- snip -->
            }),
        ],
    };
    screen.run();
}
```

* This is not possible with the version using generics

---


# Aside: Dynamically Sized Types

* Recall that we needed a `Box<dyn Window>` before
* `dyn Window` is an example of a dynamically sized type (DST)
* DSTs have to be in a `Box`, because we don't know the size at compile time
    * A `dyn Window` could be a `Chrome` or `QBittorrent` object
    * How much space should we make on the stack?
* Pointers to DSTs are double the size (wide pointers)
  * Stores both a pointer to memory and a **vtable** pointer
    * If you're interested in more information, ask us after lecture!


---


# Next Lecture: Parallelism (probably)



![bg right:30% 80%](../images/ferris_happy.svg)

* Thanks for coming!
