# yaas
Yet Another Ambari Shell

## Installation

```
pip install yaas
```

## Usage

```
env YAAS_SERVER=ambari.example.com yaas [options] [command options [...]]
```

### Global Options

* --help
  ```
  $ yaas --help
  usage: yaas ...
  ```
  ```
  $ yaas help
  usage: yaas ...
  ```

* --version
  ```
  $ yaas --version
  x.x.x
  ```
  ```
  $ yaas version
  x.x.x
  ```

* --raw
  ```
  $ yaas --raw ...
  (JSON)
  ```

* --debug
  ```
  $ yaas --debug ...
  (verbose)
  ```

### Commands

All API commands require setting these environment variables:
* `YAAS_SERVER`--the address or name of the Ambari server
  * Example: ambari.example.com
  * Default: *none* (This is required.)
* `YAAS_SCHEME`--the scheme to use when connecting to the Ambari server
  * Example: https
  * Default: http
* `YAAS_PORT`--the port of the Ambari server
  * Example: 443
  * Default: 8080
* `YAAS_USER`--the user to auth with to the Ambari server
  * Example: l337u53r
  * Default: admin
* `YAAS_PASSWORD`--the password to auth with to the ambari server
  * Example: l337p455
  * Default: admin

```
$ export YAAS_SERVER=ambari.example.com
$ yaas ...
```
```
$ env YAAS_SERVER=ambari.example.com yaas ...
```

#### blueprint

##### add

```
$ yaas blueprint add blueprint1.json blueprint2.json
$ cat blueprint3.json | yaas blueprint add
```

##### list

```
$ yaas blueprint list
blueprint1
blueprint2
blueprint3
```

* Note: This will list the name of the actual Blueprint (as specified inside the JSON file) which may differ from the file name.

##### show

```
$ yaas blueprint show blueprint1
...
```

##### remove

```
$ yaas blueprint remove blueprint2
$ yaas blueprint list
blueprint1
blueprint3
```

##### template

```
$ yaas blueprint template blueprint1 [--host_group=host1.example.com ...] > template1.json
$ yaas blueprint template blueprint2.json [--host_group=host1.example.com ...] > template2.json
WARNING: You have not specified enough hosts to satisfy the blueprint.
```

#### cluster

##### create

```
$ yaas cluster create cluster1 --template=template1.json
$ cat template2.json | yaas cluster create cluster2
$ yaas cluster create cluster3
```

###### Options

* --template

### list

```
$ yaas cluster list
cluster1
cluster2
cluster3
```

##### show

```
$ yaas cluster show cluster1 --format=blueprint > blueprint1.json
$ yaas cluster show cluster2
...
```

###### Options

* --format

##### destroy

```
$ yaas cluster destroy cluster2
$ yaas cluster list
cluster1
cluster3
```

#### host

##### list

```
$ yaas host list
host1.example.com
host2.example.com
host3.example.com
```

##### show

```
$ yaas host show [--hardware] host1.example.com host2.example.com ...
...
```

###### Options

* --hardware

#### repo

##### add

```
$ yaas repo add [--verify-baseurls=true] repo.json
```

##### list

See all configured repository URLs. Limit output by one or more of these parameters. Note that stack-version and stack-version must be specified together:
  * stack-name (e.g. HDP)
  * stack-version (e.g. 2.2)
  * os-type (e.g. redhat6)
  * repo-name (e.g. HDP-UTILS)

```
$ yaas repo list
HDP-2.2
  redhat5
    HDP: http://www.example.com/redhat5/HDP
    HDP-UTILS: http://www.example.com/redhat5/HDP
  redhat6
    HDP: http://www.example.com/redhat6/HDP
    HDP-UTILS: http://www.example.com/redhat6/HDP-UTILS-1.1.0.20
  ...
$ yaas repo list --stack-name=HDP --stack-version=2.2 --repo-name=HDP-UTILS
redhat5
  HDP: http://www.example.com/redhat5/HDP-UTILS
redhat6
  HDP: http://www.example.com/redhat6/HDP-UTILS
...
$ yaas repo list --stack-name=HDP --stack-version=2.2 --os-type=redhat6 --repo-name=HDP
http://www.example.com/redhat6/HDP
```

##### set

```
$ yaas repo set [--verify-baseurls=true] repo-changed.json
```

##### remove

```
$ yaas repo remove HDP 2.2
```