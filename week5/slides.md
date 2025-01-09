---
marp: true
theme: rust
class: invert
paginate: true
---


<!-- _class: communism invert  -->

## Intro to Rust Lang
# Ownership Revisited

<br>


<!-- ![bg right:35% 65%](../images/ferris.svg) -->


---


# The Rules

At the beginning of this course, we learned the Commandments of Rust...


---


# The Rules

At the beginning of this course, we learned the Commandments of Rust...

#### Rules of Ownership

* Each value in Rust has an _owner_
* A value can only have one owner at a time
* When the owner goes out of scope, the value will be _dropped_


---


# The Rules

At the beginning of this course, we learned the Commandments of Rust...

#### Rules of Ownership

- Each value in Rust has an _owner_
- A value can only have one owner at a time
- When the owner goes out of scope, the value will be _dropped_


---


# The Rules

At the beginning of this course, we learned the Commandments of Rust...

#### Rules of Borrowing
* Cannot access both a mutable and an immutable reference to the same object
* At any given time, may have either one mutable reference, or any number of immutable references


---


# The Catch

If we follow these rules and pass the compiler, is our code perfect?

Not quite...
* Rejected programs are not necessarily unsafe
* Passing programs are not necessarily the "best"
    * "Best" being most performant, most elegant, most robust


---


# Objective

* When my program is rejected, why might it be unsafe?

* Between multiple safe fixes, how do I choose the "best" fix?

<!-- Speaker note:
First, we have to understand what makes a program unsafe.
Why do we have these rules in the first place?
What sorts of behavior is the compiler trying to prevent?
-->


---


# Defining Unsafety


Safety is the absence of undefined behavior


---


# Defining Unsafety

However, undefined behavior is a lot

Definition in Rust Reference prints on five sheets...

![list](./img/rust-undefined-list.png)

<!-- Speaker note:
Undefined behavior can encapsulate a lot of things,
so we'll simplify it and say that
-->


---


# Defining Unsafety

Safety is the absence of undefined behavior

However, undefined behavior is a lot

Simplification: **invalid memory access ⇒ unsafety****


<!-- Speaker note:
Our program is unsafe if we make an invalid memory access
Double asterisk, see Rust Reference for full definition
-->


---


# Invalid Memory Access ⇒ Unsafety

Memory access can be unsafe if

* Deallocated
    * Ownership rules prevent this
* Overwritten by "someone else"
    * Borrowing rules prevent this

<!-- Speaker note:
The "someone else" will be explained in Parallelism lecture
-->

---


# Invalid Memory Access ⇒ Unsafety

Memory access can be unsafe if

- Deallocated
- Overwritten by "someone else"

Trivially safe for immutable globals


---


# Invalid Memory Access ⇒ Unsafety

Memory access can be unsafe if

- Deallocated
- Overwritten by "someone else"

Trivially safe for immutable globals

We'll focus on local variables

---


# Local Variables

Local variables live in a function's **stack frame**

The stack frame
* Contains everything needed for the function to run
* Is allocated on function call
* Is deallocated on function return


---


# Local Variables

Here's `main`'s stack frame:
![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
stack frame has x=1 -->

```rust
fn main() {
    let x = 1;
}
```


---

# Local Variables

![bg right 100%](./img/COMINGSOON.png)

Now we call `my_function`, and...

```rust
fn main() {
    let x = 1;
    my_function(x);
}
```


---


# Local Variables

Here's `my_function`'s stack frame:
![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
stack frame has arg=1, y=2, z=3 -->

```rust
fn main() {
    let x = 1;
    my_function(x);
}

fn my_function(arg: i32) {
    let y = 2;
    let z = 3;
}
```

<!-- Speaker note:
Emphasize that `x` is copied to create `arg`
-->


---


# Local Variables

Finally, we return from `my_function`
![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
remove my_function stack frame -->

```rust
fn main() {
    let x = 1;
    my_function(x);
}
```


---


# Motivating the Heap

![bg right 100%](./img/COMINGSOON.png)

What if instead of an integer `x = 1`

```rust
fn main() {
    let x = 1;
    my_function(x);
}
```

---


# Motivating the Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
Replace x=1 with x = [ 15GB of 0xdeadbeef ]
-->

We have a 15GB's worth of `Vector<u32>`?

```rust
fn main() {
    let x = vec![0xdeadbeef; 4_000_000];
    my_function(x);
}
```

---


# Motivating the Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
add `my_function` stack frame
-->

When we call `my_function`

```rust
fn main() {
    let x = vec![0xdeadbeef; 4_000_000];
    my_function(x);
}

fn my_function(arg : Vec<u32>) {
    ...
}
```


---


# Motivating the Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
add `my_function` stack frame
add `arg`
-->

When we call `my_function`,

```rust
fn main() {
    let x = vec![0xdeadbeef; 4_000_000];
    my_function(x);
}

fn my_function(arg : Vec<u32>) {
    ...
}
```

We must allocate `arg` for its stack frame


---


# Motivating the Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
add `my_function` stack frame
add `arg`
fill `arg`
-->

When we call `my_function`,

```rust
fn main() {
    let x = vec![0xdeadbeef; 4_000_000];
    my_function(x);
}

fn my_function(arg : Vec<u32>) {
    ...
}
```

We must allocate `arg` for its stack frame
⇒ Copy 15GB of `0xdeadbeef`'s

---


# Motivating the Heap

Unsustainable!

```rust
fn main() {
    let x = vec![0xdeadbeef; 4_000_000];
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
}
```


---


# The Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
cross out "x = [ 15GB of 0xdeadbeef ] in main's stack frame"
-->

Fortunately, our `Vector` does not live in the stack


---


# The Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
add rectangle for heap
draw arrow from x to heap alloc
-->

Fortunately, our `Vector` does not live in the stack

It lives in the **heap**


---


# The Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
highlight heap alloc
-->

Value lives in the heap


---


# The Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- replace COMINGSOON
highlight x
-->

Value lives in the heap

**Pointer** lives in the stack


---


# The Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- add my_function's stack frame -->

When we call `my_function`

```rust
fn main() {
    let x = vec![0xdeadbeef; 4_000_000];
    my_function(x);
}

fn my_function(arg : Vec<u32>) {
    ...
}
```


---


# The Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- add my_function's stack frame -->
<!-- draw arrow from arg to heap -->

We can copy the pointer `x` into `arg`

```rust
fn main() {
    let x = vec![0xdeadbeef; 4_000_000];
    my_function(&x);
}

fn my_function(arg : &Vec<u32>) {
    ...
}
```


---


# The Heap

![bg right 100%](./img/COMINGSOON.png)
<!-- add my_function's stack frame -->
<!-- draw arrow from arg to heap -->

**Before:** 15GB per `Vector`

**After:** 8 bytes per 64-bit pointer

Much better!

```rust
fn main() {
    let x = vec![0xdeadbeef; 4_000_000];
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
    my_function(x);
}
```


---


# Recap


Variable placement:
* **Stack-allocated:** Value on stack
* **Heap-allocated:** Value on heap, **pointer** on stack

Stack:
* Allocated on function call, deallocated on return
* Stores pointers and fixed-size data (like integers, floats)

Heap:
* Allocated on programmer request
* For dynamically sized or long-lived data (like `String`, `Vector`)


---


# Motivating Ownership

Recall that accessing **deallocated** memory is unsafe.


---


# Motivating Ownership

When do we deallocate memory?

* Stack: deallocated when function returns
    * Valid, unless dangling pointer ✅
    * We'll discuss more in Lifetimes lecture
* Heap: deallocated when ???
    * ⚠️


---


# Motivating Ownership


Heap: deallocated when ???

* C's proposal: leave it to the programmer
    * Manual malloc / free <!-- "but this is prone to MANY bugs" -->
* Java's proposal: leave it to runtime
    * Garbage collector <!-- "but runtime processes are inefficient" -->
* Rust's proposal: prevent it at compile time
    * Borrow checker
<!--
Speaker Note:
    Emphasize that we're accepting longer compile times
    for enhanced runtime performance
-->

---


# Motivating Ownership


How can we be confident that heap memory is deallocated safely?


---


# Motivating Ownership


How can we be confident that heap memory is deallocated safely?

Inspired by the stack
* Local variable lives in function's **stack frame**
* Allocated on function call
* Deallocated on function return

---


# Motivating Ownership


How can we be confident that heap memory is deallocated safely?

Inspired by the stack
- Local variable "owned by" stack frame
- One copy per stack frame
- Dropped on function return


<!-- Speaker notes:
We draw inspiration from stack memory!
Why are stack deallocations safe?
Well, do you notice that in stack allocations,
each value on the stack has an "owner"?
Each value is allocated when we enter the function,
and each value is deallocated when we exit the function?
You can think of it as the value being "owned" by the function,
    and it's valid when we're in the function,
    and dropped when we exit the function!
-->


---


# Motivating Ownership

How can we be confident that heap memory is deallocated safely?

Inspired by the stack
- Local variables "owned by" stack frame
- One copy per stack frame
- Dropped on function return

Now we apply it to the heap


<!-- Speaker notes:
What if we take this idea of ownership for stacks,
    and apply it to the heap?
Before, in C-land, heap memory is laissez-faire for the programmer.
Now we impose the following rules:
-->


---


# Motivating Ownership


How can we be confident that heap memory is deallocated safely?

#### Rules of Ownership

* Each value in Rust has an _owner_
* A value can only have one owner at a time
* When the owner goes out of scope, the value will be _dropped_
    * Deallocate the value here
    * Safe because value has only one owner

<!-- Speaker note:
Q: Given these rules, pretend you're the compiler.
    You're marking out places in the programmer's code where you can deallocate heap memory.
    Can someone tell me, under these rules, when is it safe to free memory?
        And how do you know it's safe?
-->


---


# Motivating Borrowing Rules

Recall that accessing **overwritten** memory is unsafe.


---


# Pop Goes X

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Suppose we have a `Vector` like this:

```rust
fn x_shouldnt_exist() {
    let mut v = vec![1, 2, 3, 4];
}
```

<!--
This is review problem 3 from Lecture 3, animated out
-->


---


# Pop Goes X

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

We take a reference `x` to its last element,

```rust
fn x_shouldnt_exist() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
}
```


---


# Pop Goes X

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

We take a reference `x` to its last element, remove the last element,

```rust
fn x_shouldnt_exist() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
    v.pop(); // Removes last element in `v`
}
```


---


# Pop Goes X

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

We take a reference `x` to its last element, remove the last element, and print `x`.

```rust
fn x_shouldnt_exist() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
    v.pop(); // Removes last element in `v`
    println!("{}", x); // What is `x`?
}
```


---


# Pop Goes X

![bg right:25% 75%](../images/ferris_panics.svg)

We take a reference `x` to its last element, remove the last element, and print `x`.

```rust
fn x_shouldnt_exist() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
    v.pop(); // Removes last element in `v`
    println!("{}", x); // What is `x`?
}
```

`x` is invalid! `v[3]` can be any value ⇒ undefined behavior


---


# Pop Goes X

![bg right:25% 75%](../images/ferris_happy.svg)

Thankfully, our borrowing rules prevent this

```
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> src/main.rs:4:5
  |
3 |     let x = &v[3];
  |              - immutable borrow occurs here
4 |     v.pop(); // Removes last element in `vec`
  |     ^^^^^^^ mutable borrow occurs here
5 |     println!("{}", x); // What is `x`?
  |                    - immutable borrow later used here
```

* We cannot mutably borrow a value with an existing immutable borrow
* Without the borrowing rules, `x` would point to invalid memory!


---


# Push Comes to Shove

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Instead of removing the last element,

```rust
fn please_dont_move() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
    v.pop(); // Remove last element in `v`
}
```


---


# Push Comes to Shove

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Instead of removing the last element, let's add a new element!

```rust
fn please_dont_move() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
    v.push(5); // Add an element to the end of `v`
}
```


---


# Push Comes to Shove

![bg right:25% 75%](../images/ferris_does_not_compile.svg)

Surely nothing will happen to `x` this time?

```rust
fn please_dont_move() {
    let mut v = vec![1, 2, 3, 4];
    let x = &v[3];
    v.push(5); // Add an element to the end of `v`
    println!("{}", x); // What is `x`?
}
```


---


# Push Comes to Shove

![bg right:25% 75%](../images/ferris_panics.svg)

Quandary!

```
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> src/main.rs:4:5
  |
3 |     let x = &v[2];
  |              - immutable borrow occurs here
4 |     v.push(5);
  |     ^^^^^^^^^ mutable borrow occurs here
5 |     println!("{}", x); // What is `x`?
  |                    - immutable borrow later used here
```


---


# Push Comes to Shove

![bg right:25% 75%](../images/ferris_happy.svg)

The compiler isn't paranoid! It's prudent.

```
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> src/main.rs:4:5
  |
3 |     let x = &v[2];
  |              - immutable borrow occurs here
4 |     v.push(5);
  |     ^^^^^^^^^ mutable borrow occurs here
5 |     println!("{}", x); // What is `x`?
  |                    - immutable borrow later used here
```

* What if pushing `5` onto `v` triggers a resize?
    * Resizing means allocating new memory for `v`, copying data, and deallocating old `v`
* `x` would no longer point to valid memory!


<!--
What if you, as the programmer, knew that this push doesn't resize?
    e.g. vector is power of 2

You can calm the compiler with a special keyword, `unsafe`
We will talk about `unsafe` in the later weeks.
-->


---


# Unveiling the Borrow Checker

> "His blade works so smoothly that the ox does not feel it." - The Dextrous Butcher

Become the borrow checker whisperer
- Fix errors with ease
- Craft elegant, efficient solutions



---


# Permissions of Places

Denote the left side of assignments as **places**.

```rust
let x = &v[3];
    ^ place
```

The borrow checker checks permissions of **places**.


---


# Permissions of Places


Places include:
* Variables, like `a`
* Dereferences of places, like `*a`
* Array accesses of places, like `a[0]`
* Fields of places, like `a.0`, `a.field`
* Any combination of the above, like `*((*&a[2].field)[5].0.1)`

First, let's talk about variables.

---


# Permissions of Variables

Upon birth, a variable has the permissions
* Read: can be copied
* Own: can be moved or dropped


If declared `mut`,
* Write: can be mutated

References temporarily remove these permissions.


---

<!--
High-level sketch:
    => references are non-owning pointers
    => introduce diagrams with RWO permissions
            can skip flow permission since we haven't discussed Lifetimes yet
After walking through example with RWO permissions, check time

If time, we address the second question "Between multiple safe fixes, how do I choose the 'best' fix?"
    - heuristic: most performant is minimize copying via references
        - however, don't always want this
        - example: in FP, prevent side effects, avoid argument mutation
    - 
-->
