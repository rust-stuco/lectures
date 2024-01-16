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

* Type Aliases
* Const Generics
* Error Handling
    * `Result<V,E>`
    * `panic!`
* The Never Type
* Traits
    * Trait Bounds
    * `Copy` vs `Clone`
    * Supertraits
    * Derivable Traits


---


# **Type Aliases**


---


# Type Aliases

You can declare a type alias to give a name to an already existing type.

```rust
type Kilometers = i32;

let x: i32 = 5;
let y: Kilometers = 5;

println!("x + y = {}", x + y); // Rust knows the types are really the same
```


---


# Generic Type Aliases

You can also include generics in your type aliases.

```rust
type Grades = Vec<u8>;

fn main() {
    let mut empty_grades = Grades::new();
    empty_grades.push(42);
}
```

```rust
type Stack<T> = Vec<T>;

fn main() {
    let mut stack: Stack<i32> = Stack::new();
    stack.push(42);
}
```



---


# **Const Generics**


---


# Const Generics

```rust
struct ArrayPair<T, const N: usize> {
    left: [T; N],
    right: [T; N],
}
```

* Const Generics allow items to be generic over constant values


---


# Const Generics

Here's an example of constructing an `ArrayPair` with generic constant `5`:

```rust
struct ArrayPair<T, const N: usize> {
    left: [T; N],
    right: [T; N],
}

fn main() {
    let pair = ArrayPair::<i32, 5> {
        left: [0; 5],
        right: [1; 5],
    };

    println!("{:?}, {:?}", pair.left, pair.right);
}
```

```sh
[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]
```


---


# Const Generics Rules

Currently, `const` parameters may only be instantiated by `const` arguments of the following forms:

* A literal (i.e. an integer, bool, or character)
* A standalone `const` parameter
* A concrete constant expression (enclosed by `{}`), involving no generic parameters


---


# Const Generic Literals

```rust
fn foo<const N: usize>() {}

fn bar<T, const M: usize>() {
    foo::<2021>(); // Okay: `2021` is a literal
}
```

* Note that any valid constant with the correct type `usize` can be a generic parameter


---


# Standalone Const Parameter

```rust
fn foo<const N: usize>() {}

fn bar<T, const M: usize>() {
    foo::<M>(); // Okay: `M` is a const parameter
    let _: [u8; M]; // Okay: `M` is a const parameter
}
```

* Since `M` and `N` are const generic parameters of the same type, `M` is a valid parameter


---


# A Concrete Constant Expression

```rust
fn foo<const N: usize>() {}

fn bar<T, const M: usize>() {
    foo::<{20 * 100 + 20 * 10 + 1}>(); // Okay: const expression
                                       // contains no generic parameters
}
```


---


# Bad Constant Expressions

```rust
fn foo<const N: usize>() {}

fn bar<T, const M: usize>() {
    foo::<{ M + 1 }>(); // Error: const expression
                        // contains the generic parameter `M`

    foo::<{ std::mem::size_of::<T>() }>(); // Error: const expression
                                           // contains the generic parameter `T`

    let _: [u8; std::mem::size_of::<T>()]; // Error: const expression
                                           // contains the generic parameter `T`
}
```


---


# Const Generic Design Patterns

```rust
fn alternating<const ODD: bool>(nums: &[usize]) {
    let mut i = if ODD { 1 } else { 0 };

    while i < nums.len() {
        print!("{} ", nums[i]);
        i += 2;
    }

}
```

* Const generics allow for multiple compilations of the same function with slightly different behavior
* Const Generics representing "optional flags" is a common pattern


---


# Const Generic Design Patterns

```rust
fn alternating<const ODD: bool>(nums: &[usize]) {
    // <-- snip -->
}

fn main() {
    let nums = [0, 1, 2, 3, 4, 5, 6, 7];

    alternating::<false>(&nums);
    println!();
    alternating::<true>(&nums);
}
```

```sh
0 2 4 6
1 3 5 7
```



---


# **Error Handling**


---


# What `type_of` Error?

![bg right:25% 75%](../images/ferris_panics.svg)

In Rust there are **two** main types of errors we care about: _recoverable_ and _unrecoverable_ errors (panics).

* `Result<V, E>`
    * A return type for recoverable errors
* `panic!`
    * A macro (_notice the `!`_) to invoke unrecoverable errors


---


# The Result Type

Rust provides a `Result` type to represent "success" and "failure" states in code.

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

* Notice how the "success" does _not_ have to have the same type as the "error"


---


# Errors Example 1

```rust
fn integer_divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("Divide by zero".to_string())
    } else {
        Ok(a/b)
    }
}
```

* Here, the "success" type is an `i32`, and the "failure" a `String`
* The caller has to handle both cases


---


# Errors Example 2

`Result<T, E>` is fully generic, so we can create our own error types!

```rust
enum ArithError {
    DivideByZero,
    IllegalShift(i32)
}

fn shift_and_divide(x: i32, div: i32, shift: i32) -> Result<i32, ArithError> {
    if shift <= 0 {
        Err(ArithError::IllegalShift(shift))
    } else if div == 0 {
        Err(ArithError::DivideByZero)
    } else {
        Ok((x << shift) / div)
    }
}
```

* Creating your own "error" enum like `ArithError` is a common pattern


---


# The `?` Operator


To make error handling more ergonomic, Rust provides the `?` operator.

```rust
let x = potential_fail()?;

let x = match potential_fail() {
    Ok(v) => v
    Err(e) => return Err(e.into()), // Error is propogated up a level
}
```

* If `potential_fail` returns an `Err`, return early
* Else we can unwrap the inner value and continue
* Think of the `?` as quick way to see where a function short-circuit returns on failure


---


# The `?` Operator Example

```rust
use std::num::ParseIntError;

fn multiply(
    first_number_str: &str,
    second_number_str: &str,
) -> Result<i32, ParseIntError> {

    let first_number = first_number_str.parse::<i32>()?;
    let second_number = second_number_str.parse::<i32>()?;

    Ok(first_number * second_number)
}
```

* If either of the `parse` calls fail, we return their `Err`s
* Else we take the parsed values and multiply them


---


# The ? Operator Example

```rust
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

```
n is 20
Error: invalid digit found in string
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


# **Panics**


---


# Panics

Panics in Rust are unrecoverable errors. They can happen in many different ways:

* Out of bounds slice indexing
* Integer overflow (only in debug mode)
* `.unwrap()` on a `None` or `Err`
* Calls to the `panic!` macro


---


# More Panics

There are other useful macros that panic:

* `assert!`, `assert_eq!`, `assert_ne!`
    * Conditionally panics based on inputs
* `unimplemented!` / `todo!`
    * Usually used while something is in progress
* `unreachable!`
    * Can help the compiler optimize a code segment away


---


# `unwrap()`

Consider the following example from the Rust book:

```rust
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt").unwrap();
}
```

* What happens if we don't have `"hello.txt"`?


---


# `unwrap()`


```rust
fn main() {
    let greeting_file = File::open("hello.txt").unwrap();
}
```

```
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value:
    Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

* This error message isn't the best...


---


# `expect()`

We can do better than this if we *expect* this error and know what message to print to the user if something goes wrong.

```rust
fn main() {
    let greeting_file = File::open("hello.txt")
        .expect("'hello.txt' should be included in this project");
}
```

Now we get:

```
thread 'main' panicked at src/main.rs:5:33:
'hello.txt' should be included in this project:
    Os { code: 2, kind: NotFound, message: "No such file or directory" }
```


---


# **The Never Type**


---


# Functions that never return

Consider the following code, what should the type of `x` be?

```rust
let x = loop { println!("forever"); };
```

* This is not immediately obvious, right?


---


# The "Never" Type - `!`

Rust has a special type called `!`, or the "never type", for this exact reason.

Another example:

```rust
fn bar() -> ! {
    loop {}
}
```


---


# What's the point?

Why have a type that never has a value? Consider the following:

```rust
let guess: u32 = match guess.trim().parse() {
    Ok(num) => num,
    Err(_) => continue,
};
```

* Recall match statements can only return 1 type
* `continue` has the `!` type
    * Rust knows this can't be value and allows `guess: u32`


---


# What else is `!`?

* `panic!`
* `break`
* `continue`
* Everything that doesn't return a value - typically related to control flow
    * `print!` and `assert!` return `()`, so they don't use `!`


---


# **Traits**


---


# Traits

A _trait_ defines functionality a particular type has and can share with other types.

```rust
trait Shape {
    // Associated function signature; `Self` refers to the implementor type.
    fn new_shape() -> Self;

    // Method signature to be implemented by a struct.
    fn area(&self) -> f32;

    fn name(&self) -> String;
}
```

* Traits are defined with the `trait` keyword


---


# Trait Definitions

So how do we use traits? We `impl`ement them `for` a `struct`:

```rust
struct Rectangle {
    height: f32,
    width: f32
}

impl Shape for Rectangle {
    fn new_shape() -> Self {
        Rectangle { height: 1.0, width: 1.0 }
    }

    // <-- snip -->
}
```


---


# Default Trait Implementations

Traits can also provide a default implementation of functions.

```rust
trait Shape {
    // <-- snip -->

    // Default method implementation (can be overriden)
    fn print(&self) {
        println!("{} has an area of {}", self.name(), self.area());
    }
}
```

* These can be overriden by any `impl Shape for MyStruct`


---


# Overriding Default Trait Implementations

We can simply override functions as such:

```rust
impl Shape for Rectangle {
    // <-- snip -->

    fn print(&self) {
        println!("I am a rectangle! :)");
    }
}
```


---


# Traits in Action

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

What happens we try and construct a `Shape`?

```rust
let rec = Shape::new_unit();
```


---


# Traits `!=` Types


```rust
let rec = Shape::new_unit();
```

```
error[E0790]: cannot call associated function on trait without
              specifying the corresponding `impl` type
  --> src/main.rs:20:15
   |
3  |     fn new_shape() -> Self;
   |     ----------------------- `Shape::new_shape` defined here
...
20 |     let rec = Shape::new_shape();
   |               ^^^^^^^^^^^^^^^^ cannot call associated function of trait
   |
help: use the fully-qualified path to the only available implementation
   |
20 |     let rec = <Rectangle as Shape>::new_shape();
   |               +++++++++++++      +
```

* Traits are _abstract_, we cannot construct a trait by itself


---


# Traits in Action

![bg right:25% 80%](../images/ferris_happy.svg)

To use the `Shape` trait, Rust must know who is implementing it.

```rust
let rec: Rectangle = Shape::new_unit();
let rec = <Rectangle as Shape>::new_shape();
```


---


# Super Traits

Rust doesn't have "inheritence", but you can define a trait as being a superset of another trait.

```rust
trait Person {
    fn name(&self) -> String;
}

trait Student: Person {
    fn university(&self) -> String;
}
```

* `Person` is a supertrait of `Student`
* `Student` is a subtrait of `Person`
* Implementing `Student` on a type requires you to also `impl Person`


---


# Even Superer Traits

```rust
trait Programmer {
    fn fav_language(&self) -> String;
}

// CompSciStudent is a subtrait of both Programmer and Student
trait CompSciStudent: Programmer + Student {
    fn git_username(&self) -> String;
}
```

* We can make a trait a subtrait of multiple traits with the `+` operator
* Implementing `CompSciStudent` will now require you to `impl` both supertraits


---


# Recap: Traits

* Traits define shared behavior among types in an abstract way
* Instead of inheritance, Rust has supertraits
* Traits are similar to:
    * Interfaces
    * Abstract / Virtual Classes


---


# **Derivable Traits**


---


# Deriveable Traits

Back in week 3, we saw this example:

```rust
#[derive(Debug)]
struct Student {
    andrew_id: String,
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}
```

```sh
Student { andrew_id: "cjtsui", attendance: [true, false], grade: 42, stress_level: 1000 }
```

* Recall that we were not able to print out this struct without the
`#[derive(Debug)]`


---


# `Debug` Trait

The `Debug` trait is defined as such in the standard library:

```rust
pub trait Debug {
    // Required method
    fn fmt(&self, f: &mut Formatter<'_>) -> Result<(), Error>;
}
```

* We _could_ implement this trait for `Student` ourselves
    * It would likely be tedious...


---


# `Debug` Trait

```rust
impl fmt::Debug for Student {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Student {{ ")?;
        write!(f, "andrew_id: {:?}, ", self.andrew_id)?;
        write!(f, "attendance: {:?}, ", self.attendance)?;
        write!(f, "grade: {:?}, ", self.grade)?;
        write!(f, "stress_level: {:?}, ", self.stress_level)?;
        write!(f, "}}")
    }
}
```

```sh
Student { andrew_id: "cjtsui", attendance: [true, false], grade: 42, stress_level: 1000 }
```

* _Editor's note: it was indeed tedious_


---


# Deriveable Traits

Luckily, Rust can `derive` traits for us when there there is an obvious and common implementation.

* The compiler can provide basic implementations for some traits via the
`#[derive]` [attribute](https://doc.rust-lang.org/reference/attributes.html)
* `struct X` can `#[derive]` a trait if all the fields of `X` can derive that trait
* These traits can still be manually implemented if a more complex behavior is required


---


# Deriveable Traits

Let's break this down.

```rust
#[derive(Debug)]
struct Student {
    andrew_id: String,
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}
```

* Every single field is printable
* It is then reasonable that the struct itself should also be printable!
* Are there other traits that follow the same logic with structs?


---


# `Clone`

Recall the `Clone` trait from week 2.

```rust
let mut foo = vec![1, 2, 3];
let mut foo2 = foo.clone(); // explicit duplication of an object

foo.push(4); // foo = [1,2,3,4]
let y = foo2.pop(); // y=3, foo2 = [1, 2]
```

* A type that implements `Clone` can be duplicated / deep copied.
* The new value is independent of the original value and can be modified without affecting the original value


---


# `Clone`

We can also derive `Clone` for `Student`!

```rust
#[derive(Clone)]
struct Student {
    andrew_id: String,
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}
```

* Each field is cloneable
* So the entire struct should also be cloneable!


---


# `#[derive(Clone)]` Behind The Scenes

```rust
struct Student {
    andrew_id: String,
    attendance: Vec<bool>,
    grade: u8,
    stress_level: u64,
}

impl Clone for Student {
    fn clone(&self) -> Self {
        Self {
            andrew_id: self.andrew_id.clone(),
            attendance: self.attendance.clone(),
            grade: self.grade.clone(),
            stress_level: self.stress_level.clone(),
        }
}
```


---


# Derive Traits

Here's a list of other traits that can be derived:
- Comparison traits: `Eq`, `PartialEq`, `Ord`, `PartialOrd`
- `Clone`, to create a `T` from a `&T`
- `Copy`, to give a type "copy semantics" instead of "move semantics"
- `Hash`, to compute a hash from `&T`
- `Default`, to create an empty instance of a data type
- `Debug`, to format a value using the `{:?}` formatter


---


# Copy

Recall `Copy` only applies to:
- All integer types: `u8`, `i32`, etc
- `bool`
- All floating point types: `f32`, `f64`, etc
- `char` type

It is a differentiator in whether or not move semantics are applied to a function. (aka pass by reference vs value)


---


# Clone vs Copy

Although their end result may feel the same they are different:

Copy
* Copies happen implicitely ex: `x = y`
* `Copy` **cannot be overloaded** it is always a simple bitwise copy
    * `Copy` can't be implemented on a type for complex behaviors like other traits

Clone
* Cloning is an explicit action `x.clone()`
* `Clone` can provide any type-specific behavior necessary to duplicate values safely
    * An example of this is for `String`, `Clone` would need to copy not just the pointer but the data on the heap

---


# What Can `#[derive]` Copy?

Any type made out of types that implement Copy or holds a shared reference `&T`.

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

What happens if parameter `T` doesn't implement `Default`?

```rust
#[derive(Default)]
pub struct Gift<T> {
    to: &'static str,
    is_wrapped: bool,
    contents: T
}
```

```
   |
41 |     let _: Gift<MyType> = Gift::default();
   |                              ^^^^ the trait `Default` is not implemented for `MyType`
   |
   = help: the trait `Default` is implemented for `Gift<T>`
note: required for `Gift<MyType>` to implement `Default`
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
fn to_key<T>(
    v: Vec<T>,
) -> impl Hash
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


# Conditional Implement Methods

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

* `T` must implement `Display` to be printed
* `T` must implement `PartialOrd` to be compared
* `cmp_display` will exist for a `Pair<i32>` but not for `Pair<T: !PartialOrd>`


---


# **Next Lecture: Cargo, Testing, Modules, and Crates**

![bg right:30% 80%](../images/ferris_happy.svg)

Thanks for coming!
