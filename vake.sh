#!/bin/bash

# Store the list of errors and warnings
errs=()

# Run make and capture stderr output, putting each error/warning into errs 
while read line; do
  # Regex tests if the line is an error/warning
  if [[ $line =~ (.*):([0-9]+):([0-9]+):\ (error|warning):\  ]]; then
    errs+=("${line}")
  fi
  echo "${line}"
done < <(make $1 2>&1)

# Ask if we want to run vake or not
echo
read -p "vake: ${#errs[@]} errors or warnings. Run vake? [y/n] " -n 1 -r
echo "<Enter> to edit. 'q' to skip."
echo 

if [[ $REPLY =~ ^[Yy]$ ]]; then
  # Change IFS to colon to split file name, line number and column number
  IFS=':'

  for i in "${errs[@]}"; do
    echo 
    echo "$i"
    parts=( $(echo "${i}" | cut -d ':' -f 1-3) )

    # Print out the line of code that is concerned
    sed -n "${parts[1]}p" "${parts[0]}"
    sed -n "${parts[1]}p" "${parts[0]}" | tr -c '[:space:]' ' ' | \
      sed "s/./^/${parts[2]}"

    # Prompt for ex command
    read -p ":"
    vim "${parts[0]}" "+call cursor(${parts[1]}, ${parts[2]})" "+ ${REPLY}"
  done
fi
