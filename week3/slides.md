---
marp: true
theme: rust
class: invert
paginate: true
---
<!-- _class: communism invert  -->

## INTRO TO RUST LANG
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
# Compilation failed :-(

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
* No luck for the `cool_guy` function.
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
    let s = String::from("yo");
    helper_guy(s);
    println!("I *totally* still own {}", s);
}

fn helper_guy(some_string: String) {
    println!("{} is mine now
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
* Nope, same issue as before
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
* Works now!
---
# Exclusive references save lives
* Prevent data races and weird circumstances
```rust
fn main() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
    v.pop(); // Removes last element in `vec`
    println!("{}", x); // What is `x`?
}
```
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
* Like tuples, we can "package" data together
* Very similar to C at first glance
```rust
struct Student {
    andrew_id: String,
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}
```
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
        grade, // Skip assignment if variable has the same name
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
# Also, Tuple Structs Exist
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
# Also, Unit Structs Exist
```rust
struct AlwaysEqual;

fn main() {
    let subject = AlwaysEqual;
}
```
* Sometimes useful for cool wizardry
* Rarely useful for normal stuff
---


<!-- TODO: Double check it all compiles -->
<!-- TODO: Chaotic evil alignment enum example -->