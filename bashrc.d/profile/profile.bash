good_cows=(
    "blowfish"
    "cheese"
    "cower"
    "default"
    "dragon-and-cow"
    "dragon"
    "elephant"
    "flaming-sheep"
    "ghostbusters"
    "meow"
    "milk"
    "moofasa"
    "moose"
    "stegosaurus"
    "turkey"
    "turtle"
    "tux"
    "vader"
)
if [ -z "$bash_profile_loaded" ]
then
    uptime
    cow=${good_cows[$RANDOM % (${#good_cows[@]}) ]}
    if [[ -z "$cow" ]]; then
        cow=default
    fi
    fortune | cowsay -f "$cow"
    export bash_profile_loaded=1
fi
