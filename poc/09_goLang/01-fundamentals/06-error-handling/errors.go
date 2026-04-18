package main

import "errors"

var (
	ErrEmptyPath    = errors.New("path is empty")
	ErrFileNotFound = errors.New("file not found")
)
