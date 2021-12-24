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
- [x] Download and remove all files in a space

## Roadmap

- [ ] Documentation and usage guides
- [x] Persist code between executions
- [x] Keep a record of visited, active spaces and allow users to swap between spaces
- [x] Upload all files in a directory
- [ ] Sync a local directory with the contents of a space

## Installation

### Linux

TODO

### Windows

TODO

### Mac

1. Clone the repository

```
$ git clone https://github.com/garethlau/floatingfile-cli.git
$ cd floatingfile-cli
```

2. Bundle the app

_You may need to enable the execution permission for the script by running: `chmod +x ./scripts/bundle.sh`._

```
$ ./scripts/bundle.sh
```

This will generate a `dist` folder that contains the executable, `floatingfile`, as well as all necessary dependencies.

3. Create a symlink for global access.

By default, Mac OS X has `/usr/local/bin` in the `PATH`.

```
$ sudo ln -s "$PWD/dist/floatingfile/floatingfile" /usr/local/bin
```

4. Check that the executable is accessible

```
$ which floatingfile
> /usr/local/bin/floatingfile
```

5. **OPTIONAL** but recommended: You can rename the executable for easier usage.

```
$ mv /usr/local/bin/floatingfile /usr/local/bin/ff
```

The floatingfile CLI is now accessible via the `ff` command. For example:

```
$ ff create -h
> NAME
>    ff create - Create a space. This will overwrite the code saved in memory.
>
> SYNOPSIS
>    ff create -
>
> DESCRIPTION
>    Create a space. This will overwrite the code saved in memory.
```

## Usage

### Create a new space

```
$ floatingfile create
>
> >>> floatingfile
>
> Your newly created space can be accessed here:
> https://app.floatingfile.space/s/6B1574
>
> The code has been saved and will be used for following commands. If you wish to override this code, you can do so via the --code flag.
```

### Destroy an existing space

```
$ floatingfile destroy
>
> >>> floatingfile
>
> Done!
```

### Download files

```
$ floatingfile download
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
$ floatingfile upload ./test_files
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
$ floatingfile files
>
> >>> floatingfile
>
> test3 248da3d2-4585-4216-8c28-52fcb18f63c4
> test1 aae092f2-81e0-4f2d-bb0f-b6348f66e209
> Done!
```

### Remove files

```
$ floatingfile remove
>
> >>> floatingfile
>
> ? Which files(s) would you like to remove?
> (0) test3.txt
> (1) test1.txt
$ 0
> Done!
```
