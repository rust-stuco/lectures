// these aren't _quite_ functional tests,
// and should all be compile_fail,
// but may be illustrative

use crate::cell::Cell;

#[test]
fn concurrent_set() {
    use std::sync::Arc;
    let x = Arc::new(Cell::new(42));
    let x1 = Arc::clone(&x);
    std::thread::spawn(move || {
        x1.set(43);
    });
    let x2 = Arc::clone(&x);
    std::thread::spawn(move || {
        x2.set(44);
    });
}

#[test]
fn set_during_get() {
    let x = Cell::new(String::from("hello"));
    let first = x.get();
    x.set(String::new());
    x.set(String::from("world"));
    eprintln!("{}", first);
}

#[test]
fn concurrent_set_take2() {
    use std::sync::Arc;
    let x = Arc::new(Cell::new([0; 40240]));
    let x1 = Arc::clone(&x);
    let jh1 = std::thread::spawn(move || {
        x1.set([1; 40240]);
    });
    let x2 = Arc::clone(&x);
    let jh2 = std::thread::spawn(move || {
        x2.set([2; 40240]);
    });
    jh1.join().unwrap();
    jh2.join().unwrap();
    let xs = x.get();
    for &i in xs.iter() {
        eprintln!("{}", i);
    }
}

#[test]
fn concurrent_get_set() {
    use std::sync::Arc;
    let x = Arc::new(Cell::new(0));
    let x1 = Arc::clone(&x);
    let jh1 = std::thread::spawn(move || {
        for _ in 0..1000000 {
            let x = x1.get();
            x1.set(x + 1);
        }
    });
    let x2 = Arc::clone(&x);
    let jh2 = std::thread::spawn(move || {
        for _ in 0..1000000 {
            let x = x2.get();
            x2.set(x + 1);
        }
    });
    jh1.join().unwrap();
    jh2.join().unwrap();
    assert_eq!(x.get(), 2000000);
}