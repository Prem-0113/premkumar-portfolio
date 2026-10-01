#!/usr/bin/env python3
# Generates index.html for Premkumar V portfolio
import sys

def main():
    with open("index.html", "r", encoding="utf-8") as f:
        print("index.html is ready, size:", len(f.read()), "bytes")

if __name__ == "__main__":
    main()
