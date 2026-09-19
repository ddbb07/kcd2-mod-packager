# kcd2-mod-packager

Packages a Kingdom Come: Deliverance II mod. Folders under `Data` and
`Localization` are turned into `.pak` files and everything else is copied as is.
Optionally the result is zipped.

## Install

Requires Python 3.14 or newer. From the root of this repository:

```
pipx install .
```

## Usage

```
kcd2-mod-packager [-a] package_path
```

`package_path` is the project directory and must contain a `src` directory.
With `-a` / `--archive` the output is zipped to `out.zip` and `out/` is removed.
Paths inside the zip are relative to `out`.

```
my-mod/
├── src/       your mod
├── pkg/       temporary, removed after the run
├── out/       the packaged mod
└── out.zip    only with --archive
```

`pkg` and `out` are emptied and `out.zip` is removed on every run, so don't keep
anything in them.

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
are only a substitute for the pak name. Each one becomes a pak with the same
name, and what is inside the folder ends up at the root of the pak:

```
src/Data/my_mod_tables/Libs/Tables/x.xml
  -> out/Data/my_mod_tables.pak, containing Libs/Tables/x.xml
```

- Empty folders under `Data` and `Localization` produce no pak and are left
  out.
- Everything else, including files directly in `Data` and `Localization`, is
  copied unchanged.

## License

MIT, see [LICENSE](LICENSE). The project follows the
[REUSE](https://reuse.software) specification.
