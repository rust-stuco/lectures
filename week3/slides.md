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


# Review: Ownership

* Manual memory management is tricky
    * Prone to memory leaks or double frees
* Garbage collection is slow and unpredictable
* What if the compiler generated allocations and frees for us?
    * Rust does this for us through the _Ownership_ system


---


# Review: Ownership Rules

* Each value in Rust has an _owner_
* There can only be one owner at a time
* When the owner goes out of scope, the value will be _dropped_


---


# Review: Ownership Example 1

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Does this compile?

```rust
fn main() {
    let s = String::from("yo");
    taker(s);
    println!("I *totally* still own {}", s);
}

fn taker(some_string: String) {
    println!("{} is mine now!", some_string);
}
```


---


# Ownership Example 1

```
error[E0382]: borrow of moved value: `s`
 --> src/main.rs:4:42
  |
2 |     let s = String::from("yo");
  |         - move occurs because `s` has type `String`,
  |           which does not implement the `Copy` trait
3 |     taker(s);
  |           - value moved here
4 |     println!("I *totally* still own {}", s);
  |                                          ^ value borrowed here after move
  |
```
* Looks like `taker` doesn't still own `s`, after all


---


# Ownership Example 1

```
note: consider changing this parameter type in function `taker` to borrow
      instead if owning the value isn't necessary
 --> src/main.rs:7:23
  |
7 | fn taker(some_string: String) {
  |    -----              ^^^^^^ this parameter takes ownership of the value
  |    |
  |    in this function
```

* Suggestion from the compiler: Rewrite `taker` to _borrow_ `some_string`
* Is it necessary for `taker` to own the value?


---


# Ownership Example 1 Solution (References)

```rust
fn main() {
    let s = String::from("yo");
    taker(&s);                   // <-- Change to pass a reference to a String
    println!("I *totally* still own {}", s);
}

fn taker(some_string: &String) { // <-- Change to expect a reference to a String
    println!("{} is mine now!", some_string);
}
```
* Let `taker` borrow the value instead of moving it and transferring ownership


---


# Ownership Example 1 (Alternative Solution)

```
help: consider cloning the value if the performance cost is acceptable
  |
3 |     taker(s.clone());
  |            ++++++++
```

* Making a clone (deep copy) allows this compile
    * If `s` represents a large `String`, cloning will be expensive


---


# Ownership Example 2

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Does this compile?

```rust
fn main() {
    let favorite_computers = Vec::new();
    add_to_list(favorite_computers,
        String::from("Framework Laptop"));
}

fn add_to_list(fav_items: Vec<String>, item: String) {
    fav_items.push(item);
}
```


---


# Ownership Example 2

```
error[E0596]: cannot borrow `fav_items` as mutable, as it is not declared as mutable
 --> src/main.rs:8:5
  |
8 |     fav_items.push(item);
  |     ^^^^^^^^^ cannot borrow as mutable
  |
help: consider changing this to be mutable
  |
7 | fn add_to_list(mut fav_items: Vec<String>, item: String) {
  |                +++
```

* Missing one `mut` annotation


---


# Ownership Example 2

```rust
fn cool_guy() {
    let favorite_computers = Vec::new();
    add_to_list(favorite_computers, String::from("Framework Laptop"));
}

//             vvv Add `mut` here
fn add_to_list(mut fav_items: Vec<String>, item: String) {
    fav_items.push(item);
}
```


---


# Ownership Example 2

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

* What if we want to print the list?
* `favorite_computers` was moved in the `add_to_list` call
* Same problem as example 1


---


# Ownership Example 2

Let's try a mutable reference instead of moving the entire value.

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

* This now works as intended!


---


# Ownership Example 3

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Does this compile?

```rust
fn please_dont_move() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
    v.pop(); // Removes last element in `vec`
    println!("{}", x); // What is `x`?
}
```

* Prevent data races and weird circumstances
* What should this print if it did compile?


---


# Ownership Example 3

The compiler doesn't allow this!

```
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> src/lib.rs:4:5
  |
3 |     let x = &v[3];
  |              - immutable borrow occurs here
4 |     v.pop(); // Removes last element in `vec`
  |     ^^^^^^^ mutable borrow occurs here
5 |     println!("{}", x); // What is `x`?
  |                    - immutable borrow later used here
```

* The `Vec` type is a resizable array, so popping the last element might resize it
* When it resizes, the location of its data changes too
    * Then `x` would point to an invalid location in memory!


---


# **Structs**


---


# Structs

A _struct_ is a custom data type that lets you package together and name multiple related values that make up a meaningful group.

```rust
struct Student {
    andrew_id: String,
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}
```

* To define a struct, we enter the keyword `struct` and name the entire struct
* Inside the curly braces, we define the _fields_
* Each field must be named


---


# Creating Structs

We can create an _instance_ of a struct using the name of the struct and `key: value`
pairs inside curly brackets.

```rust
fn init_connor() -> Student {
    Student {
        andrew_id: String::from("cjtsui"),
        stress_level: u64::MAX,
        grade: 80,
        attendance: vec![true, false, false, false, false, false, false],
    }
}
```

* You don't have to specify fields in the same order
* You _must_ define every field of the struct to create an instance

---


# Accessing Fields

We can access fields of a struct using dot notation.

```rust
fn init_connor() -> Student {
    let mut connor = Student {
        andrew_id: String::from("cjtsui"),
        stress_level: u64::MAX,
        grade: 80,
        attendance: vec![true, false, false, false, false, false, false],
    };

    connor.grade = 60; // shh
    println!("{} has grade {}", connor.andrew_id, connor.grade);

    connor
}
```

* Note that the entire instance must be `mut` to modify _any_ field


---


# Field Init Shorthand

We can use _field init shorthand_ to remove repetitive wording.

```rust
fn init_student(andrew_id: String, grade: u8) -> Student {
    // We can shorthand `andrew_id: andrew_id`, etc
    Student {
        andrew_id,
        grade,
        attendance: Vec::new(),
        stress_level: u64::MAX, // default stress 😔
    }
}
```


---


# Struct Updates

We can use values from another struct to create a new one.

```rust
fn relax_student(prev_student: Student) -> Student {
    Student {
        stress_level: 0,
        grade: 100,
        ..prev_student
    }
}
```

* Note that this moves the data of the old struct
    * `prev_student` is moved, so we can't use it again (_unless..._)

<!--
There is a way to make it not moved, if it is Copyable
How do we make a struct Copy?
Stay tuned to find out!
-->


---


# Tuple Structs

We can created named tuples called Tuple Structs.

```rust
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

fn main() {
    let red = Color(255, 0, 0);
    let origin = Point(0, 0, 0);
}
```

* The same as structs, except without named fields
* The same as tuples, except with an associated name


---


# Unit Structs

We can declare _unit-like_ structs as such:

```rust
struct AlwaysEqual;

fn main() {
    let subject = AlwaysEqual;
}
```

* Structs that have no fields
* Most commonly used as markers since they are zero-sized types

<!--
Isomorphic to the unit type ()
Useful when you want to implement a trait, but don't need to store any data with it
-->


---


# References in Structs

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Can we store references inside structs?

```rust
struct Student {
    andrew_id: &str, // <- &str instead of String
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}
```


---


# Lifetimes Sneak Peek

```
error[E0106]: missing lifetime specifier
 --> src/main.rs:2:16
  |
2 |     andrew_id: &str, // <- &str instead of String
  |                ^ expected named lifetime parameter
  |
help: consider introducing a named lifetime parameter
  |
1 ~ struct Student<'a> {
2 ~     andrew_id: &'a str, // <- &str instead of String
```

* We can store references in structs, but we need lifetime specifiers
    * We'll talk about this in Week 7!


---


# Struct Example

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


# Printing Structs

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

What if we wanted to print these structs for debugging?

```rust
struct Student {
    andrew_id: String,
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}

fn main() {
    let connor = init_connor();

    println!("{:?}", connor);
}
```

<!--
All they need to know about `:?` is that it is used for debugging purposes
-->


---


# Printing Structs

We get an error if we try to print something that is not printable:

```rust
fn main() {
    let connor = init_connor();

    println!("{:?}", connor);
}
```

```
error[E0277]: `Student` doesn't implement `Debug`
  --> src/main.rs:11:22
   |
11 |     println!("{:?}", connor);
   |                      ^^^^^^ `Student` cannot be formatted using `{:?}`
   |
   = help: the trait `Debug` is not implemented for `Student`
```


---


# Traits Sneak Peek

What's this all about?

```
error[E0277]: `Student` doesn't implement `Debug`
<-- snip -->
   = help: the trait `Debug` is not implemented for `Student`
```

* We'll talk about Traits in Week 5
    * They define shared functionality and behavior between types


---


# Derived Traits

As always, we should look at what the compiler tells us.

```
help: consider annotating `Student` with `#[derive(Debug)]`
   |
2  + #[derive(Debug)]
3  | struct Student {
   |
```

* For now, let's just follow its advice
    * We'll figure out why this works later!


---


# Derived Traits

As a quick overview, derived traits allow us to quickly add functionality to our types.

```rust
#[derive(Debug)]
struct Student {
    andrew_id: String,
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}
```

* We can _derive_ a trait using the `derive` macro
* This will allow us to print this struct!


---


# Derived Traits

We can try again now:

```rust
#[derive(Debug)]
struct Student {
    // <-- snip -->
}

fn main() {
    let connor = init_connor();

    println!("{:?}", connor);
}
```

```
Student { andrew_id: "cjtsui", attendance: [true, false], grade: 80, stress_level: 18446744073709551615 }
```


---


# **Struct Methods**


---


# Struct Methods

Suppose we wanted to write a function that was only dependent on the data inside a single instance of a struct.

```rust
struct Rectangle {
    x: u32,
    y: u32,
    width: u32,
    height: u32,
}
```

* What if we wanted to get the area of this rectangle?


---


# Struct Methods

_Methods_ are like functions, but their first parameter is always `self`, and are always
defined within the context of a struct

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


---


# Method Syntax

Let's dive a bit deeper into this:

```rust
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}
```

* We start with an `impl` block for `Rectangle`
* We use `&self` instead of `rectangle: &Rectangle`
    * `&self` is actually syntactic sugar for `self: &Self`
        * _A reminder that `&Self` is the same as `&Rectangle`_
* We still have to obey borrowing rules with references


---


# Calling Methods

We can call a method using dot notation.

```rust
fn main() {
    let rect = Rectangle { x: 0, y: 0, width: 42, height: 98 };

    println!("Area: {}", rect.area());
}
```

* Note that we don't need to pass anything in for `self`


---


# Consuming Methods

What would happen if we didn't borrow with `&self` and instead use `self`?

```rust
impl Rectangle {
    fn area(self) -> u32 {
        self.width * self.height
    }
}
```

```rust
fn main() {
    let rect = Rectangle { width: 42, height: 98 };
    println!("Area: {}", rect.area());
    // println!("Width: {}", rect.width); <-- Cannot use this
}
```

* Same ownership rules as before, we take in `self` and consume it

<!--
There are cases where you might want this,
for example if you want something to be done only once and
you want to prevent it from happening twice (like a initialization of a protocol)
-->


---


# `&mut self`

We can take a mutable reference to our struct as well.

```rust
impl Rectangle {
    // <-- snip -->

    fn change_width(&mut self, new_width: u32) {
        self.width = new_width;
    }
}

fn main() {
    let mut rect = Rectangle { x: 0, y: 0, width: 42, height: 98 };
    rect.change_width(100);

    println!("{:?}", rect);
}
```
* Mutable references work as expected


---


# Associated Functions


We can define _associated function_ in `impl` blocks that do not take `self`.

```rust
impl Rectangle {
    fn create_square(x: u32, y: u32, side_length: u32) -> Self {
        Self { x, y, width: side_length, height: side_length }
    }
}

fn main() {
    let square = Rectangle::create_square(0, 0, 213);
}
```

* We cannot use dot notation for these functions
    * Instead we use the struct name and the `::` operator

<!--
Also known as static methods in other languages
Often used for "constructors" that return a new instance of the struct
-->


---


# Aside: What About `->`?

```rust
p1.distance(&p2);
(&p1).distance(&p2); // This is the same!
```

* In C and C++, you use `.` for direct access and `->` for access through a pointer
* Rust instead has _**automatic referencing and dereferencing**_
* When you call `object.something()`, Rust will automatically add in the `&`, `&mut`, or `*` so that `object` matches the signature of the method
    * This is a big reason why ownership is ergonomic in practice


---


# **Enums**


---


# Enums

* Defines a type with multiple possible _variants_
* Represents the Sum Type of Algebraic Data Types
    * Structs represent the Product Type


---


# Enum Definition

IP Addresses have two major standards, IPv4 and IPv6.

```rust
enum IpAddrKind {
    V4,
    V6,
}
```

* IP Addresses can be either IPv4 or IPv6, but not both at the same time
* We can express this concept in code with an enum consisting of V4 and V6 variants
* In general, we can _enumerate_ all the possible variants with enums


---


# Enum Variants

We can make a value of type `IpAddrKind` as such:

```rust
let four = IpAddrKind::V4;
let six = IpAddrKind::V6;
```

* The `::` operator represents a _namespace_
    * `V4` is in the namespace of `IpAddrKind`
* This is useful because we can see both values are the same type: `IpAddrKind`


---


# Enum Variants

We can define a function that takes an `IpAddrKind`:

```rust
fn route(ip_kind: IpAddrKind) {}
```

And call it with the different variants:

```rust
route(IpAddrKind::V4);
route(IpAddrKind::V6);
```


---


# Enums vs Structs

At the moment, we only store the kind of address, not the data. We may want to tackle this problem with structs then:

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


# Enums Can Hold Data

Instead of using structs to hold data, we can have the enums themselves hold data.

```rust
enum IpAddr {
    V4(String),
    V6(String),
}

let home = IpAddr::V4(String::from("127.0.0.1"));

let loopback = IpAddr::V6(String::from("::1"));
```

* Much cleaner than before!


---


# Enum Associated Data

Each enum can also hold different types and different amounts of data.


```rust
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0, 0, 1); // Even cleaner than the String!

let loopback = IpAddr::V6(String::from("::1"));
```


---


# `std::net::IpAddr`

The Rust Standard Library actually has its own implementation of `IpAddr`.

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```


---


# Further Enum Example
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