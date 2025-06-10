# Boki - Book Sorter
_Simple book sorter for `.epub`, `.pdf`, and `azw3`._ 

#### It's not perfect
The `.epub` sorter works the best, due to it using the `ebooklib` module to look for author and title. Remaining file types will go by title name, it will try it's best to sort them, however it will sometimes mess it up by having the _Author_ as the book title, and _title_ as the author. 

#### Process
1. Specify book path (it will look inside all directories in the books location)
2. Specify output path
3. Wait for it to be completed.

