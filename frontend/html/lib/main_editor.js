(function () {
    CodeMirror.commands.save = function(){ alert("Saving"); };
    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        lineNumbers: true,
        mode: "text/x-c++src", keyMap: "vim",
        matchBrackets: true,
        showCursorWhenSelecting: true,
        theme: 'solarized dark',
    });
    var commandDisplay = document.getElementById('command-display');
    var keys = '';
    CodeMirror.on(editor, 'vim-keypress', function(key) {
        keys = keys + key;
        commandDisplay.innerText = keys;
    });
    CodeMirror.on(editor, 'vim-command-done', function(e) {
        keys = '';
        commandDisplay.innerHTML = keys;
    });
    var vimMode = document.getElementById('vim-mode');
    CodeMirror.on(editor, 'vim-mode-change', function(e) {
        vimMode.innerText = JSON.stringify(e);
    });

    editor.setOption('extraKeys', {
        'Ctrl-Space': function() {
            CodeMirror.showHint(editor, function () {
                const cursor = editor.getCursor();
                const token = editor.getTokenAt(cursor);
                const currentWord = token.string;
                const start = currentWord.trim() ? token.start : token.end;
                const end = cursor.ch;
                const line = cursor.line;
                // TODO: call ycmd or clangd server for completions
                const completions = [
                    { text: 'const'},
                    { text: 'constexpr'},
                    { text: 'extern'},
                ];
                return {
                    list: completions,
                    from: CodeMirror.Pos(line, start),
                    to: CodeMirror.Pos(line, end)
                }
            }, { completeSingle: false });
        }
    });
})()
