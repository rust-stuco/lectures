---
marp: true
theme: default
class: invert
paginate: true
---

# Intro to Rust Lang

# **Standard Collections and Generics**

<br>

Benjamin Owad, David Rudo, and Connor Tsui

![bg right:35% 65%](../images/ferris.svg)


---


# Welcome back!

- Homework 3 due today
- You can use 7 late days over the whole semester
- If you spent over an hour on the assignment, please let us know!
- Other announcements (TODO)


---


# Today: Standard Collections and Generics

* Rust's collection types
    - `Vec<T>`
    - `String`
    - `HashMap<K, V>`
* Generic Types


---


# Standard Collections


Rust's standard library contains very useful data structures called _collections_.

* Most data types represent one specific value, but collections can contain multiple values
* These collections are all stored on the heap
    * The amount of data each has does not need to be known at compile time
    * If you are interested in the other kinds of collections you can read the official [documentation](https://doc.rust-lang.org/std/collections/index.html) of `std::collections`


---


# **Vectors**


---


# Review: Vectors

You can create an vector with `new`, and add elements with `push`.

```rust
let mut v = Vec::new();

v.push(5);
v.push(6);
v.push(7);
v.push(8);

println!("{:?}", v);
```


---


# Review: `vec!` Macro

Rust provides a _macro_ to create vectors easily in your programs.

```rust
let v = vec![1, 2, 3];

println!("{:?}", v);
```

```
[1, 2, 3]
```


---


# Review: Indexing

You can index into a vector to retrieve a reference to an element.

```rust
let v = vec![1, 2, 3, 4, 5];

let third_ref: &i32 = &v[2];
println!("The third element is {}", third_ref);

let third: i32 = v[2]; // This is only possible because i32 is Copy
println!("The third element is {}", third);
```


---


# `Vec::get()`

You can also use the `get` method to access an optional reference.

```rust
let v = vec![1, 2, 3, 4, 5];

let third: Option<&i32> = v.get(2);
match third {
    Some(third) => println!("The third element is {}", third),
    None => println!("There is no third element."),
}
```

* Using `get` returns `None` if the index is out of bounds, instead of panicking


---


# `Vec` and References

Recall the rules for immutable and mutable references.


```rust
let mut v = vec![1, 2, 3, 4, 5];

let first = &v[0];

v.push(6);

// println!("The first element is: {}", first);
```

* You cannot mutate a vector while references to its elements exist
* Appending might resize the vector and change the location in memory


---


# `Vec` and References

If we try to run this:

```rust
let mut v = vec![1, 2, 3, 4, 5];
let first = &v[0];
v.push(6);
println!("The first element is: {}", first);
```

```
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> src/main.rs:4:5
  |
3 |     let first = &v[0];
  |                  - immutable borrow occurs here
4 |     v.push(6);
  |     ^^^^^^^^^ mutable borrow occurs here
5 |     println!("The first element is: {}", first);
  |                                          ----- immutable borrow later used here
```


---


# Iterating over a Vector

To access each element in order, we can iterate through the elements with a `for` loop rather than use indices to access each at a time.


```rust
let v = vec![100, 32, 57];
for elem in &v { // `elem` is a reference to an i32
    println!("{}", elem);
}
```

```
100
32
57
```


---


# Mutable iteration over a Vector

We can also iterate over mutable references to each element to make changes to each element

```rust
let mut v = vec![100, 32, 57];
for elem in &mut v {  // `elem` is a mutable reference to an i32
    *elem += 50;
}
println!("{:?}", elem);
```

```
[150, 82, 107]
```

* We only have a single mutable reference into the vector at a time
    * We pass the borrow checker's rules!


---


# For Loop Sugar

Removing the `&` also works when you only want immutable references:

```rust
let v = vec![100, 32, 57];
for i in v {
    println!("{}", i);
}
```

* The reason this works is subtle, and we'll talk more about why in week 8!


---


# Deref Coercion to `&[T]`

Instead of a function taking a `&Vec<T>` as a parameter, we can take a `&[T]`.

```rust
fn largest(list: &Vec<i32>) -> &i32
```
```rust
fn largest(list: &[i32]) -> &i32
```

* The latter is strictly more powerful
* We can do this because of _deref coercion_, which basically means you can turn a reference to `Vec<T>` into a reference to `[T]`, or `&Vec<T>` into `&[T]`
* We'll talk more about this in week 9!



---


# Use Enums to Store Multiple Types

Vectors can only store values of the same type, so use Enums to store variants!

```rust
enum SpreadsheetCell {
    Int(i32),
    Float(f64),
    Text(String),
}

let row = vec![
    SpreadsheetCell::Int(3),
    SpreadsheetCell::Text(String::from("blue")),
    SpreadsheetCell::Float(10.12),
];
```


---

# Vectors and Ownership

Vectors owns all of the elements it contains. To insert an owned value into a vector, it must be moved.

```rust
let mut v = vec![String::from("rust"), String::from("is")];

let s = String::from("great!");

v.push(s); // move `s` into `v`

// `s` is no longer valid!
```


---


# Dropping a Vector

Like any other struct, a vector is dropped when it goes out of scope.

```rust
{
    let v = vec![String::from("rust"), String::from("is"), String::from("great!")];

    // do stuff with `v`
} // <- `v` goes out of scope and is freed here
```

* When the vector gets dropped, all of its contents are also dropped
* The borrow checker will ensure that any reference into the vector are only used while the vector is valid


---


# **String**


---


# What is a String?

* A `String` is a collection of bytes, interpreted as text
* We introduced them back in week 2, but now we'll look at them in more depth
* New Rustaceans commonly get stuck on strings for a combination of reasons:
    * UTF-8
    * Rust's propensity for exposing possible errors
    * Strings being more complicated than many programmers think


---


# What is a String?

- Rust only has one string type in the core language, `str`
    * We almost always see it in its borrowed form, `&str`
    * String slices are `&str`
    * String literals are `&str` that are stored in the program's binary
* `String` is a growable, mutable, owned, UTF-8 encoded string type


---


# Creating a `String`

You can create an empty `String` with `new`, `to_string`, or `from`.

```rust
let mut s = String::new(); // empty mutable string

let data = "initial contents"; // string literal

let s = data.to_string(); // string literal into `String`

// the method also works on a literal directly:
let s = "initial contents".to_string();

let s = String::from("initial contents"); // string literal into `String`
```


---


# Strings are UTF-8 Encoded

We can include any properly encoded data in `String`.

Here are some greetings in different languages!

```rust
let hello = String::from("السلام عليكم");
let hello = String::from("Dobrý den");
let hello = String::from("Hello");
let hello = String::from("שָׁלוֹם");
let hello = String::from("नमस्ते");
let hello = String::from("こんにちは");
let hello = String::from("안녕하세요");
let hello = String::from("你好");
let hello = String::from("Olá");
let hello = String::from("Здравствуйте");
let hello = String::from("Hola");
```


---


# Updating a `String`

We can grow a `String` by using the `push_str` method.

```rust
let mut s = String::from("foo");
s.push_str("bar");
println!("{}", s);
```

```
foobar
```


---


# Updating a `String`

The `push_str` method takes a string slice, because we don't necessarily want to take ownership of the string passed in.

```rust
let mut s1 = String::from("foo");
let s2 = String::from("bar");
s1.push_str(&s2);
println!("s2 is {}", s2); // `s2` is still valid!
```

```
s2 is bar
```

---


# Updating a `String`

The `push` method takes a single character and adds it to the `String`

```rust
let mut s = String::from("Monka");
s.push('S');
println!("{}", s);
```

```
MonkaS
```


---


# Concatenating Strings

You can combine two strings with `+`:

```rust
let s1 = String::from("Hello, ");
let s2 = String::from("world!");
let s3 = s1 + &s2; // note s1 has been moved here and can no longer be used
```

This is syntactic sugar for a function whose signature looks something like this:
```rust
fn add(self, s: &str) -> String
```

* Notice that it takes full ownership of `self`
* Also notice it takes `&str` and not `&String`
    * This is the same _deref coercion_ as with vectors!


---


# Concatenating Multiple Strings

```rust
let s1 = String::from("tic");
let s2 = String::from("tac");
let s3 = String::from("toe");
```

To combine multiple strings, you could do something like this:

```rust
let s = s1 + "-" + &s2 + "-" + &s3;
```

But you can instead use the `format!` macro to do the same thing.

```rust
let s = format!("{}-{}-{}", s1, s2, s3);

let s = format!("{s1}-{s2}-{s3}"); // relatively new Rust feature!
```


---


# Indexing into Strings

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

The code below might seem normal if you know other programming languages like Python or C/C++.

```rust
let s1 = String::from("hello");
let h = s1[0];
```

- Accessing individual characters in a string by indexing is common in many languages.
* However, if you try to access parts of a `String` using an index, you'll get an error.



---


# Indexing into Strings

Let's see what happens when we try to index into a `String`.

```rust
let s1 = String::from("hello");
let h = s1[0];
```

```
error[E0277]: the type `String` cannot be indexed by `{integer}`
 --> src/main.rs:3:13
  |
3 |     let h = s1[0];
  |             ^^^^^ `String` cannot be indexed by `{integer}`
  |
  = help: the trait `Index<{integer}>` is not implemented for `String`
```

* Why doesn't Rust support indexing?


---


# Internal Representation of Strings

A `String` is really a wrapper over `Vec<u8>`, or a vector of bytes. Let's look at some properly encoded UTF-8 strings.

```rust
let hello = String::from("Hola");
```

* How long is this string?
    * The length of the string is 4
    * The internal vector storing the string `"Hola"` is 4 bytes long
* Simple enough, right?


---


# Internal Representation: Cyrillic

Now suppose we wanted to say "Hello", but in Russian.

```rust
// Note that this string begins with the capital Cyrillic letter Ze,
// NOT the number 3
let hello = String::from("Здравствуйте");
// З vs 3
```

* How long is this string?
    * There are 12 characters
    * Rust's answer is 24, the number of bytes needed in the internal vector


---


# Internal Representation: UTF-8

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Let's revisit some invalid Rust code again.

```rust
let hello = "Здравствуйте";
let answer = &hello[0];
```

* What _should_ `answer` be?
    * It can't be `З`, internally it is represented by 2 bytes `[208, 151]`
    * Do we return 208 instead?
* Not so simple, eh?


---


# Internal Representation: UTF-8

```rust
let hello = "Здравствуйте";
let answer = &hello[0];
```

* We don't want to return an unexpected value that might cause bugs
* Rust chooses to not compile this code at all!
    * Prevents misunderstandings early in the development process
* Further reading on UTF-8: [Rust Book Chapter 8.2](https://doc.rust-lang.org/book/ch08-02-strings.html#bytes-and-scalar-values-and-grapheme-clusters-oh-my)



---


# Slicing Strings

Instead of indexing with a single number, you can use `[]` with a range to create a string slice containing specific bytes.

```rust
let hello = "Здравствуйте";

let s = &hello[0..4]; // `s` == "Зд"
```


---


# Slicing Strings

However, if we try to slice only a part of a character's bytes, Rust would panic at runtime in the same way as if an invalid index were accessed in a vector.

```rust
let hello = "Здравствуйте";

let s = &hello[0..1];
```

```
thread 'main' panicked at 'byte index 1 is not a char boundary;
it is inside 'З' (bytes 0..2) of `Здравствуйте`'
```


---


# Iterating Over Strings

Normally, we want to iterate over individual Unicode scalar values, and we can use the `chars` method.

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

```
З
д
```


---


# Iterating Over Strings

Alternatively, if you want the actual raw bytes, you can use the `bytes` method.

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

```
208
151
208
180
```


---


# Recap: Strings

* Strings are complicated!
* Rust chooses to make correct handling of `String` data the default
    * Programmers have to put more thought into handling UTF-8 upfront
    * The complexity of strings is more apparent in Rust
    * But this prevents you from dealing with errors non-ASCII characters later!
* The standard library offers a lot of methods for [`String`](https://doc.rust-lang.org/std/string/struct.String.html) and [`&str`](https://doc.rust-lang.org/std/primitive.str.html) types to help handle these complex situations correctly


---


# **HashMap**


---


# `HashMap<K, V>`

The type `HashMap<K, V>` stores keys with type `K` mapped to values with type `V`.

* Many languages support this kind of data structure, even if they use a different name:
    - Hash
    - Map
    - Object
    - Hash Table
    - Dictionary
    - Associative Array


---


# Creating a Hash Map

We can create a new hash map with `new` and insert entries with `insert`.

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();

scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Yellow"), 50);
```

* Note that we need to bring in `HashMap` with `use` from the collections portion of the standard library
* We'll talk more about `use` in week 6!

<!-- Mention that because Vec and String are used so frequently, they are automatically "imported" -->


---


# Accessing Values in a Hash Map

We can use the `get` method to get the value of a key.

```rust
let mut scores = HashMap::new();
scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Yellow"), 50);

let team_name = String::from("Blue");
let score = scores.get(&team_name).unwrap_or(&0);
```

* The `get` method returns an `Option<&V>`, similar to `Vec::get()`
    * If it returns `Some(&x)`, we unwrap and get out `&x`
    * If it returns `None`, we go to the default case `&0`


---


# Iterating over a Hash Map

We can iterate over each key/value pair using a `for` loop, similarly to vectors.

```rust
let mut scores = HashMap::new();

scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Yellow"), 50);

for (key, value) in scores {
    println!("{key}: {value}");
}
```

```
Yellow: 50
Blue: 10
```


---


# Hash Maps and Ownership

Hash Maps own the data that is contained inside them, much like vectors.

```rust
let field_name = String::from("Favorite color");
let field_value = String::from("Blue");

let mut map = HashMap::new();
map.insert(field_name, field_value);

// field_name and field_value are invalid at this point,
// try using them and see what compiler error you get!
```


---


# Updating a Hash Map

`HashMap` only contains one key/value pair at a time, so you can overwrite old pairs.

```rust
let mut scores = HashMap::new();

scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Blue"), 25);

println!("{:?}", scores);
```

```
{"Blue": 25}
```


---


# Updating a Hash Map with Defaults

- This is a common pattern with map types:
    * If the key exists in the hash map, do something with the value
    * If it doesn't exist, insert the key and a default value for it
* `HashMap` has a special API for this called `Entry`


---


# `hash_map::Entry`

If you want to insert a value if the key doesn't already exist, you can use the `Entry` method `or_insert`.

```rust
let mut scores = HashMap::new();
scores.insert(String::from("Blue"), 10);

scores.entry(String::from("Yellow")).or_insert(50);
scores.entry(String::from("Blue")).or_insert(50);

println!("{:?}", scores);
```

```
{"Yellow": 50, "Blue": 10}
```


---


# `hash_map::Entry`

If you want to update a value if it exists, or provide a default, you can do something similar:

```rust
let text = "hello world wonderful world";

let mut map = HashMap::new();

for word in text.split_whitespace() {
    let count = map.entry(word).or_insert(0);
    *count += 1;
}

println!("{:?}", map);
```

```
{"world": 2, "hello": 1, "wonderful": 1}
```


---


# `hash_map::Entry::or_insert`

The method `or_insert` has the following signature:

```rust
fn or_insert(self, default: V) -> &mut V
```

* It gives out a mutable reference
    * That reference is guaranteed to point to valid data
    * We need the default otherwise the data might not exist
* Be sure to check out the [documentation](https://doc.rust-lang.org/stable/std/collections/hash_map/enum.Entry.html) for `Entry`!


---


# Recap:

* [The Rust Book Chapter 8](https://doc.rust-lang.org/book/ch08-00-common-collections.html)
* Always refer to the documentation!
    * `Vec<T>` [documentation](https://doc.rust-lang.org/std/vec/struct.Vec.html)
    * `String` [documentation](https://doc.rust-lang.org/std/string/struct.String.html)
    * `HashMap<K, V>` [documentation](https://doc.rust-lang.org/stable/std/collections/hash_map/struct.HashMap.html)


---


# **Generics**


---


# Generics

So what was the deal with the `T` in `Vec<T>`, and `K, V` in `HashMap<K, V>`?

* We refer to these as _generic_ types
* Think of it as being able to fill in almost any type you want in place of `T`
* Generics allow us to replace specific types with a placeholder that represents multiple types to remove code duplication

---


# Removing Code Duplication

Let's say we want to find the largest number in a list.

```rust
let number_list = vec![34, 50, 25, 100, 65];

let mut largest = &number_list[0];

for number in &number_list {
    if number > largest {
        largest = number;
    }
}

println!("The largest number is {}", largest);
```


---


# Removing Code Duplication

What if we have multiple lists?

```rust
let number_list = vec![34, 50, 25, 100, 65];
let mut largest = &number_list[0];
for number in &number_list {
    if number > largest {
        largest = number;
    }
}
println!("The largest number is {}", largest);

let number_list = vec![102, 34, 6000, 89, 54, 2, 43, 8];
let mut largest = &number_list[0];
for number in &number_list {
    if number > largest {
        largest = number;
    }
}
println!("The largest number is {}", largest);
```


---


# Removing Code Duplication

That was ugly, let's extract our logic into a function called `largest`.

```rust
fn largest(list: &[i32]) -> &i32 {
    let mut largest = &list[0];
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];
    println!("The largest number is {}", largest(&number_list));

    let number_list = vec![102, 34, 6000, 89, 54, 2, 43, 8];
    println!("The largest number is {}", largest(&number_list));
}
```

<!-- For now we'll ignore the fact that this requires there to be at least 1 element in the vector -->


---


# Remove Code Duplication

What did we just do?

1. We identified duplicate code
2. We extracted the duplicate code into a function
3. We updated the duplicate code to call the function instead


---


# Remove Function Duplication

What if we wanted to also find the largest character in a slice?

```rust
fn largest_char(list: &[char]) -> &char {
    let mut largest = &list[0];
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}
```

* Seems awfully familiar...
* Can we remove a _function_ that has been duplicated?


---


# Generic Functions

We can define a function as generic with `<T>` (or any name like `<K>` or `<Hi>`):

```rust
fn largest<T>(list: &[T]) -> &T
```

```rust
fn largest<K>(list: &[K]) -> &K
```

```rust
fn largest<Hi>(list: &[Hi]) -> &Hi
```

* All of these essentially mean the same thing!
    * This function is generic over `T`
    * This function takes in a slice of `T` as input
    * This function returns a reference to `T`


---


# Generic Functions

Let's try and just modify our old function directly:

```rust
fn largest<T>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];
    println!("The largest number is {}", largest(&number_list));

    let char_list = vec!['y', 'm', 'a', 'q'];
    println!("The largest char is {}", largest(&char_list));
}
```

---

# Generic Functions

We get an error:

```
error[E0369]: binary operation `>` cannot be applied to type `&T`
 --> src/main.rs:4:17
  |
4 |         if item > largest {
  |            ---- ^ ------- &T
  |            |
  |            &T
  |
help: consider restricting type parameter `T`
  |
1 | fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
  |             ++++++++++++++++++++++
```


---


```
error[E0369]: binary operation `>` cannot be applied to type `&T`
 --> src/main.rs:4:17
  |
4 |         if item > largest {
  |            ---- ^ ------- &T
  |            |
  |            &T
  |
help: consider restricting type parameter `T`
  |
1 | fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
  |             ++++++++++++++++++++++
```

* We cannot compare two `&T` to each other
* We'll talk about type restrictions with _traits_ next week!
* For now, all you need to know is that we need the `PartialOrd` trait in order to enable comparisons
* Let's just follow the compiler's advice for now!


---


# Generic Functions

Once we make that change, this works!

```rust
fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}
```


---


# Generic Structs

We can define structs to use a generic type parameter using the `<>` syntax.

```rust
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let integer = Point { x: 5, y: 10 };
    let float = Point { x: 1.0, y: 4.0 };
}
```


---


# Generic Structs

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Observe that this requires both the `x` field and the `y` field to be the same type.

```rust
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let wont_work = Point { x: 5, y: 4.0 };
}
```


---


# Generic Structs

If we try to compile this, we get an error

```
error[E0308]: mismatched types
 --> src/main.rs:7:38
  |
7 |     let wont_work = Point { x: 5, y: 4.0 };
  |                                      ^^^ expected integer,
                                             found floating-point number
```


---


# Generic Structs

If we want a struct with different generic fields, we need to define other generic types with the `<>` syntax.

```rust
struct Point<T, U> {
    x: T,
    y: U,
}

fn main() {
    let both_integer = Point { x: 5, y: 10 };
    let both_float = Point { x: 1.0, y: 4.0 };
    let integer_and_float = Point { x: 5, y: 4.0 };
}
```


---


# Generic Enums

Recall the `Option<T>` type:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

* This is just a generic enum over `T`!


---


# Generic Enums

Enums can be generic over multiple types, just like structs.

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

* This enum is generic over `T` and `E`, with each represented in a variant
* `Result<T, E>` is actually a common type in the standard library that we'll talk about next week!


---


# Generic Methods

Methods on structs can also be generic.

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

fn main() {
    let p = Point { x: 5, y: 10 };
    println!("p.x = {}", p.x());
}
```


---


# Generic Methods

```rust
impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}
```

* Observe that we have to declare `T` after the `impl` as well as after `Point`
* This is to specify that we're implementing methods on the _type_ `Point<T>`
* This is different from implementing methods on the _type_ `Point<f32>`


---


# Generic `impl`

We could have made an implementation specific to `Point<f32>`:

```rust
impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

* This code means that `Point<f32>` will have an additional `distance_from_origin` method on top of the methods defined for `Point<T>`


---


# Generic `impl`

Suppose we went back to the `Point<T, U>`.

```rust
struct Point<T, U> {
    x: T,
    y: U,
}
```

We could implement for when `x` is always an integer, but `y` could be anything.

```rust
impl<U> Point<i32, U> {
    fn get_sum_x(&self, other: Point<i32, U>) -> i32 {
        self.x + other.x
    }
}
```


---


# Generic `impl`

This actually still requires for the two `y`s to have the same type.

```rust
impl<U> Point<i32, U> {
    fn get_sum_x(&self, other: Point<i32, U>) -> i32 {
        self.x + other.x
    }
}

fn main() {
    let p1 = Point { x: 5, y: 3.2 }; // y is f64
    let p2 = Point { x: 5, y: 4.4 }; // y is also f64
    println!("{}", p1.get_sum_x(p2))
}
```


---


# Generic `impl`

We can make the method generic over yet another type:

```rust
impl<U> Point<i32, U> {
    fn get_sum_x<V>(&self, other: Point<i32, V>) -> i32 {
        self.x + other.x
    }
}

fn main() {
    let p1 = Point { x: 5, y: 3.2 };           // y is f64
    let p2 = Point { x: 5, y: String::new() }; // y is String
    println!("{}", p1.get_sum_x(p2))
}
```



---


```rust
// Another example

struct Point<X1, Y1> {
    x: X1,
    y: Y1,
}

impl<X1, Y1> Point<X1, Y1> {
    fn mixup<X2, Y2>(self, other: Point<X2, Y2>) -> Point<X1, Y2> {
        Point {
            x: self.x,
            y: other.y,
        }
    }
}

fn main() {
    let p1 = Point { x: 5, y: 10.4 };
    let p2 = Point { x: "Hello", y: 'c' };

    let p3 = p1.mixup(p2);
    println!("p3.x = {}, p3.y = {}", p3.x, p3.y);
}
```


---


# Generic `impl`

- The purpose of these examples was to demonstrate a situation where some generics are defined with `impl`, and others with the method definition
* Take some time to understand these examples
    * These slides were based on examples made in the [book](https://doc.rust-lang.org/book/ch10-01-syntax.html)


---


# Performance of Generics

- You might be wondering whether there is a runtime cost to using generics
* The good news is that there is _zero_ overhead to using generics!
* Rust accomplishes this with _monomorphization_


---


# Monomorphization

Let’s look at how this works by using the standard library’s generic `Option<T>`:

```rust
let integer = Some(5);
let float = Some(5.0);
```

* The compiler will identify which types `T` can take on by find all instances of `Option<T>`, in this case `i32` and `f64`
* It creates monomorphized versions of `Option` specific to those types


---


# Monomorphization

The compiler will generate something similar to the following:

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

* Compile time cost instead of runtime cost!


---


# Recap: Generics

* Generics allow us to reduce code duplication
* Monomorphization means we do not incur any runtime cost!


---


# Homework 4

* TODO


---


# **Next Lecture: Errors and Traits**

![bg right:30% 80%](../images/ferris_happy.svg)

Thanks for coming!
