---
marp: true
theme: rust
class: invert
paginate: true
---
<!-- _class: communism invert  -->

## Intro to Rust Lang
# Structs and Enums

<br>

Benjamin Owad, David Rudo, and Connor Tsui

<!-- ![bg right:35% 65%](../images/ferris.svg) -->


---
# Reminders:
* Homework 2 due today
* Homework 3 out today, due next week
* The pattern continues...

---
# Review: Ownership

* Manual memory management is tricky
    * Prone to memory leaks or double frees
* Garbage collection is slow and unpredictable
* What if the compiler decided when to generate allocations and frees for us?
---
# Review: Ownership Rules

* Each value in Rust has an _owner_
* There can only be one owner at a time
* When the owner goes out of scope, the value will be _dropped_
---
# Review: Ownership Example

```rust
fn cool_guy() {
    let s = String::from("yo");
    helper_guy(s);
    println!("I *totally* still own {}", s);
}

fn helper_guy(some_string: String) {
    println!("{} is mine now!", some_string);
}
```
* Does this compile?
---
# Compilation failed!

```
error[E0382]: borrow of moved value: `s`
  --> cool_example.rs:8:42
   |
6  |     let s = String::from("yo");
   |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
7  |     helper_guy(s);
   |                - value moved here
8  |     println!("I *totally* still own {}", s);
   |                                          ^ value borrowed here after move
   |
```
* Looks like `cool_guy` doesn't still own `s`, after all.
---
# Possible solutions?
```
note: consider changing this parameter type in function `helper_guy`
 to borrow instead if owning the value isn't necessary
 --> cool_example.rs:11:28
  |
7 | fn helper_guy(some_string: String) {
  |    ----------              ^^^^^^ this parameter takes ownership of the value
  |    |
  |    in this function
```
* Suggestion from the compiler: rewrite `helper_guy` to use a reference instead.
* Is it necessary for `helper_guy` to own the value?
---
# Let `helper_guy` borrow it
```rust
fn cool_guy() {
    let s = String::from("yo");
    helper_guy(&s);                // <-- Change to pass by reference
    println!("I *totally* still own {}", s);
}

fn helper_guy(some_string: &String) { // <-- Change to expect a reference
    println!("{} is mine now!", some_string);
}
```
---
# Another suggestion from `rustc`...
```
help: consider cloning the value if the performance cost is acceptable
   |
7  |     helper_guy(s.clone());
   |                 ++++++++

error: aborting due to previous error
```
* If we make a deep copy, it will compile, but copying a `String` is not free.
---
# Review: Ownership Example 2
```rust
fn cool_guy() {
    let favorite_computers = Vec::new();
    add_to_list(favorite_computers, String::from("Framework Laptop"));
}

fn add_to_list(fav_items: Vec<String>, item: String) {
    fav_items.push(item);
}
```
* Does this compile?
---
# Not quite...
```
error[E0596]: cannot borrow `fav_items` as mutable, as it is not declared as mutable
  --> cool_example.rs:11:5
   |
11 |     fav_items.push(item);
   |     ^^^^^^^^^^^^^^^^^^^^ cannot borrow as mutable
   |
help: consider changing this to be mutable
   |
10 | fn add_to_list(mut fav_items: Vec<String>, item: String) {
   |                +++

error: aborting due to previous error

```
---
# Okay, now it compiles
```rust
fn cool_guy() {
    let favorite_computers = Vec::new();
    add_to_list(favorite_computers, String::from("Framework Laptop"));
}

fn add_to_list(mut fav_items: Vec<String>, item: String) {
    fav_items.push(item);
}
```
---
# What if I want to print my list?
```rust
fn cool_guy() {
    let favorite_computers = Vec::new();
    add_to_list(favorite_computers, String::from("Framework Laptop"));
    println!("{:?}", favorite_computers);
}

fn add_to_list(mut fav_items: Vec<String>, item: String) {
    fav_items.push(item);
}
```
* `favorite_computers` was moved in the `add_to_list` call.
* Same problem as before
---
# Let's try a mutable reference
```rust
fn cool_guy() {
    let favorite_computers = Vec::new();
    add_to_list(&mut favorite_computers, String::from("Framework Laptop"));
    println!("{:?}", favorite_computers);
}

fn add_to_list(fav_items: &mut Vec<String>, item: String) {
    fav_items.push(item);
}
```
* Does this compile?
* Yes, it does!
---
# Exclusive references save lives
```rust
fn main() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
    v.pop(); // Removes last element in `vec`
    println!("{}", x); // What is `x`?
}
```
* Prevent data races and weird circumstances
* What should this print?
---
# Compiler doesn't allow this!
```
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> example.rs:4:5
  |
3 |     let x = &v[3];
  |              - immutable borrow occurs here
4 |     v.pop(); // Removes last element in `vec`
  |     ^^^^^^^ mutable borrow occurs here
5 |     println!("{}", x); // What is `x`?
  |                    - immutable borrow later used here

error: aborting due to previous error
```
* We failed early!
* Debugging session prevented!
---
# **Structs**
---
# Structs
```rust
struct Student {
    andrew_id: String,
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}
```
* Like tuples, we can "package" data together
* Very similar to C at first glance
---
# Struct Instantiation
```rust
fn init_connor() -> Student {
    let mut connor = Student {
        andrew_id: "cjtsui",
        attendance: Vec::from([true, false, false, false, false, false, false]),
        grade: 11,
        stress_level: u64::MAX,
    };

    connor.grade = 97; // shhh
    connor // return cjtsui
}
```
---
# Field Init Shorthand
```rust
fn init_connor(grade: u8, stress_level: u64, att_vec: Vec<bool>) -> Student {
    let mut connor = Student {
        andrew_id: "cjtsui",
        attendance: att_vec,
        grade, // Shorter syntax if variable has the same name
        stress_level,
    };

    connor.grade = 97; // shhh
    connor // return cjtsui
}
```
---
# Field Init Shorthand
```rust
fn relax_connor(prev_connor: Student) -> Student {
    let new_connor = Student {
        stress_level: 0,
        ..prev_connor
    };
    new_connor
}
```
---
# Tuple Structs
```rust
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

fn main() {
    let red = Color(255, 0, 0);
    let origin = Point(0, 0, 0);
} 
```
* The same as structs, except without named fields
* The same as tuples, except with a type (...and more)
---
# Unit Structs
```rust
struct AlwaysEqual;

fn main() {
    let subject = AlwaysEqual;
}
```
* Structs that have no fields
* You will see why these may be useful later...

<!-- Only reasonable/common use I know of is implementing a trait for a unit struct (e.g. different implementations of an algorithm) -->

---
# Can we store references in a struct?
```rust
struct Borrower {
    borrowed_num: &i32,
}
```
---
# Not quite...
```
error[E0106]: missing lifetime specifier
 --> cool_example.rs:2:19
  |
2 |     borrowed_num: &i32,
  |                   ^ expected named lifetime parameter
  |
help: consider introducing a named lifetime parameter
  |
1 ~ struct Borrower<'a> {
2 ~     borrowed_num: &'a i32,
  |
```
* We don't know how long the reference will last!
* What if we store a reference to a variable and then it is freed?
* Lifetimes solve this problem (Lecture 7)!
---
# Quick Struct Example
```rust
fn draw_rectangle(x: u32, y: u32, width: u32, height: u32) {}
```

```rust
fn draw_rectangle(rect_tuple: (u32, u32, u32, u32)) {}
```

```rust
struct Rectangle {
    x: u32,
    y: u32,
    width: u32,
    height: u32,
}

fn draw_rectangle(rect: Rectangle) {}
```
* Which do you prefer?
---
# **Struct Methods**
---
# Struct Methods
```rust
struct Rectangle {
    x: u32,
    y: u32,
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}
```
* Functions defined within the context of a struct
* Similar to object-oriented design patterns in other languages
---
# Calling a method
```rust
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let rect = Rectangle { x: 0, y: 0, width: 42, height: 2691/39 };
    println!("Area: {}", rect.area());
}
```
---
# What's this "self"? 
```rust
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}
```
* `self` refers to the context of the current struct
* This context is the main difference between functions and methods
* The `&` indicates we are taking an immutable reference to the struct
* Same borrowing rules as before
---
# Function equivalent of a method
```rust
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}
```
```rust
fn area(rect: &Rectangle) -> u32 {
    rect.width * rect.height
}
```
* We borrow for the same reasons in both cases.
---
# What if we didn't borrow?
```rust
impl Rectangle {
    fn area(self) -> u32 {
        self.width * self.height
    }
}
```
```rust
fn area(rect: Rectangle) -> u32 {
    rect.width * rect.height
}
```
---
# The `area` function "consumes" the `Rectangle`
```rust
fn main() {
    let rect = Rectangle { width: 42, height: 2691/39 };
    println!("Area: {}", rect.area());
    println!("Width: {}", rect.width); // <-- error: can't use `rect` anymore
}
```
* Same behavior in the equivalent function
* Sometimes, you might want this!
---
# Another Method Example
```rust
impl Rectangle {
    fn copy_width(&mut self, other: &Rectangle) {
        self.width = other.width;
    }
}

fn main() {
    let mut rect = Rectangle { x: 0, y: 0, width: 42, height: 2691/39 };
    let rect2 = Rectangle { width: 99, ..rect };
    println!("Width before: {}", rect.width); // immutable borrow
    rect.copy_width(&rect2); // mutable borrow rect, immutable borrow rect2
    println!("Width after: {}", rect.width); // immutable borrow
}
```
* Mutable references work as expected
---
# Associated Functions
* Also known as static methods in other languages
* Functions that don't take in a `self`
    * Don't refer to an instance of the struct
* Often used for "constructors" that return a new instance of the struct
---
# Associated Function Example
```rust
impl Rectangle {
    fn new_square(x: u32, y: u32, side_length: u32) -> Rectangle {
        Rectangle {
            x,
            y,
            width: side_length,
            height: side_length,
        }
    }
}

fn main() {
    // Call associated function with struct name rather than an instance
    let sq = Rectangle::new_square(0, 0, 213);
}
```
---
# **Enums**
---
# Enums
* Allow us to encode/enumerate different possibilities
* Similar to C enums, but much more powerful 
    * More akin to a tagged union
---
# Enum Definition
```rust
enum IpAddrKind {
    V4,
    V6,
}
```
* IP Addresses can be either IPv4 or IPv6, but not both at the same time.
* We can express this concept in code with an enum consisting of V4 and V6 variants.
---
# Enum Values
We can make a value of type `IpAddrKind` as such:
```rust
let four = IpAddrKind::V4;
let six = IpAddrKind::V6;
```
* The `::` operator represents a _namespace_
    * `V4` is in the namespace of `IpAddrKind`
---
# Enum Example
```rust
enum IpAddrKind {
    V4,
    V6,
}

struct IpAddr {
    kind: IpAddrKind,
    address: String,
}
```
* IPv4 addresses look like `8.8.8.8`
* IPv6 addresses look like `2001:4860:4860:0:0:0:0:8888`
* When we have an `IpAddr` struct, can check the `kind` field to determine how to interpret the `address` field.
---
# Enum Associated Data
Enum variants can hold fields:
```rust
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0, 0, 1);
```
---
# Futher Enum Example
```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```
* The `Move` variant has named fields.
    * Seem familiar?
* Can we do this equivalently with structs?
---
# Struct Equivalent
```rust
struct QuitMessage; // unit struct
struct MoveMessage {
    x: i32,
    y: i32,
}
struct WriteMessage(String); // tuple struct
struct ChangeColorMessage(i32, i32, i32); // tuple struct
```
* Each of these structs has a separate type—we couldn't easily define a function to take any of these.
* Enums seem to have a lot in common with structs...
---
# Enum Methods
```rust
struct Message {
    Write(string),
    // --snip--
}
impl Message {
    fn call(&self) {
        // --snip--
    }
}

let m = Message::Write(String::from("hello"));
m.call();
```
* `self` holds the value of the enum
* Same borrowing semantics as before
---
# **Option Types**
---
# Option Types
> I call it my billion-dollar mistake. At that time, I was designing the first comprehensive type system for references in an object-oriented language. My goal was to ensure that all use of references should be absolutely safe, with checking performed automatically by the compiler. But I couldn’t resist the temptation to put in a null reference, simply because it was so easy to implement. This has led to innumerable errors, vulnerabilities, and system crashes, which have probably caused a billion dollars of pain and damage in the last forty years.

—Tony Hoare, "inventer of null", 2009
* This is why references always point to valid memory, and are never `NULL`!
* But then how can we return _nothing_?

---
# Option Types
The standard library defines an enum `Option<T>`:
```rust
enum Option<T> {
    None,
    Some(T),
}
```
* We can return either `None` or `Some`, where `Some` contains a value
* The `<T>` is a generic type parameter—more on this next week

---
# Option Types Example
```rust
fn identity_theft() {
    let result: Option<u32> = steal_david_ssn(); // might fail
    if (result.is_none()) {
        // Guess we failed
    } else if (result.is_some()) {
        // We have successfully stolen David's social security number
    }
}
```
* There is a better syntax for this...
---
# **Pattern Matching** 

---
# Pattern Matching
```rust
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}
fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}
```
* Allows us to execute code conditionally based on the variant of an enum using `match`

---
# Pattern Matching
```rust
fn value_in_cents(coin: Coin) -> u8 {
    let res = match coin {
        Coin::Penny => {
            println!("Lucky penny!");
            1
        }
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    };
    res
}
```
* Every `match` arm is an expression
* `match` itself is also an expression, evaluating to the expression at the relevant arm
* We can use block expressions here, too!
---
# Patterns That Bind to Values
```rust
fn identity_theft() {
    let result: Option<u32> = steal_david_ssn(); // might fail
    match result {
        None => println!("Theft failed"),
        Some(ssn) => println!("David Rudo's SSN is {}", ssn),
    }
}
```
* Clean, and we can access the value in the `Some` variant easily.

---
# Another Option Pattern Matching Example
```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}
```
* Takes in an option, and returns an option
* Binds to the value `i` and constructs a new enum variant using it

---
# Matches Are Exhaustive
Continuing with the theme of Rust failing early, `match` must cover all of the possibilities—in our case, all of the variants of an enum.

---
# Matches Are Exhaustive
```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        Some(i) => Some(i + 1),
    }
}
```
* This does not compile: `non-exhaustive patterns: None not covered`
* Prevents us from forgetting to explicitly handle the `None` case.
* Protecting us from the billion-dollar mistake!

---
# Catch-all Pattern
```rust
fn value_in_cents(coin: Coin) -> u8 {
    let res = match coin {
        Coin::Penny => {
            println!("Lucky penny!");
            1
        }
        other_coin => { // matches anything
            println!("Not a penny—don't care");
            less_opinionated_value_in_cents(other_coin)
        }
    };
    res
}
```
* Matches anything not covered in previous cases

---
# Placeholder for Unused Values
```rust
fn value_in_cents(coin: Coin) -> u8 {
    let res = match coin {
        Coin::Penny => {
            println!("Lucky penny!");
            1
        }
        _ => { // matches anything
            println!("Not a penny—don't care");
            0
        }
    };
    res
}
```
* `_` matches anything as well, but no variable is assigned

---
# `if let` shorthand
```rust
fn value_in_cents(coin: Coin) -> u8 {
    if let res = Coin::Penny {
        println!("Lucky penny!");
        return 1;
    };
    println!("Not a penny—don't care");
    0
}
```

* If there are only one or two cases, it might be cleaner to use `if let`
* Works with `else` and `else if`, also

---
# Pattern Matching Is Really Powerful
```rust
fn judge_number(num: Option<u8>) -> u8 { // returns rating from 0-5 stars
    match num {
        Some(13) => 1 // unlucky
        Some(8) => 4 // lucky
        Some(7) => 5 // very lucky
        Some(4) => 0 // very unlucky
        Some(x) => x % 5 // idk just act important
        _ => 0 // Anything else (only None left) is a 0
    }
}
```
* We can pattern match on numbers
* We can pattern match within other structures
    * And we can use catch-all here, too!
---
# Pattern Matching
* Pattern matching lets you quickly and cleanly case on structures
    * Commonly used in compilers and parsers
    * Very useful in general

---
# Next Lecture: Standard Collections and Generics

![bg right:30% 80%](../images/ferris_happy.svg)

* Thanks for coming!

<!-- TODO: Add ferrises -->
<!-- TODO: Double check it all compiles -->