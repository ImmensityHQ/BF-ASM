// WIP

use std::collections::HashMap;
use std::env;
use std::fs;
use std::io::Read;
use std::process;

#[inline]
fn remove_redundant_code(program: String) -> String {
    return program
        .replace("+-", "")
        .replace("<>", "")
        .replace("-+", "")
        .replace("><", "")
        .replace("][-]", "]")
        .replace("[]", "");
}

#[inline]
fn optimize(program: String) -> String {
    let mut prg = program;
    prg = remove_redundant_code(prg);
    return prg;
}

#[inline]
fn compute_jmp_table(program: &Vec<char>) -> HashMap<usize, usize> {
    let mut idx = 0;
    let mut open: u32;
    let mut jmp_table: HashMap<usize, usize> = HashMap::new();
    // let mut closed: u32;
    while idx < program.len() {
        match program[idx] {
            '[' => {
                open = 1;
                let sidx = idx;
                let mut scan_idx = idx;
                while open != 0 {
                    scan_idx += 1;
                    match program[scan_idx] {
                        '[' => open += 1,
                        ']' => open -= 1,
                        _ => (),
                    }
                }
                let eidx = scan_idx;
                jmp_table.insert(sidx, eidx);
            }
            ']' => {
                // closed += 1;
            }
            _ => {}
        }
        idx += 1;
    }
    return jmp_table;
}

#[inline]
fn interpret(program: Vec<char>) {
    let mut mem: Vec<u8> = vec![0];
    let mut ptr = 0;
    let mut prg_idx = 0; // program cannot exceed 32-bit integer limit in length
    let jmp_table: HashMap<usize, usize> = compute_jmp_table(&program);
    while prg_idx < program.len() {
        match &program[prg_idx] {
            // TODO: optimize repeated instructions.
            '+' => {
                if mem[ptr] == 255 {
                    mem[ptr] = 0;
                } else {
                    mem[ptr] += 1;
                }
            }
            '-' => {
                if mem[ptr] == 0 {
                    mem[ptr] = 255;
                } else {
                    mem[ptr] -= 1;
                }
            }
            '>' => {
                ptr += 1;
                if mem.len() - 1 < ptr {
                    mem.push(0);
                }
            }
            '<' => {
                if ptr >= 1 {
                    ptr -= 1;
                }
            }
            ',' => {
                let mut buf = [0; 1];

                match std::io::stdin().read_exact(&mut buf) {
                    Ok(_) => mem[ptr] = buf[0],
                    Err(_) => {
                        panic!("Cannot read stdin");
                    }
                }
            }
            '.' => {
                print!("{}", mem[ptr] as char);
            }
            '[' => {
                /* When the interpreter encounters a '[',
                it should jump to the matching end ']',
                but only if the current cell is zero. */

                // Check if the current cell is zero.
                if mem[ptr] == 0 {
                    // If the current cell is zero, go to the matching end bracket.
                    prg_idx = *jmp_table.get(&prg_idx).expect("Cannot find matching ].");
                }
            }
            ']' => {
                /* When the interpreter encounters the end of a loop,
                it should go to the beginning of the loop if the
                current cell is not zero. */

                // Check if the current cell is not zero
                if mem[ptr] != 0 {
                    // if the current cell is not zero, set the program counter to the beginning of the loop
                    // prg_idx = *jmp_table.get(&prg_idx).expect("Cannot find matching [.");

                    for (key, value) in jmp_table.iter() {
                        if *value == prg_idx {
                            prg_idx = *key;
                            break;
                        }
                    }
                }
            }
            _ => {}
        }
        prg_idx += 1;
    }
}

#[inline]
fn usage() -> String {
    return "Usage: ./bfasm-interpeter filename.bf".to_string();
}

#[inline]
fn read_file(filename: String) -> String {
    return fs::read_to_string(filename).expect("Something went wrong reading the file");
}

fn main() {
    // TODO: Add proper argument parsing
    // TODO: ADD a way to print output to file.
    // e.g. "./interpreter mandelbrot.bf -o mandelbrot.out"
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("{}", usage());
        process::exit(0);
    }
    let filename = &args[1];
    let program = read_file(filename.to_string());
    let program = optimize(program);
    interpret(program.chars().collect());
}
