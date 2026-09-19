# kcd2-mod-packager

Packages a Kingdom Come: Deliverance II mod. Folders under `Data` and
`Localization` become `.pak` files, everything else is copied as is, and the
result can be zipped.

## Install

Needs Python 3.14 or newer. From the root of this repository:

```
pipx install .
```

## Usage

```
kcd2-mod-packager [-a] package_path
```

`package_path` is the project directory and must contain a `src` directory.
The packaged mod ends up in `out/`. With `-a` / `--archive` it is zipped to
`out.zip` instead, with paths relative to `out`.

```
my-mod/
├── src/       your mod
├── pkg/       temporary, removed after the run
├── out/       the packaged mod
└── out.zip    only with --archive
```

Every run empties `pkg` and `out` and removes `out.zip`, so don't keep anything
in them.

## Layout of src

```
src/
├── mod.manifest
├── Data/
│   ├── my_mod_tables/
│   │   └── Libs/
│   │       └── Tables/
│   │           └── ...
│   └── my_mod_scripts/
│       └── Scripts/
│           └── ...
└── Localization/
    └── English_xml/
        └── ...
```

The folders directly under `Data` and `Localization` (`my_mod_tables`,
`my_mod_scripts` and `English_xml` above) don't exist in the base game. They
only stand in for the pak name. Each becomes a pak with the same name, holding
whatever is inside the folder:

```
src/Data/my_mod_tables/Libs/Tables/x.xml
  -> out/Data/my_mod_tables.pak, containing Libs/Tables/x.xml
```

Empty folders produce no pak and are left out. Everything else, including files
directly in `Data` and `Localization`, is copied unchanged.

## License

MIT, see [LICENSE](LICENSE). The project follows the
[REUSE](https://reuse.software) specification.
