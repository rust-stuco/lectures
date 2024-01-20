---
marp: true
theme: rust
class: invert
paginate: true
---


<!-- _class: communism invert  -->

## Intro to Rust Lang
# Modules and Testing

<br>

Benjamin Owad, David Rudo, and Connor Tsui


---


# Today: Modules and Testing

* File system
    * Crates
    * Packages
    * Modules
* Testing


---


# **File System**


---


# Making a new crate

As mentioned previously, to create a new project called `hello_cargo`, run:

```
cargo new hello_cargo
````

* This will yield an empty package called `hello_cargo`, with:
    * A `src/main.rs` file that prints "Hello, world!"
    * And a `cargo.toml`
        * What is `cargo.toml`?


---

# Cargo.toml

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2021"

[dependencies]
```

* File written in `toml`, a file format for configuration files
* Defines metadata and dependencies for a package
    * Wait, aren't these crates?

<!--
Don't say crate name, crate version, crate edition, this is a *package*!
-->


---


# Terminology: Packages and Crates

* Packages are bundles comprising one or more crates
    * Packages are defined by a cargo.toml, describing its crates
* A crate is the smallest amount of code the rust compiler will consider at a time
    * Even if you run `rustc` on a single source file, it is considered a crate
* The terms are used interchangeably in practice


---

# Terminology: Types of Crates

* Binary crates compile to an executable that you can run
* Library crates define functionality to be shared between different projects
* Packages contain at most one library crate, and any number of binary crates
* Example: `cargo` has a binary crate and a library crate
    * The binary crate has the executable itself
    * The library crate has functionality that other projects can depend on to use the same logic


---


# Modules

In Rust, *modules* are used to hierarchically split code into separate units.

* A module is a collection of functions, structs, traits, etc
* Used to manage visibility (public/private)
* Mitigates name collisions
* More explicit and flexible than importing files directly


---


# Root Module

The root module is in our `main.rs` (for a binary crate) or `lib.rs` (for a library crate).

###### main.rs
```rust
// `main` is defined implicitly the root module
fn main() {
    println!("Hello, world!");
}
```

---


# Declaring Modules

We can declare a new module inline, in the same file as our crate root.

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

###### main.rs
```rust
fn main() {
    kitchen::cook();
}

mod kitchen {
    // `cook` is defined in the module `kitchen`
    fn cook() {
        println!("I'm cooking");
    }
}
```

* Can we call `cook` from `main`?


---


# Declaring Modules

We need to explicitly declare `cook` as `pub`—everything is private by default in Rust.
###### main.rs
```rust
fn main() {
    kitchen::cook();
}

mod kitchen {
    pub fn cook() { println!("I'm cooking"); }

    // Only those internal to the kitchen should be able to do this
    fn examine_ingredients() {}
}
```

<!-- Private by default is very very good -->


---


# Declaring Submodules


Modules are a tree! We can declare submodules inside of modules.
###### main.rs
```rust
fn main() {
    kitchen::stove::cook();
}

mod kitchen {
    pub mod stove {
        pub fn cook() { println!("I'm cooking"); }
    }

    fn examine_ingredients() {}
}
```

* Submodules also have to be declared as `pub` to be accessible.

---


# Modules in Different Files

Let's move the `kitchen` module to its own file.
###### main.rs
```rust
mod kitchen; // The compiler will look for kitchen.rs

fn main() {
    kitchen::stove::cook();
}

```

###### kitchen.rs
```rust
pub mod stove {
    pub fn cook() { println!("I'm cooking"); }
}

fn examine_ingredients() {}
```

* Can we separate `stove`, while maintaining that it is a submodule of `kitchen`?


---

# Submodules in Different Folders

We can put `stove.rs` in the `kitchen` folder to indicate the hierarchy.
###### kitchen.rs
```rust
pub mod stove; // note this still has to be `pub`

fn examine_ingredients() {}
```

###### kitchen/stove.rs
```rust
pub fn cook() {
    println!("I'm cooking");
}
```


* `main.rs` is unchanged (omitted for room on the slide)


---


# Alternate Submodule File Naming

`kitchen.rs` can be moved into the kitchen folder as well, if we wanted
###### kitchen/mod.rs
```rust
pub mod stove;

fn examine_ingredients() {}
```

###### kitchen/stove.rs
```rust
pub fn cook() {
    println!("I'm cooking");
}
```


* The other style is newer and generally preferred
* Often this style is used if `mod.rs` only contains other `mod` declarations


---


# The Module Tree, Visualized
![width:500px](../images/module-tree.png)
- Does this look familiar?
&nbsp;
&nbsp;

---


# The Module Tree, Visualized

![width:500px](../images/module-tree.png)
![bg right:35% 75%](../images/module-tree-fs.png)

- Does this look familiar?

* The module tree corresponds to the filesystem tree


---


# Paths for Referring to Modules

You may have noticed a path from the previous sequence:

```rust
kitchen::stove::cook();
```

This is saying:
* In the module `kitchen`
    * In the submodule `stove`
        * call the function `cook`


---


# Paths for Referring to Modules

You may have noticed a path from the previous sequence:

```rust
kitchen::stove::cook();
```

* This is a relative path, relative to the module of `main.rs` (which is the root).
* Another example of a relative path is `stove::cook()`, valid from within the `kitchen` module.
* We can also express this absolutely, as `crate::kitchen::stove::cook()`.
* There also exists a `super` keyword for paths relative to parent modules.


---


# Bringing Paths into Scope with `use`

###### main.rs
```rust
mod kitchen;

fn main() {
    kitchen::stove::cook();
}
```

* Programmers are lazy, and this is a lot to type


---


# Bringing Paths into Scope with `use`

###### main.rs
```rust
mod restaurant;

fn main() {
    restaurant::back::kitchen::stove::stovetop::burner::gasknob::cook();
    restaurant::back::kitchen::stove::stovetop::burner::gasknob::cook();
    restaurant::back::kitchen::stove::stovetop::burner::gasknob::cook();
}
```

- Programmers are lazy, and this is a lot to type
    - Especially if the hierarchy is deep, and we are using it multiple times

---


# Bringing Paths into Scope with `use`

###### main.rs
```rust
mod restaurant;

// The path must be absolute
use crate::restaurant::back::kitchen::stove::stovetop::burner::gasknob;

fn main() {
    gasknob::cook();
    gasknob::cook();
    gasknob::cook();
}
```

- Programmers are lazy, and this is a lot to type
    - Especially if the hierarchy is deep, and we are using it multiple times
- We can bring `gasknob` into scope with `use` to eliminate the need to fully qualify this function call
&nbsp;


---


# Bringing Paths into Scope with `use`

###### main.rs
```rust
mod restaurant;

// The path must be absolute
use crate::restaurant::back::kitchen::stove::stovetop::burner::gasknob::cook;

fn main() {
    cook();
    cook();
    cook();
}
```

- Programmers are lazy, and this is a lot to type
    - Especially if the hierarchy is deep, and we are using it multiple times
- We can bring `gasknob` into scope with `use` to eliminate the need to fully qualify this function call
- Or, we can bring the function itself into scope


---


# More `use` syntaxes

We can also import items from the standard library.

```rust
use std::io::Bytes;
use std::io::Write;
use std::io;
```
* `Bytes` is a struct, and `Write` is a trait.


---


# More `use` syntaxes

We can combine those 3 imports into one statement:

```rust
use std::io::{Bytes, Write, Self};
```

* One could also write `use std::io::*`
    * Called the "glob operator"
    * Generally not recommended to avoid this

<!--
The one case where glob is idiomatic is with the prelude pattern
-->


---


