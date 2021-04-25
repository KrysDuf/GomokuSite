var turn = 0;
var width = 15;
var height = 15;
var gameOver = false;
var board = Array(width * height);

function announceWinner(winner) {
    console.log("a");
    if (winner == 0) {
        window.alert("X wins");
    }
    if (winner == 1) {
        window.alert("O wins");
    }
    if (winner == 2) {
        window.alert("Board filled");
    }
}

function checkWinner() {
    var filled = true;
    for (var i = 0; i < board.length; i++) {
        if (board[i] == undefined) filled = false;
        if (board[i] !== undefined) {
            if (
                (board[i] == board[i + 1] &&
                    board[i + 1] == board[i + 2] &&
                    board[i + 2] == board[i + 3] &&
                    board[i + 3] == board[i + 4]) ||
                (board[i] == board[i + width] &&
                    board[i + width] == board[i + 2 * width] &&
                    board[i + 2 * width] == board[i + 3 * width] &&
                    board[i + 3 * width] == board[i + 4 * width]) ||
                (board[i] == board[i + 1 + width] &&
                    board[i + 1 + width] == board[i + 2 + 2 * width] &&
                    board[i + 2 + 2 * width] == board[i + 3 + 3 * width] &&
                    board[i + 3 + 3 * width] == board[i + 4 + 4 * width]) ||
                (board[i] == board[i - 1 + width] &&
                    board[i - 1 + width] == board[i - 2 + 2 * width] &&
                    board[i - 2 + 2 * width] == board[i - 3 + 3 * width] &&
                    board[i - 3 + 3 * width] == board[i - 4 + 4 * width])
            ) {
                gameOver = true;
                announceWinner(board[i]);
            }
        }
    }
    if (filled) {
        announceWinner(2);
    }
}

function tileClick(row, tile) {
    var clicked = document.getElementById("board").children[row].children[tile];
    if (clicked.innerHTML || gameOver) return;
    board[tile + row * width] = turn;
    if (turn) {
        clicked.innerHTML = "o";
        clicked.style.color = "red";
        turn = 0;
    } else {
        clicked.innerHTML = "x";
        clicked.style.color = "blue";
        turn = 1;
    }
    checkWinner();
}

//generate board and listen to click event
var domBoard = document.createElement("table");
domBoard.id = "board";
for (let i = 0; i < height; i++) {
    var row = document.createElement("tr");
    for (let j = 0; j < width; j++) {
        var tile = document.createElement("td");
        tile.onclick = function () {
            tileClick(i, j);
        };
        row.appendChild(tile);
    }
    domBoard.appendChild(row);
}
document.body.appendChild(domBoard);