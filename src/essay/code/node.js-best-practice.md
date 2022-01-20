# Node.js 最佳實作

## Do In Code

1.  Compression: proxy > app.use(compression())
2.  Asynchronous (async.) >> Synchronous (sync.) - The **only** reason to use sync. function is the time to start up server.
    唯一有理由使用同步函數的時機是在最初啟動之時
3.  Static files: proxy > serve-static > res.sendFile()
4.  Console is sync! Always use async or use sync only in development.
    - Debugging: debug >> console
    - Application: Winston / Bunyan >> console
5.  Handle Error ( Important!, Detail in next section )
    - Try-catch
    - Promise

## Handle Error

1. Try-catch is **synchronous**.
2. Express catch all sync. error in default (v.5 catch _Promise_ as well)

### What will log?

```js
const callback = async () => {
  console.log("do another thing");
  throw new Error("foo");
  console.log("do more thing");
};

const method = async () => {
  console.log("do first thing");
  await callback();
  console.log("do second thing");
};

const main = async () => {
  try {
    await method();
  } catch (err) {
    console.log("fire try-catch!");
  }

  console.log("finish project!");
};
```

#### result:

```
do first  thing
do another thing
do second thing
finish project!
UnhandledPromiseRejectionWarning: Error: foo
... (error stack)
```

#### why?

1. `callback` invoked some time later after `method` (`do another thing`)
2. happend exception! wait to finish other process
3. finish method (`do second thing`)
4. finish try-catch block
5. final run (`finish project!`)

### Category

1.  Operational Errors
    - The errors you are/can except.
    - Log, Show, Retry/Abort.
2.  Programmer Errors
    - [The best way to recover from programmer errors is to crash immediately](https://www.joyent.com/node-js/production/design/errors#fnref:1)
    - Try debug your program rather than handle it.

## Do In Configuration

1. `env.NODE_ENV='production';`
2. Rebuild after error, use [helpers](http://strong-pm.io/compare/) or _init_ system [[1]](https://wiki.debian.org/systemd)[[2]](http://upstart.ubuntu.com/)
3. Multi-threads [[1](https://nodejs.org/docs/latest/api/cluster.html)][[2](https://docs.strongloop.com/display/SLC/Clustering)]
4. Caching [[Varnish](https://www.varnish-cache.org/)][[Nginx](https://serversforhackers.com/nginx-caching/)]
5. Reverse-Proxy [[Nginx](https://serversforhackers.com/nginx-caching/)][[HAProxy](http://www.haproxy.org/)]