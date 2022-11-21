---
tags: Changelog
---

# Nginx from 1.18.0 to 1.22.1

Nginx using [calendar versioning](https://calver.org), and it release stable version every 2 years.

If you are wondering what changes between 1.18 and 1.20 then you can see all changes in 1.19.
The reason 1.22 has additional version (1.22.1) is because CVE
([CVE-2022-41741](https://www.google.com/search?client=safari&rls=en&q=CVE-2022-41741&ie=UTF-8&oe=UTF-8),
[CVE-2022-41742](https://nvd.nist.gov/vuln/detail/CVE-2022-41742))

Message prefix **👁️** is change that I think it is important.

You can grep the messages by raw changes: [by-versions](#by-versions)
or by structured: [by-module](#by-module)/[by-protocols](#by-protocols)/[others](#global).

## Global

Security:

-   1-byte memory overwrite might occur during DNS server response processing if the `resolver` directive was used, allowing an attacker who is able to forge UDP packets from the DNS server to cause worker process crash or, potentially, arbitrary code execution ([CVE-2021-23017](https://nvd.nist.gov/vuln/detail/CVE-2021-23017)). [1.21.0]

Feature:

-   the `min_free` parameter of the `proxy_cache_path`, `fastcgi_cache_path`, `scgi_cache_path`, and `uwsgi_cache_path` directives. Thanks to Adam Bambuch. [1.19.1]
-   the `userid_flags` directive. [1.19.3]
-   the `proxy_cookie_flags` directive. [1.19.3]
-   the same source files can now be specified in different modules while building addon modules. [1.19.5]
-   the -e switch. [1.19.5]
-   **👁️** now, if free worker connections are exhausted, nginx starts closing not only keepalive connections, but also connections in lingering close. [1.19.7]
-   flags in the `proxy_cookie_flags` directive can now contain variables. [1.19.8]
-   the `$connection_time` variable. [1.19.10]
-   the `keepalive_time` directive. [1.19.10]
-   request body filters API now permits buffering of the data being processed. [1.21.2]
-   support for sendfile(SF_NOCACHE) on FreeBSD. [1.21.5]

Bugfix:

-   `negative size buf in writer` alerts might appear in logs if a memcached server returned a malformed response. [1.19.1]
-   on XFS and NFS file systems disk cache size might be calculated incorrectly. [1.19.1]
-   zero length UDP datagrams were not proxied. [1.19.1]
-   **👁️** nginx did not delete unix domain listen sockets during graceful shutdown on the SIGQUIT signal. [1.19.1]
-   a segmentation fault might occur in a worker process if different `large_client_header_buffers` sizes were used in different virtual servers. [1.19.2]
-   `[crit] cache file ... has too long header` messages might appear in logs if caching was used and the backend returned responses with the `Vary` header line. [1.19.3]
-   the `stale-if-error` cache control extension was erroneously applied if backend returned a response with status code 500, 502, 503, 504, 403, 404, or 429. [1.19.3]
-   in request body filters internal API. [1.19.5]
-   `upstream sent frame for closed stream` errors might occur when working with gRPC backends. [1.19.5]
-   nginx returned the 400 response on requests like `GET http://example.com?args HTTP/1.0`. [1.19.6]
-   a segmentation fault might occur in a worker process if HTTPS was used; the bug had appeared in [1.19.5]. [1.19.6]
-   `no live upstreams` errors if a `server` inside `upstream` block was marked as `down`. [1.19.6]
-   in the `add_trailer` directive. [1.19.7]
-   HEAD requests were handled incorrectly if the `return` directive was used with the `image_filter` or `xslt_stylesheet` directives. [1.19.7]
-   `zero size buf in output` alerts might appear in logs if an upstream server returned an incorrect response during unbuffered proxying; the bug had appeared in [1.19.1]. [1.19.7]
-   in the eventport method. [1.19.8]
-   some errors were logged as unknown if nginx was built with glibc 2.32. [1.19.8]
-   in the eventport method. [1.19.9]
-   **👁️** nginx might not detect that a connection was already closed by the client when waiting for `auth_delay` or `limit_req` delay, or when working with backends. [1.19.9]
-   **👁️** nginx might not close a connection till keepalive timeout expiration if the connection was closed by the client while discarding the request body. [1.19.9]
-   special characters were not escaped during automatic redirect with appended trailing slash. [1.21.0]
-   reduced memory consumption for long-lived requests when proxying with more than 64 buffers. [1.21.1]
-   keepalive connections with gRPC backends might not be closed after receiving a GOAWAY frame. [1.21.1]
-   nginx did not escape `"`, `<`, `>`, `\`, `^`, ```, `{`, `|`, and `}` characters when proxying with changed URI. [1.21.1]
-   invalid headers from backends were logged at the `info` level instead of `error`; the bug had appeared in [1.21.1]. [1.21.4]
-   **👁️** after receiving a response with incorrect length from a proxied backend nginx might nevertheless cache the connection. Thanks to Awdhesh Mathpal. [1.21.4]
-   in the `$content_length` variable when using chunked transfer encoding. [1.21.4]
-   nginx returned the `Connection: keep-alive` header line in responses during graceful shutdown of old worker processes. [1.21.6]
-   when using `EPOLLEXCLUSIVE` on Linux client connections were unevenly distributed among worker processes. [1.21.6]

Change:

-   now extra data sent by a backend are always discarded. [1.19.1]
-   optimization of client request body reading when using chunked transfer encoding. [1.19.2]
-   now nginx starts closing keepalive connections before all free worker connections are exhausted, and logs a warning about this to the error log. [1.19.2]
-   the default value of the `keepalive_requests` directive was changed to 1000. [1.19.10]
-   optimization of configuration testing when using many listening sockets. [1.21.1]
-   **👁️** now nginx always returns an error if spaces or control characters are used in the `Host` request header line. [1.21.1]
-   **👁️** now nginx always returns an error if spaces or control characters are used in a header name. [1.21.1]
-   **👁️** now nginx always returns an error if spaces or control characters are used in the request line. [1.21.1]
-   **👁️** now nginx always returns an error if both `Content-Length` and `Transfer-Encoding` header lines are present in the request. [1.21.1]
-   **👁️** now nginx always returns an error for the CONNECT method. [1.21.1]
-   export ciphers are no longer supported. [1.21.2]
-   now nginx rejects HTTP/1.0 requests with the `Transfer-Encoding` header line. [1.21.2]
-   the default value of the `sendfile_max_chunk` directive was changed to 2 megabytes. [1.21.4]
-   now nginx always uses sendfile(SF_NODISKIO) on FreeBSD. [1.21.5]
-   now nginx is built with the PCRE2 library by default. [1.21.5]

Workaround:

-   `[crit] SSL_write() failed` messages might appear in logs when using OpenSSL 1.1.1. [1.19.3]
-   `gzip filter failed to use preallocated memory` alerts appeared in logs when using zlib-ng. [1.19.10]

## By module

Grouped by modules.

Bugfix:

-   in the ngx_http_xslt_filter_module. [1.19.2]
-   in the ngx_http_slice_module. [1.19.2]
-   in the ngx_http_flv_module and ngx_http_mp4_module. Thanks to Chris Newton. [1.19.6]
-   the `mp4_start_key_frame` directive in the ngx_http_mp4_module. Thanks to Tracey Jaquith. [1.21.4]

### Stream

Feature:

-   the ngx_stream_set_module. [1.19.3]
-   the `fastopen` parameter of the `listen` directive in the stream module. Thanks to Anbang Wen. [1.21.0]
-   support for `SSL_sendfile()` when using OpenSSL 3.0. [1.21.4]
-   the `ssl_alpn` directive in the stream module. [1.21.4]
-   the `proxy_half_close` directive in the stream module. [1.21.4]

### Mail proxy

Feature:

-   the `proxy_smtp_auth` directive in mail proxy. [1.19.4]
-   the `proxy_protocol` parameter of the `listen` directive, the `proxy_protocol` and `set_real_ip_from` directives in mail proxy. [1.19.8]
-   the mail proxy module supports POP3 and IMAP pipelining. [1.21.0]
-   the `max_errors` directive in the mail proxy module. [1.21.0]

Bugfix:

-   nginx could not be built with the mail proxy module, but without the ngx_mail_ssl_module; the bug had appeared in [1.19.8]. [1.19.9]
-   connections with clients in the mail proxy module might be closed unexpectedly when using SMTP pipelining. [1.21.0]

## By protocols

Grouped by protocols.

### SSL

Feature:

-   the `ssl_reject_handshake` directive. [1.19.4]
-   the `ssl_conf_command`, `proxy_ssl_conf_command`, `grpc_ssl_conf_command`, and `uwsgi_ssl_conf_command` directives. [1.19.4]
-   variables support in the `proxy_ssl_certificate`, `proxy_ssl_certificate_key` `grpc_ssl_certificate`, `grpc_ssl_certificate_key`, `uwsgi_ssl_certificate`, and `uwsgi_ssl_certificate_key` directives. [1.21.0]
-   the `Auth-SSL-Protocol` and `Auth-SSL-Cipher` header lines are now passed to the mail proxy authentication server. Thanks to Rob Mueller. [1.21.2]
-   OpenSSL 3.0 compatibility. [1.21.2]
-   the `$ssl_alpn_protocol` variable. [1.21.4]
-   the `$ssl_curve` variable. [1.21.5]

Bugfix:

-   in error handling when using the `ssl_ocsp` directive. [1.19.1]
-   proxying to uwsgi backends using SSL might not work. Thanks to Guanzhong Chen. [1.19.1]
-   `SSL_shutdown() failed (SSL: ... bad write retry)` messages might appear in logs. [1.19.2]
-   SSL shutdown might not work. [1.19.2]
-   memory leak if the `ssl_ocsp` directive was used. [1.19.2]
-   `SSL_shutdown() failed (SSL: ... bad write retry)` messages might appear in logs; the bug had appeared in [1.19.2]. [1.19.3]
-   SSL shutdown did not work when lingering close was used. [1.19.5]
-   SSL variables might be empty when used in logs; the bug had appeared in [1.19.5]. [1.21.1]
-   the security level, which is available in OpenSSL 1.1.0 or newer, did not affect loading of the server certificates when set with `@SECLEVEL=N` in the `ssl_ciphers` directive. [1.21.2]
-   backend SSL connections in the stream module might hang after an SSL handshake. [1.21.2]
-   in the `ssl_session_ticket_key` when using TLSv1.3. [1.21.6]

Change:

-   now nginx rejects SSL connections if ALPN is used by the client, but no supported protocols can be negotiated. [1.21.4]

### gRPC

Bugfix:

-   `upstream sent frame for closed stream` errors might occur when working with gRPC backends. [1.19.5]
-   SSL connections with gRPC backends might hang if select, poll, or /dev/poll methods were used. [1.21.2]

### OCSP

Feature

-   client certificate validation with OCSP. [1.19.0]

Bugfix:

-   OCSP stapling might not work if the `resolver` directive was not specified. [1.19.0]
-   `upstream sent response body larger than indicated content length` errors might occur when working with gRPC backends; the bug had appeared in [1.19.1]. [1.19.9]

### HTTP.2

Bugfix:

-   connections with incorrect HTTP/2 preface were not logged. [1.19.0]
-   socket leak when using HTTP/2 and subrequests in the njs module. [1.19.3]
-   a segmentation fault might occur in a worker process when using HTTP/2 if errors with code 400 were redirected to a proxied location using the `error_page` directive. [1.19.3]
-   HTTP/2 connections were immediately closed when using `keepalive_timeout 0`; the bug had appeared in [1.19.7]. [1.19.8]
-   **👁️** when using HTTP/2 client request body was always written to disk if the `Content-Length` header line was not present in the request. [1.21.2]
-   in request body filters internal API when using HTTP/2 and buffering of the data being processed. [1.21.3]
-   requests might hang when using HTTP/2 and the `aio_write` directive. [1.21.4]
-   connections might hang when using HTTP/2 without SSL with the `sendfile` and `aio` directives. [1.21.5]

Change:

-   the `lingering_close`, `lingering_time`, and `lingering_timeout` directives now work when using HTTP/2. [1.19.1]
-   the `http2_max_field_size` and `http2_max_header_size` directives have been removed, the `large_client_header_buffers` directive should be used instead. [1.19.7]
-   connections handling in HTTP/2 has been changed to better match HTTP/1.x; the `http2_recv_timeout`, `http2_idle_timeout`, and `http2_max_requests` directives have been removed, the `keepalive_timeout` and `keepalive_requests` directives should be used instead. [1.19.7]
-   optimization of client request body reading when using HTTP/2. [1.21.3]
-   support for NPN instead of ALPN to establish HTTP/2 connections has been removed. [1.21.4]

### FastCGI

Bugfix:

-   `zero size buf in output` alerts might appear in logs if a FastCGI server returned an incorrect response; the bug had appeared in [1.19.1]. [1.19.2]

Change:

-   now after receiving a too short response from a FastCGI server nginx tries to send the available part of the response to the client, and then closes the client connection. [1.19.1]

## By versions

from 1.19.0 to 1.22.1(stable)

### 1.21.6

> 📆 25 Jan 2022

-   Bugfix: when using EPOLLEXCLUSIVE on Linux client connections were unevenly distributed among worker processes.
-   Bugfix: nginx returned the "Connection: keep-alive" header line in responses during graceful shutdown of old worker processes.
-   Bugfix: in the "ssl_session_ticket_key" when using TLSv1.3.

### 1.21.5

> 📆 28 Dec 2021

-   Change: now nginx is built with the PCRE2 library by default.
-   Change: now nginx always uses sendfile(SF_NODISKIO) on FreeBSD.
-   Feature: support for sendfile(SF_NOCACHE) on FreeBSD.
-   Feature: the $ssl_curve variable.
-   Bugfix: connections might hang when using HTTP/2 without SSL with the "sendfile" and "aio" directives.

### 1.21.4

> 📆 02 Nov 2021

-   Change: support for NPN instead of ALPN to establish HTTP/2 connections has been removed.
-   Change: now nginx rejects SSL connections if ALPN is used by the client, but no supported protocols can be negotiated.
-   Change: the default value of the "sendfile_max_chunk" directive was changed to 2 megabytes.
-   Feature: the "proxy_half_close" directive in the stream module.
-   Feature: the "ssl_alpn" directive in the stream module.
-   Feature: the $ssl_alpn_protocol variable.
-   Feature: support for SSL_sendfile() when using OpenSSL 3.0.
-   Feature: the "mp4_start_key_frame" directive in the ngx_http_mp4_module. Thanks to Tracey Jaquith.
-   Bugfix: in the $content_length variable when using chunked transfer encoding.
-   Bugfix: after receiving a response with incorrect length from a proxied backend nginx might nevertheless cache the connection. Thanks to Awdhesh Mathpal.
-   Bugfix: invalid headers from backends were logged at the "info" level instead of "error"; the bug had appeared in 1.21.1.
-   Bugfix: requests might hang when using HTTP/2 and the "aio_write" directive.

### 1.21.3

> 📆 07 Sep 2021

-   Change: optimization of client request body reading when using HTTP/2.
-   Bugfix: in request body filters internal API when using HTTP/2 and buffering of the data being processed.

### 1.21.2

> 📆 31 Aug 2021

-   Change: now nginx rejects HTTP/1.0 requests with the "Transfer-Encoding" header line.
-   Change: export ciphers are no longer supported.
-   Feature: OpenSSL 3.0 compatibility.
-   Feature: the "Auth-SSL-Protocol" and "Auth-SSL-Cipher" header lines are now passed to the mail proxy authentication server. Thanks to Rob Mueller.
-   Feature: request body filters API now permits buffering of the data being processed.
-   Bugfix: backend SSL connections in the stream module might hang after an SSL handshake.
-   Bugfix: the security level, which is available in OpenSSL 1.1.0 or newer, did not affect loading of the server certificates when set with "@SECLEVEL=N" in the "ssl_ciphers" directive.
-   Bugfix: SSL connections with gRPC backends might hang if select, poll, or /dev/poll methods were used.
-   Bugfix: when using HTTP/2 client request body was always written to disk if the "Content-Length" header line was not present in the request.

### 1.21.1

> 📆 06 Jul 2021

-   Change: now nginx always returns an error for the CONNECT method.
-   Change: now nginx always returns an error if both "Content-Length" and "Transfer-Encoding" header lines are present in the request.
-   Change: now nginx always returns an error if spaces or control characters are used in the request line.
-   Change: now nginx always returns an error if spaces or control characters are used in a header name.
-   Change: now nginx always returns an error if spaces or control characters are used in the "Host" request header line.
-   Change: optimization of configuration testing when using many listening sockets.
-   Bugfix: nginx did not escape """, "<", ">", "\", "^", "`", "{", "|", and "}" characters when proxying with changed URI.
-   Bugfix: SSL variables might be empty when used in logs; the bug had appeared in 1.19.5.
-   Bugfix: keepalive connections with gRPC backends might not be closed after receiving a GOAWAY frame.
-   Bugfix: reduced memory consumption for long-lived requests when proxying with more than 64 buffers.

### 1.21.0

> 📆 25 May 2021

-   Security: 1-byte memory overwrite might occur during DNS server response processing if the "resolver" directive was used, allowing an attacker who is able to forge UDP packets from the DNS server to cause worker process crash or, potentially, arbitrary code execution (CVE-2021-23017).
-   Feature: variables support in the "proxy_ssl_certificate", "proxy_ssl_certificate_key" "grpc_ssl_certificate", "grpc_ssl_certificate_key", "uwsgi_ssl_certificate", and "uwsgi_ssl_certificate_key" directives.
-   Feature: the "max_errors" directive in the mail proxy module.
-   Feature: the mail proxy module supports POP3 and IMAP pipelining.
-   Feature: the "fastopen" parameter of the "listen" directive in the stream module. Thanks to Anbang Wen.
-   Bugfix: special characters were not escaped during automatic redirect with appended trailing slash.
-   Bugfix: connections with clients in the mail proxy module might be closed unexpectedly when using SMTP pipelining.

### 1.19.10

> 📆 13 Apr 2021

-   Change: the default value of the "keepalive_requests" directive was changed to 1000.
-   Feature: the "keepalive_time" directive.
-   Feature: the $connection_time variable.
-   Workaround: "gzip filter failed to use preallocated memory" alerts appeared in logs when using zlib-ng.

### 1.19.9

> 📆 30 Mar 2021

-   Bugfix: nginx could not be built with the mail proxy module, but without the ngx_mail_ssl_module; the bug had appeared in 1.19.8.
-   Bugfix: "upstream sent response body larger than indicated content length" errors might occur when working with gRPC backends; the bug had appeared in 1.19.1.
-   Bugfix: nginx might not close a connection till keepalive timeout expiration if the connection was closed by the client while discarding the request body.
-   Bugfix: nginx might not detect that a connection was already closed by the client when waiting for auth_delay or limit_req delay, or when working with backends.
-   Bugfix: in the eventport method.

### 1.19.8

> 📆 09 Mar 2021

-   Feature: flags in the "proxy_cookie_flags" directive can now contain variables.
-   Feature: the "proxy_protocol" parameter of the "listen" directive, the "proxy_protocol" and "set_real_ip_from" directives in mail proxy.
-   Bugfix: HTTP/2 connections were immediately closed when using "keepalive_timeout 0"; the bug had appeared in 1.19.7.
-   Bugfix: some errors were logged as unknown if nginx was built with glibc 2.32.
-   Bugfix: in the eventport method.

### 1.19.7

> 📆 16 Feb 2021

-   Change: connections handling in HTTP/2 has been changed to better match HTTP/1.x; the "http2_recv_timeout", "http2_idle_timeout", and "http2_max_requests" directives have been removed, the "keepalive_timeout" and "keepalive_requests" directives should be used instead.
-   Change: the "http2_max_field_size" and "http2_max_header_size" directives have been removed, the "large_client_header_buffers" directive should be used instead.
-   Feature: now, if free worker connections are exhausted, nginx starts closing not only keepalive connections, but also connections in lingering close.
-   Bugfix: "zero size buf in output" alerts might appear in logs if an upstream server returned an incorrect response during unbuffered proxying; the bug had appeared in 1.19.1.
-   Bugfix: HEAD requests were handled incorrectly if the "return" directive was used with the "image_filter" or "xslt_stylesheet" directives.
-   Bugfix: in the "add_trailer" directive.

### 1.19.6

> 📆 15 Dec 2020

-   Bugfix: "no live upstreams" errors if a "server" inside "upstream" block was marked as "down".
-   Bugfix: a segmentation fault might occur in a worker process if HTTPS was used; the bug had appeared in 1.19.5.
-   Bugfix: nginx returned the 400 response on requests like "GET <http://example.com?args> HTTP/1.0".
-   Bugfix: in the ngx_http_flv_module and ngx_http_mp4_module. Thanks to Chris Newton.

### 1.19.5

> 📆 24 Nov 2020

-   Feature: the -e switch.
-   Feature: the same source files can now be specified in different modules while building addon modules.
-   Bugfix: SSL shutdown did not work when lingering close was used.
-   Bugfix: "upstream sent frame for closed stream" errors might occur when working with gRPC backends.
-   Bugfix: in request body filters internal API.

### 1.19.4

> 📆 27 Oct 2020

-   Feature: the "ssl_conf_command", "proxy_ssl_conf_command", "grpc_ssl_conf_command", and "uwsgi_ssl_conf_command" directives.
-   Feature: the "ssl_reject_handshake" directive.
-   Feature: the "proxy_smtp_auth" directive in mail proxy.

### 1.19.3

> 📆 29 Sep 2020

-   Feature: the ngx_stream_set_module.
-   Feature: the "proxy_cookie_flags" directive.
-   Feature: the "userid_flags" directive.
-   Bugfix: the "stale-if-error" cache control extension was erroneously applied if backend returned a response with status code 500, 502, 503, 504, 403, 404, or 429.
-   Bugfix: "[crit] cache file ... has too long header" messages might appear in logs if caching was used and the backend returned responses with the "Vary" header line.
-   Workaround: "[crit] SSL_write() failed" messages might appear in logs when using OpenSSL 1.1.1.
-   Bugfix: "SSL_shutdown() failed (SSL: ... bad write retry)" messages might appear in logs; the bug had appeared in 1.19.2.
-   Bugfix: a segmentation fault might occur in a worker process when using HTTP/2 if errors with code 400 were redirected to a proxied location using the "error_page" directive.
-   Bugfix: socket leak when using HTTP/2 and subrequests in the njs module.

### 1.19.2

> 📆 11 Aug 2020

-   Change: now nginx starts closing keepalive connections before all free worker connections are exhausted, and logs a warning about this to the error log.
-   Change: optimization of client request body reading when using chunked transfer encoding.
-   Bugfix: memory leak if the "ssl_ocsp" directive was used.
-   Bugfix: "zero size buf in output" alerts might appear in logs if a FastCGI server returned an incorrect response; the bug had appeared in 1.19.1.
-   Bugfix: a segmentation fault might occur in a worker process if different large_client_header_buffers sizes were used in different virtual servers.
-   Bugfix: SSL shutdown might not work.
-   Bugfix: "SSL_shutdown() failed (SSL: ... bad write retry)" messages might appear in logs.
-   Bugfix: in the ngx_http_slice_module.
-   Bugfix: in the ngx_http_xslt_filter_module.

### 1.19.1

> 📆 07 Jul 2020

-   Change: the "lingering_close", "lingering_time", and "lingering_timeout" directives now work when using HTTP/2.
-   Change: now extra data sent by a backend are always discarded.
-   Change: now after receiving a too short response from a FastCGI server nginx tries to send the available part of the response to the client, and then closes the client connection.
-   Change: now after receiving a response with incorrect length from a gRPC backend nginx stops response processing with an error.
-   Feature: the "min_free" parameter of the "proxy_cache_path", "fastcgi_cache_path", "scgi_cache_path", and "uwsgi_cache_path" directives. Thanks to Adam Bambuch.
-   Bugfix: nginx did not delete unix domain listen sockets during graceful shutdown on the SIGQUIT signal.
-   Bugfix: zero length UDP datagrams were not proxied.
-   Bugfix: proxying to uwsgi backends using SSL might not work. Thanks to Guanzhong Chen.
-   Bugfix: in error handling when using the "ssl_ocsp" directive.
-   Bugfix: on XFS and NFS file systems disk cache size might be calculated incorrectly.
-   Bugfix: "negative size buf in writer" alerts might appear in logs if a memcached server returned a malformed response.

### 1.19.0

> 📆 26 May 2020

-   Feature: client certificate validation with OCSP.
-   Bugfix: "upstream sent frame for closed stream" errors might occur when working with gRPC backends.
-   Bugfix: OCSP stapling might not work if the "resolver" directive was not specified.
-   Bugfix: connections with incorrect HTTP/2 preface were not logged.

[1.21.6]: #1216
[1.21.5]: #1215
[1.21.4]: #1214
[1.21.3]: #1213
[1.21.2]: #1212
[1.21.1]: #1211
[1.21.0]: #1210
[1.19.10]: #11910
[1.19.9]: #1199
[1.19.8]: #1198
[1.19.7]: #1197
[1.19.6]: #1196
[1.19.5]: #1195
[1.19.4]: #1194
[1.19.3]: #1193
[1.19.2]: #1192
[1.19.1]: #1191
[1.19.0]: #1190
