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

`POST /api/v1/blueprints/:name`

Store a blueprint on `YAAS_SERVER`.

```
$ yaas blueprint add blueprint1.json blueprint2.json
$ cat blueprint3.json | yaas blueprint add
```

###### Options

* --validate-topology

  `POST /api/v1/blueprints/:name?validate_topology=...`

  Toggle topology validation.

##### list

`GET /api/v1/blueprints`

Show blueprints that are stored on `YAAS_SERVER`.

```
$ yaas blueprint list
blueprint1
blueprint2
blueprint3
```

* Note: This will list the name of the actual Blueprint (as specified inside the JSON file) which may differ from the file name.

###### Options

* --fields

  `GET /api/v1/blueprints?fields=...`

  Add blueprint details to the list.

##### show

`GET /api/v1/blueprints/:name`

Show details about a blueprint stored on `YAAS_SERVER`.

```
$ yaas blueprint show blueprint1
```

##### remove

`DELETE /api/v1/blueprints/:name`

Remove a blueprint stored on `YAAS_SERVER`.

```
$ yaas blueprint remove blueprint2
$ yaas blueprint list
blueprint1
blueprint3
```

#### bootstrap

##### agents

`POST /api/v1/bootstrap`

Set up hosts as Ambari agents pointing at YAAS_SERVER.

```
$ yaas bootstrap agents -k id_rsa -u root --userRunAs root host1.example.com.
Request 1 OK Running Bootstrap now.
```

##### show

`GET /api/v1/bootstrap/:id`

Show the status of a bootstrap request.

```
$ yaas bootstrap show 1
Request 1 SUCCESS
    host1.example.com DONE (status: 0)
```

###### Options

* --log

  Show bootstrap logs for each host.

#### cluster

##### create

```
$ yaas cluster create cluster1 --template=template1.json
$ cat template2.json | yaas cluster create cluster2
$ yaas cluster create cluster3
```

###### Options

* --template

##### list

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

`GET /api/v1/hosts`

Show hosts that are registered with `YAAS_SERVER`.

```
$ yaas host list
host1.example.com - cluster1
host2.example.com - cluster1
host3.example.com
```

###### Options

* --fields

  `GET /api/v1/hosts?fields=...`

  Add host details to the list.
  See [the Ambari API documentation](https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1/host-resources.md) for valid fields.

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

#### template

##### create

```
$ yaas template create [--blueprint=blueprint1] [--host_group=host1.example.com ...] > template1.json
$ cat clueprint2.json | yaas template create [--host_group=host1.example.com ...] > template2.json
WARNING: You have not specified enough hosts to satisfy the blueprint.
```
