// It uses data_handler.js to visualize elements
import {dataHandler} from "./data_handler.js";

export let dom = {
    _appendToElement: function (elementToExtend, textToAppend, prepend = false) {
        // function to append new DOM elements (represented by a string) to an existing DOM element
        let fakeDiv = document.createElement('div');
        fakeDiv.innerHTML = textToAppend.trim();

        for (let childNode of fakeDiv.childNodes) {
            if (prepend) {
                elementToExtend.prepend(childNode);
            } else {
                elementToExtend.appendChild(childNode);
            }
        }

        console.log(elementToExtend.lastChild);
    },
    init: function () {
        this.addNewBoard()
    },
    loadBoards: function () {
        // retrieves boards and makes createBoards called
        dataHandler.getBoards(function (boards) {
            dom.createBoards(boards);
        });
    },
    createBoards: function (boards) {
        // shows boards appending them to #boards div
        // it adds necessary event listeners also
        const boardDiv = document.querySelector('.board-container');
        for (let i = 1; i < boards.length; i++) {
            const boardTemplateClone = document.querySelector('section').cloneNode(true);
            boardDiv.appendChild(boardTemplateClone)
        }

        const createdBoards = document.querySelectorAll('section');
        createdBoards.forEach((b, i) => {
            b.firstElementChild.firstElementChild.innerHTML = boards[i].title
        });
        boardDiv.hidden = false;

    },
    loadCards: function (boardId) {
        // retrieves cards and makes showCards called
    },
    showCards: function (cards) {
        // shows the cards of a board
        // it adds necessary event listeners also
    },
    addNewBoard: function () {
        document.querySelector('#submit-new-board').addEventListener('click', () => {
            const boardName = document.querySelector('#board-name').value;
            const newBoard = `
                        <section class="board">
                            <div class="board-header"><span class="board-title">${boardName}</span>
                                <button class="board-add">Add Card</button>
                                <button class="board-toggle"><i class="fas fa-chevron-down"></i></button>
                            </div>
                        </section>`;
            this._appendToElement(document.querySelector('.board-container'), newBoard, true);
            dataHandler.createNewBoard(boardName, function(response) {
                console.log(response)
            })
        })

    }
};
