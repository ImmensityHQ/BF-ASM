// WIP

use std::env;
use std::fs;
use std::io::Read;
use std::process;

fn remove_redundant_code(program: String) -> String {
    return program
        .replace("+-", "")
        .replace("<>", "")
        .replace("-+", "")
        .replace("><", "")
        .replace("][-]", "]")
        .replace("[]", "");
}

fn optimize(program: String) -> String {
    let mut prg = program;
    prg = remove_redundant_code(prg);
    return prg;
}

// fn compute_jmp_table(program: String) -> String {}

fn interpret(program: Vec<char>) {
    let mut mem: Vec<u8> = vec![0];
    let mut ptr = 0;
    let mut prg_idx = 0; // program cannot exceed 32-bit integer limit in length
    let mut open: u32;
    let mut closed: u32;
    while prg_idx < program.len() {
        match &program[prg_idx] {
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
                if mem[ptr] == 0 {
                    let mut tmp_idx = prg_idx;
                    open = 1;
                    while open != 0 {
                        tmp_idx += 1;
                        match &program[prg_idx] {
                            '[' => open += 1,
                            ']' => open -= 1,
                            _ => (),
                        }
                    }
                    prg_idx = tmp_idx;
                }
            }
            ']' => {
                if mem[ptr] != 0 {
                    let mut tmp_idx = prg_idx;
                    closed = 1;
                    while closed != 0 {
                        tmp_idx -= 1;

                        if tmp_idx >= *&program.len() {
                            panic!("Cannot find matching ]")
                        }

                        match &program[tmp_idx] {
                            '[' => closed -= 1,
                            ']' => closed += 1,
                            _ => (),
                        }
                    }
                    prg_idx = tmp_idx;
                }
            }
            _ => {}
        }
        prg_idx += 1;
    }
}

fn usage() -> String {
    return "Usage: ./bfasm-interpeter filename.bf".to_string();
}

fn read_file(filename: String) -> String {
    return fs::read_to_string(filename).expect("Something went wrong reading the file");
}

fn main() {
    let mut args: Vec<String> = env::args().collect();
    args.push("test2.bf".to_string());
    if args.len() != 2 {
        println!("{}", usage());
        process::exit(0);
    }
    let filename = &args[1];
    let program = read_file(filename.to_string());
    let program = optimize(program);
    interpret(program.chars().collect());
}
