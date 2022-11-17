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

function sendCompletionsRequest(line_num, column_num, contents) {
    request_data = {
        "file_name": "code.cpp",
        "file_type": "cpp",
        "line_num": line_num,
        "column_num": column_num,
        "contents": contents,
    };

    return $.ajax({
        type: "POST",
        url: "http://localhost:8081/completions",
        contentType: "application/json",
        async: false,
        data: JSON.stringify(request_data)
    });
}

function sendCompileRequest(session_id, contents, flags) {
    request_data = {
        "session_id": session_id,
        "contents": contents,
        "flags": flags,
    };

    return $.ajax({
        type: "POST",
        url: "http://localhost:8082/compile",
        contentType: "application/json",
        async: false,
        data: JSON.stringify(request_data),
    });
}

function sendExecuteRequest(session_id) {
    request_data = {
        "session_id": session_id,
        "arguments": [],
    };

    return $.ajax({
        type: "POST",
        url: "http://localhost:8082/execute",
        contentType: "application/json",
        async: false,
        data: JSON.stringify(request_data),
    });
}

function showCompletions(editor) {
    CodeMirror.showHint(editor, function () {
        const cursor = editor.getCursor();
        const end = cursor.ch;
        const line = cursor.line;
        const response = sendCompletionsRequest(line + 1, end + 1, editor.getValue());
        const completion_start = response.responseJSON["completion_start_column"];
        const completion_offset = end + 1 - completion_start;
        const completions = $.map(response.responseJSON["completions"], function (x) {
            return {
                displayText: x["menu_text"],
                text: x["insertion_text"].substring(completion_offset),
                signature: x["detailed_info"],
                hint: function (editor, completions, selected) {
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

function compileCode(editor) {
    const session_id = "dummy_session";
    const response = sendCompileRequest(session_id, editor.getValue(), ["-std=c++2a"]).responseJSON;
    var compilationDetails = $("#compilation-details");
    compilationDetails.empty();
    compilationDetails.append($("<li>").text("stdout: " + response["stdout"]));
    compilationDetails.append($("<li>").text("stderr: " + response["stderr"]));
    compilationDetails.append($("<li>").text("returncode: " + response["returncode"]));
}

function executeCode(editor) {
    const session_id = "dummy_session";
    const response = sendExecuteRequest(session_id, editor.getValue()).responseJSON;
    var executionDetails = $("#execution-details");
    executionDetails.empty();
    executionDetails.append([
        $("<li>").text("stdout: " + response["stdout"]),
        $("<li>").text("stderr: " + response["stderr"]),
        $("<li>").text("returncode: " + response["returncode"])
    ]);
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

    $("#build-button").click(function() {
        compileCode(editor);
    });

    $("#execute-button").click(function() {
        executeCode(editor);
    });
})()
