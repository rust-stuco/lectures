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


# Review: Borrowing Rules

* At any given time, you can have either:
    * One mutable reference (exclusive reference)
    * Or any number of immutable references (shared references)
* References must always be valid


---


# Pop Quiz: Question 1

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


# Pop Quiz: Question 1

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


# Pop Quiz: Question 1

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


# Pop Quiz: Question 1 Solution (References)

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


# Pop Quiz: Question 1 (Alternative Solution)

```
help: consider cloning the value if the performance cost is acceptable
  |
3 |     taker(s.clone());
  |            ++++++++
```

* Making a clone (deep copy) allows this compile
    * If `s` represents a large `String`, cloning will be expensive


---


# Pop Quiz: Question 2

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


# Pop Quiz: Question 2

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


# Pop Quiz: Question 2 Solution

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


# Pop Quiz: Question 2 (Bonus)

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


# Pop Quiz: Question 2 (Bonus)

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


# Pop Quiz: Question 3

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

* What should this print if it did compile?


---


# Pop Quiz: Question 3

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
* The compiler will prevent errors under weird circumstances


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
    * This is a big reason why ownership and borrowing is ergonomic in practice


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

let home = IpAddr::V4(127, 0, 0, 1);

let loopback = IpAddr::V6(String::from("::1"));
```

* Even cleaner than carrying around a `String` that we need to parse!


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


# Enum Example

Let's take a look at another example of an enum that models data with variants.

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

* `Quit` has not data associated at all
* `Move` has named fields like a struct
* `Write` includes a single `String`
* `ChangeColor` includes 3 `i32` values


---


# Enums vs Structs

How would this look if we just used structs?

```rust
struct QuitMessage; // unit struct
struct MoveMessage {
    x: i32,
    y: i32,
}
struct WriteMessage(String); // tuple struct
struct ChangeColorMessage(i32, i32, i32); // tuple struct
```

* Each of these structs has a separate type
    * We couldn't easily define a function to take in all of these types
* Enums seem to have a lot in common with structs...


---


# Enum Methods

We can define `impl` blocks for enums as well as structs.

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
    * Same borrowing semantics as with structs


---


# **The Option Type**


---


# `NULL`

`NULL` is a pointer that does not point to a valid object or value.

> I call it my billion-dollar mistake...
My goal was to ensure that all use of references should be absolutely safe, with checking performed automatically by the compiler.
But I couldn’t resist the temptation to put in a null reference, simply because it was so easy to implement.
This has led to innumerable errors, vulnerabilities, and system crashes, which have probably caused a billion dollars of pain and damage in the last forty years.
— Tony Hoare, "inventer of `NULL`", 2009

* The issue is not the concept of `NULL`, rather its _implementation_
* We still want a way to express that a a value could be _something_ **or** _nothing_

---


# The Option Type

The standard library defines an enum `Option<T>`:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

* We can return either `None` or `Some`, where `Some` contains a value
* The `<T>` is a generic type parameter which means it can hold any type
    * We'll talk about this next week!


---


# The Option Type

Here are some examples of `Option<T>`:

```rust
enum Option<T> {
    None,
    Some(T),
}

let some_number = Some(5);
let some_char = Some('e');

let absent_number: Option<i32> = None;
```

* Rust will infer that `some_number` has type `Option<i32>` and `some_char` has type `Option<char>`
* We still have to annotate `absent_number` with `Option<i32>`


---


# `Option<T>` vs `NULL`

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

So why is `Option<T>` better than `NULL`? Consider this:

```rust
let x: i8 = 5;
let y: Option<i8> = Some(5);

let sum = x + y;
```

* What might be wrong with this?


---


# `Option<T>` vs `NULL`

If we try to compile this, we get an error.

```rust
let x: i8 = 5;
let y: Option<i8> = Some(5);

let sum = x + y;
```

```
error[E0277]: cannot add `Option<i8>` to `i8`
 --> src/main.rs:6:17
  |
6 |     let sum = x + y;
  |                 ^ no implementation for `i8 + Option<i8>`
  |
  = help: the trait `Add<Option<i8>>` is not implemented for `i8`
```

* We need a way to extract the number out of the `Some(5)`

---


# Working With `Option<T>`

```rust
let x: i8 = 5;
let y: Option<i8> = Some(5);
let sum = x + y;

if y.is_none() {
    // do something
} else if y.is_some() {
    // How do we even extract the `5` out???
    // Something like `y.get() + x`???
}
```

* This syntax is also kind of ugly...

<!-- Cough cough C++ std::optional -->


---


# **Pattern Matching**


---


# `match`

Rust has an extremely powerful control flow construct called `match`.

* You can compare a value against a series of patterns
* You can execute code based on which pattern matches
* Patterns can be made up of literal values, variable names, wildcards, etc.

<!--
It's like a coin-sorting machine, where the coin rolls down
and will fall into the hole that fits it first
-->


---


# Pattern Matching

Here's an example of a coin sorting function that tells us the value of the coin!

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


---


# Pattern Matching

Let's break this down:

```rust
match coin {
    Coin::Penny => 1,
    Coin::Nickel => 5,
    Coin::Dime => 10,
    Coin::Quarter => 25,
}
```

* First we write `match`, followed by an expression (in this case `coin`)
* Similar to `if` branch, but the expression does not need to be a `bool`
* Each arm has a pattern, followed by `=>`, followed by another expression
    * The patterns here are the `Coin` enum variants
    * The expressions here are just the values of each coin

---


# Pattern Matching

Here's another similar example.

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

* The `match` arms can be any valid expression, including code blocks!


---


# Binding Patterns: Quarters

Patterns can bind to specific parts of the values that match the pattern.

From 1999 through 2008, the United States minted quarters with different designs for each of the 50 states on one side.

```rust
#[derive(Debug)] // so we can inspect the state in a minute
enum UsState {
    Alabama,
    Alaska,
    // --snip--
}

enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(UsState),
}
```


---


# Binding Patterns: Quarters

```rust
fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {:?}!", state);
            25
        }
    }
}
```

* We bind `state` to the `UsState` the coin belongs to!


---


# Binding Patterns: `Option<T>`

Let's revisit the example from before.

```rust
let x: i8 = 5;
let y: Option<i8> = Some(5);

let sum = match y {
    Some(num) => Some(x + num),
    //   ^^^ `num` binds to 5
    None => None,
};

println!("{:?}", sum); // Prints "Some(10)"
```

* Clean, and we can access the value in the `Some` variant easily


---


# Matches Are Exhaustive

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

`match` must cover all of the possibilities that the expression it is matching against may take.

What happens when we don't?

```rust
let x: i8 = 5;
let y: Option<i8> = Some(5);

let sum = match y {
    Some(num) => x + num,
};
```


---


# Matches Are Exhaustive

We get a compile-time error if we fail to specific what to do in every possibility.

```rust
let x: i8 = 5;
let y: Option<i8> = Some(5);

let sum = match y {
    Some(num) => x + num,
};
```

```
error[E0004]: non-exhaustive patterns: `None` not covered
   --> src/main.rs:6:21
    |
6   |     let sum = match y {
    |                     ^ pattern `None` not covered
```

* Forces us to explicitly handle the `None` case
* Protecting us from the billion-dollar mistake!


---


# Catch-all Pattern

Sometimes we want to do something special for a specific pattern, but for all other patterns we want to default to something else.

```rust
fn add_fancy_hat() {}
fn remove_fancy_hat() {}
fn move_player(num_spaces: u8) {}

let dice_roll = 9;
match dice_roll {
    3 => add_fancy_hat(),
    7 => remove_fancy_hat(),
    other => move_player(other),
}
```

* `other` matches anything not covered in the previous cases


---


# `_` Pattern

If we don't care about the matched value, we can use `_` instead.

```rust
fn add_fancy_hat() {}
fn remove_fancy_hat() {}
fn reroll() {}

let dice_roll = 9;
match dice_roll {
    3 => add_fancy_hat(),
    7 => remove_fancy_hat(),
    _ => reroll(),
}
```

* `_` matches anything as well, but it doesn't bind the value


---


# Concise Control Flow with `if let`

Sometimes we just want to match against 1 pattern while ignoring the rest.

`if let` provides a more concise way to do this:

```rust
if let Coin::Penny = coin {
    println!("Lucky penny!");
}
```

* Works with `else if <pattern> = <expr>` and `else` as well


---


# `if let` Example

Here's another example of the same program written 2 different ways:

```rust
let mut count = 0;
match coin {
    Coin::Quarter(state) => println!("State quarter from {:?}!", state),
    _ => count += 1,
}
```

```rust
let mut count = 0;
if let Coin::Quarter(state) = coin {
    println!("State quarter from {:?}!", state);
} else {
    count += 1;
}
```


---


# Pattern Matching

Pattern Matching is an incredibly powerful tool.

* Gives you more control over a program’s control flow
* Allows you to you quickly and cleanly case on structures, usually enums
* Very useful in general
    * Commonly used in compilers and parsers
* Rust has many more patterns than we have time to cover!
    * Read [Chapter 18](https://doc.rust-lang.org/book/ch18-00-patterns.html) of the Rust Book to find out more!
        * _Will take less than 20 minutes_


---


# Homework 3

* This will be the first homework where you will actually need to program something
* You have been tasked with implementing two types of Pokemon:
    * `Charmander` is a struct
    * `Eevee` is a struct that can evolve into `EvolvedEevee`
        * `EvolvedEevee` is an enum representing different evolutions
* We _highly_ recommend reading [Chapter 18](https://doc.rust-lang.org/book/ch18-00-patterns.html) of the Rust book if you have time!


---


# Next Lecture: Standard Collections and Generics

![bg right:30% 80%](../images/ferris_happy.svg)

* Thanks for coming!