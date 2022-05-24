#!/usr/bin/env bash

if [[ $(basename $SHELL) = 'bash' ]]; then
   if [ -f ~/.bashrc ]; 
   then
      echo "Installing bash autocompletion..."
      grep -q 'dotpyle-complete' ~/.bashrc
      if [[ $? -ne 0 ]]; 
      then
         echo "" >> ~/.bashrc
         echo "# Dotpyle autocompletion" >> ~/.bashrc
         echo 'eval "$(_DOTPYLE_COMPLETE=bash_source dotpyle)"' >> ~/.dotpyle-complete.bash
         echo "source ~/.dotpyle-complete.bash" >> ~/.bashrc
      fi
   fi
elif [[ $(basename $SHELL) = 'zsh' ]];
then
   if [ -f ~/.zshrc ];
   then
      echo "Installing zsh autocompletion..."
      grep -q 'dotpyle-complete' ~/.zshrc
      if [[ $? -ne 0 ]]; then
         echo "" >> ~/.zshrc
         echo "# Dotpyle autocompletion" >> ~/.zshrc
         # echo "autoload bashcompinit" >> ~/.zshrc
         # echo "bashcompinit" >> ~/.zshrc
         echo 'eval "$(_DOTPYLE_COMPLETE=zsh_source dotpyle)"' >> ~/.dotpyle-complete.zsh
         echo "source ~/.dotpyle-complete.zsh" >> ~/.zshrc
      fi
   fi
fi
