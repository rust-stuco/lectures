Can fit in ~20 more minutes of content. Some examples I'm considering:

Written:
* Aliasing and Mutating a Data Structure (see below)
* Mutable vs Immutable Borrowing in Loops (see below)
* Downgrading Mutable References (see downgrade-mutable.md)
    * missing a problem, ideally provide a problem that would require students to understand downgrading

Not written:
* Borrowing in structs
* Borrowing in tuples

# Example: Aliasing and Mutating a Data Structure

For each string in `src`, if it is larger than the first string in `dest`, we add it to the end of `dest`

```rust
fn add_big_strings(dest: &mut Vec<String>, src: &[String]) {
    let first: &String = &dest[0];
    for s in src {
        if s.len() > first.len() {
            dest.push(s.clone());
        }
    }
}
```

Does not compile because `let first = &dest[0]` removes the W permissions on `dest`, but `dest.push()` requires the W permission

Solution 1: `clone()`, but inefficient
```rust
fn add_big_strings(dest: &mut Vec<String>, src: &[String]) {
    let first: &String = &dest[0].clone(); // previously &dest[0]
    for s in src {
        if s.len() > first.len() {
            dest.push(s.clone());
        }
    }
}
```

Solution 2: create a temporary vector, copy all strings to add into this temporary vector, then copy temporary vector into `dest`

Also very inefficient!

Solution 3: save the _length_ of first string, rather than its contents
```rust
fn add_big_strings(dest: &mut Vec<String>, src: &[String]) {
    let first_len: usize = dest[0].len();
    for s in src {
        if s.len() > first_len {
            dest.push(s.clone());
        }
    }
}
```

# Example: Mutable vs Immutable Borrowing in Loops

Since students asked about hypothetical scenarios involving loops in lecture 2

This is another example about loops, but it involves some knowledge of iterators, which we talk about in lecture 8

Even though we take a mutable reference `&mut numbers`, it doesn't work! Although `&mut numbers` creates a mutable reference, the **iterator borrow** takes precedence and locks the collection in a way that prohibits further mutation like 

```rust
fn main() {
    let mut numbers = vec![1, 2, 3];

    for n in &mut numbers {
        numbers.push(*n); // ERROR: Cannot borrow `numbers` as mutable
    }
}
```

So actually, the code desugars to
```rust
let iter = (&mut numbers).into_iter(); // Creates a mutable iterator.
while let Some(n) = iter.next() {
    numbers.push(*n); // ERROR
}
```
Students don't need to know the specifics of the iterator; they just need to know that `iter.next()` is some black box that gives an immutable reference to the array elements


To fix, we must create a temporary vector:

```rust
fn main() {
    let mut numbers = vec![1, 2, 3];
    let mut temp = vec![];

    for n in &mut numbers {
        temp.push(*n);
    }
    numbers.append(&mut temp);
}
```