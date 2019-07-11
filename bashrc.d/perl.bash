export PERL_MB_OPT="--install_base \"$HOME/perl5\""
export PERL_MM_OPT="INSTALL_BASE=$HOME/perl5"
add_path PERL_LOCAL_LIB_ROOT begin "$HOME/perl5"
add_path PERL5LIB begin "$HOME/perl5/lib/perl5"
add_path PATH end ~/perl5/bin
