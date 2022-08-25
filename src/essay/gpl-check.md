# GPL 的檢查

GPL 和 AGPL 不管是啥版本都要求**直接引用**該程式庫的專案要公開（儘管有些人反對）。

> If you are not directly linking against the GPL'd library, then your software should not need to be licensed as GPL.
>
> [Reference](https://answers.ros.org/question/12313/using-gpl-licensed-packages-in-a-commercial-product/)

但是 LGPL 或 GPL with classpath exception 可以允許引用套件，但是不允許直接複製貼上進程式碼中。

> There are less permissive licenses like the LGPL and the GPL with classpath exception that allow the code to be linked by any other code (so in Java terms, you can have dependencies with those licenses), but not embedded (or, more likely copy-pasted).
>
> [Reference](https://carlomorelli.github.io/2018/04/01/Audit-licenses-in-your-Java-dependencies.html)

下表是不同許可間的比較。

![image alt](https://raw.githubusercontent.com/HansHammel/license-compatibility-checker/f243eb4523ebc7d019a5928103e5b82b59b3b803/licenses.svg)

> <https://medium.com/@fokusman/the-easiest-way-to-check-all-your-npm-dependency-licenses-753075ef1d9d>

---

在多個 Repo 中找到相依套件是否有使用 GPL 的策略會是：

-   [把所有 Repo 的 Dependecy 整合起來](https://github.com/evan361425/playground-github-api#好用腳本)
-   透過套件管理工具的 API 檢查套件的 License
    -   [npm](https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md#getpackageversion)
    -   [composer](https://packagist.org/apidoc#get-package-data)
    -   [maven](https://repo1.maven.org/maven2)

## 方法

用了哪些 script 找資料。

### NPM

```shell=
$ awk '{print $2}' data/derived/package.json.deps.txt \
  | sort -u \
  | xargs -P 8 -I{} bash -c 'curl "https://registry.npmjs.org/{}/latest" -s \
  | jq -r '"'"'select(.name != null) | [.name, .license|tostring] | @tsv'"'"' \
  | tee -a data/derived/package.json.deps.license.txt'
```

### Composer

```shell=
$ awk '{print $2}' data/derived/composer.json.deps.txt \
  # 避免特定 vendor 的套件
  | grep -v '^104' \
  # 避免非套件的相依，例如 php
  | grep '\/' \
  | sort -u \
  | xargs -P 8 -I{} bash -c '
    curl "https://repo.packagist.org/p2/$1.json" -s \
    | jq -r ".packages[] | to_entries | .[].value | select(.name != null) | [.name, .license|tostring] | @tsv" \
    | sed "s/\",\"/\\t/g" | sed "s/\\[\"//" | sed "s/\"\\]//" \
    | tee -a data/derived/composer.json.deps.license.txt' - {}
```

### Maven

Maven 需要的步驟有點多，先取最新版本再取該版本的 POM 檔，以下以 `org.springframework.boot` 的 `spring-boot-starter-data-jpa` 為例。

> scripts/parse-pom.js 詳見於[此](https://github.com/evan361425/playground-github-api/blob/master/scripts/parse-pom.js)

```shell=
$ base='https://repo1.maven.org/maven2'
# 不是 `.` 做區隔而是 `/`
$ project='org/springframework/boot'
$ app='pring-boot-starter-data-jpa'
# 取得指定套件最新版本
$ curl -s "$base/$project/$app/maven-metadata.xml" \
  | grep '<latest>' \
  # 移除 <latest>2.7.1</latest> 的 tag
  | cut -c 13- | rev | cut -c 10- | rev
2.7.1

# 取該版本的 POM 檔
$ curl "$base/$project/$app/2.7.1/$app-2.7.1.pom" \
  | node scripts/parse-pom.js
org.springframework.boot pring-boot-starter-data-jpa Apache-License-Version-2.0
```

依照上面的邏輯，就可以使用下面的 script：

> `build.gradle` 和 `pom.xml` 差不多，只有第一步的篩選需要調一下，
> `pom.xml` 只需要篩選 `dep` 就可以

-   篩選需要的資料
    1. 需要大於等於四個參數，也就是至少需要有 app 名稱
    2. path（第二個參數）需要包含 dependency 這關鍵字
    3. project 名稱（但三個參數）不能包含內部使用的
    4. project 名稱必須包含 `.`
    5. 把結果以 `/` 連結
-   透過前面得到 metadata 的方式得到最新版本
-   得到最新版本的 license

```shell=
$ file='data/derived/build.gradle.deps'
$ filter='NF >= 4'
$ filter="$filter && \$2 ~ /.*dependency.*/"
$ filter="$filter && \$3 !~ /(104|jar|androidx|com\.cac\.)/"
$ filter="$filter && \$3 ~ /\./"
$ awk "$filter {print \$3 \"/\" \$4}" "$file.txt" | \
  sed 's/\./\//g' | \
  sort -u > "$file.trimmed.txt"

$ cat data/derived/build.gradle.deps.trimmed.txt | \
  xargs -P 8 -I{} bash -c '
    curl -s "$base/$1/maven-metadata.xml" \
    | grep "<latest>" \
    | cut -c 13- | rev | cut -c 10- | rev \
    | awk "{print \"$1 \" \$1}" >> "$file.latest.txt"' - {}

$ cat "$file.latest.txt" | \
  awk '{print $1 "/" $2 " " $1 "-" $2 ".pom"}'  | \
  sed 's/ .*\//\//g' | \
  xargs -P 8 -I{} bash -c '
    curl "$base/$1" -s \
    | node scripts/parse-pom.js \
    >> "$file.license.txt"' - {}
```

## 結果

查找結果

### NPM

-   [block-ui](https://www.npmjs.com/package/block-ui) MIT GPL
-   [easejs](https://www.npmjs.com/package/easejs) GPL-3.0+
-   [express-sitemap](https://www.npmjs.com/package/express-sitemap) GPL-3.0
-   [hipchatter](https://www.npmjs.com/package/hipchatter) GPL-2.0
-   [intro.js](https://www.npmjs.com/package/intro.js) AGPL-3.0
-   [jszip](https://www.npmjs.com/package/jszip) MIT GPL-3.0-or-later
-   [jszip-utils](https://www.npmjs.com/package/jszip-utils) MIT GPL-3.0
-   [mariadb](https://www.npmjs.com/package/mariadb) LGPL-2.1-or-later
-   [node-forge](https://www.npmjs.com/package/node-forge) BSD-3-Clause GPL-2.0
-   [pm2](https://www.npmjs.com/package/pm2) AGPL-3.0
-   [scrollmagic](https://www.npmjs.com/package/scrollmagic) MIT GPL-3.0+
-   [sonarqube-scanner](https://www.npmjs.com/package/sonarqube-scanner) LGPL-3.0

### Composer

-   [matomo/device-detector](https://packagist.org/packages/matomo/device-detector) LGPL-3.0-or-later
-   [php-amqplib/php-amqplib](https://packagist.org/packages/php-amqplib/php-amqplib) LGPL-2.1-or-later
-   [phpoffice/phpexcel](https://packagist.org/packages/phpoffice/phpexcel) LGPL-2.1
-   [phpmailer/phpmailer](https://packagist.org/packages/phpmailer/phpmailer) LGPL-2.1-only
-   [silvertipsoftware/wkhtmltopdf-amd64](https://packagist.org/packages/silvertipsoftware/wkhtmltopdf-amd64) LGPL-3.0-only

### Maven

`build.gradle` 和 `pom.xml` 都要跑完。

-   [com.experlog/xapool](https://mvnrepository.com/artifact/com.experlog/xapool) LGPL
-   [com.github.jsqlparser/jsqlparser](https://mvnrepository.com/artifact/com.github.jsqlparser/jsqlparser) GNU-Library-or-Lesser-General-Public-License-(LGPL)-V2.1 The-Apache-Software-License-Version-2.0
-   [com.rabbitmq/amqp-client](https://mvnrepository.com/artifact/com.rabbitmq/amqp-client) AL-2.0 GPL-v2 MPL-2.0
-   [com.whalin/Memcached-Java-Client](https://mvnrepository.com/artifact/com.whalin/Memcached-Java-Client) LGPLv3
-   [net.java/jvnet-parent](https://mvnrepository.com/artifact/net.java/jvnet-parent) CDDL-1.1 GPL2-w/-CPE
-   [org.glassfish.jersey/project](https://mvnrepository.com/artifact/org.glassfish.jersey/project) EPL-2.0 The-GNU-General-Public-License-(GPL)-Version-2-With-Classpath-Exception Apache-License-2.0 Modified-BSD
-   [org.glassfish.jersey.media/project](https://mvnrepository.com/artifact/org.glassfish.jersey.media/project) EPL-2.0 The-GNU-General-Public-License-(GPL)-Version-2-With-Classpath-Exception Apache-License-2.0
-   [org.javassist/javassist](https://mvnrepository.com/artifact/org.javassist/javassist) MPL-1.1 LGPL-2.1 Apache-License-2.0
-   [org.mariadb.jdbc/mariadb-java-client](https://mvnrepository.com/artifact/org.mariadb.jdbc/mariadb-java-client) LGPL-2.1
-   [org.sonatype.oss/oss-parent](https://mvnrepository.com/artifact/org.sonatype.oss/oss-parent) LGPL
