# Rust StuCo S24 Outline

_Each lecture is 50 minutes on Tuesdays from 7:00-7:50pm._


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
- The `Vec<T>` type
- The `String` type
- The `HashMap<K, V>` type
- Generics


## Week 5: Error Handling and Traits
- Error Handling
- Traits


## Week 6: Cargo, Modules, Crates, and Testing
- Packages and Crates
- Modules
- The `use` Keyword
- Module Paths and File Structure
- Unit Tests
- Integration Tests


## Week 7: Lifetimes
- Validating References
- The Borrow Checker
    - Lifetimes vs. Scope
    - Lifetimes vs. Memory
- Generic Lifetimes
- Lifetime Annotations
- Lifetime Elision
- `'static` Lifetimes


## Week 8: Iterators, Closures, and Advanced Functional
- Closures
    - Captures
    - The `move` Keyword
    - `Fn` traits
- Iterators
    - `Iterator` Trait and `next`
- Loops vs. Iterators


## Week 9: Smart Pointers and Trait Objects
- The `Box<T>` Type
- The `Deref` Trait and Deref Coercion
- The `Drop` Trait and `std::mem::drop`
- The `Rc<T>` Type
- `RefCell<T>`
- Memory Leaks
- Object-Oriented Programming
- Trait Objects
    - Dynamic dispatch with `dyn`
- Dynamically Sized Types
- Object Safety


## Week 10: Parallelism
- The `Mutex<T>` Smart Pointer
- The `Arc<T>` Smart Pointer
- `std::sync::mspc::channel`
- TODO


## Week 11: Concurrency
- `async`
- `await`
- The `Pin<T>` Type
- TODO


## Week 12: Macros
- Declarative Macros
    - `macro_rules!`
- Procedural Macros
- TODO


## Week 13: `unsafe`
- Unsafe Superpowers
- Raw Pointers
- `UnsafeCell<T>`
- The `Rc<T>` Type Revisited
- The `Vec<T>` Type Revisited
- FFI


## Misc
Essential Rust Crates
- `no_std`
    - `rand`
    - `time`
- `std`
    - `log`
    - `tracing`
    - `anyhow`
    - `clap`
    - `rayon`
    - `flamegraph`
- Frameworks
    - `serde`
    - `criterion`
    - `tokio`