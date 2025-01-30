# Main Outline

INTRODUCTION
- Thesis: We present two alternate ways of looking at ownership, for the purpose of making informed decisions in light of compile errors.
- Objective: Given a compile error message, diagnose as one of the following scenarios:
    - Scenario 1: Code is unsafe, and borrow checker correctly deduces this
    - Scenario 2: Code is safe, but borrow checker has limitations
- In order to confidently differentiate the two scenarios, we must understand how the borrow checker works

BACKGROUND
- Restatement of Ownership Rules and Borrowing Rules
- Definition of Safety

OWNERSHIP RULES
- **ALTERNATE POV 1: The “owners” are stack frames**
    - Context: Stack, Heap
        - Introduce `Box` type. Instead of a `Vec` of 0xDEADBEEFS, we'll have an array of deadbeefs that gets wrapped in `Box`
    - Example: Lecture 3's `self` vs `&self`
        - Show stack frame diagrams of `self` vs `&self`
        - Why we need this alternate POV: It’s easier to think of owners as stack frames. Under our old POV “owners are variables,” students get confused by `self`, `rectangle`, especially the idea that we’re moving `rectangle` into itself. Instead, think of it as moving `rectangle` into the function `area`'s stack frame.

BORROWING RULES
- Review: Vector Resizing Example
    - Primary purpose: jog memory of borrowing rules
    - Secondary purpose: foreshadow `unsafe`
        - Although this example is Scenario 1 (code is unsafe), it *can* be Scenario 2 (code is safe, but borrow checker has limitations). If we’re confident it doesn’t trigger a resize, can use `unsafe`
        - Transition: emphasize that `unsafe` must be used judiciously, so we must understand how the borrow checker works
- **ALTERNATE POV 2: The borrowing rules are implemented by checking permissions of places**
    - Context
        - Definition of place: left-hand side of assignments
        - Definition of permissions: R, W, O
        - References temporarily remove these permissions
            - Talk through permission rules for Immutable and Mutable References, subtle differences
    - Example: Mutating Different Array Elements
        - Verdict: Scenario 2, is safe but borrow checker has limitations
        - Borrow checker doesn’t have a unique places for each array index; a single place represents all array indices
            - Fix 1: `unsafe` block
            - Fix 2: `split_at_mut`, which uses `unsafe` under the hood (doesn’t have a slide but can add)
        - Why we can’t fix without this alternative POV: Requires understanding what a “place” is, hence why “check permissions of places” is important to know

CONCLUSION
- To confidently diagnose Scenario 1 from Scenario 2, adopt the following:
    - Summarize Alternate POV 1:
        - Think of owners as stack frames
        - Draw stack-heap diagrams to reason about memory
    - Summarize Alternate POV 2:
        - Draw RWO tables to reason about permissions of places
    - If the above process revealed the reason code was unsafe ⇒ Scenario 1
    - Otherwise, if am convinced code is safe after the above process ⇒ Scenario 2
        - Use `unsafe` block

# Additional Content

thoughts on adding these?

## Mutable Reference Downgrading
Left it out because it didn’t directly connect to the example “Mutating Different Array Elements,” so I felt like audience might forget it

## Borrowing from Composite Data Types
[Borrowing Fields of Struct](https://rust-book.cs.brown.edu/ch05-01-defining-structs.html#borrowing-fields-of-a-struct)
[Borrowing Fields of Tuple](https://rust-book.cs.brown.edu/ch04-03-fixing-ownership-errors.html#fixing-a-safe-program-mutating-different-tuple-fields)

## Copy vs non-Copy
https://rust-book.cs.brown.edu/ch04-03-fixing-ownership-errors.html#fixing-an-unsafe-program-copying-vs-moving-out-of-a-collection

