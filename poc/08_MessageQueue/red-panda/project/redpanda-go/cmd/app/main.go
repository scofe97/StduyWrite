package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	chapter := os.Args[1]
	switch chapter {
	case "ch01":
		fmt.Println("TODO: Ch01 - Basic Setup & Health Check")
	case "ch02":
		fmt.Println("TODO: Ch02 - Configuration Patterns")
	case "ch03":
		fmt.Println("TODO: Ch03 - Producer Patterns")
	case "ch04":
		fmt.Println("TODO: Ch04 - Consumer & Manual Commit")
	case "ch05":
		fmt.Println("TODO: Ch05 - Error Handling & DLQ")
	case "ch06":
		fmt.Println("TODO: Ch06 - Idempotent Consumer")
	case "ch07":
		fmt.Println("TODO: Ch07 - Transaction Patterns")
	case "ch08":
		fmt.Println("TODO: Ch08 - SAGA Choreography")
	case "ch09":
		fmt.Println("TODO: Ch09 - SAGA Orchestration")
	case "ch10":
		fmt.Println("TODO: Ch10 - Testing Strategies")
	case "ch11":
		fmt.Println("TODO: Ch11 - Pipeline & EIP Patterns")
	case "ch12":
		fmt.Println("TODO: Ch12 - Schema Registry & Avro")
	default:
		fmt.Fprintf(os.Stderr, "Unknown chapter: %s\n", chapter)
		printUsage()
		os.Exit(1)
	}
}

func printUsage() {
	fmt.Println("Usage: redpanda-go <chapter>")
	fmt.Println()
	fmt.Println("Chapters:")
	fmt.Println("  ch01  Basic Setup & Health Check")
	fmt.Println("  ch02  Configuration Patterns")
	fmt.Println("  ch03  Producer Patterns")
	fmt.Println("  ch04  Consumer & Manual Commit")
	fmt.Println("  ch05  Error Handling & DLQ")
	fmt.Println("  ch06  Idempotent Consumer")
	fmt.Println("  ch07  Transaction Patterns")
	fmt.Println("  ch08  SAGA Choreography")
	fmt.Println("  ch09  SAGA Orchestration")
	fmt.Println("  ch10  Testing Strategies")
	fmt.Println("  ch11  Pipeline & EIP Patterns")
	fmt.Println("  ch12  Schema Registry & Avro")
}
