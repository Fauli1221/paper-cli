# paper-cli

![Badge](https://img.shields.io/github/license/Fauli1221/paper-cli) ![Badge](https://img.shields.io/github/issues/Fauli1221/paper-cli)

Configure & download [PaperMC](https://papermc.io/) servers using the command line

## Usage

```sh
paper-cli [ARGUMENTS]
```

```sh
ARGUMENTS:
  -h, --help            show this help message and exit
  --projects {paper,travertine,waterfall,velocity}, -p {paper,travertine,waterfall,velocity}
                        select the paper project ['paper', 'travertine', 'waterfall', 'velocity']
  --version VERSION, -v VERSION
                        Select target Minecraft Version
  --build BUILD, -b BUILD
                        Select Build
  --filename FILENAME, -f FILENAME
                        Select your filename when unset it defaults to {projectname}.jar
  --latest [LATEST]     Download latest version
```

## Installation

#### Installing with [pip](https://pypi.org/) using pypi:

```sh
pip install paper-cli
```

#### Installing from source with [pip](https://pypi.org/):

```sh
pip install git+https://github.com/Fauli1221/paper-cli.git#egg=paper-cli
```

## Maintained by

-   [Fauli1221](https://github.com/Fauli1221)
-   [Tch1b0](https://github.com/Tch1b0)
