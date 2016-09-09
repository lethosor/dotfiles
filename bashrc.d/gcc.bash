export CC="$(which gcc-4.8 2>/dev/null || which gcc)"
export CXX="$(which g++-4.8 2>/dev/null || which g++)"
export REAL_CC="$CC"
export REAL_CXX="$CXX"
