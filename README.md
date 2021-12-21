# The Official CLI for floatingfile

![](/.github/assets/banner.jpg)

[floatingfile](https://floatingfile.space) is a file sharing platform that marries the flexibility of file storage applications with the convenience of file transfer applications.

## Functions

At the moment, the CLI has not reached feature parity with the web and iOS applications, but this is the goal.

- [x] Create a space
- [x] Destroy a space
- [x] Upload a file (or files)
- [x] Remove a file (or files)
- [x] Download a file (or files)
- [x] View files
- [ ] View users
- [ ] View space's history (logs)
- [ ] Download files as zip

## Usage

### Create a new space

```
$ python main.py create
>
> >>> floatingfile
>
> ====================
>        420293
> ====================
>
> Done!
> The code has been saved and will be used for following commands. If you wish to override this code, you can do so via the --code flag.
```

### Destroy an existing space

```
$ python main.py destroy
>
> >>> floatingfile
>
> Done!
```

### Download files

```
$ python main.py download
>
> >>> floatingfile
>
> ? Which file would you like to download?
> (0) test3
> (1) test1
$ 0
> Done!
```

### Upload files

```
$ python main.py upload ./test_files
>
> >>> floatingfile
>
> ? Which files do you want to upload?
> (0) test1.txt
> (1) test2.txt
> (2) test3.txt
$ 0 2
> [==============================] 100%
> Done!
```

### List files

```
$ python main.py list
>
> >>> floatingfile
>
> test3 248da3d2-4585-4216-8c28-52fcb18f63c4
> test1 aae092f2-81e0-4f2d-bb0f-b6348f66e209
> Done!
```

### Remove files

```
$ python main.py remove
>
> >>> floatingfile
>
> ? Which files(s) would you like to remove?
> (0) test3.txt
> (1) test1.txt
$ 0
> Done!
```

## Roadmap

- [ ] Error handling and user feedback
- [ ] Generate executable binary
- [ ] Documentation and usage guides
- [x] Persist code between executions
