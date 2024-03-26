// use std::cell::UnsafeCell;

pub struct Cell<T> {
    value: T,
}

impl<T> Cell<T> {
    pub fn new(value: T) -> Self {
        todo!()
    }

    pub fn set(&self, value: T) {
        todo!()
    }

    pub fn get(&self) -> T
    where
        T: Copy,
    {
        todo!()
    }
}
