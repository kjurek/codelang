function makeList(str) {
    var splitStr = str.trim().split("\n");
    var li = splitStr.map(e => $("<li>").text(e));
    return li;
}

function showCompletionDetails(completion) {
    $("#hint-details").empty();
    if (completion.signature) {
        $("#hint-details").append(makeList(completion.signature));
    }
}

function showCompletions(editor) {
    CodeMirror.showHint(editor, function () {
        const cursor = editor.getCursor();
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
                displayText: x["menu_text"],
                text: x["insertion_text"].substring(completion_offset),
                signature: x["detailed_info"],
                hint: function(editor, completions, selected) {
                    showCompletionDetails(selected);
                    editor.replaceRange(selected.text, completions.from);
                }
            };
        });

        return {
            list: completions,
            from: CodeMirror.Pos(line, completion_start - 1 + completion_offset),

        }
    }, { completeSingle: false });
}

(function () {
    CodeMirror.commands.save = function () { alert("Saving"); };
    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        lineNumbers: true,
        mode: "text/x-c++src", keyMap: "vim",
        matchBrackets: true,
        showCursorWhenSelecting: true,
        theme: 'solarized dark',
    });
    var commandDisplay = document.getElementById('command-display');
    var keys = '';
    CodeMirror.on(editor, 'vim-keypress', function (key) {
        keys = keys + key;
        commandDisplay.innerText = keys;
    });
    CodeMirror.on(editor, 'vim-command-done', function (e) {
        keys = '';
        commandDisplay.innerHTML = keys;
    });
    var vimMode = document.getElementById('vim-mode');
    CodeMirror.on(editor, 'vim-mode-change', function (e) {
        vimMode.innerText = JSON.stringify(e);
    });

    editor.setOption('extraKeys', {
        'Ctrl-Space': function () {
            showCompletions(editor);
            var completion = editor.state.completionActive.data;
            CodeMirror.on(completion, "select", function (completion, element) {
                showCompletionDetails(completion);
            });
        }
    });
})()
