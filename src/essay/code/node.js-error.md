# Node.js 的錯誤有哪些

## Network

| Error        | Context | Ambiguous | Meaning                                            |
| ------------ | ------- | --------- | -------------------------------------------------- |
| EACCES       | Server  | N/A       | Cannot listen on port due to permissions           |
| EADDRINUSE   | Server  | N/A       | Cannot listen on port since another process has it |
| ECONNREFUSED | Client  | No        | Client unable to connect to server                 |
| ENOTFOUND    | Client  | No        | DNS lookup for the server failed                   |
| ECONNRESET   | Client  | Yes       | Server closed connection with client               |
| EPIPE        | Client  | Yes       | Connection to server has closed                    |
| ETIMEDOUT    | Client  | Yes       | Server didn’t respond in time                      |

## Process

- `EACCES` (Permission denied): An attempt was made to access a file in a way forbidden by its file access permissions.
- `EADDRINUSE` (Address already in use): An attempt to bind a server ([`net`](https://nodejs.org/api/net.html), [`http`](https://nodejs.org/api/http.html), or [`https`](https://nodejs.org/api/https.html)) to a local address failed due to another server on the local system already occupying that address.
- `EPERM` (Operation not permitted): An attempt was made to perform an operation that requires elevated privileges.

## File System

- `EEXIST` (File exists): An existing file was the target of an operation that required that the target not exist.
- `EISDIR` (Is a directory): An operation expected a file, but the given pathname was a directory.
- `EMFILE` (Too many open files in system): Maximum number of [file descriptors](https://en.wikipedia.org/wiki/File_descriptor) allowable on the system has been reached, and requests for another descriptor cannot be fulfilled until at least one has been closed. This is encountered when opening many files at once in parallel, especially on systems (in particular, macOS) where there is a low file descriptor limit for processes. To remedy a low limit, run `ulimit -n 2048` in the same shell that will run the Node.js process.
- `ENOENT` (No such file or directory): Commonly raised by [`fs`](https://nodejs.org/api/fs.html) operations to indicate that a component of the specified pathname does not exist. No entity (file or directory) could be found by the given path.
- `ENOTDIR` (Not a directory): A component of the given pathname existed, but was not a directory as expected. Commonly raised by [`fs.readdir`](https://nodejs.org/api/fs.html#fs_fs_readdir_path_options_callback).
- `ENOTEMPTY` (Directory not empty): A directory with entries was the target of an operation that requires an empty directory, usually [`fs.unlink`](https://nodejs.org/api/fs.html#fs_fs_unlink_path_callback).
