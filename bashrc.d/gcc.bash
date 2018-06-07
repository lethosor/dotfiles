export CC="$(which gcc-7 2>/dev/null || which gcc)"
export CXX="$(which g++-7 2>/dev/null || which g++)"
export REAL_CC="$CC"
export REAL_CXX="$CXX"
