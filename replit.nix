{ pkgs }: {
  deps = [
    pkgs.python39
    pkgs.python39Packages.flask
    pkgs.python39Packages.geopy
    pkgs.python39Packages.pip
    pkgs.python39Packages.setuptools
    pkgs.python39Packages.wheel
    pkgs.python39Packages.requests
    pkgs.python39Packages.line-bot-sdk
  ];
}
