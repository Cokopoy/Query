{ pkgs }: {
    deps = [
        pkgs.python311
        pkgs.python311Packages.pip
        pkgs.python311Packages.streamlit
        pkgs.python311Packages.pandas
        pkgs.python311Packages.openpyxl
        pkgs.python311Packages.requests
        pkgs.python311Packages.pyarrow
    ];
    env = {
        PYTHONUNBUFFERED = "1";
    };
}
