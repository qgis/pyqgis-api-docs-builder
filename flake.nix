{
  description = "PyQGIS API Documentation";

  nixConfig = {
    #   extra-substituters = [ "https://example.cachix.org" ];
    #   extra-trusted-public-keys = [ "example.cachix.org-1:xxxx=" ];

    # IFD is required for QGIS repo.
    allow-import-from-derivation = true;
  };

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    qgisMaster = {
      url = "github:qgis/QGIS";
    };

    qgisLatest = {
      url = "github:qgis/QGIS/release-3_44";
    };

    qgisLtr = {
      url = "github:qgis/QGIS/release-3_40";
    };
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      qgisMaster,
      qgisLatest,
      qgisLtr,
    }:

    let
      # Flake system
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      nixpkgsFor = forAllSystems (
        system:
        import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        }
      );

    in
    {
      #
      ### PACKAGES
      #

      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgsFor.${system};
        in
        rec {
          docs-master = pkgs.callPackage ./nix/package.nix {
            qgis = inputs.qgisMaster.packages.${system}.qgis;
            qgisRepo = qgisMaster;
            qgisIsMasterVersion = true;
          };

          docs-latest = pkgs.callPackage ./nix/package.nix {
            qgis = inputs.qgisLatest.packages.${system}.qgis;
            qgisRepo = qgisLatest;
          };

          docs-ltr = pkgs.callPackage ./nix/package.nix {
            qgis = inputs.qgisLtr.packages.${system}.qgis;
            qgisRepo = qgisLtr;
          };

          default = docs-master;
        }
      );

      #
      ### APPS
      #

      apps = forAllSystems (
        system:
        let
          pkgs = nixpkgsFor.${system};
          inherit (nixpkgs) lib;

          wwwLauncherMaster = pkgs.writeShellApplication {
            name = "website";
            runtimeInputs = [ pkgs.python3 ];
            text = ''
              exec ${lib.getExe pkgs.python3} \
                -m http.server 8000 \
                -d ${self.packages.${system}.docs-master}/
            '';
          };

          wwwLauncherLatest = pkgs.writeShellApplication {
            name = "website";
            runtimeInputs = [ pkgs.python3 ];
            text = ''
              exec ${lib.getExe pkgs.python3} \
                -m http.server 8000 \
                -d ${self.packages.${system}.docs-latest}/
            '';
          };

          wwwLauncherLtr = pkgs.writeShellApplication {
            name = "website";
            runtimeInputs = [ pkgs.python3 ];
            text = ''
              exec ${lib.getExe pkgs.python3} \
                -m http.server 8000 \
                -d ${self.packages.${system}.docs-ltr}/
            '';
          };
        in
        rec {
          docs-master = {
            type = "app";
            program = "${wwwLauncherMaster}/bin/website";
          };

          docs-latest = {
            type = "app";
            program = "${wwwLauncherLatest}/bin/website";
          };

          docs-ltr = {
            type = "app";
            program = "${wwwLauncherLtr}/bin/website";
          };

          default = docs-master;
        }
      );

      #
      ### SHELLS
      #

      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgsFor.${system};
        in
        {
          # Development environment
          default = pkgs.mkShell {
            buildInputs = [ ];
          };
        }
      );
    };
}
