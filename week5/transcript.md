# Stack and Heap

Same as current slides

# Boxes

Explain that `Box` points to data on the heap - rehash Brown example

Then add that we can convert `Box`s to and from raw pointers with
* `ptr = Box::into_raw(some_box)` is like `ptr = malloc(...)`, consumes `some_box` to create raw `ptr`
*  `Box::from_raw(ptr)` is like `free(ptr)`, consumes `ptr` to create `Box`

# Vector Push and Pop Example

illustrate how vector resizing causes invalid memory accesses => undefined behavior!!

# Why Undefined Behavior is "Bad"

Up until today, we basically hand-waved undefined behavior as "bad".

We say, "segfault!" and you all unanimously go, "Woaaah that's bad!"

We say "double free!!" and you all unanimously go, "Woaah, bad!"

When we show you a program that doesn't compile and ask you why it doesn't compile,
you raise your hand and say, "That's a double free!" or "That points to invalid memory!"
and we say, "Very good, that IS a double free!" and left it at that.

But can someone tell me why is this "bad"? What's wrong with freeing memory twice, or accessing freed memory?

Say I have some memory, pointed to by `ptr`. I free it twice:
```c
free(ptr)
free(ptr)
```

What's actually wrong with this double-free? My program goes on as normal, right?

And what's wrong with accessing invalid memory addresses? I know some people who purposefully read invalid memory and treat the values in invalid memory as their very own random number generator. Aside from the fact that it's not a terribly good random number generator, what's wrong with this?

(Ask for audience guesses)

Okay, there's nothing wrong with the examples we mentioned above. We might get weird behavior in our program, sure, but nothing earth-shattering.

The reason why our examples were okay was because we had full control over what we're freeing, what we're allocating, and in what order.
* We free `ptr` twice, but the important thing is that we chose to free `ptr`, and we didn't take a weirdly specific sequence of steps that would cause anything "bad" to happen.
* We read from invalid memory, but that's it, we just read from invalid memory. We don't write to invalid memory, and we especially don't ask the user what we should write.

However, what if we hand over some of this control? What if, say, we give the user some control over when we allocate and when we free? What if, in addition to giving the user this control, we also ask the user what we should write in our memory?

That's where the problem comes in.

## WIP

To understand why this is a problem, we must understand the heap allocator. This will just be a high level overview:

You can think of the heap allocator as a manager of linked lists. Your heap memory is divided into small units called "chunks," and each chunk is on a linked list.

Actual allocators will have many, many linked lists for different sized chunks, and we call each linked list a "bin". There's a long, complicated flowchart of which bins your allocator will look through and in what order.

But for the purposes of our discussion, we'll just look at one bin, aka one linked list.

When you request memory, the heap allocator serves you a chunk from the linked list if one exists, or creates a brand new chunk if it's empty. When you free memory, your chunk gets inserted onto the linked list.

## UAF

When you free chunk A, it gets added to the linked list. Later, when you allocate chunk B, if it's in the same size range as chunk A, then (depending on your allocator implementation) your allocator look in the same linked list as A and serve you the chunk that had once been A's.

Now say that you forgot you freed chunk A, and you continue using it as though it's chunk A. Remember that chunk B points to the same memory as chunk A! Now you're stepping on yourself; whatever you write to chunk B will affect chunk A, so you better not keep using it as though it's chunk A.

If the person who's writing to chunk B is also you, and you know what you're doing, then, uh, this is kind of awkward and weird to do in a program, but it's fine. But! If the person who's using chunk B is not you and quite malicious, then they can mess with your chunk A by writing to chunk B.

## Double-free

Suppose we want to overwrite `super_special_address` with a magic value

When you free chunk A twice, your linked list looks like this:

> HEAD -> A -> A
        
Then when you allocate chunk B, chunk B gets the same memory address as chunk A

> HEAD -> A

*However*, note that chunk A is still in the linked list!

When you write to chunk B, you can modify chunk A's metadata. Since chunk A is on the linked list, it stores a forward and backward pointer.

So, you can overwrite chunk A's forward pointer to `super_special_address`, and by carefully matching the metadata checks made by your allocator, you can fake a chunk at `super_special_address`

Then your next allocation will give you memory at `super_special_address`, which you can overwrite with your desired value

Actual heap allocators have way more protections than this, so you can't easily exploit these vulnerabilities. It can be a rabbit hole and we're happy to recommend resources if you're interested.

We'll move on and talk about how Rust's borrow checker prevents these issues.

# RWO Permissions

same explanation "borrow checker checks permissions of places, references temporarily remove permissions of places"

same explanation as before about how permissions are tracked for immutable vs mutable references

then same example as before about mutating places in an array