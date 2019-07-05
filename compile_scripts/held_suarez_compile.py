from isca import DryCodeBase, GFDL_BASE

cb = DryCodeBase.from_directory(GFDL_BASE)
cb.compile(debug=True)
