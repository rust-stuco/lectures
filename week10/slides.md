---
marp: true
theme: rust
class: invert
paginate: true
---

<!-- _class: communism communism2 invert  -->

## Intro to Rust Lang
# Smart Pointers

<br>

Benjamin Owad, David Rudo, and Connor Tsui

<!-- ![bg right:35% 65%](../images/ferris.svg) -->


---

# Today: Box<T> and Trait Objects

- `Rc<T>`
- `RefCell<T>`
- Interior Mutability
- Memory Leaks

---


# **Motivation for `Rc<T>`**


---


# Let's Make a List (again)

![bg right:30% 80%](../images/ferris_does_not_compile.svg)
Let's say we wanted to make recursive-style list with `Box` like before
```rust
enum List {
  Cons(i32, Box<List>),
  Nil,
}

use crate::List::{Cons, Nil};

fn main() {
  let a = Cons(5, Box::new(Cons(10, Box::new(Nil))));
  let b = Cons(3, Box::new(a));
  let c = Cons(4, Box::new(a));
}
```


---


# Cargo's Suggestion

```
   Compiling cons-list v0.1.0 (file:///projects/cons-list)
error[E0382]: use of moved value: `a`
  --> src/main.rs:11:30
   |
9  |     let a = Cons(5, Box::new(Cons(10, Box::new(Nil))));
   |         - move occurs because `a` has type `List`, which does not implement the `Copy` trait
10 |     let b = Cons(3, Box::new(a));
   |                              - value moved here
11 |     let c = Cons(4, Box::new(a));
   |                              ^ value used here after move

```
* `Cons` needs to **own** the data it holds (Recall: `Box`)
* Using `a` again when creating `c`, but `a` has been moved


---


# References?

```rust
enum List<'a> {
    Cons(i32, &'a List<'a>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
  let nil = Nil;
  let a = Cons(10, &nil);
  let b = Cons(5, &a);
  let c = Cons(3, &a);
  let d = Cons(4, &a);
}
```
* While it can be done, it's a little messy
* Now we have to deal with lifetimes... gross


---


# Introducing `Rc<T>`

```rust
enum List {
  Cons(i32, Rc<List>),
  Nil,
}

use crate::List::{Cons, Nil};
use std::rc::Rc;

fn main() {
  let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
  let b = Cons(3, Rc::clone(&a));
  let c = Cons(4, Rc::clone(&a));
}
```
* Short for reference counter
* keeps track of the number of references to a value to determine dropping


---


# When to use `Rc<T>`

* Allocate data on the heap for *multiple* parts of our program to *read*
  * Can’t determine at compile time which part will use the data last
* Only used for single threaded scenarios (We'll talk about `Arc<T>` next week)
* Use `Rc::new(T)` to create a new `Rc<T>`
  * `Rc::clone()` isn't a deep clone, it increments the ref counter


---


# Cloning Demonstrated

```rust
fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    println!("count after creating a = {}", Rc::strong_count(&a));

    let b = Cons(3, Rc::clone(&a));
    println!("count after creating b = {}", Rc::strong_count(&a));
    
    {
        let c = Cons(4, Rc::clone(&a));
        println!("count after creating c = {}", Rc::strong_count(&a));
    }
    println!("count after c goes out of scope = {}", Rc::strong_count(&a));
}
// Rc::strong_count(&a) is now 0, cleaned up and dropped
```
```
count after creating a = 1
count after creating b = 2
count after creating c = 3
count after c goes out of scope = 2
```


---


# `Rc<T>` Recap

* Great for sharing **immutable** references without lifetimes
* Should be used when last variable to use the data is unknown
  * Otherwise, make that variable the owner and have everything borrow
* Provides almost no overhead
  * O(1) increment of counter
  * Potential allocation/de-allocation on heap


---



# **`RefCell<T>` and Interior Mutability**
*A safe abstraction over unsafe code*™


---


# First, `Cell<T>`

```rust
use std::cell::Cell;

let c1 = Cell::new(5i32);
c1.set(15i32);

let c2 = Cell::new(10i32);
c1.swap(&c2);

assert_eq!(10, c1.into_inner()); // consumes cell
assert_eq!(15, c2.get()); // returns copy of value
```
* Shareable, mutable container
* Move values in and out of cell
* Is used for `Copy` types
  * where copying or moving values isn’t too resource intensive
* If an option, should always be used for low overhead


---


# `RefCell<T>`

* Hold's sole ownership like `Box<T>`
* Allows borrow checker rules to be enforced at **runtime**
  * Interface with `.borrow()` or `borrow_mut()`
  * If borrowing rules are violated, `panic!`
* Typically used when Rust's conservative checking "gets in the way"
* It is **not** thread safe!
  * Use `Mutex<T>` instead


---


# Interior Mutability

```rust
fn main() {
  let x = 5;
  let y = &mut x; // cannot borrow immutable x as mutable
}
```

* It would be useful for a value to mutate itself in its methods but appear immutable to other code
* Code outside the value's methods wouldn't be able to mutate it
* This can be achieved with `RefCell<T>`


---


# Interior Mutability with Mock Objects

```rust
pub trait Messenger {
    fn send(&self, msg: &str); // Note how this takes an &self NOT &mut self
}

pub struct LimitTracker<'a, T: Messenger> {
    messenger: &'a T,
    value: usize,
    max: usize,
}
```

* `LimitTracker` tracks a value against a maximum value and sends messages based on how close to the maximum value the current value is
* We want to mock a messenger for our limit tracker to keep track of messages for testing


---


# Limit Tracker
```rust
impl<'a, T> LimitTracker<'a, T>
where
    T: Messenger,
{
    // --- snip ---
    pub fn set_value(&mut self, value: usize) {
        self.value = value;

        let percentage_of_max = self.value as f64 / self.max as f64;

        if percentage_of_max >= 1.0 {
            self.messenger.send("Error: You are over your quota!");
        } else if percentage_of_max >= 0.9 {
            self.messenger
                .send("Urgent warning: You've used up over 90% of your quota!");
        } else if percentage_of_max >= 0.75 {
            self.messenger
                .send("Warning: You've used up over 75% of your quota!");
        }
    }
}
```


---


# Our Mock Messenger

```rust
struct MockMessenger {
  sent_messages: Vec<String>,
}

impl MockMessenger {
  fn new() -> MockMessenger {
    MockMessenger { sent_messages: vec![] }
  }
}

impl Messenger for MockMessenger {
  fn send(&self, message: &str) {
    self.sent_messages.push(String::from(message));
  }
}
```

* This code won't compile! `self.sent_messages.push` requires `&mut self`


---


# Let's Use Interior Mutability

```rust
use std::cell::RefCell;

struct MockMessenger {
  sent_messages: RefCell<Vec<String>>,
}

impl MockMessenger {
  fn new() -> MockMessenger {
    MockMessenger {
      sent_messages: RefCell::new(vec![]),
    }
  }
}

impl Messenger for MockMessenger {
  fn send(&self, message: &str) {
    self.sent_messages.borrow_mut().push(String::from(message));
  }
}
```


---


# Managing Borrows

![bg right:30% 80%](../images/ferris_panics.svg)
```rust
impl Messenger for MockMessenger {
  fn send(&self, message: &str) {
    let mut one_borrow = self.sent_messages.borrow_mut();
    let mut two_borrow = self.sent_messages.borrow_mut();

    one_borrow.push(String::from(message));
    two_borrow.push(String::from(message));
  }
}
```

* We still use the `&` and `mut` syntax for `RefCell`
* `borrow` returns either a `Ref` or `RefMut` which implement `Deref`
  * This means coercion applies: treat them like normal references


---


# What Makes Each Smart Pointer Unique


* `Rc<T>` - Enables multiple owners of the same data
* `Box<T>` - Allows immutable or mutable borrows that are checked at compile time
* `RefCell<T>` - Allows immutable/mutable borrows that are checked at runtime


---


# Combining Smart Pointers: `Rc<RefCell<T>>`

```rust
#[derive(Debug)]
enum List {
  Cons(Rc<RefCell<i32>>, Rc<List>),
  Nil,
}
```

* Common type seen in Rust
* Enables multiple owners of mutable data (with runtime checks)
* Extremely powerful, but comes with some overhead


---

# `Rc<RefCell<T>>` List

```rust
let value = Rc::new(RefCell::new(5));

let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));

let b = Cons(Rc::new(RefCell::new(3)), Rc::clone(&a));
let c = Cons(Rc::new(RefCell::new(4)), Rc::clone(&a));

*value.borrow_mut() += 10;

println!("a after = {:?}", a);
println!("b after = {:?}", b);
println!("c after = {:?}", c);
```
```
a after = Cons(RefCell { value: 15 }, Nil)
b after = Cons(RefCell { value: 3 }, Cons(RefCell { value: 15 }, Nil))
c after = Cons(RefCell { value: 4 }, Cons(RefCell { value: 15 }, Nil))
```

---


# Let's Try Another List

```rust
enum List {
  Cons(i32, RefCell<Rc<List>>),
  Nil,
}

impl List {
  fn tail(&self) -> Option<&RefCell<Rc<List>>> {
    match self {
      Cons(_, item) => Some(item),
      Nil => None,
    }
  }
}
```
* This implementation allows modifying the list structure instead of list values
* Now we have a function `tail` that gets the rest of our list


---


# What Happens?

```rust
let a = Rc::new(Cons(5, RefCell::new(Rc::new(Nil))));

println!("a initial rc count = {}", Rc::strong_count(&a));
println!("a next item = {:?}", a.tail());

let b = Rc::new(Cons(10, RefCell::new(Rc::clone(&a))));

println!("a rc count after b creation = {}", Rc::strong_count(&a));
println!("b initial rc count = {}", Rc::strong_count(&b));
println!("b next item = {:?}", b.tail());

if let Some(link) = a.tail() {
  *link.borrow_mut() = Rc::clone(&b);
}

println!("b rc count after changing a = {}", Rc::strong_count(&b));
println!("a rc count after changing a = {}", Rc::strong_count(&a));

println!("a next item = {:?}", a.tail());
```


---


# Answer

```
Exited with signal 6 (SIGABRT): abort program

a initial rc count = 1
a next item = Some(RefCell { value: Nil })
a rc count after b creation = 2
b initial rc count = 1
b next item = Some(RefCell { value: Cons(5, RefCell { value: Nil }) })
b rc count after changing a = 2
a rc count after changing a = 2
a next item = Some(RefCell { value: Cons(10, RefCell { value: Cons(5, RefCell...
```

* We see that at the end we have a reference cycle!


---


# Let's Look Closer
```rust
let a = Rc::new(Cons(5, RefCell::new(Rc::new(Nil))));
// a is Cons(5, Nil)

let b = Rc::new(Cons(10, RefCell::new(Rc::clone(&a))));
// b is Cons(10, a) = Cons(10, Cons(5, Nil))

if let Some(link) = a.tail() {
    // link is Nil (pointed to by a)
    *link.borrow_mut() = Rc::clone(&b);
    // link is now b = Cons(10, a)
}
// a = Cons(5, link) = Cons(5, b) = Cons(5, Cons(10, a))
// ^^^ reference cycle of a made!
```

* This can cause a memory leak!
  * `Rc` only frees when the `strong_count` is 0


---


# Avoiding Reference Cycles

* We know `Rc::clone` increases the `strong_count`
* You can create a `Weak<T>` reference to a value with `Rc::downgrade`
  * This increases the `weak_count` and can be nonzero when the `Rc` is freed
* To ensure valid references, `Weak<T>` must be upgraded before any use
  * Returns an `Option<Rc<T>>`


---


# `Weak<T>` Trees

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

#[derive(Debug)]
struct Node {
  value: i32,
  parent: RefCell<Weak<Node>>,
  children: RefCell<Vec<Rc<Node>>>,
}
```


---


# `Weak<T>` Trees In Action

```rust
fn main() {
  let leaf = Rc::new(Node {
    value: 3,
    parent: RefCell::new(Weak::new()),
    children: RefCell::new(vec![]),
  });

  println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());

  let branch = Rc::new(Node {
    value: 5,
    parent: RefCell::new(Weak::new()),
    children: RefCell::new(vec![Rc::clone(&leaf)]),
  });

  *leaf.parent.borrow_mut() = Rc::downgrade(&branch);

  println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
} // Tree is effectively dropped even with parent references!
```


---
