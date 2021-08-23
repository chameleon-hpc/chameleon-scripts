#!/usr/local_rwth/bin/zsh
echo "Hallo" > text.txt
for i in {0..10} 
do
    echo "Hallo" >>! text.txt
done


# printf '%s\n%s\n' "$(env)" "$(cat text.txt)" >text.txt


printEnv(){
    module list
    env
}

printEnv &>> text.txt