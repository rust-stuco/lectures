Can fit in ~20 more minutes of content. Some examples I'm considering:

Written:
* Aliasing and Mutating a Data Structure (see below)
* Mutable vs Immutable Borrowing in Loops (see below)
* Borrowing in Structs (see below)
* Downgrading Mutable References (see downgrade-mutable.md)
    * missing a problem, ideally provide a problem that would require students to understand downgrading

Not written:
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

# Example: Borrowing in Structs

Copy the below code into [aquascope](https://cel.cs.brown.edu/aquascope/) to illustrate how `self` is laid out in struct methods

```rust
struct Rectangle {
    width: u32,
    height: u32,
}
impl Rectangle {    
  fn max(self, other: Self) -> Self {
    let w = self.width.max(other.width);
    let h = self.height.max(other.height);
    Rectangle { 
      width: w,
      height: h
    }
  }
    fn set_to_max(&mut self, other: Rectangle) {
        let max = self.max(other);
        *self = max;
    }
}

fn main() {
    let mut rect = Rectangle { width: 0, height: 1 };
    let other_rect = Rectangle { width: 1, height: 0 };
    rect.set_to_max(other_rect);
}
```

Code doesn't compile until we add `Copy`, `Clone` traits to Rectangle
```rust
#[derive(Copy, Clone)]
struct Rectangle {
    width: u32,
    height: u32,
}
```

To prevent double-free, Rust doesn't automatically derive `Copy` for structs.

Example: Suppose Rectangle has the `Copy` trait. Also suppose that we add a `name: String` field to `Rectangle`.
In short, `rect.name` gets freed twice:
    * First free is in `let max = self.max(other)`. In short, the method `max()`'s stack frame takes ownership of `self.name` and `other.name`. When the method `max()` returns, Rust deallocates its stack frame, and hence frees `self.name`, aka `rect.name`
    * Second free is in `*self = max`. When `*self` is overwritten, Rust implicitly calls drop on the data previously in `*self`, which subsequently frees all fields in the struct. Hence, `self.name`, aka `rect.name`, gets freed a second time