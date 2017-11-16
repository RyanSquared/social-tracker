autocmd BufWritePost *.py AsyncRun pip2 install --user --upgrade ..
autocmd BufWritePost *.html AsyncRun pip2 install --user --upgrade ..
autocmd FileType htmldjango setlocal ts=2 sw=2 et
