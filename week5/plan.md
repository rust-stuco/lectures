## Week 5: Ownership, Unpacked

- The Rules
- The Objective
    - Q1: Why unsafe
    - Q2: How fix
- Q1: Defining Unsafety
- Types of Memory
    - Static, Heap, Stack
    - When allocated
    - Where allocated
- Motivation for Ownership
    - Safely deallocating heap memory
- Motivation for Borrowing
- Q2: Choosing Between Fixes

<!--
Remaining sketch:
    Motivation for Borrowing
        Revisit ownership review problem
        "what if we don't want to clone()"
        "we create a reference instead"
        => references are non-owning pointers
        => introduce diagrams with RWO permissions

After taking through Motivation for Borrowing,
    this answers our first question, "When my program is rejected, why might it be unsafe?"

Then we address the second question "Between multiple safe fixes, how do I choose the 'best' fix?"
    - heuristic: most performant is minimize copying via references
        - however, don't always want this
        - example: in FP, prevent side effects, avoid argument mutation
    - 
-->