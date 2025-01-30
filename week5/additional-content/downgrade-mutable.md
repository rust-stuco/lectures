---
marp: true
theme: rust
class: invert
paginate: true
---

<!-- This would go before "Recap: Mutable References" -->

---


# Example: Mutable References

We can **downgrade** mutable references.

<div class = "container">
<div class = "col">

```rust
let mut v = vec![1, 2, 3, 4];
let x = &mut v[3];
```

</div>

<div class = "col">

Place | R | W | O
-----|-----|-----|-----:
v | - | - | -
x | R | - | O
*x | R | W | -

</div>

</div>


---


# Example: Mutable References

We can **downgrade** mutable references.

Say we take a reference `y` to `x`.

<div class = "container">
<div class = "col">

```rust
let mut v = vec![1, 2, 3, 4];
let x = &mut v[3];
let y = &*x;
```

</div>

<div class = "col">

Place | R | W | O
-----|-----|-----|-----:
v | - | - | -
x | R | - | O
*x | R | W | -
*y | - | - | -

</div>

</div>


---


# Example: Mutable References

We can **downgrade** mutable references.

`y` is an immutable reference, but...

<div class = "container">
<div class = "col">

```rust
let mut v = vec![1, 2, 3, 4];
let x = &mut v[3];
let y = &*x;
```

</div>

<div class = "col">

Place | R | W | O
-----|-----|-----|-----:
v | - | - | -
x | R | - | O
*x | R | W | -
*y | R | - | -

</div>

</div>


---


# Example: Mutable References

We can **downgrade** mutable references.

`y` is an immutable reference, but...`x` is a mutable reference.

<div class = "container">
<div class = "col">

```rust
let mut v = vec![1, 2, 3, 4];
let x = &mut v[3];
let y = &*x;
```

</div>

<div class = "col">

Place | R | W | O
-----|-----|-----|-----:
v | - | - | -
x | R | - | O
*x | R | W | -
*y | R | - | -

</div>

</div>


---


# Example: Mutable References

We downgrade x by removing W.

* Avoid simultaneous aliasing with mutation ✓

<div class = "container">
<div class = "col">

```rust
let mut v = vec![1, 2, 3, 4];
let x = &mut v[3];
let y = &*x;
```

</div>

<div class = "col">

Place | R | W | O
-----|-----|-----|-----:
v | - | - | -
x | R | - | O
*x | R | - | -
*y | R | - | -

</div>

</div>

