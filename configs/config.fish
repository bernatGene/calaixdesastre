### MANAGED BY RANCHER DESKTOP START (DO NOT EDIT)
set --export --prepend PATH "/Users/bernatskrabec/.rd/bin"
### MANAGED BY RANCHER DESKTOP END (DO NOT EDIT)

function newnote --description 'create & edit a timestamped file, then copy its contents'
    if test (count $argv) -gt 0
        set prefix $argv[1]
    else
        set prefix (basename (pwd))"_"
    end

    set ts (date +%Y%m%d_%H%M%S)
    set file $prefix$ts.txt

    vim $file

    # on successful save, copy to clipboard
    if test $status -eq 0
        if type -q pbcopy
            pbcopy < $file
        end
        echo "✔  $file → clipboard"
    end
end

function nn --description 'alias for newnote'
    newnote $argv
end
