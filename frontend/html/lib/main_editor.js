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

                request_data = {
                    "file_name": "code.cpp",
                    "file_type": "cpp",
                    "line_num": line + 1,
                    "column_num": end + 1,
                    "contents": editor.getValue()
                };

                response = $.ajax({
                    type: "POST",
                    url: "http://localhost:8081/completions",
                    dataType: "json",
                    async: false,
                    data: JSON.stringify(request_data)
                });

                const completion_start = response.responseJSON["completion_start_column"];
                const completion_offset = end + 1 - completion_start;
                const completions = $.map(response.responseJSON["completions"], function (x) {
                    return {
                        displayText: x["kind"] == "FUNCTION" ? x["menu_text"] : x["insertion_text"],
                        text: x["insertion_text"].substring(completion_offset),
                        signature: x["extra_menu_info"] + " " + x["menu_text"]
                    };
                });

                return {
                    list: completions,
                    from: CodeMirror.Pos(line, completion_start - 1 + completion_offset)
                }
            }, { completeSingle: false });
            var completion = editor.state.completionActive.data;
            CodeMirror.on(completion, "select", function(completion, element) {
                $("#hint-details").text(completion.signature);
            });

            CodeMirror.on(completion, "pick", function (completion, element) {
                $("#hint-details").text(completion.signature);
            });
        }
    });
})()
