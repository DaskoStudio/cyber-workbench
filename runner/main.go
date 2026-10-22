package main

import (
	"errors"
	"fmt"
	"os"
)

func tcpConnect() error {
	// logique privée — non incluse
	return errors.New("not implemented")
}

func tlsAudit() error {
	// logique privée — non incluse
	return errors.New("not implemented")
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: runner <tcp-connect|tls-audit>")
		os.Exit(2)
	}
	var err error
	switch os.Args[1] {
	case "tcp-connect":
		err = tcpConnect()
	case "tls-audit":
		err = tlsAudit()
	default:
		fmt.Fprintln(os.Stderr, "unknown command")
		os.Exit(2)
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
