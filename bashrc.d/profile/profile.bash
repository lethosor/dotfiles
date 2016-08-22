echo profile
if [ -z "$bash_profile_loaded" ]
then
    uptime
    fortune | cowsay
    export bash_profile_loaded=1
fi
