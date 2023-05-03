{ pkgs, ... }:

{
  packages = with pkgs; [ git ];

  languages.python = {
    enable = true;
    poetry.enable = true;
  };
}
