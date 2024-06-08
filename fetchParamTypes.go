package main

import (
	"log"
	"strings"
	"fmt"
	"bufio"
	"io"
	"os"
	"encoding/json"
	"golang.org/x/exp/maps"
)

func main() {
	err := mainAux()
	if err != nil {
		log.Fatal(err)
	}
}

func mainAux() error {
	f, err := os.Open("out.txt")
	if err != nil {
		return err
	}
	defer f.Close()
	fTypes, err := os.Open("params.txt")
	if err != nil {
		return err
	}
	defer fTypes.Close()
	var types []funSpec
	err = json.NewDecoder(fTypes).Decode(&types)
	if err != nil {
		return err
	}
	return addTypes(f, types)
}

type funSpec struct {
	Name string `json:"name"`
	Params []map[string]string `json:"params"`
}

func addTypes(f io.Reader, types []funSpec) error {
	funs := make(map[string]map[string]string)
	for _, funSpec := range types {
		funs[funSpec.Name] = make(map[string]string)
		for _, p := range funSpec.Params {
			funs[funSpec.Name][maps.Keys(p)[0]] = maps.Values(p)[0]
		}
	}
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		var newFields []string
		fields := strings.Split(sc.Text(), "\t")
		for i, field := range fields {
			newField := field
			if i > 0 {
				newField = newField + ":" + funs[fields[0]][field]
			}
			newFields = append(newFields, newField)
		}
		fmt.Println(strings.Join(newFields, "\t"))
	}
	return sc.Err()
}
