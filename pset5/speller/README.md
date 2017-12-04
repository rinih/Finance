# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?
   This is lung diseae caused by sicila dust.

## According to its man page, what does `getrusage` do?
 'getrusage' is used to access the usage information of a program (send pointer to the struct with the usage information)
  such as the memory usage, program runnng time, etc.

## Per that same man page, how many members are in a variable of type `struct rusage`?
   'Struct Rusage' has 16 members.

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?
   We do this because since the 'getrusage' sends pointers to the struct with the usage information, thus this command
   expects pointers which require these refernces instead of values to move around faster.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.


## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?
   We use 'fgetc' as it goes through each character one at a time and dont use 'fscanf' as it ignores whitespace and so it can not
    distinguish when the end of the word is, however 'fgetc' can.


## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

