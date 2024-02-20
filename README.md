# Rust StuCo S24 Outline

_Each lecture is 50 minutes on Tuesdays from 7:00-7:50pm._ On some weeks, we might have extra content planned for after lecture under **After Dark**, but we'll only do it if people want to stay and hang out since it won't be required material.


</br>

# Course Materials:
- Main Source: [The Rust Programming Language (The Rust Book)](https://doc.rust-lang.org/book/)
    - The Rust Lang Book [in video format](https://www.youtube.com/playlist?list=PLai5B987bZ9CoVR-QEIN9foz4QCJ0H2Y8) on YouTube
- [Rust By Example](https://doc.rust-lang.org/rust-by-example/index.html)
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/)
- [The Rust Reference](https://doc.rust-lang.org/reference/index.html)
- Rust for Rustaceans - PDF available on O'Reilly for CMU students
- [Exercism](https://exercism.org/tracks/rust)
- [`rustlings`](https://github.com/rust-lang/rustlings)

</br>


# **Schedule**


## Week 1: Introduction
- Why Rust?
- `cargo` basics
- Rust Syntax
    - Variables and Mutability
    - Types
    - Functions, Statements, and Expressions
    - Control Flow
- Course Logistics
    - Installing Rust

### After Dark
- Setting up rust-analyzer
- RustRover


## Week 2: Ownership
- Ownership
    - The `String` Type
    - Move Semantics
- References and Borrowing
- Slices
- The `Vec` Type


## Week 3: Structs and Enums
- Ownership review
- Structs
- Enums
    - Pattern Matching


## Week 4: Standard Collections and Generics
- The `Vec<T>` Type
- The `String` Type
- The `HashMap<K, V>` Type
- Generics

### After Dark
- Remaining collections in `std::collections`


## Week 5: Error Handling and Traits
- Error Handling
- Traits

### After Dark
- `anyhow`


## Week 6: Modules and Testing
- Packages and Crates
- Modules
    - Module Paths and File Structure
    - The `use` Keyword
- Testing
    - Unit Tests
    - Integration Tests


## Week 7: Crates, Closures, and Iterators
- `no_std`: `rand`, `time`
- `std`: `clap`, `log`, `tracing`, `anyhow`, `flamegraph`
- Closures
    - Captures
    - The `move` Keyword
    - `Fn` traits
- Iterators
    - `Iterator` Trait and `next`
- Loops vs. Iterators

### After Dark
- More Essential Rust Crates
    - `rayon`
    - `serde`
    - `criterion`


## Week 8: Lifetimes
- Validating References
- The Borrow Checker
    - Lifetimes vs. Scope
    - Lifetimes vs. Memory
- Generic Lifetimes
- Lifetime Annotations
- Lifetime Elision
- `'static` Lifetimes


## Week 9: `Box<T>` and Trait Objects
- The `Box<T>` Type
- The `Deref` Trait and Deref Coercion
- The `Drop` Trait and `std::mem::drop`
- Object-Oriented Programming
- Trait Objects
    - Dynamic dispatch with `dyn`
- Dynamically Sized Types
- Object Safety


## Week 10: Smart Pointers and `unsafe`
- The `Rc<T>` Type
- The `RefCell<T>` Type
- Memory Leaks
- Unsafe Superpowers
- Raw Pointers
- FFI

### After Dark
- `Cow<'a, B>`
- `UnsafeCell<T>` and `Cell<T>`
- Implementation of:
    - `Cell<T>`
    - `RefCell<T>`
    - `Rc<T>`


## Week 11: Parallelism
- The `Arc<T>` Smart Pointer
- The `Mutex<T>` Smart Pointer
- The `RwLock<T>` Smart Pointer
- `std::sync::mspc::channel`
- Shared State vs Channels
- `Sync` and `Send` traits

### After Dark
- `Weak<T>`
- `CondVar`
- Implementation of:
    - `Arc<T>`
    - `Mutex<T>`


## Week 12: Concurrency
- `async`
- `await`
- The `Pin<T>` Type
- TODO


## Week 13: Macros
- Declarative Macros
    - `macro_rules!`
- Procedural Macros
- TODO
