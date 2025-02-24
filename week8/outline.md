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

CONTEXT: STACK, HEAP, `Box`s, AND UNDEFINED BEHAVIOR 
- **ALTERNATE POV 1: The “owners” are stack frames**
    - Context: Stack, Heap
        - Introduce `Box` type. Instead of a `Vec` of 0xDEADBEEFS, we'll have an array of deadbeefs that gets wrapped in `Box`
- Review: Vector Resizing Example
    - Primary purpose: jog memory of borrowing rules
    - Secondary purpose: foreshadow `unsafe`
        - Although this example is Scenario 1 (code is unsafe), it *can* be Scenario 2 (code is safe, but borrow checker has limitations). If we’re confident it doesn’t trigger a resize, can use `unsafe`
        - Transition: emphasize that `unsafe` must be used judiciously, so we must understand how the borrow checker works

WHY UNDEFINED BEHAVIOR IS "BAD"
- We handwaved undefined behavior as "bad," but why bad?
- Heap allocator as manager of linked list
- Sample exploits
    - UAF
    - Double-free

HOW BORROW CHECKER ENFORCES RULES
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
