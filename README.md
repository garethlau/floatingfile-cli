# The Official CLI for floatingfile

## Usage

### Create a new space

```
$ python main.py create
> Created a new space: ABC123
```

### Destroy an existing space

```
$ python main.py destroy --code=ABC123
> Space deleted.
```

### Upload files

```
$ python main.py upload --code=c52505 ./test_files
Which files do you want to upload?
(0) test1.txt
(1) test2.txt
(2) test3.txt

$ 0 2
> [==============================] 100%
> Done!
```

### List files

```
$ python main.py list --code=c52505
> test3 248da3d2-4585-4216-8c28-52fcb18f63c4
> test1 aae092f2-81e0-4f2d-bb0f-b6348f66e209
```

### Remove files

```
$ python main.py remove --code=c52505
> Which files(s) would you like to remove?
> (0) test3.txt
> (1) test1.txt
$ 1
> Files successfully removed. The remaining files are:
> test3.txt
```

## Roadmap

- [] Error handling and user feedback
- [] Generate executable binary
- [] Documentation and usage guides
- [] Persist code between executions
