{
  lib,
  stdenv,

  qgis,
  qgisRepo,
  qgisIsMasterVersion ? false,

  fontconfig,
  graphviz,
  python3Packages,
  libsForQt5,
  noto-fonts
}:

let
  qgisPackage = qgis.override { withServer = true; };
  qgisMinorVersion =
    let
      versionSplit = builtins.splitVersion qgis.version;
      version =
        if qgisIsMasterVersion then
          "master"
        else
          builtins.elemAt versionSplit 0 + "." + builtins.elemAt versionSplit 1;
    in
    version;

in

stdenv.mkDerivation {
  pname = "qgis-pyqgis-documentation";
  version = qgisMinorVersion;

  src = lib.cleanSourceWith {
    src = ../.;
    filter = (
      path: type:
      (builtins.all (x: x != baseNameOf path) [
        ".git"
        ".github"
        "flake.nix"
        "flake.lock"
        "package.nix"
        "result"
      ])
    );
  };

  dontWrapQtApps = true;

  buildInputs =
    with python3Packages;
    [
      qgisPackage
      python

      noto-fonts
      fontconfig
      graphviz
      sphinx
      sphinx-rtd-theme
    ]
    ++ qgisPackage.passthru.unwrapped.pythonBuildInputs;

  env.QT_PLUGIN_PATH="${libsForQt5.qt5.qtbase}/${libsForQt5.qt5.qtbase.qtPluginPrefix}";
  env.QT_QPA_PLATFORM_PLUGIN_PATH="${libsForQt5.qt5.qtbase}/${libsForQt5.qt5.qtbase.qtPluginPrefix}/platforms";
  env.QT_QPA_PLATFORM="offscreen";

  env.FONTCONFIG_FILE="${fontconfig.out}/etc/fonts/fonts.conf";
  env.FONTCONFIG_PATH="${fontconfig.out}/etc/fonts/";

  # Taken from
  # https://github.com/qgis/pyqgis-api-docs-builder/blob/main/scripts/build-docs.sh
  buildPhase = ''
    export HOME=$(mktemp -d)

    # Build RST
    mkdir -p temp
    for module in "3d" "analysis" "core" "gui" "server"; do
        CLASS_MAP_FILE="temp/$module/class_map.yaml"
        mkdir -p temp/$module
        cp ${qgisRepo}/python/$module/class_map.yaml $CLASS_MAP_FILE
    done

    export PYTHONPATH=$PYTHONPATH:./:${qgisPackage}/share/qgis/python

    python ./scripts/make_api_rst.py --version ${qgisMinorVersion}

    mkdir api/${qgisMinorVersion}/_static
    cp -r _static/css api/${qgisMinorVersion}/_static/css
    cp -r _static/js api/${qgisMinorVersion}/_static/js
    cp _static/*.rst api/${qgisMinorVersion}/

    # Build HTML
    sed -r "s/__QGIS_VERSION__/${qgisMinorVersion}/g;" conf.in.py > api/${qgisMinorVersion}/conf.py
    sphinx-build -M html api/${qgisMinorVersion} build/${qgisMinorVersion} -T -j auto

    # Move files around
    rm -rf build/${qgisMinorVersion}/doctrees
    mv build/${qgisMinorVersion}/html/* build/${qgisMinorVersion}
    rm -rf build/${qgisMinorVersion}/html
  '';

  installPhase = ''
    mkdir -p $out
    cp -r build/* $out/
  '';
}
